#!/bin/bash
set -e

echo "=============================================="
echo "Initializing PostgreSQL Primary (Main DC)"
echo "=============================================="

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replica_password';
    SELECT * FROM pg_create_physical_replication_slot('drc_slot');
EOSQL

cat <<EOF >> "$PGDATA/pg_hba.conf"
host replication replicator 0.0.0.0/0 md5
EOF

cat <<EOF >> "$PGDATA/postgresql.conf"
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
hot_standby_feedback = on
EOF

echo "PostgreSQL Primary initialization completed."
