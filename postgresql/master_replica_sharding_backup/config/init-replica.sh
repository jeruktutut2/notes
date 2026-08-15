#!/bin/bash
set -e

echo "=== Initializing Standby Replica Node ==="

until pg_isready -h citus-coordinator -p 5432 -U postgres; do
  echo "Waiting for citus-coordinator to be ready..."
  sleep 2
done

chown -R postgres:postgres "$PGDATA"

# Jika PG_VERSION belum ada, lakukan pg_basebackup dari master
if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo "Cloning data directory from Master via pg_basebackup..."
    rm -rf ${PGDATA:?}/*
    gosu postgres PGPASSWORD=replica_pass pg_basebackup -h citus-coordinator -D "$PGDATA" -U replicator -v -P -X stream -Fp
    touch "$PGDATA/standby.signal"
    echo "primary_conninfo = 'host=citus-coordinator port=5432 user=replicator password=replica_pass'" >> "$PGDATA/postgresql.conf"
    echo "hot_standby = on" >> "$PGDATA/postgresql.conf"
    chown -R postgres:postgres "$PGDATA"
    chmod 700 "$PGDATA"
fi

echo "Starting Standby Replica Postgres as user postgres..."
exec gosu postgres postgres -D "$PGDATA"
