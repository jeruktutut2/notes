#!/usr/bin/env python3
"""
03_normalization_and_dimensions.py
----------------------------------
Simulasi Normalisasi L2 dan Matryoshka Embeddings (Pemotongan Dimensi Vektor).
"""

import numpy as np

def l2_normalize(vector: np.ndarray) -> np.ndarray:
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def matryoshka_truncate(vector: np.ndarray, target_dim: int) -> np.ndarray:
    """
    Memotong dimensi vektor embedding (misal 1536 -> 256) 
    dan melakukan re-normalization.
    """
    truncated = vector[:target_dim]
    return l2_normalize(truncated)

def main():
    print("=" * 70)
    print("📏 NORMALIZATION & MATRYOSHKA EMBEDDING DIMENSION TRUNCATION")
    print("=" * 70)

    # Buat Vektor Sederhana 1536-Dimensi (Seukuran OpenAI text-embedding-3-small)
    np.random.seed(42)
    vec_a_full = np.random.randn(1536)
    vec_b_full = vec_a_full + np.random.normal(0, 0.3, size=1536) # Mirip
    vec_c_full = np.random.randn(1536)                           # Berbeda

    # Normalize Full Vectors
    vec_a_full = l2_normalize(vec_a_full)
    vec_b_full = l2_normalize(vec_b_full)
    vec_c_full = l2_normalize(vec_c_full)

    dims_to_test = [1536, 512, 256, 64, 16]

    print("\n📊 Pengaruh Pemotongan Dimensi terhadap Presisi Cosine Similarity:")
    print(f"{'Dimensi':<10} | {'Sim(A, B) [Mirip]':<20} | {'Sim(A, C) [Beda]':<20} | {'Memory Ratio':<12}")
    print("-" * 70)

    for dim in dims_to_test:
        a_sub = matryoshka_truncate(vec_a_full, dim)
        b_sub = matryoshka_truncate(vec_b_full, dim)
        c_sub = matryoshka_truncate(vec_c_full, dim)

        sim_ab = float(np.dot(a_sub, b_sub))
        sim_ac = float(np.dot(a_sub, c_sub))
        mem_ratio = f"{dim / 1536 * 100:.1f}%"

        print(f"{dim:<10} | {sim_ab:<20.4f} | {sim_ac:<20.4f} | {mem_ratio:<12}")

    print("-" * 70)
    print("💡 KESIMPULAN:")
    print("   Bahkan saat dipotong dari 1536 ke 256 dimensi (hemat 83.3% RAM),")
    print("   kemampuan membedakan data mirip vs berbeda tetap sangat tinggi!")
    print("=" * 70)

if __name__ == "__main__":
    main()
