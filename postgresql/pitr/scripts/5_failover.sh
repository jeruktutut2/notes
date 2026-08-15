#!/bin/bash
set -e

echo "Simulating Primary Database Failure (Stopping 'db' container)..."
docker compose stop db

echo "Promoting Replica to become the new Primary..."
docker exec pitr_replica pg_ctl promote -D /var/lib/postgresql/data

echo "Updating PgBouncer to route traffic to the new Primary (pitr_replica)..."
# macOS uses sed -i '', Linux uses sed -i. We will use Perl for cross-platform compatibility
perl -pi -e 's/host=pitr_postgres/host=pitr_replica/g' ../pgbouncer/pgbouncer.ini

echo "Reloading PgBouncer configuration..."
docker exec pitr_pgbouncer pkill -HUP pgbouncer

echo "Waiting a few seconds for PgBouncer to reload..."
sleep 3

echo "================================================================"
echo "Validating Failover: Inserting new data (Transaksi Pasca Failover)..."
curl -X POST http://localhost:8080/transactions \
     -H "Content-Type: application/json" \
     -d '{"amount": 500.00, "notes": "Transaksi Pasca Failover"}'

echo -e "\n\nSelecting data to verify INSERT succeeded on new Primary:"
curl -s http://localhost:8080/transactions
echo -e "\n================================================================"
echo "Failover Complete! The API is now talking to pitr_replica."
