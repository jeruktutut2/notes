#!/usr/bin/env python3
"""
02_user_profile_vector_aggregation.py
------------------------------------
Membangun Vektor Profil Pengguna Sintetis (User Vector Aggregation) 
berdasarkan riwayat interaksi weighted.
"""

import numpy as np

PRODUCTS = [
    {"id": 101, "name": "Laptop Gaming ASUS ROG RTX 4080", "desc": "Laptop gaming performa ekstrem dengan GPU RTX 4080 dan prosesor Intel i9."},
    {"id": 102, "name": "Mouse Gaming Wireless Razer", "desc": "Mouse gaming tanpa kabel presisi tinggi 30K DPI dan tombol mekanis."},
    {"id": 103, "name": "Buku Panduan Data Science Python", "desc": "Panduan praktis belajar analisis data, pandas, numpy, dan machine learning."},
    {"id": 104, "name": "Buku Pemrograman AI & LLM Engineering", "desc": "Langkah membangun aplikasi berbasis LLM, RAG, Vector Database, dan Prompt Engineering."},
    {"id": 105, "name": "Monitor Gaming Curved 240Hz 4K", "desc": "Layar monitor lengkung respons super cepat 1ms untuk esports gaming."},
]

def mock_product_embedding(desc: str, dim: int = 12) -> np.ndarray:
    t = desc.lower()
    vec = np.zeros(dim)
    if any(w in t for w in ["gaming", "rtx", "gpu", "mouse", "monitor", "240hz"]):
        vec[0:6] += 0.95
    if any(w in t for w in ["buku", "python", "data", "ai", "llm", "rag", "pembelajaran"]):
        vec[6:12] += 0.95
    
    seed = sum(ord(c) for c in desc[:20])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def build_user_vector(user_history: list) -> np.ndarray:
    dim = 12
    weighted_vectors = []
    total_weights = 0.0

    for prod_id, weight in user_history:
        prod = next((p for p in PRODUCTS if p["id"] == prod_id), None)
        if prod:
            vec = mock_product_embedding(prod["desc"], dim=dim)
            weighted_vectors.append(vec * weight)
            total_weights += weight

    if not weighted_vectors:
        return np.zeros(dim)

    aggregated = np.sum(weighted_vectors, axis=0) / total_weights
    norm = np.linalg.norm(aggregated)
    return aggregated / norm if norm > 0 else aggregated

def recommend_for_user(user_vector: np.ndarray, exclude_ids: list, top_n: int = 2):
    results = []
    for prod in PRODUCTS:
        if prod["id"] in exclude_ids:
            continue
        p_vec = mock_product_embedding(prod["desc"], dim=12)
        sim = float(np.dot(user_vector, p_vec))
        results.append((prod, sim))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:top_n]

def main():
    print("=" * 70)
    print("👤 DEMO: USER PROFILE VECTOR AGGREGATION RECOMMENDER")
    print("=" * 70)

    # User History: Membeli Laptop Gaming (101) & Melihat Mouse Gaming (102)
    user_history = [
        (101, 1.0), # Beli Laptop Gaming (Weight 1.0)
        (102, 0.3), # View Mouse Gaming (Weight 0.3)
    ]

    history_ids = [hid for hid, w in user_history]
    print(f"\n📜 Riwayat Interaksi Pengguna:")
    for hid, w in user_history:
        p = next(x for x in PRODUCTS if x["id"] == hid)
        print(f"   • {p['name']} (Interaksi Weight: {w})")

    print("\n🧮 Membangun Aggregate User Profile Vector...")
    user_vec = build_user_vector(user_history)

    print("\n🎁 Rekomendasi Item Baru Berdasarkan Profile Vector:")
    recs = recommend_for_user(user_vec, exclude_ids=history_ids, top_n=2)
    for p, sim in recs:
        print(f"   🏆 [ID #{p['id']}] {p['name']} (Match Score: {sim:.4f})")

    print("=" * 70)

if __name__ == "__main__":
    main()
