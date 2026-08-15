"""
Modul 01: Persiapan Dataset & Formatting
Skrip 1: Format Dataset Instruction Tuning (Alpaca vs ShareGPT)
"""

import json

def alpaca_to_sharegpt(alpaca_item):
    """
    Mengonversi 1 item sampel berformat Alpaca menjadi format ShareGPT / ChatML.
    """
    instruction = alpaca_item.get("instruction", "")
    user_input = alpaca_item.get("input", "")
    output = alpaca_item.get("output", "")
    
    # Gabungkan instruction dan input jika input ada
    full_prompt = f"{instruction}\n\nInput Tambahan: {user_input}" if user_input else instruction

    return {
        "conversations": [
            {"from": "human", "value": full_prompt},
            {"from": "gpt", "value": output}
        ]
    }

def demo_format_conversions():
    print("=" * 60)
    print("MODUL 01 - SKRIP 1: Format Dataset Fine-Tuning")
    print("=" * 60)
    
    # Sample Dataset Alpaca Format
    alpaca_samples = [
        {
            "instruction": "Tuliskan kode Python sederhana untuk menghitung faktorial angka.",
            "input": "n = 5",
            "output": "def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)\n\nprint(factorial(5))"
        },
        {
            "instruction": "Apa perbedaan antara Supervised Fine-Tuning dan Preference Tuning?",
            "input": "",
            "output": "Supervised Fine-Tuning (SFT) melatih model dengan target teks eksplisit. Preference Tuning (seperti DPO) menyelaraskan respon berdasarkan pasangan pilihan (chosen vs rejected)."
        }
    ]
    
    print("\n--- 1. Contoh Data Format Alpaca (Single-turn) ---")
    print(json.dumps(alpaca_samples[0], indent=2, ensure_ascii=False))
    
    print("\n--- 2. Mengonversi Format Alpaca ke ShareGPT / ChatML (Multi-turn) ---")
    sharegpt_converted = [alpaca_to_sharegpt(item) for item in alpaca_samples]
    print(json.dumps(sharegpt_converted[0], indent=2, ensure_ascii=False))
    
    print("\n--- 3. Struktur ChatML Standard dengan System Prompt ---")
    chatml_example = {
        "messages": [
            {"role": "system", "content": "Anda adalah pakar AI Engineering yang ramah dan adaptif."},
            {"role": "user", "content": "Apa itu LoRA?"},
            {"role": "assistant", "content": "LoRA (Low-Rank Adaptation) adalah metode melatih matriks rank kecil untuk menghemat VRAM."}
        ]
    }
    print(json.dumps(chatml_example, indent=2, ensure_ascii=False))
    
    print("\n[KESIMPULAN] Memahami format dataset penting karena setiap framework (TRL, Unsloth, LLaMA-Factory) membutuhkan skema input yang tepat.")

if __name__ == "__main__":
    demo_format_conversions()
