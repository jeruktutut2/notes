#!/bin/bash
set -e

echo "=== Initializing PostgreSQL Master ==="

# Create replication user and application database/user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replica_password';
    
    CREATE USER appuser WITH ENCRYPTED PASSWORD 'apppassword';
    CREATE DATABASE appdb OWNER appuser;
    
    \c appdb
    GRANT ALL PRIVILEGES ON SCHEMA public TO appuser;
    
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    
    GRANT ALL PRIVILEGES ON TABLE users TO appuser;
    GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO appuser;
EOSQL

echo "host replication replicator 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
echo "host appdb appuser 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"
echo "host all all 0.0.0.0/0 md5" >> "$PGDATA/pg_hba.conf"

echo "=== Master Initialization Complete ==="
