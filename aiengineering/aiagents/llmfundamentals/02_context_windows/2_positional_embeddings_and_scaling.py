#!/usr/bin/env python3
"""
Modul 2.2: Positional Embeddings & Context Length Scaling (RoPE, ALiBi, YaRN)
Simulasi cara LLM memahami urutan token dan teknik ekstrapolasi context window dari 4K ke 128K+.
"""

import math
from typing import List, Tuple

def simulate_rope_embedding(dim: int = 4, seq_len: int = 4):
    """
    Simulasi matematika Rotary Position Embedding (RoPE).
    RoPE memutar vektor token pada bidang 2D berdasarkan posisi token (m) dan frekuensi theta.
    """
    print("\n" + "="*70)
    print(" 1. SIMULASI ROTARY POSITION EMBEDDING (RoPE)")
    print("="*70)
    print("RoPE (LLaMA, Qwen, Mistral) mengodekan posisi relatif dengan memutar matriks 2D:")
    print("  R_{\\Theta, m}^d = \\text{diag}\\left(R_{\\theta_1, m}, R_{\\theta_2, m}, \\dots, R_{\\theta_{d/2}, m}\\right)\n")
    
    base_theta = 10000.0
    
    for pos in range(seq_len):
        print(f"Token Posisi {pos}:")
        for i in range(0, dim, 2):
            theta = 1.0 / (base_theta ** (i / dim))
            m_theta = pos * theta
            cos_val = math.cos(m_theta)
            sin_val = math.sin(m_theta)
            print(f"  • Dimensi ({i},{i+1}) -> Angle: {m_theta:.4f} rad | Cos: {cos_val:+.4f}, Sin: {sin_val:+.4f}")
    print()


def compare_positional_encodings():
    print("="*70)
    print(" 2. PERBANDINGAN TEKNIK POSITIONAL EMBEDDING")
    print("="*70)
    
    encodings = [
        ("Absolute Positional (Sinusoidal / Learned)", "GPT-2 / Original Transformer", "Memetakan posisi 0..N secara konstan.", "Sangat buruk dalam ekstrapolasi ke luar panjang konteks training."),
        ("RoPE (Rotary Position Embedding)", "LLaMA, Qwen, Mistral, PaLM", "Memutar vektor query/key dengan matriks rotasi.", "Sangat kuat untuk perhatian relatif, mendukung RoPE Scaling (YaRN)."),
        ("ALiBi (Attention with Linear Biases)", "BLOOM, MPT", "Menambahkan penalti linier negatif pada skor attention berbasis jarak.", "Mampu melakukan ekstrapolasi context tanpa fine-tuning posisi sama sekali.")
    ]
    
    for name, models, mechanism, scaling_ability in encodings:
        print(f" • \033[93m{name}\033[0m")
        print(f"   Model Digunakan : {models}")
        print(f"   Mekanisme       : {mechanism}")
        print(f"   Ekstrapolasi    : \033[96m{scaling_ability}\033[0m")
        print("-" * 65)
    print()


def demonstrate_rope_scaling_yarn():
    print("="*70)
    print(" 3. TEKNIK CONTEXT EXPANSION: LINEAR INTERPOLATION VS YARN")
    print("="*70)
    
    original_ctx = 4096
    target_ctx = 32768
    scale_factor = target_ctx / original_ctx
    
    print(f"Panjang Konteks Asli Training  : {original_ctx:,} tokens")
    print(f"Target Perluasan Konteks      : {target_ctx:,} tokens (Scale Factor: {scale_factor}x)\n")
    
    print("1. Linear RoPE Scaling (PI):")
    print(f"   Memperkecil frekuensi rotasi sebesar 1/{scale_factor:.1f}.")
    print("   Dampak: Perhatian frekuensi tinggi menjadi buram, menyebabkan penurunan kinerja penalaran.\n")
    
    print("2. YaRN (Yet another RoPE NTI Extension):")
    print("   Membagi frekuensi menjadi 3 band (High frequency, Medium, Low frequency):")
    print("   • Frekuensi Tinggi : Tanpa interpolasi (menjaga kemampuan bahasa lokal).")
    print("   • Frekuensi Sedang : Interpolasi halus (smooth blend).")
    print("   • Frekuensi Rendah : Linear scaling (menjangkau jarak jauh).")
    print("   Dampak: Memungkinkan konteks 128K+ tokens dengan loss perplexity yang minimal!\n")


def main():
    print("\n" + "█"*70)
    print("  MODUL 2.2: POSITIONAL EMBEDDINGS & SCALING MECHANICS")
    print("█"*70)
    
    simulate_rope_embedding()
    compare_positional_encodings()
    demonstrate_rope_scaling_yarn()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. RoPE adalah standar industri saat ini untuk arsitektur LLM modern.")
    print(" 2. RoPE Scaling (seperti YaRN) memungkinkan model 4K diperluas ke 128K tanpa retraining dari awal.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
