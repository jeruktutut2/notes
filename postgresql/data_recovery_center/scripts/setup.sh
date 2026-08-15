#!/bin/bash
# ============================================
# Script: setup.sh
# Memulai seluruh lingkungan DC dan DRC
# ============================================
set -e

echo "=================================================="
echo "  Data Recovery Center (DRC) Setup Environment"
echo "=================================================="

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "[1/4] Cleaning previous docker containers and volumes..."
docker-compose down -v --remove-orphans || true

echo ""
echo "[2/4] Building and starting containers..."
echo "  - pg-dc (PostgreSQL Data Center Primary)"
echo "  - pg-drc (PostgreSQL Recovery Center Standby)"
echo "  - pgbouncer-dc (Connection pooler DC)"
echo "  - pgbouncer-drc (Connection pooler DRC)"
echo "  - app (Golang Echo v5 API)"
echo ""

docker-compose up -d --build

echo ""
echo "[3/4] Waiting for services to become healthy..."
echo "  This may take 30-45 seconds while pg-drc syncs via pg_basebackup..."

attempt=0
max_attempts=30

until [ $attempt -ge $max_attempts ]; do
    dc_status=$(docker inspect --format='{{.State.Health.Status}}' pg-dc 2>/dev/null || echo "starting")
    drc_status=$(docker inspect --format='{{.State.Health.Status}}' pg-drc 2>/dev/null || echo "starting")
    app_status=$(docker inspect --format='{{.State.Health.Status}}' drc-app 2>/dev/null || echo "starting")

    echo "  Status check ($((attempt+1))/$max_attempts): pg-dc=[$dc_status] pg-drc=[$drc_status] app=[$app_status]"

    if [ "$dc_status" = "healthy" ] && [ "$drc_status" = "healthy" ] && [ "$app_status" = "healthy" ]; then
        echo ""
        echo "=================================================="
        echo "  [SUCCESS] Environment fully initialized!"
        echo "=================================================="
        echo "  - App API:        http://localhost:8080"
        echo "  - DC PostgreSQL:  localhost:5432"
        echo "  - DRC PostgreSQL: localhost:5433"
        echo "  - DC PgBouncer:   localhost:6432"
        echo "  - DRC PgBouncer:  localhost:6433"
        echo "=================================================="
        exit 0
    fi

    attempt=$((attempt+1))
    sleep 3
done

echo ""
echo "[WARN] Timeout waiting for healthy status. Displaying container logs..."
docker-compose logs --tail=30 pg-drc
