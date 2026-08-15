"""
==============================================================================
CONTOH MODUL 6A: AGENTIC AI (REACT PATTERN DARI NOL)
==============================================================================
Agentic AI adalah sistem di mana LLM bekerja secara otonom dalam siklus loop:
    Observe -> Think (Penalaran) -> Act (Bertindak/Panggil Tool) -> Observe -> Repeat

Pada contoh ini, kita membuat Agent ReAct (Reasoning + Acting) MURNI dari nol
tanpa memakai framework apapun, agar kita paham betul mekanisme internalnya.

ALUR WORKFLOW AGENT:
    1. Agent membaca tugas dari User
    2. Agent menuliskan 'Thought' (apa yang sedang dipikirkan)
    3. Agent menuliskan 'Action' (tool apa yang ingin dipanggil)
    4. Sistem mengeksekusi tool dan mengembalikan 'Observation'
    5. Agent mengulangi loop sampai menemukan 'Final Answer'

CARA PAKAI:
    - Jalankan: python agent_manual.py
==============================================================================
"""

import os
import re
import json
import requests
from dotenv import load_dotenv

load_dotenv()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.getenv("DEFAULT_MODEL", "gemma3:4b")


# ------------------------------------------------------------------------------
# 1. TOOLS YANG TERSEDIA UNTUK AGENT
# ------------------------------------------------------------------------------

def cari_wiki_produk(kata_kunci: str) -> str:
    """Tool simulasi pencarian pengetahuan internal perusahaan."""
    data = {
        "diskon": "Promo bulan ini: Gunakan kupon MERDEKA10 untuk diskon 10%.",
        "pengiriman": "Pengiriman gratis ke Jabodetabek untuk pembelian minimal Rp 200.000.",
        "garansi": "Garansi resmi berlaku 1 tahun untuk kerusakan pabrik."
    }
    for k, v in data.items():
        if k in kata_kunci.lower():
            return f"[HASIL SEARCH]: {v}"
    return "[HASIL SEARCH]: Informasi tidak ditemukan di wiki."


def kalkulator(ekspresi: str) -> str:
    """Tool evaluasi matematika aman sederhana."""
    try:
        # Bersihkan string dari karakter berbahaya
        sanitized = re.sub(r'[^0-9\+\-\*\/\(\)\.]', '', ekspresi)
        hasil = eval(sanitized)
        return f"[HASIL KALKULATOR]: {hasil}"
    except Exception as e:
        return f"[HASIL KALKULATOR ERROR]: {e}"


TOOLS = {
    "cari_wiki_produk": cari_wiki_produk,
    "kalkulator": kalkulator
}


# ------------------------------------------------------------------------------
# 2. SYSTEM PROMPT UNTUK ATURAN FORMAT REACT
# ------------------------------------------------------------------------------

SYSTEM_PROMPT_REACT = """Kamu adalah AI Agent cerdas yang menyelesaikan tugas secara otonom.
Kamu harus mengikuti pola berpikir ReAct berikut di SETIAP respon:

Thought: [Jelaskan penalaranmu tentang apa yang perlu dilakukan]
Action: [Nama tool yang dipanggil (hanya pilih antara: cari_wiki_produk atau kalkulator)]
Action Input: [Argumen masukan untuk tool]

Ketika kamu mendapatkan hasil dari Observation, lanjutkan berpikir.
Jika kamu sudah memiliki jawaban akhir yang lengkap, akhiri dengan format:

Final Answer: [Jawaban akhir lengkap untuk pengguna dalam Bahasa Indonesia]

Tools yang tersedia:
- cari_wiki_produk(kata_kunci): Mencari informasi tentang diskon, pengiriman, garansi.
- kalkulator(ekspresi): Menghitung ekspresi matematika murni.
"""


# ------------------------------------------------------------------------------
# 3. RE-ACT LOOP ENGINE
# ------------------------------------------------------------------------------

def jalankan_agent_manual(tugas_user: str, max_iterasi: int = 5):
    print(f"\n=========================================================")
    print(f"START REACT AGENT (MANUAL LOOP)")
    print(f"TUGAS: '{tugas_user}'")
    print("=========================================================")

    history = [
        {"role": "system", "content": SYSTEM_PROMPT_REACT},
        {"role": "user", "content": tugas_user}
    ]

    for iterasi in range(1, max_iterasi + 1):
        print(f"\n--- [ITERASI AGENT #{iterasi}] ---")

        payload = {
            "model": MODEL,
            "messages": history,
            "stream": False,
            "options": {"temperature": 0.1}
        }

        try:
            res = requests.post(OLLAMA_URL, json=payload, timeout=30)
            res.raise_for_status()
            response_teks = res.json()["message"]["content"]
            
            print(f"🤖 Agent Output:\n{response_teks}")
            history.append({"role": "assistant", "content": response_teks})

            # Cek apakah agent sudah menemukan Jawaban Akhir (Final Answer)
            if "Final Answer:" in response_teks:
                jawaban_akhir = response_teks.split("Final Answer:")[1].strip()
                print("\n🎯 AGENT BERHASIL MENYELESAIKAN TUGAS!")
                print(f"Jawaban Akhir: {jawaban_akhir}")
                return jawaban_akhir

            # Parse Action dan Action Input dari teks menggunakan Regex
            match_action = re.search(r"Action:\s*(\w+)", response_teks)
            match_input = re.search(r"Action Input:\s*(.+)", response_teks)

            if match_action and match_input:
                nama_tool = match_action.group(1).strip()
                input_tool = match_input.group(1).strip()

                fungsi_tool = TOOLS.get(nama_tool)
                if fungsi_tool:
                    hasil_obs = fungsi_tool(input_tool)
                    print(f"👁️ Observation System: {hasil_obs}")
                    
                    # Berikan hasil observasi kembali ke Agent
                    history.append({
                        "role": "user", 
                        "content": f"Observation: {hasil_obs}"
                    })
                else:
                    history.append({
                        "role": "user",
                        "content": f"Observation: Tool '{nama_tool}' tidak ditemukan."
                    })
            else:
                # Jika agent lupa format, ingatkan kembali
                history.append({
                    "role": "user",
                    "content": "Harap gunakan format 'Thought:', 'Action:', 'Action Input:' atau 'Final Answer:'!"
                })

        except Exception as e:
            print(f"❌ Error Loop Agent: {e}")
            break

    print("⚠️ Agent mencapai batas iterasi maksimum tanpa hasil akhir.")


if __name__ == "__main__":
    # Skenario 1: Butuh riset wiki + perhitungan kalkulator
    jalankan_agent_manual("Berapa total harga jika saya membeli 2 barang seharga Rp 150.000 setelah mendapat potongan diskon dari promo bulan ini?")
