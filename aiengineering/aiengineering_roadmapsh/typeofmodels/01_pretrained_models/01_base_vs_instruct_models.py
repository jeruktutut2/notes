#!/usr/bin/env python3
"""
Modul 01: Base Models vs Instruct / Chat Models
Menjelaskan perbedaan mendasar antara model pre-trained murni (Base Completion)
dan model yang diselaraskan dengan instruksi manusia (Instruct/Chat Alignment).
"""

import time

def print_header(title: str):
    print("\n" + "=" * 70)
    print(f"  {title.upper()}")
    print("=" * 70)

def simulate_base_model_completion(prompt: str) -> str:
    """
    Simulasi perilaku Base Model:
    Hanya memprediksi kelanjutan teks secara statistik dari web crawl data,
    tanpa memahami bahwa user sedang memberikan instruksi/pertanyaan.
    """
    prompt_clean = prompt.strip()
    
    if "apa ibukota indonesia" in prompt_clean.lower():
        # Base model sering melanjutkan pola dokumen alih-alih menjawab
        return prompt + " Jakarta.\nApa ibukota Malaysia? Kuala Lumpur.\nApa ibukota Jepang? Tokyo."
    elif "buat fungsi python" in prompt_clean.lower():
        return prompt + " untuk penjumlahan dua angka.\n\ndef tambah(a, b):\n    return a + b\n\n# Contoh penggunaan:\n# print(tambah(5, 3))"
    else:
        return prompt + " dan hal ini menjadi topik utama dalam diskusi teknologi terbaru tahun 2026."

def simulate_instruct_model_response(messages: list) -> str:
    """
    Simulasi perilaku Instruct / Chat Fine-Tuned Model:
    Memahami peran System/User/Assistant dan menjawab instruksi dengan tepat.
    """
    user_msg = ""
    system_msg = "Anda adalah asisten AI yang responsif dan sopan."
    
    for msg in messages:
        if msg["role"] == "system":
            system_msg = msg["content"]
        elif msg["role"] == "user":
            user_msg = msg["content"]

    if "ibukota indonesia" in user_msg.lower():
        return f"[{system_msg}]\nJawab: Ibukota Negara Indonesia saat ini adalah Ibu Kota Nusantara (IKN) di Kalimantan Timur, melanjutkan peran Jakarta sebagai pusat perekonomian."
    elif "fungsi python" in user_msg.lower():
        return f"[{system_msg}]\nBerikut adalah fungsi Python sederhana:\n\n```python\ndef tambah(a: int, b: int) -> int:\n    return a + b\n```"
    else:
        return f"[{system_msg}]\nSaya memahami pertanyaan Anda mengenai '{user_msg}'. Berikut informasi yang dapat saya berikan..."

def format_chatml_template(messages: list) -> str:
    """
    Menampilkan bagaimana pesan percakapan diubah menjadi ChatML Prompt Template
    yang dimengerti oleh LLM Chat model (seperti Llama-3, Qwen, Mistral).
    """
    formatted = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        formatted += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    formatted += "<|im_start|>assistant\n"
    return formatted

def main():
    print_header("Demo 1: Perbedaan Output Base Model vs Instruct Model")
    
    input_text = "Apa ibukota Indonesia?"
    
    print(f"\n[INPUT PROMPT POLOS]: '{input_text}'\n")
    
    print("--- 1. SIMULASI BASE MODEL (Completion Mode) ---")
    base_output = simulate_base_model_completion(input_text)
    print(f"Output Base Model:\n{base_output}\n")
    
    print("--- 2. SIMULASI INSTRUCT MODEL (Chat Mode) ---")
    messages = [
        {"role": "system", "content": "Anda adalah asisten cerdas AI Engineering."},
        {"role": "user", "content": input_text}
    ]
    instruct_output = simulate_instruct_model_response(messages)
    print(f"Output Instruct Model:\n{instruct_output}\n")

    print_header("Demo 2: Format ChatML Prompt Template")
    chatml = format_chatml_template(messages)
    print("Sebelum dimasukkan ke LLM, percakapan dikonversi menjadi format template khusus:")
    print("-" * 50)
    print(chatml)
    print("-" * 50)

    print("\n💡 KESIMPULAN:")
    print("• Base Models berguna untuk domain-specific pre-training & completion.")
    print("• Instruct Models telah diselaraskan dengan SFT & RLHF untuk mengikuti perintah pengguna.")

if __name__ == "__main__":
    main()
