#!/usr/bin/env bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODEL_NAME="gemma3:4b"

echo "============================================================"
echo "🚀 SKENARIO PENJALANAN 04_RAG (TRANSFORMER VERSION)"
echo "============================================================"

if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker tidak ditemukan."
    exit 1
fi

# Kita membangun ulang image untuk memastikan dependensi sentence-transformers
# dan file main_transformer.py sudah masuk ke dalam container.
echo "🏗️ 1. Membangun (Build) Docker Image Chatbot..."
docker compose build chatbot

echo "📦 2. Menjalankan service Ollama (hanya untuk Chat Model gemma3:4b)..."
docker compose up -d ollama

echo "⏳ 3. Menunggu service Ollama siap di http://localhost:11434..."
until curl -s http://localhost:11434/ > /dev/null; do
    sleep 2
    echo -n "."
done
echo ""
echo "✅ Service Ollama telah aktif!"

echo "📥 4. Memastikan model AI '$MODEL_NAME' sudah ter-download..."
docker compose exec ollama ollama pull "$MODEL_NAME"

echo "------------------------------------------------------------"
echo "🤖 5. Memulai Aplikasi RAG Sentence-Transformers..."
echo "------------------------------------------------------------"
# Kita menimpa CMD bawaan Dockerfile dengan 'python main_transformer.py'
docker compose run --build --rm chatbot python main_transformer.py

echo "🧹 6. Menghentikan service Docker Compose..."
docker compose down -v

echo "============================================================"
echo "👋 Selesai!"
echo "============================================================"
