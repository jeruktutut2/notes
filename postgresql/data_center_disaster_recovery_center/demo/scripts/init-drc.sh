#!/bin/bash
set -e

echo "=============================================="
echo "Initializing PostgreSQL Standby (DRC Site)"
echo "=============================================="

PGDATA="/var/lib/postgresql/data"

echo "Waiting for PostgreSQL Primary (postgres-dc:5432) to be ready..."
until PGPASSWORD=replica_password psql -h postgres-dc -U replicator -d dcdrc_db -c '\q' 2>/dev/null; do
  echo "Primary DC DB not ready yet, sleeping 3s..."
  sleep 3
done

echo "Primary DC DB is READY! Cleaning PGDATA and starting pg_basebackup..."
rm -rf ${PGDATA}/*

PGPASSWORD=replica_password pg_basebackup \
  -h postgres-dc \
  -D ${PGDATA} \
  -U replicator \
  -vP \
  -R \
  -S drc_slot \
  -X stream

chmod 700 ${PGDATA}

echo "Starting PostgreSQL Standby in DRC..."
exec docker-entrypoint.sh postgres
