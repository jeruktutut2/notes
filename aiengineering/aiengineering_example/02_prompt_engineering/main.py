"""
==============================================================================
CONTOH MODUL 2: PROMPT ENGINEERING (TEKNIK-TEKNIK PROMPT)
==============================================================================
Script ini mendemonstrasikan berbagai teknik Prompt Engineering tingkat lanjut
yang diubah menjadi interaktif.

CARA PAKAI:
    - Jalankan: python main.py
==============================================================================
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")


def panggil_llm(messages: list, temperature: float = 0.7) -> str:
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature
        }
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        return f"❌ Error API: {e}"


def demo_zero_shot(input_teks: str):
    print("\n--- ZERO-SHOT PROMPTING ---")
    prompt_user = f"Klasifikasikan sentimen dari teks berikut menjadi POSITIF, NEGATIF, atau NETRAL:\n'{input_teks}'"
    messages = [{"role": "user", "content": prompt_user}]
    print(f"Prompt Input:\n{prompt_user}\n")
    hasil = panggil_llm(messages, temperature=0.0)
    print(f"Hasil Zero-Shot:\n{hasil}")


def demo_few_shot(input_teks: str):
    print("\n--- FEW-SHOT PROMPTING ---")
    prompt_user = f"""Terjemahkan istilah teknis berikut ke dalam analogi bahasa sehari-hari.

Contoh 1:
Istilah: API (Application Programming Interface)
Analogi: Pelayan restoran yang mencatat pesananmu lalu membawakannya dari dapur.

Contoh 2:
Istilah: Database
Analogi: Lemari arsip berlabel tempat kamu menyimpan dokumen kantor secara teratur.

Contoh 3:
Istilah: CPU (Central Processing Unit)
Analogi: Otak manusia yang menghitung dan mengambil keputusan utama.

Sekarang giliranmu:
Istilah: {input_teks}
Analogi:"""
    messages = [{"role": "user", "content": prompt_user}]
    hasil = panggil_llm(messages, temperature=0.2)
    print(f"Hasil Few-Shot:\n{hasil}")


def demo_chain_of_thought(input_teks: str):
    print("\n--- CHAIN-OF-THOUGHT (CoT) PROMPTING ---")
    prompt_user = f"""{input_teks}

Jelaskan penalaranmu langkah demi langkah (Step-by-step) sebelum memberikan jawaban akhir!"""
    messages = [{"role": "user", "content": prompt_user}]
    hasil = panggil_llm(messages, temperature=0.0)
    print(f"Hasil Chain-of-Thought:\n{hasil}")


def demo_role_prompting(input_teks: str):
    print("\n--- ROLE / PERSONA PROMPTING ---")
    system_prompt = """Kamu adalah seorang Senior Cybersecurity Auditor.
Gaya bicaramu sangat formal, mengedepankan keamanan data, dan selalu memberikan analisis risiko serta rekomendasi mitigasi teknis."""
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": input_teks}
    ]
    hasil = panggil_llm(messages, temperature=0.3)
    print(f"System Role: Senior Cybersecurity Auditor")
    print(f"Hasil Role Prompting:\n{hasil}")


def demo_temperature_comparison(input_teks: str):
    print("\n--- EKSPERIMEN PARAMETER TEMPERATURE ---")
    messages = [{"role": "user", "content": input_teks}]

    print("\n>>> Temperature = 0.0 (Presisi, Konsisten, Deterministik):")
    hasil_rendah = panggil_llm(messages, temperature=0.0)
    print(hasil_rendah)

    print("\n>>> Temperature = 1.0 (Kreatif, Bervariasi, Eksploratif):")
    hasil_tinggi = panggil_llm(messages, temperature=1.0)
    print(hasil_tinggi)


if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: PROMPT ENGINEERING (MODUL 2)")
    print("=========================================================")
    print("Ketik 'keluar' atau 'exit' untuk berhenti.\n")

    while True:
        print("Pilih Teknik Prompting:")
        print("1. Zero-Shot (Klasifikasi Sentimen)")
        print("2. Few-Shot (Analogi Istilah Teknis)")
        print("3. Chain-of-Thought (Penalaran Matematika/Logika)")
        print("4. Role Prompting (Cybersecurity Auditor)")
        print("5. Temperature Test (Misal: Tulis slogan pemasaran)")
        pilihan = input("Pilihan (1/2/3/4/5): ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break

        if pilihan not in ['1', '2', '3', '4', '5']:
            print("Pilihan tidak valid.")
            continue

        input_teks = input("\nMasukkan teks/pertanyaanmu: ").strip()
        if input_teks.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
        
        if not input_teks:
            continue

        if pilihan == '1':
            demo_zero_shot(input_teks)
        elif pilihan == '2':
            demo_few_shot(input_teks)
        elif pilihan == '3':
            demo_chain_of_thought(input_teks)
        elif pilihan == '4':
            demo_role_prompting(input_teks)
        elif pilihan == '5':
            demo_temperature_comparison(input_teks)
        
        print("\n" + "-"*50 + "\n")
