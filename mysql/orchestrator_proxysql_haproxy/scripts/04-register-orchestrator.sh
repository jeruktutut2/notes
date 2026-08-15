#!/bin/bash
set -e

echo "=================================================="
echo "🎯 Menginstruksikan Orchestrator Menemukan Topologi MySQL..."
echo "=================================================="

# Daftarkan master node ke Orchestrator via API
curl -s "http://localhost:3000/api/discover/mysql-master/3306" > /dev/null || true
curl -s "http://localhost:3000/api/discover/mysql-replica1/3306" > /dev/null || true
curl -s "http://localhost:3000/api/discover/mysql-replica2/3306" > /dev/null || true

sleep 3
echo "✅ Status Topologi dari Orchestrator API:"
curl -s "http://localhost:3000/api/topology-tabulated" || true
echo ""
