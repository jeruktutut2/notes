#!/bin/bash
# ============================================
# Script: monitor.sh
# Real-time Monitoring Dashboard for DC & DRC
# ============================================

INTERVAL=3

clear

while true; do
    tput cup 0 0
    echo "================================================================================"
    echo "         DATA RECOVERY CENTER (DRC) REAL-TIME MONITORING DASHBOARD              "
    echo "================================================================================"
    echo " Time: $(date '+%Y-%m-%d %H:%M:%S')  |  Refresh Rate: ${INTERVAL}s"
    echo "--------------------------------------------------------------------------------"

    # Container status
    echo " [1] CONTAINER STATUS:"
    docker ps --format "  - {{.Names}}\t: {{.Status}}" 2>/dev/null || echo "  No containers running"
    echo "--------------------------------------------------------------------------------"

    # App Status API
    echo " [2] GOLANG APP ACTIVE TARGET & HEALTH:"
    APP_STATUS=$(curl -s http://localhost:8080/health 2>/dev/null || echo '{"status":"OFFLINE"}')
    echo "  App Status: $APP_STATUS"
    echo "--------------------------------------------------------------------------------"

    # DB Row count & sync check
    echo " [3] DATA CONSISTENCY (ROW COUNTS):"
    DC_ROWS=$(docker exec -i pg-dc psql -U appuser -d appdb -t -c "SELECT COUNT(*) FROM application_data;" 2>/dev/null | tr -d ' ' || echo "OFFLINE")
    DRC_ROWS=$(docker exec -i pg-drc psql -U appuser -d appdb -t -c "SELECT COUNT(*) FROM application_data;" 2>/dev/null | tr -d ' ' || echo "OFFLINE")

    echo "  - DC Primary  Row Count : $DC_ROWS"
    echo "  - DRC Standby Row Count : $DRC_ROWS"
    echo "--------------------------------------------------------------------------------"

    # Replication Stats
    echo " [4] REPLICATION METRICS (from DC):"
    docker exec -i pg-dc psql -U appuser -d appdb -c "
    SELECT
        client_addr AS standby_ip,
        state,
        sync_state,
        pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS lag_bytes
    FROM pg_stat_replication;
    " 2>/dev/null || echo "  Unable to fetch replication stats (DC offline or failover active)"
    echo "--------------------------------------------------------------------------------"

    # Recent DR Logs
    echo " [5] RECENT DISASTER RECOVERY LOGS (Last 3 events):"
    docker exec -i pg-drc psql -U appuser -d appdb -c "
    SELECT id, event_type, event_source, description, created_at
    FROM disaster_recovery_logs
    ORDER BY id DESC LIMIT 3;
    " 2>/dev/null || echo "  Unable to fetch DR logs"
    echo "================================================================================"
    echo " Press [Ctrl+C] to stop monitoring."

    sleep $INTERVAL
done
