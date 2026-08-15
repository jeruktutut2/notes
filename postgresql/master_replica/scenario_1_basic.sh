#!/bin/bash
set -e

echo "========================================================"
echo " SKENARIO 1: CLUSTER INIT (PATRONI + ETCD + HAPROXY + PGBOUNCER)"
echo "========================================================"

echo "[1/8] Membersihkan container & volume lama, lalu Menjalankan Cluster Patroni..."
docker compose --profile scale down -v --remove-orphans || true
docker compose up -d --build etcd postgres_node1
sleep 5
docker compose up -d --build postgres_node2 postgres_node3 haproxy pgbouncer app_echo

echo "Menunggu seluruh service & health check Patroni & HAProxy siap (25 detik)..."
sleep 25

echo ""
echo "[2/8] Memeriksa Status Cluster Patroni (patronictl list)..."
docker compose exec postgres_node1 patronictl -c /tmp/patroni.yml list || true

echo ""
echo "[3/8] Memeriksa HAProxy Dashboard Status (http://localhost:7000)..."
curl -s http://localhost:7000/ > /dev/null && echo "HAProxy Stats Web Dashboard is UP on http://localhost:7000"

echo ""
echo "[4/8] Memeriksa Node Status via Golang Echo API (/api/status)..."
curl -s http://localhost:8085/api/status | jq . || curl -s http://localhost:8085/api/status

echo ""
echo "[5/8] SEBELUM INSERT: Memeriksa Isi Tabel 'users' Awal di Seluruh Node..."
echo "--- SQL SELECT di Node 1 (postgres_node1) ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 3 (postgres_node3) ---"
docker compose exec postgres_node3 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "[6/8] Menguji Write ke Active Leader via Echo API (Golang -> PgBouncer -> HAProxy:5000 -> Patroni Leader)..."
curl -s -X POST http://localhost:8085/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Budi Master User", "email": "budi@example.com"}' | jq . || true

echo ""
echo "[7/8] Menguji Read dari Replica via Echo API (Golang -> PgBouncer -> HAProxy:5001 -> Patroni Replicas)..."
curl -s http://localhost:8085/api/users | jq . || true

echo ""
echo "[8/8] SESUDAH INSERT: Memeriksa Isi Tabel 'users' Hasil di Seluruh Node..."
echo "--- SQL SELECT di Node 1 (postgres_node1) ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 3 (postgres_node3) ---"
docker compose exec postgres_node3 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "Menghentikan dan membersihkan container Docker Compose..."
docker compose --profile scale down -v --remove-orphans || true

echo ""
echo "=== SKENARIO 1 SELESAI DENGAN SUKSES ==="

