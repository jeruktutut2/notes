#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Queue (Asynq/Redis)"
echo "====================================================="

echo "[1/4] Menyalakan Redis (Docker)..."
docker-compose up -d --wait
echo "✅ Redis siap di port 6382!"
echo ""

echo "[2/4] Build Client & Worker..."
go build -o app_client cmd/client/main.go
go build -o app_worker cmd/worker/main.go

echo "[3/4] Menjalankan Worker di Background..."
./app_worker &
WORKER_PID=$!

sleep 2
echo ""
echo "[4/4] Menjalankan Client untuk push task ke Antrean..."
echo "-----------------------------------------------------"
./app_client
echo "-----------------------------------------------------"
echo "Client selesai melakukan enqueue. Perhatikan log Worker di bawah ini!"
echo "Worker akan memproses task secara asinkron."
echo "Tunggu sekitar 8-10 detik agar task delay dieksekusi..."
echo ""

# Beri waktu worker menyelesaikan tugas (termasuk tugas delay 5 detik)
sleep 10

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $WORKER_PID
rm -f app_client app_worker
docker-compose down
echo "🎉 Selesai!"
