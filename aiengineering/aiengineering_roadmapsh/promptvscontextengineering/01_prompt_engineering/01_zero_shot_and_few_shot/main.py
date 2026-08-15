#!/usr/bin/env python3
"""
Modul: Zero-Shot & Few-Shot Prompting
Simulasi perbandingan langsung Zero-Shot vs Few-Shot Learning dalam tugas ekstraksi entitas & sentiment analysis.
"""

import json

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: ZERO-SHOT VS FEW-SHOT PROMPTING", "1;34"))
    print("=" * 70)

    input_text = "Saldo E-Wallet saya terpotong Rp 250.000 tapi transaksi merchant Kopi Janji Jiwa gagal!"

    # 1. Zero-Shot Prompting
    zero_shot_prompt = f"Ekstrak nominal, merchant, dan status dari teks ini: '{input_text}'"
    
    # 2. Few-Shot Prompting
    few_shot_prompt = f"""Ekstrak informasi transaksi sesuai contoh berikut:

Teks: "Transfer ke BCA Rp 500.000 ke rekening 12345 sukses"
Hasil: {{"nominal": "Rp 500.000", "merchant": "BCA", "status": "sukses"}}

Teks: "Topup OVO Rp 100.000 via Indomaret pending"
Hasil: {{"nominal": "Rp 100.000", "merchant": "Indomaret", "status": "pending"}}

Teks: "{input_text}"
Hasil:"""

    print(color("\n1. ZERO-SHOT PROMPT:", "1;33"))
    print(zero_shot_prompt)
    print(color("\n[Simulasi Hasil Zero-Shot Output]:", "31"))
    print("Nominalnya 250ribu, merchant Janji Jiwa, status gagal.")

    print(color("\n2. FEW-SHOT PROMPT (In-Context Examples):", "1;33"))
    print(few_shot_prompt)
    print(color("\n[Simulasi Hasil Few-Shot Output (Strict JSON)]:", "1;32"))
    res_json = {"nominal": "Rp 250.000", "merchant": "Kopi Janji Jiwa", "status": "gagal"}
    print(json.dumps(res_json, indent=2))

    print("\n" + "=" * 70)
    print("✓ Few-Shot menjamin konsistensi struktur JSON untuk sistem otomatis downstream.")
    print("✓ Zero-Shot lebih hemat token tetapi format keluarannya tidak terprediksi.")

if __name__ == "__main__":
    main()
