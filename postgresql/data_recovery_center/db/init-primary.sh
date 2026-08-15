#!/bin/bash
set -e

echo "============================================"
echo "  Initializing Data Center (Primary) DB"
echo "============================================"

# ============================================
# 1. Create replication user for DRC streaming
# ============================================
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create dedicated replication user
    CREATE ROLE replicator WITH REPLICATION LOGIN PASSWORD 'replicator_pass';

    -- Grant connect permission
    GRANT CONNECT ON DATABASE ${POSTGRES_DB} TO replicator;

    -- Log the initialization
    DO \$\$
    BEGIN
        RAISE NOTICE 'Replication user "replicator" created successfully';
    END
    \$\$;
EOSQL

echo "[OK] Replication user 'replicator' created"

# ============================================
# 2. Configure pg_hba.conf for replication
# ============================================
# Allow replication connections from any host in Docker network
echo "" >> "$PGDATA/pg_hba.conf"
echo "# ============================================" >> "$PGDATA/pg_hba.conf"
echo "# Replication access for DRC standby" >> "$PGDATA/pg_hba.conf"
echo "# ============================================" >> "$PGDATA/pg_hba.conf"
echo "host replication replicator 0.0.0.0/0 scram-sha-256" >> "$PGDATA/pg_hba.conf"
echo "host all appuser 0.0.0.0/0 scram-sha-256" >> "$PGDATA/pg_hba.conf"

echo "[OK] pg_hba.conf configured for replication"

# ============================================
# 3. Create replication slot for DRC
# ============================================
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    -- Create physical replication slot
    -- This ensures WAL segments are retained until DRC consumes them
    SELECT pg_create_physical_replication_slot('drc_slot');
EOSQL

echo "[OK] Replication slot 'drc_slot' created"

echo ""
echo "============================================"
echo "  Primary DB initialization complete!"
echo "  - Replication user: replicator"
echo "  - Replication slot: drc_slot"
echo "  - WAL level: replica"
echo "============================================"
