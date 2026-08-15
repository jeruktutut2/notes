#!/bin/bash
set -e

PRIMARY_HOST="${PRIMARY_HOST:-postgres_node1}"
PRIMARY_PORT="${PRIMARY_PORT:-5432}"

echo "=== Initializing PostgreSQL Replica connected to ${PRIMARY_HOST}:${PRIMARY_PORT} ==="

if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo "Data directory is empty. Waiting for Master at ${PRIMARY_HOST}:${PRIMARY_PORT}..."
    
    until PGPASSWORD=replica_password pg_isready -h "$PRIMARY_HOST" -p "$PRIMARY_PORT" -U replicator; do
        echo "Master is not ready yet. Retrying in 2 seconds..."
        sleep 2
    done

    echo "Master is ready. Starting pg_basebackup snapshot..."
    
    # Clear directory to prevent pg_basebackup error
    rm -rf "$PGDATA"/*

    export PGPASSWORD=replica_password
    pg_basebackup -h "$PRIMARY_HOST" -p "$PRIMARY_PORT" -U replicator -D "$PGDATA" -Fp -Xs -P -R

    chmod 700 "$PGDATA"

    echo "=== Snapshot completed successfully. Starting Replica in Standby mode ==="
else
    echo "Data directory already exists. Skipping pg_basebackup."
fi

exec docker-entrypoint.sh postgres
