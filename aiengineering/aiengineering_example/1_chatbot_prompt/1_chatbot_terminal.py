"""
==============================================================================
CONTOH 1.1: CHATBOT TERMINAL
==============================================================================
Chatbot sederhana yang berjalan di terminal.
Kamu ketik pesan, AI menjawab. Seperti ChatGPT versi terminal.

CARA PAKAI:
    1. Pastikan Ollama sudah jalan:  ollama serve
    2. Pastikan model sudah ada:     ollama pull gemma3:4b
    3. Jalankan:                      python 1_chatbot_terminal.py

YANG DIPELAJARI:
    - Cara memanggil LLM (Ollama) dari Python via HTTP API
    - Apa itu "system prompt" dan "user prompt"
    - Cara menyimpan history percakapan agar AI ingat konteks
    - Cara streaming response (jawaban muncul kata per kata)
==============================================================================
"""

# ==============================================================================
# IMPORT LIBRARY
# ==============================================================================
# Di Python, "import" artinya kita meminjam kode yang sudah dibuat orang lain
# agar tidak perlu menulis semuanya dari nol.
#
# Analoginya: import = meminjam alat dari kotak perkakas

import os
import requests  # Library untuk mengirim HTTP request (seperti browser, tapi dari kode)
                 # Kita pakai ini untuk "berbicara" dengan Ollama API
                 # Install: pip install requests

import json      # Library bawaan Python untuk memproses data JSON
                 # JSON = format data yang dipakai untuk komunikasi antar program
                 # Contoh JSON: {"nama": "Budi", "umur": 25}


# ==============================================================================
# KONFIGURASI
# ==============================================================================

# URL Ollama API — Default localhost:11434, atau dari ENV (misal: http://ollama:11434/api/chat di Docker)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

# Model AI yang dipakai — Default gemma3:4b, atau dari ENV
MODEL = os.getenv("MODEL", "gemma3:4b")

# SYSTEM PROMPT — instruksi untuk AI tentang "siapa dia" dan "bagaimana berperilaku"
#
# APA ITU SYSTEM PROMPT?
#   System prompt adalah "aturan main" yang kita berikan ke AI SEBELUM
#   percakapan dimulai. AI akan mengikuti aturan ini di SETIAP jawaban.
#
#   Bayangkan kamu merekrut karyawan baru:
#     System prompt = buku panduan kerja yang kamu kasih di hari pertama
#     User prompt   = pertanyaan/tugas dari pelanggan
#
#   CONTOH system prompt lain yang bisa kamu coba:
#     - "Kamu adalah chef profesional. Jawab hanya tentang masakan."
#     - "Kamu adalah guru matematika. Jelaskan langkah per langkah."
#     - "Kamu adalah dokter. Berikan saran kesehatan umum."
#
# TIPS: Coba ganti system prompt di bawah ini dan lihat bagaimana
#       perilaku AI berubah!
SYSTEM_PROMPT = """Kamu adalah asisten AI yang ramah dan membantu.
Jawab dalam bahasa Indonesia.
Jawab dengan singkat dan jelas, maksimal 3 paragraf."""


# ==============================================================================
# FUNGSI: Kirim pesan ke AI dan terima jawaban
# ==============================================================================

def kirim_ke_ai(history_pesan: list) -> str:
    """
    Mengirim percakapan ke Ollama dan menerima jawaban AI.

    Parameter:
        history_pesan: Daftar semua pesan dalam percakapan.
                       Formatnya: [{"role": "system/user/assistant", "content": "..."}]

    Return:
        String berisi jawaban dari AI.

    PENJELASAN ALUR:
        1. Kita kirim seluruh history percakapan ke Ollama
        2. Ollama memproses dengan model AI (gemma3:4b)
        3. Ollama mengirim jawaban kembali
        4. Kita ambil teks jawabannya
    """

    # --- Siapkan data yang akan dikirim ke Ollama ---
    # Format ini mengikuti standar Ollama API
    data = {
        "model": MODEL,          # Model AI yang dipakai
        "messages": history_pesan, # Seluruh history percakapan
        "stream": False           # False = tunggu jawaban lengkap sekaligus
                                  # True  = jawaban dikirim kata per kata (streaming)
    }

    # --- Kirim request ke Ollama ---
    try:
        # requests.post() mengirim data ke URL Ollama
        # Ini seperti kita "mengetuk pintu" Ollama dan memberikan pertanyaan
        response = requests.post(OLLAMA_URL, json=data)

        # Cek apakah request berhasil (status code 200 = OK)
        response.raise_for_status()

        # --- Ambil jawaban dari response ---
        # Response dari Ollama berformat JSON, contoh:
        # {
        #   "message": {
        #     "role": "assistant",
        #     "content": "Halo! Saya asisten AI..."
        #   }
        # }
        hasil = response.json()
        jawaban = hasil["message"]["content"]
        return jawaban

    except requests.exceptions.ConnectionError:
        # Error ini muncul kalau Ollama belum dijalankan
        return (
            "❌ Tidak bisa terhubung ke Ollama.\n"
            "   Pastikan Ollama sudah jalan dengan perintah: ollama serve"
        )
    except Exception as e:
        # Error lain yang tidak terduga
        return f"❌ Terjadi error: {e}"


# ==============================================================================
# FUNGSI: Kirim pesan ke AI dengan STREAMING (jawaban muncul kata per kata)
# ==============================================================================

def kirim_ke_ai_streaming(history_pesan: list) -> str:
    """
    Sama seperti kirim_ke_ai(), tapi jawaban ditampilkan KATA PER KATA
    saat AI sedang "berpikir" — seperti efek mengetik di ChatGPT.

    APA ITU STREAMING?
        Tanpa streaming (stream=False):
          AI berpikir 5 detik... lalu SELURUH jawaban muncul sekaligus.
          User menunggu tanpa tahu apa-apa selama 5 detik.

        Dengan streaming (stream=True):
          AI mulai berpikir... kata pertama muncul dalam 0.5 detik...
          kata-kata berikutnya muncul satu per satu sambil AI berpikir.
          User langsung bisa mulai membaca.

        Analogi:
          Tanpa streaming = pesan WhatsApp (muncul sekaligus setelah selesai)
          Dengan streaming = chat voice note (bisa dengar sambil orang bicara)
    """

    data = {
        "model": MODEL,
        "messages": history_pesan,
        "stream": True  # ← Perbedaannya di sini: True = streaming
    }

    try:
        # stream=True di requests berarti kita terima data sedikit demi sedikit
        response = requests.post(OLLAMA_URL, json=data, stream=True)
        response.raise_for_status()

        jawaban_lengkap = ""

        # Baca response baris per baris saat data masuk
        for baris in response.iter_lines():
            if baris:
                # Setiap baris adalah JSON yang berisi potongan jawaban
                potongan = json.loads(baris)

                # Ambil teks dari potongan ini
                teks = potongan["message"]["content"]

                # Cetak ke terminal TANPA newline (end="") agar menyambung
                # flush=True agar langsung tampil, tidak menunggu buffer penuh
                print(teks, end="", flush=True)

                # Gabungkan ke jawaban lengkap untuk disimpan di history
                jawaban_lengkap += teks

        # Cetak newline di akhir agar prompt berikutnya di baris baru
        print()

        return jawaban_lengkap

    except requests.exceptions.ConnectionError:
        pesan_error = (
            "❌ Tidak bisa terhubung ke Ollama.\n"
            "   Pastikan Ollama sudah jalan dengan perintah: ollama serve"
        )
        print(pesan_error)
        return pesan_error
    except Exception as e:
        pesan_error = f"❌ Terjadi error: {e}"
        print(pesan_error)
        return pesan_error


# ==============================================================================
# FUNGSI UTAMA: Loop percakapan
# ==============================================================================

def main():
    """
    Fungsi utama yang menjalankan chatbot.

    ALUR:
        1. Tampilkan pesan pembuka
        2. Siapkan history percakapan (dimulai dengan system prompt)
        3. Loop: user ketik → AI jawab → simpan ke history → ulangi
        4. User ketik "keluar" → program berhenti
    """

    # --- Tampilkan pesan pembuka ---
    print("=" * 60)
    print("🤖 CHATBOT TERMINAL — Contoh 1.1")
    print("=" * 60)
    print(f"Model    : {MODEL}")
    print(f"Perintah : Ketik pesan lalu Enter")
    print(f"Keluar   : Ketik 'keluar' atau 'exit'")
    print("=" * 60)
    print()

    # --- Siapkan history percakapan ---
    #
    # KENAPA PERLU HISTORY?
    #   AI itu TIDAK punya memori sendiri. Setiap kali kita kirim pesan,
    #   AI sebenarnya sudah "lupa" percakapan sebelumnya.
    #
    #   Solusinya: kita kirim SELURUH history percakapan setiap kali.
    #   Jadi AI bisa "membaca ulang" semua pesan sebelumnya.
    #
    #   Contoh: setelah 3 pesan, history-nya jadi seperti ini:
    #   [
    #     {"role": "system",    "content": "Kamu asisten ramah..."},  ← aturan
    #     {"role": "user",      "content": "Halo!"},                 ← pesan 1
    #     {"role": "assistant", "content": "Halo! Ada yang bisa..."},← jawaban 1
    #     {"role": "user",      "content": "Siapa namamu?"},         ← pesan 2
    #     {"role": "assistant", "content": "Saya asisten AI..."},    ← jawaban 2
    #     {"role": "user",      "content": "Apa yang tadi kukatakan?"}← pesan 3
    #   ]
    #   AI bisa baca semua di atas, jadi dia "ingat" kamu bilang "Halo!"
    #
    # TIGA JENIS ROLE:
    #   "system"    = Instruksi untuk AI (dari developer, bukan user)
    #   "user"      = Pesan dari pengguna
    #   "assistant" = Jawaban dari AI
    history = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

    # --- Loop percakapan ---
    while True:
        # Minta input dari user
        # input() menunggu user mengetik sesuatu lalu tekan Enter
        pesan_user = input("Kamu: ").strip()

        # Cek apakah user mau keluar
        if pesan_user.lower() in ["keluar", "exit", "quit", "q"]:
            print("\n👋 Sampai jumpa!")
            break

        # Cek apakah input kosong
        if not pesan_user:
            print("💡 Ketik sesuatu untuk mulai chat.\n")
            continue

        # --- Tambahkan pesan user ke history ---
        # Kita simpan pesan user agar AI tahu apa yang ditanyakan
        history.append({"role": "user", "content": pesan_user})

        # --- Kirim ke AI dan tampilkan jawaban ---
        print()  # Baris kosong sebelum jawaban
        print("AI: ", end="", flush=True)

        # Panggil fungsi streaming agar jawaban muncul kata per kata
        jawaban_ai = kirim_ke_ai_streaming(history)

        # --- Simpan jawaban AI ke history ---
        # Ini penting! Tanpa ini, AI tidak akan "ingat" jawaban sebelumnya
        # di percakapan berikutnya
        history.append({"role": "assistant", "content": jawaban_ai})

        print()  # Baris kosong setelah jawaban


# ==============================================================================
# JALANKAN PROGRAM
# ==============================================================================

# Bagian ini memastikan fungsi main() hanya berjalan kalau file ini
# dijalankan langsung (python 1_chatbot_terminal.py),
# bukan kalau di-import dari file lain
if __name__ == "__main__":
    main()
