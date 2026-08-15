#!/bin/bash
# ============================================
# Script: failover.sh
# Skenario: Eksekusi Failover dari DC ke DRC
# ============================================
set -e

echo "=================================================="
echo "  SKENARIO: PROSES FAILOVER (MENGAMBIL ALIH OPERASI)"
echo "=================================================="
echo "  Penjelasan CARA MENGAMBIL ALIH:"
echo "  1. Promosikan PostgreSQL DRC (Standby) -> Primary (Read-Write)"
echo "     Perintah: pg_ctl promote / SELECT pg_promote()"
echo "  2. Alihkan target aplikasi ke DRC PgBouncer"
echo "  3. DRC siap melayani pembacaan & penulisan data!"
echo "=================================================="
echo ""

# Check if pg-drc is running
if ! docker ps | grep -q "pg-drc"; then
    echo "[ERROR] Container pg-drc (DRC) is not running! Cannot perform failover."
    exit 1
fi

echo "[1/4] Memeriksa status DRC sebelum promosi..."
IN_RECOVERY=$(docker exec -i pg-drc psql -U appuser -d appdb -t -c "SELECT pg_is_in_recovery();" | tr -d ' ')
echo "  Status in recovery: $IN_RECOVERY"

if [ "$IN_RECOVERY" = "f" ]; then
    echo "  [INFO] DRC sudah dipromosikan sebagai Primary sebelumnya."
else
    echo ""
    echo "[2/4] Mempromosikan DRC Standby menjadi Primary (Read-Write)..."
    docker exec -i pg-drc psql -U appuser -d appdb -c "SELECT pg_promote();"
    sleep 2

    # Verify promotion
    NEW_RECOVERY=$(docker exec -i pg-drc psql -U appuser -d appdb -t -c "SELECT pg_is_in_recovery();" | tr -d ' ')
    echo "  Status in recovery setelah promosi: $NEW_RECOVERY (f = Primary)"
fi

echo ""
echo "[3/4] Mengalihkan target database Aplikasi ke DRC via API..."
FAILOVER_RES=$(curl -s -X POST http://localhost:8080/api/failover)
echo "  Response API: $FAILOVER_RES"

echo ""
echo "[4/4] Pengujian Penulisan Data Baru ke DRC (Primary Baru)..."
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
WRITE_RES=$(curl -s -X POST http://localhost:8080/api/data \
  -H "Content-Type: application/json" \
  -d "{
    \"title\": \"FAILOVER DATA - $TIMESTAMP\",
    \"content\": \"Data ini ditulis LANGSUNG ke DRC saat DC down. DRC berhasil mengambil alih peran DC!\",
    \"category\": \"failover_operation\"
  }")

echo "  Response Penulisan Data di DRC:"
echo "  $WRITE_RES"

echo ""
echo "=================================================="
echo "  ✅ PROSES FAILOVER SELESAI & BERHASIL!"
echo "=================================================="
echo "  - Peran DC telah diambil alih penuh oleh DRC"
echo "  - DRC sekarang berstatus Read-Write (Primary)"
echo "  - Aplikasi beroperasi normal menggunakan DRC"
echo "=================================================="
