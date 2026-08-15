#!/usr/bin/env bash
set -e

# File: scenario_playground.sh
# Purpose: Skenario Playground (Hanya 1 DB: DB1 & Golang Echo API)
# Melakukan Insert & Select langsung ke DB1 dan via Golang Echo API

echo "=========================================================================="
echo " 🚀 SKENARIO PLAYGROUND: Single DB (DB1) & Golang Echo API Test "
echo "=========================================================================="

echo ""
echo "[1/4] Memulai Service (Hanya DB1 & App Echo)..."
docker compose up -d postgres_node1 app_echo

echo ""
echo "Menunggu service DB1 & Golang Echo API siap (10 detik)..."
sleep 10

echo ""
echo "[2/4] DIRECT DB1: Melakukan INSERT & SELECT langsung ke DB1 (postgres_node1)..."
echo "--- Performing Direct INSERT on DB1 ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c \
  "INSERT INTO users (name, email) VALUES ('User Direct DB1', 'db1_direct@playground.local');"

echo ""
echo "--- Performing Direct SELECT on DB1 ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c \
  "SELECT id, name, email, created_at FROM users ORDER BY id DESC LIMIT 5;"

echo ""
echo "[3/4] GOLANG API: Melakukan INSERT via Golang Echo API (POST http://localhost:8085/api/users)..."
curl -s -X POST http://localhost:8085/api/users \
  -H "Content-Type: application/json" \
  -d '{"name": "User Golang Playground", "email": "golang_playground@example.com"}' | jq . || true

echo ""
echo "[4/4] VERIFIKASI AKHIR: Memeriksa Data di DB1..."
echo "--- SQL SELECT di DB1 (postgres_node1) ---"
docker compose exec postgres_node1 psql -U appuser -d appdb -c \
  "SELECT id, name, email, created_at FROM users ORDER BY id DESC LIMIT 5;" || true

echo ""
echo "--- SQL SELECT via Golang API (GET http://localhost:8085/api/users) ---"
curl -s http://localhost:8085/api/users | jq . || true

echo ""
echo "Menghentikan dan membersihkan container Docker Compose..."
docker compose --profile scale down -v --remove-orphans || true

echo ""
echo "=========================================================================="
echo " ✅ Skenario Playground (Single DB1) selesai dijalankan!"
echo "=========================================================================="
