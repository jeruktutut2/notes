#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Database (Sharding)"
echo "====================================================="

echo "[1/3] Build Node & Client..."
go build -o db_node cmd/node/main.go
go build -o db_client cmd/client/main.go

echo "[2/3] Menyalakan 3 Node Database di Background..."
NODE_ID="Node-A" PORT=8081 ./db_node &
PIDA=$!

NODE_ID="Node-B" PORT=8082 ./db_node &
PIDB=$!

NODE_ID="Node-C" PORT=8083 ./db_node &
PIDC=$!

# Tunggu server siap
sleep 2
echo "✅ Tiga node berjalan (Port 8081, 8082, 8083)"
echo ""

echo "[3/3] Menjalankan Client untuk Menyebar Data (Sharding)..."
echo "-----------------------------------------------------"
./db_client
echo "-----------------------------------------------------"
echo "Perhatikan log di atas!"
echo "Data (User 101-105) tidak disimpan di 1 server, melainkan DISEBAR/DIPECAH ke Node A, B, dan C berdasarkan algoritma Consistent Hashing."
echo ""

echo "Mari kita buktikan dengan melihat isi masing-masing database:"
echo "Isi Node-A:"
curl -s http://localhost:8081/dump
echo -e "\n\nIsi Node-B:"
curl -s http://localhost:8082/dump
echo -e "\n\nIsi Node-C:"
curl -s http://localhost:8083/dump
echo -e "\n"

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
kill $PIDA $PIDB $PIDC 2>/dev/null || true
rm -f db_node db_client
echo "🎉 Selesai!"
