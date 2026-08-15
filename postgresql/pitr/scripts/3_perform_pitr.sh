#!/bin/bash
set -e

if [ -z "$1" ]; then
  echo "Usage: $0 'YYYY-MM-DD HH:MM:SS'"
  echo "Example: $0 '2026-08-11 16:00:00'"
  exit 1
fi

TARGET_TIME="$1"

echo "Stopping PostgreSQL and PgBouncer containers..."
docker compose stop db pgbouncer

echo "Cleaning up current data directory (simulating corruption/data loss state)..."
# We need to clear the data dir but keep the volume.
# Since it's mounted to ./data on host, we can remove contents locally
rm -rf ../data/*

echo "Restoring from Base Backup..."
cp -R ../backup/base_backup/* ../data/

echo "Creating recovery.signal to initiate Point-In-Time Recovery..."
touch ../data/recovery.signal

echo "Configuring PostgreSQL to recover until '$TARGET_TIME'..."
# Adding recovery parameters to postgresql.conf inside the restored data directory
# In PG 12+, recovery settings go into postgresql.conf
cat <<EOF >> ../data/postgresql.conf
restore_command = 'cp /var/lib/postgresql/archive/%f %p'
recovery_target_time = '$TARGET_TIME'
recovery_target_action = 'promote'
EOF

echo "Starting PostgreSQL container..."
docker compose start db

echo "PostgreSQL is now starting in recovery mode. It may take a few seconds."
echo "Please monitor the logs: docker compose logs -f db"
echo "Once recovered, you can start PgBouncer: docker compose start pgbouncer"
