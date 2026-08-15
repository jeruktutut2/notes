#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Consensus (etcd)"
echo "====================================================="

echo "[1/4] Menyalakan etcd (Docker)..."
docker-compose up -d --wait
echo "✅ etcd siap di port 2379!"
echo ""

echo "[2/4] Build Node App..."
go build -o app_node cmd/node/main.go

echo "[3/4] Menjalankan 3 Node sekaligus..."
echo "-----------------------------------------------------"
echo "Tiga node akan berlomba menjadi Leader. Hanya 1 yang akan menang."
echo "Begitu pemenang selesai bekerja dan mengundurkan diri (resign),"
echo "node berikutnya yang antre otomatis akan langsung diangkat jadi Leader baru."
echo "-----------------------------------------------------"

NODE_ID="NODE-A" ./app_node &
PIDA=$!
sleep 0.5 # Beri selisih dikit biar kelihatan ngantrenya

NODE_ID="NODE-B" ./app_node &
PIDB=$!
sleep 0.5

NODE_ID="NODE-C" ./app_node &
PIDC=$!

# Tunggu sampai semua node selesai bekerja dan resign otomatis
wait $PIDA $PIDB $PIDC || true

echo ""
echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
rm -f app_node
docker-compose down
echo "🎉 Selesai!"
