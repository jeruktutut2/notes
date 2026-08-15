#!/bin/bash
# ============================================
# Script: check-replication.sh
# Memeriksa status streaming replication dari DC ke DRC
# ============================================
set -e

echo "=================================================="
echo "  PostgreSQL Streaming Replication Status Check"
echo "=================================================="

# Check if containers are running
if ! docker ps | grep -q "pg-dc"; then
    echo "[ERROR] Container pg-dc is not running!"
    exit 1
fi

echo "[1/3] Primary (DC) Replication Status:"
docker exec -i pg-dc psql -U appuser -d appdb -c "
SELECT
    client_addr,
    application_name,
    state,
    sync_state,
    sync_priority,
    pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes
FROM pg_stat_replication;
" || echo "  [WARN] Unable to query pg_stat_replication (Primary might be down)"

echo ""
echo "[2/3] Standby (DRC) Recovery Status:"
if docker ps | grep -q "pg-drc"; then
    docker exec -i pg-drc psql -U appuser -d appdb -c "
    SELECT
        pg_is_in_recovery() AS is_standby,
        pg_last_wal_receive_lsn() AS receive_lsn,
        pg_last_wal_replay_lsn() AS replay_lsn,
        pg_last_xact_replay_timestamp() AS last_transaction_time;
    " || echo "  [WARN] Unable to query DRC (Might be offline or promoted)"
else
    echo "  [INFO] Container pg-drc is not running"
fi

echo ""
echo "[3/3] Data Consistency Check (Row Counts):"
DC_COUNT=$(docker exec -i pg-dc psql -U appuser -d appdb -t -c "SELECT COUNT(*) FROM application_data;" 2>/dev/null | tr -d ' ' || echo "N/A (DC Offline)")
DRC_COUNT=$(docker exec -i pg-drc psql -U appuser -d appdb -t -c "SELECT COUNT(*) FROM application_data;" 2>/dev/null | tr -d ' ' || echo "N/A (DRC Offline)")

echo "  - Total records in DC Primary:  $DC_COUNT"
echo "  - Total records in DRC Standby: $DRC_COUNT"

if [ "$DC_COUNT" = "$DRC_COUNT" ] && [ "$DC_COUNT" != "N/A (DC Offline)" ]; then
    echo ""
    echo "  ✅ PERFECT SYNC: Data di DC dan DRC 100% identik!"
elif [ "$DC_COUNT" != "N/A (DC Offline)" ]; then
    echo ""
    echo "  ⚠️ LAG DETECTED: Jumlah data DC ($DC_COUNT) != DRC ($DRC_COUNT)"
fi
echo "=================================================="
