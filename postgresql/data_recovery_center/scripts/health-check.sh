#!/bin/bash
# ============================================
# Script: health-check.sh
# Memeriksa kesehatan seluruh komponen sistem DC dan DRC
# ============================================
set -e

echo "=================================================="
echo "  Data Recovery Center System Health Check"
echo "=================================================="
echo "Checked at: $(date)"
echo ""

echo "[1/4] Docker Containers Status:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo ""

echo "[2/4] Application Health API Check:"
APP_HEALTH=$(curl -s http://localhost:8080/health || echo '{"status":"OFFLINE"}')
echo "  http://localhost:8080/health -> $APP_HEALTH"
echo ""

echo "[3/4] Database Status & Modes:"
DC_MODE=$(docker exec -i pg-dc psql -U appuser -d appdb -t -c "SELECT pg_is_in_recovery();" 2>/dev/null | tr -d ' ' || echo "OFFLINE")
DRC_MODE=$(docker exec -i pg-drc psql -U appuser -d appdb -t -c "SELECT pg_is_in_recovery();" 2>/dev/null | tr -d ' ' || echo "OFFLINE")

echo "  - PostgreSQL DC  (Port 5432): Mode in_recovery = $DC_MODE (f = Primary)"
echo "  - PostgreSQL DRC (Port 5433): Mode in_recovery = $DRC_MODE (t = Standby)"
echo ""

echo "[4/4] PgBouncer Connection Pools:"
DC_PGBOUNCER=$(docker exec -i pgbouncer-dc pg_isready -h 127.0.0.1 -p 6432 2>/dev/null && echo "READY" || echo "OFFLINE")
DRC_PGBOUNCER=$(docker exec -i pgbouncer-drc pg_isready -h 127.0.0.1 -p 6432 2>/dev/null && echo "READY" || echo "OFFLINE")

echo "  - PgBouncer DC  (Port 6432): $DC_PGBOUNCER"
echo "  - PgBouncer DRC (Port 6433): $DRC_PGBOUNCER"

echo "=================================================="
