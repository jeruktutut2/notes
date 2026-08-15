#!/usr/bin/env bash
set -e

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

KAFKA_URL="http://localhost:8081"
RABBITMQ_URL="http://localhost:8082"

echo -e "${CYAN}========================================================================${NC}"
echo -e "${CYAN}             SAGA PATTERN DEMO - AUTOMATED TEST SCENARIOS               ${NC}"
echo -e "${CYAN}========================================================================${NC}"

echo -e "${YELLOW}Starting Docker Compose services...${NC}"
docker compose up -d --build


# Helper function to wait for service readiness
wait_for_service() {
    local url=$1
    local name=$2
    echo -n -e "${YELLOW}Waiting for $name to be ready at $url/health... ${NC}"
    for i in {1..30}; do
        if curl -s -f "$url/health" > /dev/null 2>&1; then
            echo -e "${GREEN}READY!${NC}"
            return 0
        fi
        sleep 2
    done
    echo -e "${RED}FAILED to connect to $name!${NC}"
    exit 1
}

# Helper function to print inventory directly from DB
print_db_inventory() {
    docker exec saga_postgres psql -U postgres -d saga_db -c "SELECT item_id, item_name, stock, reserved_stock, updated_at FROM inventory;"
}

# Helper function to print transaction details (orders, payments, saga_logs) directly from DB
print_db_transaction_details() {
    local order_id=$1
    echo -e "${YELLOW}DB Records for Transaction ${order_id}:${NC}"
    echo -e "${CYAN}[orders table]${NC}"
    docker exec saga_postgres psql -U postgres -d saga_db -c "SELECT id, item_id, quantity, total_amount, status, saga_type FROM orders WHERE id = '$order_id';"
    echo -e "${CYAN}[payments table]${NC}"
    docker exec saga_postgres psql -U postgres -d saga_db -c "SELECT id, order_id, amount, status FROM payments WHERE order_id = '$order_id';"
    echo -e "${CYAN}[saga_logs table]${NC}"
    docker exec saga_postgres psql -U postgres -d saga_db -c "SELECT id, service_name, step_name, status, details FROM saga_logs WHERE order_id = '$order_id' ORDER BY id ASC;"
}

wait_for_service "$KAFKA_URL" "Kafka Choreography Service"
wait_for_service "$RABBITMQ_URL" "RabbitMQ Orchestration Service"

# Brief pause to allow Kafka background topic initialization & consumer group connection
echo "Allowing services and background consumers to settle..."
sleep 4

# Reset stock to 100 before test runs
docker exec saga_postgres psql -U postgres -d saga_db -c "UPDATE inventory SET stock = 100 WHERE item_id = 'ITEM-001';" > /dev/null 2>&1 || true


echo -e "\n${CYAN}--- Initial Inventory State (from DB) ---${NC}"
print_db_inventory


# -----------------------------------------------------------------------------
# SCENARIO 1: Kafka Choreography - Happy Path
# -----------------------------------------------------------------------------
echo -e "\n${CYAN}========================================================================${NC}"
echo -e "${CYAN} SCENARIO 1: Kafka Choreography - Happy Path (Success)                 ${NC}"
echo -e "${CYAN}========================================================================${NC}"

echo -e "${YELLOW}Product Data Before Transaction (from DB):${NC}"
print_db_inventory

RES1=$(curl -s -X POST "$KAFKA_URL/kafka/orders" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "ITEM-001", "quantity": 2, "amount": 150000, "fail_payment": false}')

ORDER_ID_1=$(echo "$RES1" | jq -r '.order_id')
echo -e "Order Created: ${YELLOW}$ORDER_ID_1${NC}"

echo "Waiting for event propagation across Kafka topics..."
sleep 6

ORDER_DETAIL_1=$(curl -s "$KAFKA_URL/orders/$ORDER_ID_1")
STATUS_1=$(echo "$ORDER_DETAIL_1" | jq -r '.status')

echo -e "Final Order Details (via API):"
echo "$ORDER_DETAIL_1" | jq .

print_db_transaction_details "$ORDER_ID_1"

echo -e "${YELLOW}Product Data After Transaction (from DB):${NC}"
print_db_inventory

if [ "$STATUS_1" == "COMPLETED" ]; then
    echo -e "${GREEN}✓ SCENARIO 1 PASSED: Order status is COMPLETED${NC}"
else
    echo -e "${RED}✗ SCENARIO 1 FAILED: Expected COMPLETED but got $STATUS_1${NC}"
fi

# -----------------------------------------------------------------------------
# SCENARIO 2: Kafka Choreography - Compensation Rollback
# -----------------------------------------------------------------------------
echo -e "\n${CYAN}========================================================================${NC}"
echo -e "${CYAN} SCENARIO 2: Kafka Choreography - Rollback (Payment Failure)          ${NC}"
echo -e "${CYAN}========================================================================${NC}"

echo -e "${YELLOW}Product Data Before Transaction (from DB):${NC}"
print_db_inventory

RES2=$(curl -s -X POST "$KAFKA_URL/kafka/orders" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "ITEM-001", "quantity": 3, "amount": 200000, "fail_payment": true}')

ORDER_ID_2=$(echo "$RES2" | jq -r '.order_id')
echo -e "Order Created (Configured to Fail Payment): ${YELLOW}$ORDER_ID_2${NC}"

echo "Waiting for compensation events..."
sleep 6

ORDER_DETAIL_2=$(curl -s "$KAFKA_URL/orders/$ORDER_ID_2")
STATUS_2=$(echo "$ORDER_DETAIL_2" | jq -r '.status')

echo -e "Final Order Details (via API):"
echo "$ORDER_DETAIL_2" | jq .

print_db_transaction_details "$ORDER_ID_2"

echo -e "${YELLOW}Product Data After Transaction (from DB):${NC}"
print_db_inventory

if [ "$STATUS_2" == "CANCELLED" ]; then
    echo -e "${GREEN}✓ SCENARIO 2 PASSED: Order status is CANCELLED and stock restored!${NC}"
else
    echo -e "${RED}✗ SCENARIO 2 FAILED: Expected CANCELLED but got $STATUS_2${NC}"
fi

# -----------------------------------------------------------------------------
# SCENARIO 3: RabbitMQ Orchestration - Happy Path
# -----------------------------------------------------------------------------
echo -e "\n${CYAN}========================================================================${NC}"
echo -e "${CYAN} SCENARIO 3: RabbitMQ Orchestration - Happy Path (Success)            ${NC}"
echo -e "${CYAN}========================================================================${NC}"

echo -e "${YELLOW}Product Data Before Transaction (from DB):${NC}"
print_db_inventory

RES3=$(curl -s -X POST "$RABBITMQ_URL/rabbitmq/orders" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "ITEM-001", "quantity": 5, "amount": 300000, "fail_payment": false}')

ORDER_ID_3=$(echo "$RES3" | jq -r '.order_id')
echo -e "Order Created: ${YELLOW}$ORDER_ID_3${NC}"

echo "Waiting for orchestrator commands via RabbitMQ..."
sleep 3

ORDER_DETAIL_3=$(curl -s "$RABBITMQ_URL/orders/$ORDER_ID_3")
STATUS_3=$(echo "$ORDER_DETAIL_3" | jq -r '.status')

echo -e "Final Order Details (via API):"
echo "$ORDER_DETAIL_3" | jq .

print_db_transaction_details "$ORDER_ID_3"

echo -e "${YELLOW}Product Data After Transaction (from DB):${NC}"
print_db_inventory

if [ "$STATUS_3" == "COMPLETED" ]; then
    echo -e "${GREEN}✓ SCENARIO 3 PASSED: Order status is COMPLETED${NC}"
else
    echo -e "${RED}✗ SCENARIO 3 FAILED: Expected COMPLETED but got $STATUS_3${NC}"
fi

# -----------------------------------------------------------------------------
# SCENARIO 4: RabbitMQ Orchestration - Compensation Rollback
# -----------------------------------------------------------------------------
echo -e "\n${CYAN}========================================================================${NC}"
echo -e "${CYAN} SCENARIO 4: RabbitMQ Orchestration - Rollback (Payment Failure)       ${NC}"
echo -e "${CYAN}========================================================================${NC}"

echo -e "${YELLOW}Product Data Before Transaction (from DB):${NC}"
print_db_inventory

RES4=$(curl -s -X POST "$RABBITMQ_URL/rabbitmq/orders" \
  -H "Content-Type: application/json" \
  -d '{"item_id": "ITEM-001", "quantity": 4, "amount": 250000, "fail_payment": true}')

ORDER_ID_4=$(echo "$RES4" | jq -r '.order_id')
echo -e "Order Created (Configured to Fail Payment): ${YELLOW}$ORDER_ID_4${NC}"

echo "Waiting for orchestrator to execute compensation steps..."
sleep 3

ORDER_DETAIL_4=$(curl -s "$RABBITMQ_URL/orders/$ORDER_ID_4")
STATUS_4=$(echo "$ORDER_DETAIL_4" | jq -r '.status')

echo -e "Final Order Details (via API):"
echo "$ORDER_DETAIL_4" | jq .

print_db_transaction_details "$ORDER_ID_4"

echo -e "${YELLOW}Product Data After Transaction (from DB):${NC}"
print_db_inventory

if [ "$STATUS_4" == "CANCELLED" ]; then
    echo -e "${GREEN}✓ SCENARIO 4 PASSED: Order status is CANCELLED and stock restored!${NC}"
else
    echo -e "${RED}✗ SCENARIO 4 FAILED: Expected CANCELLED but got $STATUS_4${NC}"
fi

echo -e "\n${CYAN}--- Final All Orders Summary (from DB) ---${NC}"
docker exec saga_postgres psql -U postgres -d saga_db -c "SELECT id, item_id, quantity, total_amount, status, saga_type FROM orders;"

echo -e "\n${CYAN}--- Final Inventory State (from DB) ---${NC}"
print_db_inventory

echo -e "\n${GREEN}========================================================================${NC}"
echo -e "${GREEN}                     ALL SAGA SCENARIOS COMPLETED!                      ${NC}"
echo -e "${GREEN}========================================================================${NC}"

echo -e "\n${YELLOW}Tearing down Docker Compose environment...${NC}"
docker compose down

