#!/bin/bash
set -e

echo "========================================================"
echo " SKENARIO 3: SCALE OUT NODE KE-4 DENGAN PATRONI & ETCD"
echo "========================================================"

echo ""
echo "[1/10] Membersihkan container & volume lama, lalu Menjalankan Cluster Awal (Node 1, 2, 3)..."
docker compose --profile scale down -v --remove-orphans || true
docker compose up -d --build etcd postgres_node1
sleep 5
docker compose up -d --build postgres_node2 postgres_node3 haproxy pgbouncer app_echo
echo "Menunggu seluruh service cluster awal siap (25 detik)..."
sleep 25

echo ""
echo "[2/10] PRE-SCALE OUT: Menulis Data Awal ke Cluster Awal via Echo API..."
curl -s -X POST http://localhost:8085/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Initial Cluster User", "email": "initial@example.com"}' | jq . || true

echo ""
echo "[3/10] PRE-SCALE OUT: Memeriksa Data Awal di Cluster Awal (Node 1, Node 2, Node 3)..."
echo "--- SQL SELECT di Node 1 (postgres_node1) ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 3 (postgres_node3) ---"
docker compose exec postgres_node3 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "[4/10] PRE-SCALE OUT: Memeriksa Status Cluster Patroni Awal (Node 1, 2, 3)..."
docker compose exec postgres_node1 patronictl -c /tmp/patroni.yml list || true

echo ""
echo "[5/10] SCALE OUT: Menyalakan Node ke-4 (postgres_node4) via Docker Profile..."
docker compose --profile scale up -d postgres_node4

echo "Menunggu Patroni meng-clone snapshot & mendaftarkan Node ke-4 ke etcd (15 detik)..."
sleep 15

echo ""
echo "[6/10] POST-SCALE OUT: Memeriksa Status Cluster Patroni Terbaru (Melihat postgres_node4 Bergabung)..."
docker compose exec postgres_node1 patronictl -c /tmp/patroni.yml list || docker compose exec postgres_node2 patronictl -c /tmp/patroni.yml list || true

echo ""
echo "[7/10] HASIL CLONE: Memeriksa Data di Node ke-4 (Membuktikan Node ke-4 Meng-clone Data Awal)..."
echo "--- SQL SELECT di Node 4 Baru (postgres_node4) ---"
docker compose exec postgres_node4 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "[8/10] REPLIKASI REAL-TIME: Write Data Baru (Dewi Scale-Out User) via Golang Echo API..."
curl -s -X POST http://localhost:8085/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Dewi Scale-Out User", "email": "dewi@example.com"}' | jq . || true

echo ""
echo "[9/10] Menguji Read Data via Golang Echo API..."
curl -s http://localhost:8085/api/users | jq . || true

echo ""
echo "[10/10] HASIL AKHIR: Memeriksa Isi Tabel 'users' Hasil di Seluruh Node (Node 1-4)..."
echo "--- SQL SELECT di Node 1 (postgres_node1) ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 2 (postgres_node2) ---"
docker compose exec postgres_node2 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 3 (postgres_node3) ---"
docker compose exec postgres_node3 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo "--- SQL SELECT di Node 4 (postgres_node4) ---"
docker compose exec postgres_node4 psql -U appuser -d appdb -c "SELECT * FROM users;" || true

echo ""
echo "Menghentikan dan membersihkan container Docker Compose..."
docker compose --profile scale down -v --remove-orphans || true

echo ""
echo "=== SKENARIO 3 SELESAI DENGAN SUKSES ==="




