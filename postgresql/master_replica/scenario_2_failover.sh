#!/bin/bash
set -e

echo "========================================================"
echo " SKENARIO 2: AUTOMATED PATRONI + ETCD FAILOVER & HAPROXY ROUTING"
echo "========================================================"

echo "[1/9] Membersihkan container & volume lama, lalu Menjalankan Docker Compose Cluster..."
docker compose --profile scale down -v --remove-orphans || true
docker compose up -d --build etcd postgres_node1
sleep 5
docker compose up -d --build postgres_node2 postgres_node3 haproxy pgbouncer app_echo

echo "Menunggu seluruh service & health check Patroni & HAProxy siap (25 detik)..."
sleep 25

echo ""
echo "[2/9] PRE-FAILOVER: Memeriksa Status Cluster Patroni Awal..."
docker compose exec postgres_node1 patronictl -c /tmp/patroni.yml list || true

echo ""
echo "[3/9] PRE-FAILOVER: Menulis Data User Sebelum Node 1 Down..."
curl -s -X POST http://localhost:8085/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Pre-Failover User", "email": "pre_failover@example.com"}' | jq . || true

echo ""
echo "[4/9] PRE-FAILOVER: Memeriksa Data Tersinkron di Node 1 & Node 2..."
echo "--- SQL SELECT di Node 1 (postgres_node1) ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "[5/9] FAILOVER OTOMATIS: Menghentikan Leader Awal (postgres_node1)..."
docker compose stop postgres_node1

echo ""
echo "Menunggu Patroni + etcd mendeteksi failure & mempromosikan Leader baru (35 detik agar melewati TTL 30s)..."
sleep 35

echo ""
echo "[6/9] POST-FAILOVER: Memeriksa Status Cluster Patroni (Melihat Leader Baru Otomatis)..."
docker compose exec postgres_node2 patronictl -c /tmp/patroni.yml list || true

echo ""
echo "[7/9] POST-FAILOVER: Memeriksa Data Pre-Failover di Leader Baru (postgres_node2 / node3)..."
echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "[8/9] POST-FAILOVER: Menulis Data Baru via Echo API (HAProxy OTOMATIS Mengarahkan Write ke Leader Baru)..."
curl -s -X POST http://localhost:8085/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Siti Post-Failover User", "email": "siti@example.com"}' | jq . || true

echo ""
echo "[9/9] POST-FAILOVER: Memeriksa Hasil Akhir Tabel 'users' di Node 2 & Node 3..."
echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 3 (postgres_node3) ---"
docker compose exec postgres_node3 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "Menghentikan dan membersihkan container Docker Compose..."
docker compose --profile scale down -v --remove-orphans || true

echo ""
echo "=== SKENARIO 2 SELESAI DENGAN SUKSES ==="

