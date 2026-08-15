#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Scheduler"
echo "====================================================="

echo "[1/4] Menyalakan Redis (Docker)..."
docker-compose up -d --wait
echo "✅ Redis siap di port 6383!"
echo ""

echo "[2/4] Build Server..."
go build -o app_scheduler main.go

echo "[3/4] Menjalankan 3 Node secara bersamaan..."
echo "-----------------------------------------------------"
echo "Diharapkan meskipun ketiga Node mengeksekusi cron setiap 2 detik,"
echo "HANYA ADA SATU NODE yang mengeksekusi '[WORK] Report harian' per siklus (2 detik)."
echo "-----------------------------------------------------"

NODE_ID="Node-A" ./app_scheduler &
PIDA=$!

NODE_ID="Node-B" ./app_scheduler &
PIDB=$!

NODE_ID="Node-C" ./app_scheduler &
PIDC=$!

# Biarkan berjalan selama 10 detik agar terlihat pola eksekusinya
sleep 10

echo ""
echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $PIDA $PIDB $PIDC
rm -f app_scheduler
docker-compose down
echo "🎉 Selesai!"
