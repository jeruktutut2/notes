#!/usr/bin/env bash
set -e

# Usage: ./scripts/scale-down.sh <worker_name>
# Example: ./scripts/scale-down.sh worker5

WORKER_NAME=$1

if [[ -z "$WORKER_NAME" ]]; then
  echo "Usage: $0 <worker1|worker2|worker3|worker4|worker5>"
  echo "Example: $0 worker5"
  exit 1
fi

echo "=================================================="
echo "⚠️  SCENARIO: Scale-Down / Draining Node $WORKER_NAME"
echo "=================================================="

# Check if node exists in Citus metadata
NODE_EXISTS=$(docker compose exec -T coordinator psql -U postgres -d citus_db -t -A -c "SELECT count(*) FROM pg_dist_node WHERE nodename = '$WORKER_NAME';")

if [[ "$NODE_EXISTS" -eq 0 ]]; then
  echo "❌ Node $WORKER_NAME is not present in Citus metadata."
  exit 1
fi

# Check total active nodes in cluster (excluding coordinator)
TOTAL_NODES=$(docker compose exec -T coordinator psql -U postgres -d citus_db -t -A -c "SELECT count(*) FROM pg_dist_node WHERE nodename != 'coordinator';")

if [[ "$TOTAL_NODES" -le 1 ]]; then
  echo "❌ Cannot drain node $WORKER_NAME: it is the last active worker node in the cluster!"
  exit 1
fi

echo "1️⃣  Step 1: Evacuating/Draining all shards off $WORKER_NAME to remaining active nodes..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "SELECT citus_drain_node('$WORKER_NAME', 5432);"

echo "2️⃣  Step 2: Removing node $WORKER_NAME from Citus cluster metadata..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "SELECT citus_remove_node('$WORKER_NAME', 5432);"

echo "3️⃣  Step 3: Stopping container for $WORKER_NAME..."
docker compose stop "$WORKER_NAME"

echo ""
echo "✅ Node $WORKER_NAME successfully drained and removed without data loss!"
echo "=================================================="

# Print updated cluster status
./scripts/check-shards.sh
