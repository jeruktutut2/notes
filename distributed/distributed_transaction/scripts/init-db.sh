#!/bin/bash
set -e

# Script untuk membuat multiple database di PostgreSQL
# Dijalankan saat container PostgreSQL pertama kali start

DATABASES=("order_db" "payment_db" "inventory_db" "shipping_db" "notification_db")

for db in "${DATABASES[@]}"; do
    echo "Creating database: $db"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE DATABASE $db;
        GRANT ALL PRIVILEGES ON DATABASE $db TO $POSTGRES_USER;
EOSQL
    echo "Database $db created successfully."
done

echo "All databases created!"
