#!/usr/bin/env python3
"""
01_vector_space_and_math.py
---------------------------
Demonstrasi matematis dasar Ruang Vektor (Vector Space) dan representasi Teks ke Vektor Embedding.
Dapat dijalankan secara murni tanpa external API key!
"""

import math
import numpy as np

# Deterministic Mock Embedding Engine untuk Simulasi Semantik
VOCAB_SEMANIC_MAP = {
    "raja":     np.array([0.80, 0.90, 0.10, 0.05]),
    "ratu":     np.array([0.78, 0.85, 0.85, 0.05]),
    "pria":     np.array([0.85, 0.95, 0.05, 0.02]),
    "wanita":   np.array([0.82, 0.05, 0.90, 0.02]),
    "mobil":    np.array([0.05, 0.10, 0.05, 0.95]),
    "motor":    np.array([0.08, 0.08, 0.04, 0.88]),
    "kucing":   np.array([0.15, 0.40, 0.40, 0.10]),
}

def generate_mock_embedding(text: str, dim: int = 4) -> np.ndarray:
    """Mengubah teks menjadi vektor embedding sintetis namun semantis."""
    words = text.lower().split()
    vectors = []
    for w in words:
        if w in VOCAB_SEMANIC_MAP:
            vectors.append(VOCAB_SEMANIC_MAP[w])
        else:
            # Fallback pseudo-random deterministic vector berdasarkan hash kata
            seed = sum(ord(c) for c in w)
            np.random.seed(seed)
            v = np.random.uniform(-1, 1, size=dim)
            vectors.append(v)
    
    avg_vec = np.mean(vectors, axis=0) if vectors else np.zeros(dim)
    # L2 normalize
    norm = np.linalg.norm(avg_vec)
    return avg_vec / norm if norm > 0 else avg_vec

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Menghitung Cosine Similarity antara dua vektor."""
    dot = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(dot / (norm1 * norm2))

def main():
    print("=" * 65)
    print("🧠 DEMO: VECTOR SPACE & EMBEDDING MATHEMATICS")
    print("=" * 65)

    words = ["raja", "ratu", "pria", "wanita", "mobil", "motor"]
    embeddings = {w: generate_mock_embedding(w) for w in words}

    print("\n1. Representasi Vektor 4-Dimensi:")
    for w, v in embeddings.items():
        print(f"   • {w:<8} -> {np.round(v, 3)}")

    print("\n2. Analogi Vektor Terkenal (King - Man + Woman = Queen?):")
    # Raja - Pria + Wanita
    king = embeddings["raja"]
    man = embeddings["pria"]
    woman = embeddings["wanita"]
    queen_calc = king - man + woman
    queen_calc_norm = queen_calc / np.linalg.norm(queen_calc)

    print(f"   • (Raja - Pria + Wanita)  = {np.round(queen_calc_norm, 3)}")
    print(f"   • Actual 'Ratu' Vector     = {np.round(embeddings['ratu'], 3)}")
    
    sim_to_queen = cosine_similarity(queen_calc_norm, embeddings["ratu"])
    sim_to_car = cosine_similarity(queen_calc_norm, embeddings["mobil"])
    
    print(f"\n3. Hasil Kemiripan (Cosine Similarity):")
    print(f"   • Similartiy to 'ratu'  : {sim_to_queen:.4f} (Sangat Tinggi!)")
    print(f"   • Similarity to 'mobil' : {sim_to_car:.4f} (Sangat Rendah!)")
    print("=" * 65)

if __name__ == "__main__":
    main()
