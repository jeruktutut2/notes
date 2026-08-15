#!/bin/bash
# ============================================
# Script: simulate-dc-down.sh
# Skenario: Simulasi Data Center Utam Mampu / Down (Bencana)
# ============================================
set -e

echo "=================================================="
echo "  SKENARIO: SIMULASI DATA CENTER (DC) DOWN / OFF"
echo "=================================================="
echo "  Penjelasan:"
echo "  Terjadi bencana / kegagalan server pada DC."
echo "  Container 'pg-dc' akan dimatikan secara paksa."
echo "=================================================="
echo ""

echo "[1/3] Mematikan container pg-dc (PostgreSQL Data Center)..."
docker stop pg-dc

echo ""
echo "[2/3] Verifikasi status container pg-dc..."
docker ps -a --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep pg-dc || echo "pg-dc status: STOPPED"

echo ""
echo "[3/3] Menguji kesehatan Aplikasi (Health Check)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/health || echo "000")
HEALTH_BODY=$(curl -s http://localhost:8080/health || echo "Failed to connect")

echo "  Response Code: $HTTP_CODE"
echo "  Body: $HEALTH_BODY"

echo ""
echo "=================================================="
echo "  ⚠️ KONDISI SAAT INI:"
echo "  1. DC Primary: DOWN ❌"
echo "  2. DRC Standby: UP (tetapi masih dalam mode read-only standby)"
echo "  3. Aplikasi: Terdeteksi DEGRADED (koneksi DC putus)"
echo ""
echo "  LANGKAH SELANJUTNYA:"
echo "  Jalankan './scripts/failover.sh' untuk mempromosikan DRC"
echo "  menjadi Primary baru dan mengalihkan aplikasi ke DRC!"
echo "=================================================="
