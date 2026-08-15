#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Session (Redis)"
echo "====================================================="

echo "[1/4] Menyalakan Redis (Docker)..."
docker-compose up -d --wait
echo "✅ Redis siap di port 6381!"
echo ""

echo "[2/4] Build & Menjalankan Server Go di background..."
go build -o app_server main.go
./app_server &
SERVER_PID=$!

sleep 2

echo "[3/4] Skenario Pengujian..."
echo "-> 1. Melakukan Login..."
LOGIN_RESP=$(curl -s -X POST http://localhost:8080/login)
echo "Response: $LOGIN_RESP"

# Ekstrak session_id pakai grep & sed/awk atau bash regex
SESSION_ID=$(echo $LOGIN_RESP | grep -o '"session_id":"[^"]*' | cut -d'"' -f4)
echo "🔑 Didapat Session ID: $SESSION_ID"
echo ""

echo "-> 2. Mengakses Profil (Dengan Session ID yang Valid)..."
curl -s -H "X-Session-ID: $SESSION_ID" http://localhost:8080/profile
echo -e "\n"

echo "-> 3. Mengakses Profil (Tanpa Session ID)..."
curl -s http://localhost:8080/profile
echo -e "\n"

echo "-> 4. Melakukan Logout..."
curl -s -X POST -H "X-Session-ID: $SESSION_ID" http://localhost:8080/logout
echo -e "\n"

echo "-> 5. Mengakses Profil (Setelah Logout)..."
curl -s -H "X-Session-ID: $SESSION_ID" http://localhost:8080/profile
echo -e "\n"

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $SERVER_PID
rm -f app_server
docker-compose down
echo "🎉 Selesai!"
