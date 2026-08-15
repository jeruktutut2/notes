#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Messaging (Pub/Sub)"
echo "====================================================="

echo "[1/4] Menyalakan RabbitMQ (Docker)..."
# Tunggu RabbitMQ benar-benar siap (butuh waktu lebih lama dari Redis)
docker-compose up -d
echo "Menunggu RabbitMQ siap menerima koneksi (sekitar 10 detik)..."
sleep 15
echo "✅ RabbitMQ siap!"
echo ""

echo "[2/4] Build Publisher & Subscriber..."
go build -o app_publisher cmd/publisher/main.go
go build -o app_subscriber cmd/subscriber/main.go

echo "[3/4] Menjalankan 2 Subscriber di Background..."
echo "-----------------------------------------------------"
APP_ID="Notifikasi-Service" ./app_subscriber &
SUB1_PID=$!

APP_ID="Audit-Service" ./app_subscriber &
SUB2_PID=$!

sleep 2
echo "-----------------------------------------------------"
echo "✅ 2 Service berbeda sedang mendengarkan Exchange yang sama."
echo ""

echo "[4/4] Menjalankan Publisher untuk menyebar pengumuman..."
./app_publisher
echo ""
echo "Perhatikan! SATU pesan yang dikirim Publisher di atas, HAMPIR BERSAMAAN DITERIMA oleh Notifikasi-Service dan Audit-Service!"
echo ""

# Beri waktu subscriber mencetak log
sleep 3

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $SUB1_PID $SUB2_PID
rm -f app_publisher app_subscriber
docker-compose down
echo "🎉 Selesai!"
