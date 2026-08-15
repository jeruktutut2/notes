#!/bin/bash

set -e

echo "====================================================="
echo "  🚀 Mulai Pengujian Distributed Search (Elasticsearch)"
echo "====================================================="

echo "[1/3] Menyalakan Elasticsearch (Docker)..."
# Elasticsearch butuh memori lumayan besar dan waktu start yang lama
docker-compose up -d
echo "Menunggu Elasticsearch siap (sekitar 20-30 detik)..."

# Polling untuk mengecek apakah ES sudah siap menerima request
until curl -s http://localhost:9200 | grep -q "You Know, for Search"; do
  sleep 2
  echo -n "."
done
echo -e "\n✅ Elasticsearch siap!"
echo ""

echo "[2/3] Build & Run Go Application..."
go build -o app cmd/app/main.go
echo "-----------------------------------------------------"
./app
echo "-----------------------------------------------------"
echo "✅ Pencarian Full-Text Search (seperti mesin pencari Google) berhasil!"
echo "Elasticsearch tidak mencari string persis (exact match), melainkan memahami"
echo "kata per kata (tokenization) sehingga 'go backend' bisa cocok dengan dokumen"
echo "yang mengandung kata 'Go' dan 'backend' meski posisinya terpisah jauh."
echo ""

echo "Tekan ENTER untuk mematikan server..."
read

echo "====================================================="
echo "  🧹 Bersih-bersih (Teardown)"
echo "====================================================="
rm -f app
docker-compose down -v
echo "🎉 Selesai!"
