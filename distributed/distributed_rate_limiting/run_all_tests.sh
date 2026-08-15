#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Rate Limiter"
echo "====================================================="

echo "[1/4] Menyalakan Redis (Docker)..."
docker-compose up -d --wait
echo "✅ Redis siap di port 6380!"
echo ""

echo "[2/4] Build & Menjalankan Server Go di background..."
go build -o app_server main.go
./app_server &
SERVER_PID=$!

sleep 2

echo "[3/4] Mengirim 10 request bersamaan (Kapasitas Bucket: 5)..."
echo "-----------------------------------------------------"
echo "Diharapkan ~5 request pertama berhasil (HTTP 200),"
echo "dan sisanya ditolak karena melebihi batas (HTTP 429)."
echo "-----------------------------------------------------"

for i in {1..10}
do
   curl -s -o /dev/null -w "Req $i HTTP %{http_code}\n" http://localhost:8080/api/data &
done

wait

echo ""
echo "[4/4] 💤 Menunggu 3 detik agar token terisi (refill) kembali..."
sleep 3
echo "Kirim 1 request (Seharusnya berhasil karena sudah refill):"
curl -s -o /dev/null -w "Req 11 HTTP %{http_code}\n" http://localhost:8080/api/data
echo ""
echo ""

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $SERVER_PID
rm -f app_server
docker-compose down
echo "🎉 Selesai!"
