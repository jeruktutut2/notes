#!/bin/bash
set -e

echo "=== Configured Primary Master for Replication & Citus Cluster ==="

# Izinkan koneksi replikasi di pg_hba.conf
echo "host replication replicator 0.0.0.0/0 trust" >> "$PGDATA/pg_hba.conf"
echo "host all all 0.0.0.0/0 trust" >> "$PGDATA/pg_hba.conf"

# Update konfigurasi PostgreSQL untuk Streaming Replication
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    ALTER SYSTEM SET wal_level = 'replica';
    ALTER SYSTEM SET max_wal_senders = 10;
    ALTER SYSTEM SET wal_keep_size = '64MB';
    ALTER SYSTEM SET hot_standby = 'on';
    SELECT pg_reload_conf();

    -- Buat user khusus replikasi
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = 'replicator') THEN
            CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replica_pass';
        END IF;
    END
    \$\$;
EOSQL

echo "=== Master Initialized Successfully ==="
