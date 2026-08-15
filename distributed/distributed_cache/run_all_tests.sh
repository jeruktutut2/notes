#!/bin/bash

# Pastikan script berhenti jika ada error
set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Cache & Singleflight"
echo "====================================================="

# 1. Jalankan Redis via Docker Compose
echo "[1/4] Menyalakan Redis (Docker)..."
docker-compose up -d --wait
echo "✅ Redis siap!"
echo ""

# 2. Build dan Jalankan Server Go
echo "[2/4] Build & Menjalankan Server Go di background..."
go build -o app_server main.go
./app_server &
SERVER_PID=$!

# Tunggu server siap
sleep 2

# 3. Uji Coba Konkurensi (Thundering Herd Simulation)
echo "[3/4] Mengirim 10 request bersamaan (Simulasi Cache Stampede)..."
echo "-----------------------------------------------------"
echo "Perhatikan log server! Meskipun ada 10 request bersamaan,"
echo "tulisan '[DB FETCH]' hanya boleh muncul 1 KALI SAJA untuk setiap key."
echo "Sisanya akan dilayani oleh '[SINGLEFLIGHT]'."
echo "-----------------------------------------------------"

for i in {1..10}
do
   # Kirim request ke background secara bersamaan
   curl -s -o /dev/null -w "Req $i HTTP %{http_code}\n" http://localhost:8080/product/99 &
done

# Tunggu semua background request (curl) selesai
wait

echo ""
echo "[4/4] 💤 Menunggu 3 detik lalu kirim 1 request lagi (Seharusnya kena Cache Hit)..."
sleep 3
curl -s http://localhost:8080/product/99
echo ""
echo ""

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
# Mematikan server Go
kill $SERVER_PID
rm -f app_server
echo "✅ Server Go dimatikan."

# Mematikan Redis
docker-compose down
echo "✅ Redis dimatikan."

echo "🎉 Selesai!"
