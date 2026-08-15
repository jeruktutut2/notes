#!/bin/bash
set -e

echo "Starting Docker Compose services..."
docker compose up -d

echo "Waiting for PostgreSQL to be ready..."
sleep 5

echo "Taking Base Backup..."
docker exec pitr_postgres pg_basebackup -U myuser -D /var/lib/postgresql/backup/base_backup -Fp -Xs -P -R
echo "Base backup created at ./backup/base_backup"
