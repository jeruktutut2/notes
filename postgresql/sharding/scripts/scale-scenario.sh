#!/usr/bin/env bash
set -e

# Usage: ./scripts/scale-scenario.sh <1|2|3|4|5>

NUM_WORKERS=$1

if [[ -z "$NUM_WORKERS" || "$NUM_WORKERS" -lt 1 || "$NUM_WORKERS" -gt 5 ]]; then
  echo "Usage: $0 <1|2|3|4|5>"
  echo "Example: $0 3   (Scales cluster to 3 worker DB nodes)"
  exit 1
fi

echo "=================================================="
echo "🚀 SCENARIO: Scaling Citus Cluster to $NUM_WORKERS Worker Node(s)"
echo "=================================================="

# 1. Determine list of worker services to bring up
WORKER_SERVICES=()
for ((i=1; i<=NUM_WORKERS; i++)); do
  WORKER_SERVICES+=("worker$i")
done

echo "📦 Starting containers: coordinator pgbouncer ${WORKER_SERVICES[*]}"
docker compose up -d coordinator pgbouncer "${WORKER_SERVICES[@]}"

# 2. Wait for worker node containers to be fully ready
echo "⏳ Waiting for worker node containers to accept connections..."
for ((i=1; i<=NUM_WORKERS; i++)); do
  WORKER_NAME="worker$i"
  until docker compose exec -T "$WORKER_NAME" pg_isready -U postgres -d citus_db > /dev/null 2>&1; do
    sleep 1
  done
done

sleep 2

# 3. Register worker nodes with Citus Coordinator
for ((i=1; i<=NUM_WORKERS; i++)); do
  WORKER_NAME="worker$i"
  echo "➕ Registering node: $WORKER_NAME into Citus metadata..."
  docker compose exec -T coordinator psql -U postgres -d citus_db -c "
  DO \$$
  BEGIN
      IF NOT EXISTS (SELECT 1 FROM pg_dist_node WHERE nodename = '$WORKER_NAME') THEN
          PERFORM citus_add_node('$WORKER_NAME', 5432);
          RAISE NOTICE 'Node $WORKER_NAME added successfully.';
      ELSE
          RAISE NOTICE 'Node $WORKER_NAME already exists in cluster.';
      END IF;
  END \$$;
  "
done

# 4. Ensure tables are distributed
echo "🔄 Ensuring tables (users, orders) are distributed across shards..."
docker compose exec -T coordinator psql -U postgres -d citus_db -c "
DO \$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM citus_tables WHERE table_name = 'users'::regclass) THEN
        PERFORM create_distributed_table('users', 'id');
        PERFORM create_distributed_table('orders', 'user_id', colocate_with => 'users');
        PERFORM create_reference_table('product_categories');
    END IF;
END \$$;
"

# 5. Trigger Shard Rebalancing if > 1 node
if [ "$NUM_WORKERS" -gt 1 ]; then
  echo "⚖️  Triggering Citus Shard Rebalance across $NUM_WORKERS nodes..."
  docker compose exec -T coordinator psql -U postgres -d citus_db -c "SELECT citus_rebalance_start();"
fi

echo ""
echo "✅ Scenario scaling to $NUM_WORKERS node(s) completed!"
echo "=================================================="

# 6. Print current cluster status
./scripts/check-shards.sh
