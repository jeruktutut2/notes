#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed File System (MinIO)"
echo "====================================================="

echo "[1/3] Menyalakan MinIO Server (Docker)..."
docker-compose up -d --wait
echo "✅ MinIO siap!"
echo "   - API Port     : 9000"
echo "   - Console Web  : http://localhost:9001 (User: admin | Pass: password)"
echo ""

echo "[2/3] Build & Run Go Application..."
go build -o app cmd/app/main.go
echo "-----------------------------------------------------"
./app
echo "-----------------------------------------------------"
echo "✅ Aplikasi berhasil berkomunikasi dengan MinIO via S3 SDK."
echo ""
echo "👉 Silakan buka http://localhost:9001 di Browser Anda (Login: admin / password)"
echo "   Masuk ke menu 'Object Browser', buka bucket 'storage-terdistribusi',"
echo "   dan Anda akan menemukan file Anda tersimpan rapi layaknya di AWS S3!"
echo ""
echo "Tekan ENTER untuk mematikan server..."
read

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
rm -f app
docker-compose down -v
echo "🎉 Selesai!"
