#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$ROOT_DIR"

echo "=========================================================================="
echo "   ORKESTRASI SKENARIO PROGRESIF POSTGRESQL MULTI-NODE CLUSTER"
echo "   (Master-Replica + Horizontal Sharding)"
echo "=========================================================================="

echo "[0/3] Pembersihan & Inisialisasi Lingkungan Docker Compose..."
docker compose down -v --remove-orphans || true
docker compose up -d

echo "Menunggu Master Coordinator siap..."
until docker exec citus-coordinator pg_isready -U postgres -d app_db >/dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo " Master Coordinator Siap!"

echo "Menunggu Standby Replica siap..."
until docker exec citus-coordinator-replica pg_isready -U postgres -d app_db >/dev/null 2>&1; do
    echo -n "."
    sleep 2
done
echo " Standby Replica Siap!"
echo ""

sleep 2

# Tahap 1: Master-Replica Streaming Replication
bash "$SCRIPT_DIR/step1_master_replica.sh"
echo ""

# Tahap 2: Horizontal Sharding (Citus Cluster)
bash "$SCRIPT_DIR/step2_sharding.sh"
echo ""

# Tahap 3: Automated Backup (Dilewati sesuai instruksi user)
# bash "$SCRIPT_DIR/step3_backup_restore.sh"

echo "=========================================================================="
echo "   TAHAP 1 & TAHAP 2 SKENARIO PROGRESIF BERHASIL DIJALANKAN DENGAN SUKSES!"
echo "   (Bagian Backup sengaja dilewati)"
echo "=========================================================================="
