#!/usr/bin/env python3
"""
03_top_n_item_ranking.py
------------------------
Top-N Recommendation Ranking Pipeline dengan Popularity Boost & Category Filtering.
"""

import numpy as np

CATALOG = [
    {"id": 1, "title": "Tutorial PyTorch Deep Learning", "category": "Tech", "popularity": 0.95, "desc": "Belajar deep learning dari dasar hingga pembuatan neural network dengan PyTorch."},
    {"id": 2, "title": "Buku Resep Kue Tradisional", "category": "Food", "popularity": 0.60, "desc": "Panduan membuat kue jajanan pasar nusantara yang lezat dan mudah."},
    {"id": 3, "title": "Penerapan LLM RAG di Enterprise", "category": "Tech", "popularity": 0.88, "desc": "Arsitektur RAG, Vector Database, dan Fine-tuning LLM untuk industri."},
    {"id": 4, "title": "Tips Investasi Reksa Dana untuk Pemula", "category": "Finance", "popularity": 0.75, "desc": "Strategi investasi aman jangka panjang dengan instrumen reksa dana."},
]

def mock_embed(text: str, dim: int = 8) -> np.ndarray:
    t = text.lower()
    vec = np.zeros(dim)
    if "tech" in t or "pytorch" in t or "llm" in t or "rag" in t:
        vec[0:3] += 1.0
    if "food" in t or "resep" in t or "kue" in t:
        vec[3:5] += 1.0
    if "finance" in t or "investasi" in t or "reksa" in t:
        vec[5:8] += 1.0
    
    seed = sum(ord(c) for c in text[:15])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def rank_top_n(user_query: str, alpha: float = 0.8, top_n: int = 3):
    """
    Final Score = alpha * CosineSimilarity + (1 - alpha) * PopularityScore
    """
    q_vec = mock_embed(user_query)
    ranked = []

    for item in CATALOG:
        i_vec = mock_embed(item["title"] + " " + item["desc"])
        cos_sim = float(np.dot(q_vec, i_vec))
        pop_score = item["popularity"]

        final_score = (alpha * cos_sim) + ((1 - alpha) * pop_score)
        ranked.append((item, final_score, cos_sim, pop_score))

    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked[:top_n]

def main():
    print("=" * 70)
    print("🏆 DEMO: TOP-N HYBRID RECOMMENDATION RANKING PIPELINE")
    print("=" * 70)

    user_query = "Saya ingin belajar pemrograman AI dan Deep Learning"
    print(f"\n❓ Minat Pengguna: \"{user_query}\"")
    print("   Menggunakan Kombinasi: 80% Embedding Similarity + 20% Popularity Score\n")

    results = rank_top_n(user_query, alpha=0.8, top_n=3)

    print(f"{'Rank':<6} | {'Judul Item':<35} | {'Final Score':<12} | {'Cosine Sim':<12} | {'Popularity':<10}")
    print("-" * 82)
    for r, (item, final_s, sim, pop) in enumerate(results, 1):
        print(f"{r:<6} | {item['title']:<35} | {final_s:<12.4f} | {sim:<12.4f} | {pop:<10.2f}")

    print("=" * 70)

if __name__ == "__main__":
    main()
