#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODEL_NAME="gemma3:4b"

echo "============================================================"
echo "🚀 SKENARIO PENJALANAN 10_MCP (DOCKER)"
echo "============================================================"

if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker tidak ditemukan."
    exit 1
fi

echo "📦 1. Menjalankan service Ollama via Docker Compose..."
docker compose up -d ollama

echo "⏳ 2. Menunggu service Ollama siap di http://localhost:11434..."
until curl -s http://localhost:11434/ > /dev/null; do
    sleep 2
    echo -n "."
done
echo ""
echo "✅ Service Ollama telah aktif!"

echo "📥 3. Memastikan model AI '$MODEL_NAME' sudah ter-download..."
docker compose exec ollama ollama pull "$MODEL_NAME"

echo "------------------------------------------------------------"
echo "🤖 4. Memulai Aplikasi Interaktif..."
echo "------------------------------------------------------------"
docker compose run --build --rm chatbot

echo "🧹 5. Menghentikan service Docker Compose..."
docker compose down -v

echo "============================================================"
echo "👋 Selesai!"
echo "============================================================"
