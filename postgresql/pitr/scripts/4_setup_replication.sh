#!/bin/bash
set -e

echo "Ensuring primary database is running..."
docker compose up -d db pgbouncer api
sleep 5

echo "Taking Base Backup from Primary to Replica Data Directory..."
# Ensure the directory exists, then clean it to start fresh
mkdir -p ../replica_data
rm -rf ../replica_data/*
# Use pg_basebackup with -R flag to automatically create standby.signal and connection info
docker exec pitr_postgres pg_basebackup -U myuser -h 127.0.0.1 -D /tmp/base_backup -Fp -Xs -R
# We do the backup to a temp folder inside db, then copy it to the shared volume, 
# because pg_basebackup cannot write directly to a host volume not mounted in the same container.
# Alternatively, since we can access pitr_postgres from host via docker exec, let's just do it directly:

# A cleaner way: execute pg_basebackup from inside a temporary container that mounts replica_data
docker run --rm --network pitr_net -v $(pwd)/../replica_data:/var/lib/postgresql/data postgres:16 pg_basebackup -h pitr_postgres -U myuser -D /var/lib/postgresql/data -Fp -Xs -R

echo "Starting Replica..."
docker compose up -d replica

echo "Waiting for replica to start streaming..."
sleep 5

echo "================================================================"
echo "Checking replication status on Primary..."
docker exec pitr_postgres psql -U myuser -d mydb -c "SELECT client_addr, state, sync_state FROM pg_stat_replication;"
echo "================================================================"

echo "Selecting data from DB before disaster/failover (via API)..."
curl -s http://localhost:8080/transactions
echo -e "\nSetup replication complete."
