#!/usr/bin/env python3
"""
02_distance_metrics.py
----------------------
Kalkulator dan Pembanding 4 Metrik Jarak Utama Vektor Embedding:
1. Cosine Similarity
2. Dot Product (Inner Product)
3. Euclidean Distance (L2)
4. Manhattan Distance (L1)
"""

import numpy as np

def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b))

def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))

def manhattan_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.sum(np.abs(a - b)))

def main():
    print("=" * 70)
    print("📐 METRIK JARAK & KEMIRIPAN VEKTOR EMBEDDING")
    print("=" * 70)

    # 3 Vektor Contoh:
    # A & B berada di arah yang hampir sama (Semantis Mirip)
    # C berada di arah yang berlawanan/berbeda (Semantis Beda)
    vA = np.array([0.5, 0.8, 0.1, 0.2])
    vB = np.array([0.48, 0.82, 0.15, 0.18])
    vC = np.array([-0.6, -0.1, 0.7, 0.3])

    # Versi Ter-normalisasi L2
    vA_norm = vA / np.linalg.norm(vA)
    vB_norm = vB / np.linalg.norm(vB)
    vC_norm = vC / np.linalg.norm(vC)

    pairs = [
        ("Pasangan A vs B (Sangat Mirip)", vA_norm, vB_norm),
        ("Pasangan A vs C (Sangat Berbeda)", vA_norm, vC_norm),
    ]

    for title, v1, v2 in pairs:
        print(f"\n🔹 {title}:")
        cos_sim = cosine_similarity(v1, v2)
        dot_p = dot_product(v1, v2)
        euc_d = euclidean_distance(v1, v2)
        man_d = manhattan_distance(v1, v2)

        print(f"   • Cosine Similarity : {cos_sim:8.4f} (Mendekati 1.0 = Mirip)")
        print(f"   • Dot Product (Norm): {dot_p:8.4f} (Identik dengan Cosine pada L2 Norm!)")
        print(f"   • Euclidean (L2)    : {euc_d:8.4f} (Mendekati 0.0 = Mirip)")
        print(f"   • Manhattan (L1)    : {man_d:8.4f} (Mendekati 0.0 = Mirip)")

    print("\n💡 HUBUNGAN MATEMATIS PENTING:")
    print("   Untuk vektor ter-normalisasi L2:")
    print("   Euclidean^2 = 2 * (1 - CosineSimilarity)")
    
    euc_calculated = np.sqrt(2 * (1 - cosine_similarity(vA_norm, vB_norm)))
    print(f"   • Euclidean aktual A vs B : {euclidean_distance(vA_norm, vB_norm):.4f}")
    print(f"   • Calculated via Cosine   : {euc_calculated:.4f} (Terbukti Sama!)")
    print("=" * 70)

if __name__ == "__main__":
    main()
