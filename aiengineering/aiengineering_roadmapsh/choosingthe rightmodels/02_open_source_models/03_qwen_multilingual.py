#!/usr/bin/env python3
"""
03_qwen_multilingual.py
Modul spesialisasi keluarga Alibaba Qwen 2.5:
- Qwen 2.5 (General Multilingual & Bahasa Indonesia)
- Qwen 2.5-Coder (Top-tier Open Source Code Completion)
- Qwen 2.5-Math (Matematika & STEM Benchmark Winner)
"""

def main():
    print("=" * 65)
    print(" 🌐 ALIBABA QWEN 2.5 MULTILINGUAL & SPECIALIZED MODELS")
    print("=" * 65)
    
    qwen_series = [
        {"variant": "Qwen 2.5 (0.5B - 72B)", "strength": "Pemahaman Multilingual (Bahasa Indonesia, Asia & Eropa) sangat natural."},
        {"variant": "Qwen 2.5-Coder (0.5B - 32B)", "strength": "Menyaingi Claude 3.5 Sonnet dalam HumanEval & LiveCodeBench open weights."},
        {"variant": "Qwen 2.5-Math (1.5B - 72B)", "strength": "Spesialis pemecahan rumus kalkulus, aljabar, dan GSM8K."},
        {"variant": "Qwen 2-VL (2B - 72B)", "strength": "Vision-Language model untuk ekstraksi teks dari gambar/dokumen bergambar."}
    ]
    
    print("\n📋 Qwen Specialized Ecosystem:")
    for q in qwen_series:
        print(f"• {q['variant']:<26} | Kekuatan: {q['strength']}")
        
    print("\n🔍 Mengapa Qwen 2.5 populer untuk aplikasi Bahasa Indonesia?")
    print(" 1. Tokenizer Qwen mencakup kosakata UTF-8 luas yang efisien dalam mengompres teks non-Inggris.")
    print(" 2. Lisensi Apache 2.0 (untuk versi di bawah 32B) sangat ramah bagi komersialisasi startup & enterprise.")

if __name__ == "__main__":
    main()
