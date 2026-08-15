#!/bin/bash
set -e

# ============================================
# Setup Script: Data Recovery Center (Standby)
# ============================================
# Script ini menggantikan entrypoint default PostgreSQL
# untuk mengkonfigurasi DRC sebagai Streaming Replication Standby
# ============================================

echo "============================================"
echo "  Setting Up Data Recovery Center (Standby)"
echo "============================================"

# Configuration
PGDATA=${PGDATA:-/var/lib/postgresql/data/pgdata}
PRIMARY_HOST=${PRIMARY_HOST:-pg-dc}
PRIMARY_PORT=${PRIMARY_PORT:-5432}
REPLICATOR_USER=${REPLICATOR_USER:-replicator}
REPLICATOR_PASS=${REPLICATOR_PASS:-replicator_pass}

echo ""
echo "Configuration:"
echo "  PGDATA:         $PGDATA"
echo "  Primary Host:   $PRIMARY_HOST"
echo "  Primary Port:   $PRIMARY_PORT"
echo "  Replicator:     $REPLICATOR_USER"
echo ""

# ============================================
# Step 1: Wait for Primary (DC) to be ready
# ============================================
echo "[Step 1] Waiting for Primary (${PRIMARY_HOST}) to be ready..."

MAX_RETRIES=60
RETRY=0
until PGPASSWORD=${REPLICATOR_PASS} pg_isready -h ${PRIMARY_HOST} -p ${PRIMARY_PORT} -U ${REPLICATOR_USER} 2>/dev/null; do
    RETRY=$((RETRY + 1))
    if [ $RETRY -ge $MAX_RETRIES ]; then
        echo "[ERROR] Primary not ready after ${MAX_RETRIES} attempts. Exiting."
        exit 1
    fi
    echo "  Attempt ${RETRY}/${MAX_RETRIES}: Primary not ready. Retrying in 2s..."
    sleep 2
done
echo "[OK] Primary is ready!"

# Additional wait for replication slot to be created
echo "[Step 1.1] Waiting for replication slot..."
sleep 5

# ============================================
# Step 2: Initialize Standby via pg_basebackup
# ============================================
if [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo ""
    echo "[Step 2] Data directory is empty. Running pg_basebackup..."
    echo "  This will copy all data from DC (Primary) to DRC (Standby)"
    echo ""

    # Clean data directory
    rm -rf ${PGDATA}/*

    # ============================================
    # pg_basebackup - Key flags:
    #   -h: Primary host
    #   -p: Primary port
    #   -U: Replication user
    #   -D: Target data directory
    #   -Fp: Output format = plain
    #   -Xs: WAL method = stream
    #   -R: Create standby.signal and set primary_conninfo
    #   -P: Show progress
    #   -v: Verbose output
    #   --slot: Use replication slot
    # ============================================
    PGPASSWORD=${REPLICATOR_PASS} pg_basebackup \
        -h ${PRIMARY_HOST} \
        -p ${PRIMARY_PORT} \
        -U ${REPLICATOR_USER} \
        -D ${PGDATA} \
        -Fp -Xs -R -P -v \
        --slot=drc_slot \
        --checkpoint=fast

    echo ""
    echo "[OK] Base backup completed successfully!"

    # Verify standby.signal was created by -R flag
    if [ -f "${PGDATA}/standby.signal" ]; then
        echo "[OK] standby.signal file found - Standby mode will be active"
    else
        echo "[WARN] Creating standby.signal manually..."
        touch ${PGDATA}/standby.signal
    fi

    # ============================================
    # Step 3: Configure Standby Parameters
    # ============================================
    echo ""
    echo "[Step 3] Configuring standby parameters..."

    cat >> ${PGDATA}/postgresql.auto.conf <<EOF

# ============================================
# DRC Standby Configuration
# Added by setup-standby.sh
# ============================================
hot_standby = on
hot_standby_feedback = on
wal_receiver_timeout = 60s
max_connections = 200
shared_buffers = 128MB
effective_cache_size = 256MB
EOF

    # Set proper permissions (required by PostgreSQL)
    chmod 0700 ${PGDATA}

    echo "[OK] Standby configuration complete"
else
    echo ""
    echo "[Step 2] Data directory already initialized."
    echo "  Starting as standby with existing data..."
fi

# ============================================
# Step 4: Start PostgreSQL in Standby Mode
# ============================================
echo ""
echo "============================================"
echo "  Starting PostgreSQL in Standby Mode"
echo "============================================"
echo ""
echo "  Mode: Hot Standby (read-only queries allowed)"
echo "  Replicating from: ${PRIMARY_HOST}:${PRIMARY_PORT}"
echo ""

# Start PostgreSQL
exec postgres \
    -c hot_standby=on \
    -c max_connections=200 \
    -c log_statement=all
