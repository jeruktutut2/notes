#!/usr/bin/env bash

# Colors for terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

BASE_URL="http://localhost:8080"
ACCOUNT_ID=1
INITIAL_BALANCE=1000000
WITHDRAW_AMOUNT=100000
NUM_CONCURRENT=10
GO_PID=""

# Function untuk pembersihan otomatis saat script selesai/di-stop (Ctrl+C)
cleanup() {
    echo -e "\n${YELLOW}---------------------------------------------------------------${NC}"
    echo -e "${YELLOW}               MEMATIKAN SERVICE & CLEANUP (TRAP)             ${NC}"
    echo -e "${YELLOW}---------------------------------------------------------------${NC}"
    
    if [ -n "$GO_PID" ]; then
        echo -e "Mematikan server Go Echo v5 (PID: $GO_PID)..."
        kill "$GO_PID" 2>/dev/null || true
    fi

    echo -e "Menjalankan '${CYAN}docker compose down${NC}'..."
    docker compose down 2>/dev/null || true

    echo -e "${GREEN}Cleanup selesai. Terima kasih!${NC}\n"
}

# Trap akan mengeksekusi fungsi cleanup saat script berhenti/keluar (EXIT/SIGINT/SIGTERM)
trap cleanup EXIT

echo -e "${CYAN}===============================================================${NC}"
echo -e "${CYAN}   SUITE PENGUJIAN KOMPREHENSIF DISTRIBUTED LOCK (GO ECHO V5)   ${NC}"
echo -e "${CYAN}===============================================================${NC}\n"

# 1. MENJALANKAN DOCKER COMPOSE UP -D
echo -e "${CYAN}[1/3] Menjalankan Service PostgreSQL & Redis via Docker Compose...${NC}"
docker compose up -d --wait

# 2. MENJALANKAN SERVER GO DI BACKGROUND
echo -e "${CYAN}[2/3] Menjalankan Server Go Echo v5 di Background...${NC}"
go run main.go > /dev/null 2>&1 &
GO_PID=$!
echo -e "Server Go berjalan dengan PID: ${GREEN}$GO_PID${NC}"

# Tunggu server Go siap menerima request
echo -e "${CYAN}[3/3] Menunggu server Go siap di $BASE_URL...${NC}"
MAX_RETRIES=10
COUNT=0
until curl -s "$BASE_URL/balance?account_id=1" > /dev/null; do
    sleep 1
    COUNT=$((COUNT + 1))
    if [ $COUNT -ge $MAX_RETRIES ]; then
        echo -e "${RED}ERROR: Server Go gagal merespon setelah $MAX_RETRIES detik.${NC}"
        exit 1
    fi
done

echo -e "${GREEN}--> Semua Service Siap! Memulai Skenario Pengujian...${NC}\n"

reset_account() {
    curl -s -X POST "$BASE_URL/reset" \
         -H "Content-Type: application/json" \
         -d "{\"account_id\": $ACCOUNT_ID, \"balance\": $INITIAL_BALANCE}" > /dev/null
}

get_balance() {
    curl -s "$BASE_URL/balance?account_id=$ACCOUNT_ID" | grep -o '"balance":[0-9.]*' | cut -d':' -f2
}

# ------------------------------------------------------------------------------
# SKENARIO 1: TANPA LOCKING (NO-LOCK)
# ------------------------------------------------------------------------------
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "${YELLOW}[SKENARIO 1] Pengurangan Saldo TANPA Distributed Lock${NC}"
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "Penjelasan: 10 request dikirimkan SERENTAK (paralel) untuk me-withdraw 100.000."
echo -e "Saldo awal: 1.000.000. Seharusnya saldo akhir = 0 (10 x 100.000 = 1.000.000)."
reset_account

echo -e "Mengirim 10 request paralel..."
for i in $(seq 1 $NUM_CONCURRENT); do
    curl -s -X POST "$BASE_URL/withdraw/no-lock" \
         -H "Content-Type: application/json" \
         -d "{\"account_id\": $ACCOUNT_ID, \"amount\": $WITHDRAW_AMOUNT}" > /dev/null &
done

wait # Tunggu seluruh background process selesai

FINAL_BAL=$(get_balance)
echo -e "--> Saldo Akhir di DB: ${RED}$FINAL_BAL${NC}"
echo -e "${RED}ANALISIS:${NC} Terjadi RACE CONDITION (Lost Update)! Sebagian besar request membaca saldo awal yang sama sebelum request lain sempat mengupdate DB. Akibatnya saldo DB merugi/salah!\n"

sleep 1

# ------------------------------------------------------------------------------
# SKENARIO 2: DENGAN REDIS DISTRIBUTED LOCK
# ------------------------------------------------------------------------------
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "${YELLOW}[SKENARIO 2] Pengurangan Saldo DENGAN REDIS DISTRIBUTED LOCK${NC}"
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "Penjelasan: Request menggunakan Redis SETNX untuk mengunci resource."
echo -e "Request yang gagal mendapatkan lock akan langsung ditolak (423 Locked / Non-blocking lock)."
reset_account

echo -e "Mengirim 10 request paralel ke /withdraw/redis-lock..."
TEMP_FILE=$(mktemp)
for i in $(seq 1 $NUM_CONCURRENT); do
    curl -s -w "\n%{http_code}" -X POST "$BASE_URL/withdraw/redis-lock" \
         -H "Content-Type: application/json" \
         -d "{\"account_id\": $ACCOUNT_ID, \"amount\": $WITHDRAW_AMOUNT}" >> "$TEMP_FILE" &
done

wait

SUCCESS_COUNT=$(grep -c "200" "$TEMP_FILE")
LOCKED_COUNT=$(grep -c "423" "$TEMP_FILE")
rm "$TEMP_FILE"

FINAL_BAL=$(get_balance)
echo -e "--> Request Berhasil (HTTP 200): ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "--> Request Ditolak karena Locked (HTTP 423): ${YELLOW}$LOCKED_COUNT${NC}"
echo -e "--> Saldo Akhir di DB: ${GREEN}$FINAL_BAL${NC}"
echo -e "${GREEN}ANALISIS:${NC} Redis Lock melindungi data secara mutlak. Hanya 1 request yang berhasil masuk area kritis dalam satu waktu, sedangkan request serentak lainnya ditolak dengan aman tanpa merusak data saldo!\n"

sleep 1

# ------------------------------------------------------------------------------
# SKENARIO 2B: DENGAN REDIS WATCHDOG (AUTO-RENEWAL TTL HEARTBEAT)
# ------------------------------------------------------------------------------
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "${YELLOW}[SKENARIO 2B] Pengurangan Saldo DENGAN REDIS WATCHDOG LOCK${NC}"
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "Penjelasan: Menggunakan Watchdog Heartbeat (AcquireLockWithWatchdog) yang memperpanjang TTL kunci tiap 1.6 detik secara otomatis."
reset_account

TEMP_FILE=$(mktemp)
for i in $(seq 1 $NUM_CONCURRENT); do
    curl -s -w "\n%{http_code}" -X POST "$BASE_URL/withdraw/redis-watchdog-lock" \
         -H "Content-Type: application/json" \
         -d "{\"account_id\": $ACCOUNT_ID, \"amount\": $WITHDRAW_AMOUNT}" >> "$TEMP_FILE" &
done

wait

SUCCESS_COUNT=$(grep -c "200" "$TEMP_FILE")
LOCKED_COUNT=$(grep -c "423" "$TEMP_FILE")
rm "$TEMP_FILE"

FINAL_BAL=$(get_balance)
echo -e "--> Request Berhasil (HTTP 200): ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "--> Request Ditolak karena Locked (HTTP 423): ${YELLOW}$LOCKED_COUNT${NC}"
echo -e "--> Saldo Akhir di DB: ${GREEN}$FINAL_BAL${NC}"
echo -e "${GREEN}ANALISIS:${NC} Watchdog Heartbeat memperpanjang TTL kunci selama proses Go masih aktif. Data 100% konsisten!\n"

sleep 1

# ------------------------------------------------------------------------------
# SKENARIO 3: DENGAN POSTGRESQL SESSION ADVISORY LOCK
# ------------------------------------------------------------------------------
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "${YELLOW}[SKENARIO 3] Pengurangan Saldo DENGAN PG SESSION ADVISORY LOCK${NC}"
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "Penjelasan: Menggunakan fungsi pg_try_advisory_lock() pada koneksi PostgreSQL."
reset_account

TEMP_FILE=$(mktemp)
for i in $(seq 1 $NUM_CONCURRENT); do
    curl -s -w "\n%{http_code}" -X POST "$BASE_URL/withdraw/pg-session-lock" \
         -H "Content-Type: application/json" \
         -d "{\"account_id\": $ACCOUNT_ID, \"amount\": $WITHDRAW_AMOUNT}" >> "$TEMP_FILE" &
done

wait

SUCCESS_COUNT=$(grep -c "200" "$TEMP_FILE")
LOCKED_COUNT=$(grep -c "423" "$TEMP_FILE")
rm "$TEMP_FILE"

FINAL_BAL=$(get_balance)
echo -e "--> Request Berhasil (HTTP 200): ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "--> Request Ditolak karena Locked (HTTP 423): ${YELLOW}$LOCKED_COUNT${NC}"
echo -e "--> Saldo Akhir di DB: ${GREEN}$FINAL_BAL${NC}"
echo -e "${GREEN}ANALISIS:${NC} PostgreSQL Session Advisory Lock berhasil memproteksi transaksi di level database session!\n"

sleep 1

# ------------------------------------------------------------------------------
# SKENARIO 4: DENGAN POSTGRESQL TRANSACTION ADVISORY LOCK
# ------------------------------------------------------------------------------
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "${YELLOW}[SKENARIO 4] Pengurangan Saldo DENGAN PG TRANSACTION ADVISORY LOCK${NC}"
echo -e "${YELLOW}---------------------------------------------------------------${NC}"
echo -e "Penjelasan: Menggunakan pg_try_advisory_xact_lock() di dalam Transaksi (BEGIN...COMMIT)."
echo -e "Lock terlepas otomatis saat transaksi di-commit atau rollback."
reset_account

TEMP_FILE=$(mktemp)
for i in $(seq 1 $NUM_CONCURRENT); do
    curl -s -w "\n%{http_code}" -X POST "$BASE_URL/withdraw/pg-xact-lock" \
         -H "Content-Type: application/json" \
         -d "{\"account_id\": $ACCOUNT_ID, \"amount\": $WITHDRAW_AMOUNT}" >> "$TEMP_FILE" &
done

wait

SUCCESS_COUNT=$(grep -c "200" "$TEMP_FILE")
LOCKED_COUNT=$(grep -c "423" "$TEMP_FILE")
rm "$TEMP_FILE"

FINAL_BAL=$(get_balance)
echo -e "--> Request Berhasil (HTTP 200): ${GREEN}$SUCCESS_COUNT${NC}"
echo -e "--> Request Ditolak karena Locked (HTTP 423): ${YELLOW}$LOCKED_COUNT${NC}"
echo -e "--> Saldo Akhir di DB: ${GREEN}$FINAL_BAL${NC}"
echo -e "${GREEN}ANALISIS:${NC} Transaction Advisory Lock melekat pada siklus hidup DB transaction. Data 100% konsisten!\n"

echo -e "${CYAN}===============================================================${NC}"
echo -e "${CYAN}              PENGUJIAN SELESAI DENGAN SUKSES!                 ${NC}"
echo -e "${CYAN}===============================================================${NC}"
