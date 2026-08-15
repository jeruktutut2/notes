"""
==============================================================================
CONTOH MODUL 9: GUARDRAILS & AI SAFETY (KEAMANAN AI)
==============================================================================
Aplikasi AI di lingkungan produksi rentan terhadap ancaman keamanan seperti:
    1. Prompt Injection / Jailbreak (Manipulasi pengguna untuk melanggar aturan).
    2. Data Leakage / PII Leakage (Bocornnya NIK, Email, KTP, Password).
    3. Toxic Content / Kata Kasar (Ujaran kebencian & SARA).
    4. Off-Topic Query (AI menjawab pertanyaan di luar scope aplikasi).

GUARDRAILS ADALAH LAPISAN KEAMANAN GANDA:
    [User Input] -> (INPUT GUARDRAILS) -> [LLM] -> (OUTPUT GUARDRAILS) -> [User Output]

CARA PAKAI:
    - Jalankan: python main.py
==============================================================================
"""

import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")


# ------------------------------------------------------------------------------
# 1. INPUT GUARDRAILS (PEMERIKSAAN SEBELUM DIKIRIM KE AI)
# ------------------------------------------------------------------------------

POLA_JAILBREAK = [
    r"abaikan (semua )?instruksi",
    r"sekarang kamu adalah hacker",
    r"pretend you are",
    r"ignore previous instructions",
    r"mode DAN",
    r"bypass safety"
]

KATA_KASAR_PROFANITY = ["anjing", "bangsat", "bodoh", "goblok", "bajingan"]


def periksa_input_guardrails(user_prompt: str) -> tuple[bool, str]:
    """
    Memvalidasi input dari user.
    Returns: (is_pass: bool, reason_or_cleaned_prompt: str)
    """
    # A. Cek Prompt Injection / Jailbreak
    for pola in POLA_JAILBREAK:
        if re.search(pola, user_prompt, re.IGNORECASE):
            return False, "🚨 TERDETEKSI PROMPT INJECTION: Upaya jailbreak atau manipulasi sistem ditolak!"

    # B. Cek Kata Kasar / Profanity
    for kata in KATA_KASAR_PROFANITY:
        if kata in user_prompt.lower():
            return False, "🚨 TERDETEKSI KONTEN TOKSIK: Input mengandung kata kasar yang dilarang."

    # C. Cek Batasan Panjang Input
    if len(user_prompt) > 2000:
        return False, "🚨 INPUT TERLALU PANJANG: Maksimal 2000 karakter per permintaan."

    return True, user_prompt


# ------------------------------------------------------------------------------
# 2. OUTPUT GUARDRAILS (PEMERIKSAAN & SANITASI SEBELUM DIKIRIM KE USER)
# ------------------------------------------------------------------------------

def samarkan_pii_output(teks_output: str) -> str:
    """
    Mendeteksi dan menyamarkan Data Pribadi Sensitif (PII - Personally Identifiable Information).
    - Email -> [EMAIL TERPROTEKSI]
    - Nomor HP -> [NOMOR TELEPON TERPROTEKSI]
    - NIK KTP (16 Angka) -> [NIK TERPROTEKSI]
    """
    # Pattern Email
    teks_sanitasi = re.sub(r'[\w\.-]+@[\w\.-]+\.\w+', '[EMAIL TERPROTEKSI]', teks_output)
    
    # Pattern Nomor Telepon (08xxx)
    teks_sanitasi = re.sub(r'(\+62|08)[0-9]{8,11}', '[NOMOR TELEPON TERPROTEKSI]', teks_sanitasi)

    # Pattern NIK KTP (16 Digit Angka)
    teks_sanitasi = re.sub(r'\b[0-9]{16}\b', '[NIK KTP TERPROTEKSI]', teks_sanitasi)

    return teks_sanitasi


def periksa_output_guardrails(raw_output: str) -> str:
    """
    Memfilter dan menyamarkan respon AI sebelum dikirim ke pengguna.
    """
    # 1. Redaksi Data Sensitif (PII Anonymization)
    output_aman = samarkan_pii_output(raw_output)
    return output_aman


# ------------------------------------------------------------------------------
# 3. PIPELINE AI AMAN DENGAN GUARDRAILS LENGKAP
# ------------------------------------------------------------------------------

def panggil_ai_dengan_guardrails(user_prompt: str):
    print(f"\n=========================================================")
    print(f"PROSES INPUT: '{user_prompt}'")
    print("=========================================================")

    # STEP 1: JALANKAN INPUT GUARDRAILS
    pass_input, pesan_input = periksa_input_guardrails(user_prompt)
    if not pass_input:
        print(f"🛑 [INPUT GUARDRAIL BLOCK]: {pesan_input}")
        return

    print("✅ [INPUT GUARDRAIL PASS]: Prompt aman, melanjutkan ke LLM...")

    # STEP 2: PROSES DI LLM
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Kamu adalah asisten customer service yang aman dan sopan."},
            {"role": "user", "content": pesan_input}
        ],
        "stream": False,
        "options": {"temperature": 0.2}
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=30)
        res.raise_for_status()
        raw_ai_res = res.json()["message"]["content"]
        
        print(f"\n🤖 Raw Output AI dari Model:\n{raw_ai_res}")

        # STEP 3: JALANKAN OUTPUT GUARDRAILS
        output_final = periksa_output_guardrails(raw_ai_res)
        
        print(f"\n🛡️ [FINAL SECURE OUTPUT (GUARDED)]:\n{output_final}")

    except Exception as e:
        print(f"❌ Error Server: {e}")


# ------------------------------------------------------------------------------
# MAIN EXECUTION DEMO
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("=========================================================")
    print("CHATBOT INTERAKTIF: GUARDRAILS & AI SAFETY (MODUL 9)")
    print("=========================================================")
    
    while True:
        print("\nPilih Mode Guardrails:")
        print("1. Chat Normal dengan Input Guardrails (Cegah kata kasar/jailbreak)")
        print("2. Simulasi Output Guardrails (Redaksi Data PII Otomatis)")
        pilihan = input("Pilihan (1/2) atau 'keluar': ").strip()

        if pilihan.lower() in ['keluar', 'exit', 'q']:
            print("Sampai jumpa!")
            break
            
        if pilihan not in ['1', '2']:
            print("Pilihan tidak valid.")
            continue
            
        if pilihan == '1':
            prompt = input("\nMasukkan Prompt Anda (Coba ketik 'abaikan instruksi' atau kata kasar): ").strip()
            if not prompt:
                continue
            panggil_ai_dengan_guardrails(prompt)
            
        elif pilihan == '2':
            print("\n--- Simulasi Redaksi PII pada Respon ---")
            print("Ketik kalimat yang mengandung Email, No HP (08xxx), atau NIK (16 digit)")
            simulasi_respon = input("Masukkan teks simulasi: ").strip()
            if not simulasi_respon:
                continue
            
            print("\nRespon Mentah  :", simulasi_respon)
            print("Respon Guarded :", samarkan_pii_output(simulasi_respon))
            
        print("\n" + "-"*50)
