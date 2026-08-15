#!/bin/bash
set -e

# Simulating data loss by dropping the transactions table
echo "Dropping table 'transactions' to simulate a disaster..."
docker exec pitr_postgres psql -U myuser -d mydb -c "DROP TABLE transactions;"
echo "Disaster simulated! Table 'transactions' dropped."
