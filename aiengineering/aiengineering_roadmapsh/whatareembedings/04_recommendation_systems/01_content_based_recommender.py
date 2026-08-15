#!/usr/bin/env python3
"""
01_content_based_recommender.py
-------------------------------
Sistem Rekomendasi Item-to-Item Content Filtering berbasis Kemiripan Embedding Produk.
"""

import numpy as np

PRODUCTS = [
    {"id": 101, "name": "Laptop Gaming ASUS ROG RTX 4080", "category": "Electronics", "desc": "Laptop gaming performa ekstrem dengan GPU RTX 4080 dan prosesor Intel i9."},
    {"id": 102, "name": "Mouse Gaming Wireless Razer", "category": "Electronics", "desc": "Mouse gaming tanpa kabel presisi tinggi 30K DPI dan tombol mekanis."},
    {"id": 103, "name": "Buku Panduan Data Science Python", "category": "Books", "desc": "Panduan praktis belajar analisis data, pandas, numpy, dan machine learning."},
    {"id": 104, "name": "Buku Pemrograman AI & LLM Engineering", "category": "Books", "desc": "Langkah membangun aplikasi berbasis LLM, RAG, Vector Database, dan Prompt Engineering."},
    {"id": 105, "name": "Monitor Gaming Curved 240Hz 4K", "category": "Electronics", "desc": "Layar monitor lengkung respons super cepat 1ms untuk esports gaming."},
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

def recommend_similar_items(target_item_id: int, top_n: int = 2):
    target_product = next((p for p in PRODUCTS if p["id"] == target_item_id), None)
    if not target_product:
        return []
    
    target_vec = mock_product_embedding(target_product["desc"])
    
    recommendations = []
    for product in PRODUCTS:
        if product["id"] == target_item_id:
            continue
        p_vec = mock_product_embedding(product["desc"])
        sim = float(np.dot(target_vec, p_vec))
        recommendations.append((product, sim))
    
    recommendations.sort(key=lambda x: x[1], reverse=True)
    return recommendations[:top_n]

def main():
    print("=" * 70)
    print("🛍️ DEMO: ITEM-TO-ITEM CONTENT-BASED RECOMMENDER ENGINE")
    print("=" * 70)

    target_id = 104 # Buku Pemrograman AI & LLM
    target_prod = next(p for p in PRODUCTS if p["id"] == target_id)
    
    print(f"\n🛒 Produk yang Sedang Dilihat Pengguna:")
    print(f"   [ID #{target_prod['id']}] {target_prod['name']}")
    print(f"   Deskripsi: \"{target_prod['desc']}\"")

    print(f"\n✨ Rekomendasi Produk Serupa (Cosine Similarity Terdekat):")
    recs = recommend_similar_items(target_id, top_n=2)
    for p, sim in recs:
        print(f"   • [ID #{p['id']}] {p['name']} (Sim Score: {sim:.4f})")
        print(f"     Deskripsi: \"{p['desc']}\"")

    print("=" * 70)

if __name__ == "__main__":
    main()
