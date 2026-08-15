"""
=================================================================
3. OLLAMA - LOCAL INFERENCE
=================================================================
Ollama memungkinkan menjalankan LLM secara lokal di komputer
sendiri, TANPA perlu:
- API key
- Internet (setelah download model)
- GPU cloud yang mahal

Keunggulan Ollama:
✅ Privasi total — data tidak pernah meninggalkan komputer
✅ Gratis — tidak ada biaya per token
✅ Offline — bisa dipakai tanpa internet
✅ Mudah — 1 command untuk install dan jalankan model
✅ API compatible — mirip format OpenAI API

Model yang didukung:
- Llama 3.1 (8B, 70B)
- Mistral 7B
- Gemma 2 (2B, 9B, 27B)
- Phi-3 (3.8B)
- Qwen 2.5 (0.5B - 72B)
- Dan banyak lagi...

Requirement:
- RAM minimal 8GB (untuk model 7B)
- RAM 16GB+ direkomendasikan
- macOS, Linux, atau Windows
=================================================================
"""

import requests
import json

# =====================================================
# CATATAN: Untuk menjalankan skrip ini, Ollama harus
# sudah terinstall dan berjalan di komputer Anda.
#
# Instalasi Ollama:
#   macOS : brew install ollama
#   Linux : curl -fsSL https://ollama.com/install.sh | sh
#   Windows: Download dari https://ollama.com/download
#
# Setelah install, jalankan:
#   ollama serve          (start server)
#   ollama pull llama3.2  (download model 3B, ~2GB)
#
# Atau model yang lebih kecil:
#   ollama pull phi3      (3.8B, ~2.3GB)
#   ollama pull gemma2:2b (2B, ~1.6GB)
# =====================================================

OLLAMA_BASE_URL = "http://localhost:11434"


def cek_ollama_status():
    """Mengecek apakah Ollama server sedang berjalan."""
    print("=" * 60)
    print("CEK STATUS OLLAMA SERVER")
    print("=" * 60)
    
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            print(f"\n✅ Ollama server AKTIF di {OLLAMA_BASE_URL}")
            print(f"📦 Model yang tersedia ({len(models)}):")
            for m in models:
                size_gb = m.get('size', 0) / (1024**3)
                print(f"   - {m['name']} ({size_gb:.1f} GB)")
            return True
        else:
            print(f"\n❌ Ollama merespons dengan status: {response.status_code}")
            return False
    except requests.ConnectionError:
        print(f"\n❌ Tidak bisa terhubung ke Ollama di {OLLAMA_BASE_URL}")
        print("   Pastikan Ollama sudah diinstall dan jalankan: ollama serve")
        return False


def demo_chat_sederhana():
    """Chat sederhana dengan LLM lokal via Ollama."""
    print("\n" + "=" * 60)
    print("DEMO 1: Chat Sederhana dengan Ollama")
    print("=" * 60)

    model = "llama3.2"  # Ganti dengan model yang sudah di-pull
    pesan = "Jelaskan apa itu machine learning dalam 3 kalimat sederhana."

    print(f"\n🤖 Model : {model}")
    print(f"📝 Prompt: {pesan}")
    print(f"\n💬 Respons:")

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": pesan}
                ],
                "stream": False  # Non-streaming untuk kesederhanaan
            },
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            jawaban = data["message"]["content"]
            
            # Info performa
            total_duration = data.get("total_duration", 0) / 1e9  # nanosecond -> second
            eval_count = data.get("eval_count", 0)
            
            print(f"   {jawaban}")
            print(f"\n⚡ Performa:")
            print(f"   Total waktu    : {total_duration:.2f} detik")
            print(f"   Tokens dihasilkan: {eval_count}")
            if total_duration > 0:
                print(f"   Kecepatan      : {eval_count/total_duration:.1f} tokens/detik")
        else:
            print(f"   ❌ Error: {response.status_code} - {response.text}")
            print(f"   💡 Coba jalankan: ollama pull {model}")
    except requests.ConnectionError:
        print("   ❌ Ollama server tidak aktif. Jalankan: ollama serve")


def demo_chat_streaming():
    """Chat dengan streaming output (token per token)."""
    print("\n" + "=" * 60)
    print("DEMO 2: Streaming Chat (Real-time Output)")
    print("=" * 60)

    model = "llama3.2"
    pesan = "Sebutkan 5 manfaat belajar AI engineering."

    print(f"\n🤖 Model : {model}")
    print(f"📝 Prompt: {pesan}")
    print(f"\n💬 Respons (streaming):")

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/chat",
            json={
                "model": model,
                "messages": [
                    {"role": "user", "content": pesan}
                ],
                "stream": True  # Streaming mode
            },
            stream=True,
            timeout=120
        )

        if response.status_code == 200:
            full_response = ""
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data["message"]["content"]
                    print(token, end="", flush=True)  # Print token by token
                    full_response += token

                    if data.get("done", False):
                        total_duration = data.get("total_duration", 0) / 1e9
                        eval_count = data.get("eval_count", 0)
                        print(f"\n\n⚡ Total waktu: {total_duration:.2f}s | "
                              f"Tokens: {eval_count}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except requests.ConnectionError:
        print("   ❌ Ollama server tidak aktif.")


def demo_generate_api():
    """Menggunakan Generate API (bukan Chat API) untuk completion sederhana."""
    print("\n" + "=" * 60)
    print("DEMO 3: Generate API (Text Completion)")
    print("=" * 60)

    model = "llama3.2"
    prompt = "The three most important skills for an AI engineer are:"

    print(f"\n🤖 Model : {model}")
    print(f"📝 Prompt: {prompt}")

    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,   # Kreativitas (0=deterministik, 1=kreatif)
                    "top_p": 0.9,         # Nucleus sampling
                    "num_predict": 200,   # Max tokens
                }
            },
            timeout=120
        )

        if response.status_code == 200:
            data = response.json()
            print(f"\n💬 Output: {data['response']}")
        else:
            print(f"   ❌ Error: {response.status_code}")
    except requests.ConnectionError:
        print("   ❌ Ollama server tidak aktif.")


def demo_ollama_openai_compatible():
    """Ollama juga menyediakan API yang kompatibel dengan format OpenAI."""
    print("\n" + "=" * 60)
    print("DEMO 4: OpenAI-Compatible API (Drop-in Replacement)")
    print("=" * 60)

    print("""
    💡 Ollama menyediakan endpoint yang kompatibel dengan OpenAI API!
    Ini berarti kode yang menggunakan OpenAI SDK bisa langsung dipakai 
    dengan Ollama — cukup ganti base_url.

    Contoh dengan openai Python library:
    """)

    print("""
    from openai import OpenAI

    # Ganti base_url ke Ollama
    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"  # Tidak perlu key asli
    )

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "Kamu asisten AI yang membantu."},
            {"role": "user", "content": "Apa itu inference dalam AI?"}
        ]
    )

    print(response.choices[0].message.content)
    """)

    print("    ✅ Keuntungan: Bisa switch antara OpenAI dan Ollama")
    print("       tanpa mengubah kode — cukup ganti base_url!")


def main():
    ollama_aktif = cek_ollama_status()

    if ollama_aktif:
        demo_chat_sederhana()
        demo_chat_streaming()
        demo_generate_api()

    demo_ollama_openai_compatible()

    print("\n" + "=" * 60)
    print("✅ Selesai! Lanjut ke: 03_prompt_engineering/")
    print("=" * 60)

if __name__ == "__main__":
    main()
