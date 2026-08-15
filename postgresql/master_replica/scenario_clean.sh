#!/bin/bash
set -e

echo "========================================================"
echo " SKENARIO CLEANUP: MEMBERSINKAN DOCKER CLUSTER, ETCD & VOLUMES"
echo "========================================================"

echo "[1/2] Menghentikan semua container dan menghapus volume persistent..."
docker compose --profile scale down -v --remove-orphans || true

echo ""
echo "[2/2] Memeriksa sisa container..."
docker compose ps || true

echo ""
echo "=== CLEANUP SELESAI: CLUSTER, ETCD & VOLUMES SUDAH BERSIH TOTAL ==="
