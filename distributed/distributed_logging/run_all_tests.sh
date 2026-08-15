#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Logging (Loki Stack)"
echo "====================================================="

echo "[1/3] Menyalakan Grafana, Loki, dan Promtail (Docker)..."
docker-compose up -d --wait
echo "✅ Stack Observability siap!"
echo "   - Grafana : http://localhost:3000"
echo ""

echo "[2/3] Build & Menjalankan Go API Server..."
go build -o app_server cmd/server/main.go

# Menjalankan 2 simulasi node
SERVICE_ID="Auth-Node-1" ./app_server &
PID1=$!

sleep 2

echo "[3/3] Mengirim HTTP Request ke server untuk memicu Log..."
echo "-----------------------------------------------------"
curl -s http://localhost:8080/login
echo ""
curl -s http://localhost:8080/login
echo "-----------------------------------------------------"
echo "✅ Log (termasuk Error Log) telah ditulis dalam format JSON ke file logs/app.log"
echo "   Promtail di belakang layar otomatis menyedot file tersebut dan mengirimkannya ke Loki."
echo ""
echo "👉 Untuk melihat log terpusat:"
echo "1. Buka http://localhost:3000 di Browser Anda."
echo "2. Masuk ke menu 'Explore' (Ikon Kompas di sebelah kiri)."
echo "3. Pilih Data Source: 'Loki' (Jika belum ada, tambahkan Loki URL: http://loki:3100 di Configuration)."
echo "4. Masukkan query: {job=\"go_microservice\"}"
echo ""

echo "Tekan CTRL+C untuk mematikan server dan Docker."
wait $PID1 || true

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $PID1 2>/dev/null || true
rm -f app_server
docker-compose down
echo "🎉 Selesai!"
