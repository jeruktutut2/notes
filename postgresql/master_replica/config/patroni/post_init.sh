#!/bin/bash
set -e

echo "=== Running Patroni post_init bootstrap script ==="
psql -U postgres -d postgres -c "CREATE USER appuser WITH PASSWORD 'apppassword';" || true
psql -U postgres -d postgres -c "CREATE DATABASE appdb OWNER appuser;" || true
psql -U postgres -d appdb -c "
  CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
  );
  GRANT ALL PRIVILEGES ON TABLE users TO appuser;
  GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO appuser;
" || true
echo "=== Patroni post_init complete ==="
