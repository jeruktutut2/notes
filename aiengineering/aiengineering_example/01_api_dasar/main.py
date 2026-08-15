"""
==============================================================================
CONTOH MODUL 1: MEMANGGIL LLM VIA API (DASAR)
==============================================================================
Script ini memperlihatkan cara paling dasar dan murni (tanpa framework)
untuk berkomunikasi dengan Model AI (LLM) melalui REST API.

SKENARIO DUNIA NYATA:
    Membangun layanan backend dasar yang menerima pertanyaan pengguna,
    mengirimkannya ke Ollama (lokal) atau Google Gemini API (cloud),
    dan menampilkan jawabannya secara utuh maupun streaming (kata per kata).

CARA PAKAI:
    1. Pastikan Ollama sudah berjalan: ollama serve
    2. Pastikan model tersedia:        ollama pull gemma3:4b
    3. Jalankan script:               python main.py

YANG DIPELAJARI:
    - Manajemen API Key dan variabel lingkungan via .env
    - Struktur payload HTTP Request (system prompt, user prompt, temperature)
    - Perbedaan mode response: Normal (JSON utuh) vs Streaming (Server-Sent Events)
    - Fallback error handling apabila server AI offline
==============================================================================
"""

import os
import json
import requests
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
# 1. LOAD VARIABEL LINGKUNGAN (.env)
# ------------------------------------------------------------------------------
# load_dotenv() mencari file .env di direktori proyek dan memuat isinya
# ke dalam environment variable sistem agar tidak perlu menaruh API key di kode.
load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")


# ------------------------------------------------------------------------------
# 2. FUNGSI MEMANGGIL OLLAMA (LOKAL - NON STREAMING)
# ------------------------------------------------------------------------------
def panggil_ollama_biasa(system_prompt: str, user_prompt: str) -> str:
    """
    Mengirimkan pesan ke Ollama API secara synchronously (menunggu jawaban utuh).

    Parameters:
        system_prompt (str): Instruksi peran dan aturan perilaku untuk AI.
        user_prompt (str): Pertanyaan atau perintah langsung dari pengguna.

    Returns:
        str: Jawaban teks dari AI.
    """
    print(f"\n--- [OLLAMA NON-STREAMING] Mengirim request ke model: {DEFAULT_MODEL} ---")
    
    # Payload standar Ollama Chat API
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False,  # False = respon dikembalikan sekaligus setelah selesai
        "options": {
            "temperature": 0.7  # Mengontrol kreativitas (0.0 = kaku/pasti, 1.0 = sangat kreatif)
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        response.raise_for_status()  # Lempar error jika status HTTP != 200 OK
        
        data = response.json()
        jawaban = data["message"]["content"]
        return jawaban

    except requests.exceptions.ConnectionError:
        return "❌ Error: Tidak dapat terhubung ke Ollama. Pastikan perintah 'ollama serve' sudah berjalan."
    except Exception as e:
        return f"❌ Terjadi kesalahan: {str(e)}"


# ------------------------------------------------------------------------------
# 3. FUNGSI MEMANGGIL OLLAMA (LOKAL - STREAMING)
# ------------------------------------------------------------------------------
def panggil_ollama_streaming(system_prompt: str, user_prompt: str):
    """
    Mengirimkan pesan ke Ollama API dengan mode STREAMING.
    Jawaban akan langsung ditampilkan ke terminal huruf demi huruf saat AI mengetik.
    """
    print(f"\n--- [OLLAMA STREAMING] Menunggu AI mengetik... ---")
    
    payload = {
        "model": DEFAULT_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": True  # True = Ollama mengirim potongan teks baris demi baris JSON
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=30)
        response.raise_for_status()

        # Membaca stream respon baris per baris
        for baris in response.iter_lines():
            if baris:
                # Mengubah baris JSON menjadi dictionary Python
                chunk = json.loads(baris)
                teks_potongan = chunk.get("message", {}).get("content", "")
                
                # Print langsung tanpa baris baru, flush=True agar segera tampil di terminal
                print(teks_potongan, end="", flush=True)
                
        print("\n---------------------------------------------------------")

    except Exception as e:
        print(f"\n❌ Error Streaming: {str(e)}")


# ------------------------------------------------------------------------------
# 4. FUNGSI ALTERNATIF MEMANGGIL GOOGLE GEMINI API (CLOUD)
# ------------------------------------------------------------------------------
def panggil_gemini_api(user_prompt: str) -> str:
    """
    Contoh alternatif memanggil Google Gemini 2.0 Flash API via REST HTTP.
    """
    if not GOOGLE_API_KEY or GOOGLE_API_KEY.startswith("AIzaSy_Ganti"):
        return "⚠️ Skipped: GOOGLE_API_KEY belum dikonfigurasi di file .env."

    print("\n--- [GOOGLE GEMINI API] Mengirim request ke Cloud ---")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"
    
    payload = {
        "contents": [
            {
                "parts": [{"text": user_prompt}]
            }
        ]
    }

    try:
        res = requests.post(url, json=payload, timeout=30)
        res.raise_for_status()
        data = res.json()
        jawaban = data["candidates"][0]["content"]["parts"][0]["text"]
        return jawaban
    except Exception as e:
        return f"❌ Terjadi kesalahan Gemini API: {str(e)}"


# ------------------------------------------------------------------------------
# 5. EXECUTION ENTRY POINT (DEMO ALUR)
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: API DASAR (MODUL 1)")
    print("=========================================================")

    # System prompt mengatur persona dan aturan main AI
    SYSTEM = "Kamu adalah Pakar AI Engineering yang menjelaskan konsep teknis secara singkat, ramah, dan mudah dipahami."
    print(f"Instruksi Peran (System): {SYSTEM}")
    print("Ketik 'keluar' atau 'exit' untuk berhenti.\n")

    while True:
        print("Pilih mode respons:")
        print("1. Non-Streaming (Tunggu sampai selesai)")
        print("2. Streaming (Ketik per kata)")
        print("3. Google Gemini (Cloud)")
        pilihan = input("Pilihan (1/2/3): ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break

        if pilihan not in ['1', '2', '3']:
            print("Pilihan tidak valid.")
            continue

        prompt_user = input("\nKamu: ").strip()
        if prompt_user.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
        
        if not prompt_user:
            continue

        if pilihan == '1':
            hasil = panggil_ollama_biasa(SYSTEM, prompt_user)
            print("\nAI:", hasil)
        elif pilihan == '2':
            print("\nAI: ", end="")
            panggil_ollama_streaming(SYSTEM, prompt_user)
        elif pilihan == '3':
            hasil = panggil_gemini_api(prompt_user)
            print("\nAI (Gemini):", hasil)
        
        print("\n" + "-"*50 + "\n")
