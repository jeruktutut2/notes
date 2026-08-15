#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed ID Generation"
echo "====================================================="

echo "[1/3] Build aplikasi Go..."
go build -o id_gen main.go

echo ""
echo "[2/3] Menjalankan Node 1 (Simulasi Server API 1)..."
NODE_ID=1 ./id_gen

echo ""
echo "[3/3] Menjalankan Node 2 (Simulasi Server API 2)..."
NODE_ID=2 ./id_gen

echo ""
echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
rm -f id_gen
echo "🎉 Selesai!"
