#!/bin/bash

# Scenario Execution Script for Flash Sale Architecture
# Outputs formatted execution log with DB SELECT snapshots to scenario_execution_log.md

LOG_FILE="scenario_execution_log.md"
KONG_URL="http://localhost:8000/api/v1"
SALE_ID="44444444-4444-4444-4444-444444444444"
USER_1="22222222-2222-2222-2222-222222222222"
USER_2="33333333-3333-3333-3333-333333333333"

echo "# 📜 Flash Sale System Design - Scenario Execution Log" > "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "Execution Timestamp: $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "Architecture Layers: Kong Gateway | Go Echo Services | Rust Axum Services | PgBouncer | Postgres | Redis | Kafka" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
echo "---" >> "$LOG_FILE"

run_query() {
    local title="$1"
    local sql_query="$2"
    echo "#### 🔍 DB State Snapshot: $title" >> "$LOG_FILE"
    echo "\`\`\`sql" >> "$LOG_FILE"
    echo "$sql_query" >> "$LOG_FILE"
    echo "\`\`\`" >> "$LOG_FILE"
    echo "\`\`\`text" >> "$LOG_FILE"
    docker exec -i postgres psql -U postgres -d flash_sale_db -c "$sql_query" 2>&1 >> "$LOG_FILE"
    echo "\`\`\`" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

log_header() {
    local scenario="$1"
    echo "## $scenario" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# Clean DB orders & payments before running scenario suite
docker exec -i postgres psql -U postgres -d flash_sale_db -c "TRUNCATE payments, orders CASCADE;" > /dev/null 2>&1

# -------------------------------------------------------------
# SCENARIO 1: PRE-SALE SETUP & INVENTORY PRE-HEATING
# -------------------------------------------------------------
log_header "1. Skenario 1: Pre-Sale Setup & Inventory Pre-heating"
echo "Mengaktifkan Flash Sale event dan memuat stok awal (5 unit) ke Redis Instance via API Gateway." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "BEFORE Pre-Heating (PostgreSQL flash_sales)" "SELECT id, product_id, sale_price, original_stock, remaining_stock, status FROM flash_sales WHERE id = '$SALE_ID';"

echo "Executing Preheat API Request..." >> "$LOG_FILE"
PREHEAT_RES=$(curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/preheat")
echo "\`\`\`json" >> "$LOG_FILE"
echo "$PREHEAT_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "AFTER Pre-Heating (PostgreSQL flash_sales)" "SELECT id, product_id, sale_price, original_stock, remaining_stock, status FROM flash_sales WHERE id = '$SALE_ID';"

# -------------------------------------------------------------
# SCENARIO 2: SUCCESSFUL FLASH SALE PURCHASE FLOW
# -------------------------------------------------------------
log_header "2. Skenario 2: Successful Flash Sale Purchase Flow (User 1 - Budi)"
echo "User 1 mengirim request transaksi pembelian. Service Go (Echo) memotong stok via Atomic Redis Lua script dan memasukkan event ke Kafka." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "BEFORE Purchase (PostgreSQL orders)" "SELECT id, user_id, flash_sale_id, price, status, idempotency_key, created_at FROM orders WHERE user_id = '$USER_1';"

PURCHASE_1_RES=$(curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/purchase" \
  -H "Content-Type: application/json" \
  -H "X-User-ID: $USER_1" \
  -H "X-Idempotency-Key: idemp_user1_tx01" \
  -d "{\"user_id\": \"$USER_1\"}")

echo "HTTP Response (202 Accepted):" >> "$LOG_FILE"
echo "\`\`\`json" >> "$LOG_FILE"
echo "$PURCHASE_1_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "Waiting 3 seconds for Kafka Consumer (Order Service Go) to persist order to PostgreSQL via PgBouncer..." >> "$LOG_FILE"
sleep 3

run_query "AFTER Purchase & Kafka Consumption (PostgreSQL orders)" "SELECT id, user_id, flash_sale_id, price, status, idempotency_key, created_at FROM orders WHERE user_id = '$USER_1';"

# Extract Order ID for payment scenario
ORDER_ID_1=$(docker exec -i postgres psql -U postgres -d flash_sale_db -t -A -c "SELECT id FROM orders WHERE user_id = '$USER_1' ORDER BY created_at DESC LIMIT 1;" | tr -d '\r')

# -------------------------------------------------------------
# SCENARIO 3: DUPLICATE PURCHASE CHECK (IDEMPOTENCY / ALREADY PURCHASED)
# -------------------------------------------------------------
log_header "3. Skenario 3: Duplicate Purchase Prevention (User 1 Try Again)"
echo "User 1 mencoba menekan tombol 'Beli' dua kali. Redis SISMEMBER memblokir request kedua untuk mencegah double purchase." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "BEFORE Duplicate Attempt (PostgreSQL order count for User 1)" "SELECT COUNT(*) AS user1_order_count FROM orders WHERE user_id = '$USER_1';"

PURCHASE_DUP_RES=$(curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/purchase" \
  -H "Content-Type: application/json" \
  -H "X-User-ID: $USER_1" \
  -H "X-Idempotency-Key: idemp_user1_tx02" \
  -d "{\"user_id\": \"$USER_1\"}")

echo "HTTP Response (409 Conflict):" >> "$LOG_FILE"
echo "\`\`\`json" >> "$LOG_FILE"
echo "$PURCHASE_DUP_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "AFTER Duplicate Attempt (PostgreSQL order count for User 1)" "SELECT COUNT(*) AS user1_order_count FROM orders WHERE user_id = '$USER_1';"

# -------------------------------------------------------------
# SCENARIO 4: STOCK DEPLETION & SOLD OUT PREVENTION
# -------------------------------------------------------------
log_header "4. Skenario 4: Stock Depletion & Sold Out Prevention"
echo "Menghabiskan sisa 4 unit stok hingga mencapai 0, lalu menguji request setelah SOLD OUT." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "BEFORE Stock Depletion (PostgreSQL orders summary)" "SELECT status, COUNT(*) FROM orders GROUP BY status;"

# Simulate 4 extra users purchasing to deplete stock
for i in {10..13}; do
  DUMMY_USER="00000000-0000-0000-0000-0000000000$i"
  docker exec -i postgres psql -U postgres -d flash_sale_db -c "INSERT INTO users (id, email, name, phone, password_hash) VALUES ('$DUMMY_USER', 'dummy$i@test.com', 'User $i', '08000$i', 'hash') ON CONFLICT DO NOTHING;" > /dev/null 2>&1
  curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/purchase" -H "X-User-ID: $DUMMY_USER" -d "{\"user_id\": \"$DUMMY_USER\"}" > /dev/null
done

sleep 3

echo "Attempting purchase after stock is 0 (Expect 410 Gone):" >> "$LOG_FILE"
SOLD_OUT_RES=$(curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/purchase" -H "X-User-ID: $USER_2" -d "{\"user_id\": \"$USER_2\"}")
echo "\`\`\`json" >> "$LOG_FILE"
echo "$SOLD_OUT_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "AFTER Stock Depletion (PostgreSQL orders summary - Max 5 active orders)" "SELECT status, COUNT(*) FROM orders GROUP BY status;"

# -------------------------------------------------------------
# SCENARIO 5: PAYMENT COMPLETION FLOW (SUCCESS)
# -------------------------------------------------------------
log_header "5. Skenario 5: Successful Payment Processing"
echo "User 1 menyelesaikan pembayaran via Payment Service Go (Echo). Status order diubah ke PAID dan entry dibuat di tabel payments." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "BEFORE Payment (PostgreSQL order & payments for Order $ORDER_ID_1)" "SELECT id, status, price FROM orders WHERE id = '$ORDER_ID_1'; SELECT * FROM payments WHERE order_id = '$ORDER_ID_1';"

PAYMENT_RES=$(curl -s -X POST "$KONG_URL/payments/pay/$ORDER_ID_1" \
  -H "Content-Type: application/json" \
  -d "{\"action\": \"SUCCESS\", \"payment_method\": \"E_WALLET\"}")

echo "HTTP Payment Response:" >> "$LOG_FILE"
echo "\`\`\`json" >> "$LOG_FILE"
echo "$PAYMENT_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "AFTER Payment (PostgreSQL order & payments for Order $ORDER_ID_1)" "SELECT id, status, price, updated_at FROM orders WHERE id = '$ORDER_ID_1'; SELECT id, order_id, amount, payment_method, gateway_ref_id, status, paid_at FROM payments WHERE order_id = '$ORDER_ID_1';"

# -------------------------------------------------------------
# SCENARIO 6: PAYMENT FAILURE & STOCK RESTORATION
# -------------------------------------------------------------
log_header "6. Skenario 6: Payment Failure & Redis Stock Restoration"
echo "User 2 melakukan order saat stok tersedia, namun pembayaran gagal. Payment Service mengubah status ke PAYMENT_FAILED dan memanggil Redis Lua script restore_stock.lua untuk mengembalikan 1 unit stok ke Redis." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# Reset Redis stock to 1 for testing restore
curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/preheat" > /dev/null

# Clean up orders table for user 2 test
docker exec -i postgres psql -U postgres -d flash_sale_db -c "DELETE FROM orders WHERE user_id = '$USER_2';" > /dev/null

# User 2 purchases
curl -s -X POST "$KONG_URL/flash-sales/$SALE_ID/purchase" -H "X-User-ID: $USER_2" -d "{\"user_id\": \"$USER_2\"}" > /dev/null
sleep 3

ORDER_ID_2=$(docker exec -i postgres psql -U postgres -d flash_sale_db -t -A -c "SELECT id FROM orders WHERE user_id = '$USER_2' AND status = 'AWAITING_PAYMENT' ORDER BY created_at DESC LIMIT 1;" | tr -d '\r')

run_query "BEFORE Payment Failure (PostgreSQL orders & payments for User 2)" "SELECT id, user_id, status FROM orders WHERE id = '$ORDER_ID_2';"

PAY_FAIL_RES=$(curl -s -X POST "$KONG_URL/payments/pay/$ORDER_ID_2" \
  -H "Content-Type: application/json" \
  -d "{\"action\": \"FAIL\", \"payment_method\": \"CREDIT_CARD\"}")

echo "HTTP Payment Failure Response:" >> "$LOG_FILE"
echo "\`\`\`json" >> "$LOG_FILE"
echo "$PAY_FAIL_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

run_query "AFTER Payment Failure & Stock Restoration (PostgreSQL orders & payments for User 2)" "SELECT id, user_id, status FROM orders WHERE id = '$ORDER_ID_2'; SELECT id, order_id, status FROM payments WHERE order_id = '$ORDER_ID_2';"

# -------------------------------------------------------------
# SCENARIO 7: RUST INVENTORY SERVICE RECONCILIATION
# -------------------------------------------------------------
log_header "7. Skenario 7: Rust Inventory Service Post-Sale Reconciliation"
echo "Service Rust (Axum) memeriksa konsistensi antara jumlah order terbayar di PostgreSQL via PgBouncer dengan stok di Redis." >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

RECON_RES=$(curl -s -X POST "$KONG_URL/inventory/reconcile?flash_sale_id=$SALE_ID")
echo "\`\`\`json" >> "$LOG_FILE"
echo "$RECON_RES" >> "$LOG_FILE"
echo "\`\`\`" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

echo "=== Log execution completed successfully at $(date) ==="
