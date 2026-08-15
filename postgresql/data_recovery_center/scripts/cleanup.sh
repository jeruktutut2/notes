#!/bin/bash
# ============================================
# Script: cleanup.sh
# Membersihkan seluruh container dan volume
# ============================================
set -e

echo "=================================================="
echo "  Cleaning up Data Recovery Center Environment"
echo "=================================================="

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "Stopping containers and removing volumes..."
docker-compose down -v --remove-orphans

echo ""
echo "Cleaning lingering Docker resources related to project..."
docker volume rm drc_pg_dc_data drc_pg_drc_data 2>/dev/null || true

echo "=================================================="
echo "  [OK] Environment completely cleaned up."
echo "=================================================="
