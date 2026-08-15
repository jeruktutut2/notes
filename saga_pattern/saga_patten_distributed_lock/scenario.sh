#!/bin/bash

# Exit on error if any command fails
set -e

echo "======================================================="
echo " 1. STARTING SYSTEM CONTAINERS VIA DOCKER COMPOSE UP "
echo "======================================================="
docker compose up -d --build

echo ""
echo "Waiting for services to become healthy and ready..."
until curl -s http://localhost:8080/health > /dev/null; do
    echo "Waiting for http://localhost:8080/health..."
    sleep 3
done

echo ""
echo "✔ Services are UP and healthy!"
echo ""

print_db_state() {
    local stage="$1"
    echo "-------------------------------------------------------"
    echo " DB STATE ($stage)"
    echo "-------------------------------------------------------"
    echo "Inventory Table:"
    docker exec -i postgres_saga psql -U postgres -d saga_db -c "SELECT * FROM inventory;" 2>/dev/null || true
    echo "Orders Table:"
    docker exec -i postgres_saga psql -U postgres -d saga_db -c "SELECT * FROM orders;" 2>/dev/null || true
    echo "-------------------------------------------------------"
}

echo "======================================================="
echo " 2. TEST CASE 1: SUCCESSFUL SAGA FLOW "
echo "======================================================="
print_db_state "BEFORE Test Case 1"

echo "Sending request to create order (No simulation failure)..."
RESPONSE_1=$(curl -s -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-101",
    "quantity": 2,
    "total_price": 150.00,
    "simulate_fail_at": ""
  }')

echo "Response:"
echo "$RESPONSE_1" | jq . 2>/dev/null || echo "$RESPONSE_1"
ORDER_ID_1=$(echo "$RESPONSE_1" | grep -o '"order_id":"[^"]*' | cut -d'"' -f4)

if [ -n "$ORDER_ID_1" ]; then
    echo "Fetching Order Status from DB (via PgBouncer):"
    curl -s http://localhost:8080/api/orders/$ORDER_ID_1 | jq . 2>/dev/null || true
fi

print_db_state "AFTER Test Case 1"
echo ""

echo "======================================================="
echo " 3. TEST CASE 2: SAGA ROLLBACK (PAYMENT FAILURE) "
echo "======================================================="
print_db_state "BEFORE Test Case 2"

echo "Sending request to create order with simulated PAYMENT failure..."
RESPONSE_2=$(curl -s -X POST http://localhost:8080/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": "PROD-101",
    "quantity": 1,
    "total_price": 75.00,
    "simulate_fail_at": "payment"
  }')

echo "Response:"
echo "$RESPONSE_2" | jq . 2>/dev/null || echo "$RESPONSE_2"
ORDER_ID_2=$(echo "$RESPONSE_2" | grep -o '"order_id":"[^"]*' | cut -d'"' -f4)

if [ -n "$ORDER_ID_2" ]; then
    echo "Fetching Order Status from DB (Verifying Compensating Rollback):"
    curl -s http://localhost:8080/api/orders/$ORDER_ID_2 | jq . 2>/dev/null || true
fi

print_db_state "AFTER Test Case 2"
echo ""

echo "======================================================="
echo " 4. TEST CASE 3: DISTRIBUTED LOCK WATCHDOG HEARTBEAT "
echo "======================================================="
print_db_state "BEFORE Test Case 3"

echo "Triggering 8-second long critical task holding lock with 3s initial TTL..."
echo "Background Watchdog Heartbeat will extend TTL every 1s continuously."

# Trigger long lock task in background
curl -s -X POST "http://localhost:8080/api/lock/demo?duration=normal" > /tmp/lock_bg_result.json &
BG_PID=$!

sleep 2
echo "Attempting concurrent request to the same locked resource..."
CONCURRENT_RESP=$(curl -s -X POST "http://localhost:8080/api/lock/demo")
echo "Concurrent Request Response (Expected 423 Locked):"
echo "$CONCURRENT_RESP" | jq . 2>/dev/null || echo "$CONCURRENT_RESP"

wait $BG_PID
echo "First Task Response:"
cat /tmp/lock_bg_result.json | jq . 2>/dev/null || cat /tmp/lock_bg_result.json
rm -f /tmp/lock_bg_result.json

print_db_state "AFTER Test Case 3 / FINAL"
echo ""

echo "======================================================="
echo " 5. STOPPING SYSTEM CONTAINERS VIA DOCKER COMPOSE DOWN "
echo "======================================================="
docker compose down -v

echo "======================================================="
echo " SCRIPT EXECUTED SUCCESSFULLY! "
echo "======================================================="
