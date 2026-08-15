#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Tracing (OpenTelemetry)"
echo "====================================================="

echo "[1/4] Menyalakan Jaeger (Docker)..."
docker-compose up -d --wait
echo "✅ Jaeger siap di port 16686 (UI) dan 4318 (Receiver)!"
echo ""

echo "[2/4] Build Service A & Service B..."
go build -o app_service_a cmd/service_a/main.go
go build -o app_service_b cmd/service_b/main.go

echo "[3/4] Menjalankan Service di Background..."
./app_service_a &
PIDA=$!

./app_service_b &
PIDB=$!

# Tunggu server siap
sleep 2

echo ""
echo "[4/4] Mengirim Request HTTP berantai..."
echo "-----------------------------------------------------"
echo "Client -> [Service A] -> [Service B]"
curl -s http://localhost:8081/pesan
echo ""
echo "-----------------------------------------------------"
echo "✅ Request berhasil! Jejak perjalanannya (Trace) sudah direkam ke Jaeger."
echo "Untuk melihat hasilnya dalam bentuk grafik waktu (Gantt Chart):"
echo "👉 Buka Browser Anda ke: http://localhost:16686"
echo ""

# Beri waktu beberapa detik untuk melihat log sebelum teardown, tapi di script ini
# kita tidak langsung teardown agar user bisa buka browser.
echo "Tekan CTRL+C untuk mematikan server dan Jaeger."

wait $PIDA $PIDB || true

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $PIDA $PIDB 2>/dev/null || true
rm -f app_service_a app_service_b
docker-compose down
echo "🎉 Selesai!"
