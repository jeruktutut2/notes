#!/usr/bin/env bash

# ==============================================================================
# SKENARIO PENJALANAN CHATBOT TERMINAL BERBASIS DOCKER COMPOSE
# ==============================================================================

set -e

# Berpindah ke direktori tempat script ini berada
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

MODEL_NAME="gemma3:4b"

echo "============================================================"
echo "🚀 SKENARIO PENJALANAN CHATBOT TERMINAL (DOCKER)"
echo "============================================================"

# 1. Cek ketersediaan Docker & Docker Compose
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker tidak ditemukan. Harap instal Docker terlebih dahulu."
    exit 1
fi

# 2. Jalankan Ollama Service di Background
echo "📦 1. Menjalankan service Ollama via Docker Compose..."
docker compose up -d ollama

# 3. Tunggu hingga Ollama Server Siap
echo "⏳ 2. Menunggu service Ollama siap di http://localhost:11434..."
until curl -s http://localhost:11434/ > /dev/null; do
    sleep 2
    echo -n "."
done
echo ""
echo "✅ Service Ollama telah aktif!"

# 4. Pull Model AI di Ollama
echo "📥 3. Memastikan model AI '$MODEL_NAME' sudah ter-download..."
docker compose exec ollama ollama pull "$MODEL_NAME"

# 5. Jalankan Chatbot Terminal dalam Mode Interaktif
echo "------------------------------------------------------------"
echo "🤖 4. Memulai Chatbot Terminal interaktif..."
echo "    (Ketik 'keluar' atau 'exit' untuk mengakhiri chat)"
echo "------------------------------------------------------------"
# docker compose run --rm chatbot
docker compose run --build --rm chatbot

# 6. Hentikan service Ollama dan bersihkan kontainer
echo "🧹 5. Menghentikan service Docker Compose..."
docker compose down -v

echo "============================================================"
echo "👋 Chatbot selesai. Sampai jumpa!"
echo "============================================================"

