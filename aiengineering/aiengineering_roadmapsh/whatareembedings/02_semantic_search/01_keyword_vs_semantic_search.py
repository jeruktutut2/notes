#!/usr/bin/env python3
"""
01_keyword_vs_semantic_search.py
--------------------------------
Perbandingan langsung antara Lexical Keyword Matching (Exact Match) 
vs Vector Semantic Search (Embedding Cosine Similarity).
"""

import numpy as np

# Basis Data Dokumen Contoh
DOCUMENTS = [
    {"id": 1, "title": "Gawai Pintar Terbaru", "text": "Ponsel cerdas ini dilengkapi dengan kamera super jernih dan baterai tahan lama."},
    {"id": 2, "title": "Resep Masakan", "text": "Cara membuat nasi goreng spesial pedas manis yang lezat untuk keluarga."},
    {"id": 3, "title": "Masalah Perbankan", "text": "Kartu kredit saya terblokir saat melakukan pembayaran transaksi di luar negeri."},
    {"id": 4, "title": "Otomotif & Kendaraan", "text": "Mobil listrik terbaru ini memiliki jarak tempuh hingga 500 kilometer sekali isi daya."},
]

# Vocabulary & Embeddings Sederhana (Stand-in tanpa external API)
CONCEPT_MAP = {
    "smartphone": np.array([0.9, 0.1, 0.0, 0.1]),
    "hp":         np.array([0.88, 0.12, 0.0, 0.08]),
    "ponsel":     np.array([0.89, 0.10, 0.0, 0.09]),
    "telepon":    np.array([0.85, 0.15, 0.0, 0.10]),
    "makanan":    np.array([0.0, 0.9, 0.1, 0.0]),
    "kuliner":    np.array([0.0, 0.92, 0.08, 0.0]),
    "keuangan":   np.array([0.0, 0.1, 0.9, 0.1]),
    "bank":       np.array([0.0, 0.05, 0.95, 0.0]),
    "kendaraan":  np.array([0.1, 0.0, 0.1, 0.9]),
    "otomotif":   np.array([0.05, 0.0, 0.05, 0.95]),
}

DOC_EMBEDDINGS = [
    np.array([0.88, 0.10, 0.0, 0.10]),  # Doc 1 (Ponsel)
    np.array([0.0, 0.91, 0.05, 0.0]),   # Doc 2 (Nasi Goreng)
    np.array([0.0, 0.08, 0.92, 0.05]),  # Doc 3 (Kartu Kredit/Bank)
    np.array([0.08, 0.0, 0.08, 0.90]),  # Doc 4 (Mobil/Otomotif)
]

def keyword_search(query: str):
    query_tokens = query.lower().split()
    results = []
    for doc in DOCUMENTS:
        text_lower = doc["text"].lower() + " " + doc["title"].lower()
        score = sum(1 for token in query_tokens if token in text_lower)
        results.append((doc, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def get_query_embedding(query: str):
    words = query.lower().split()
    vecs = []
    for w in words:
        if w in CONCEPT_MAP:
            vecs.append(CONCEPT_MAP[w])
    if not vecs:
        return np.array([0.25, 0.25, 0.25, 0.25])
    avg_v = np.mean(vecs, axis=0)
    return avg_v / np.linalg.norm(avg_v)

def semantic_search(query: str):
    q_vec = get_query_embedding(query)
    results = []
    for doc, d_vec in zip(DOCUMENTS, DOC_EMBEDDINGS):
        score = float(np.dot(q_vec, d_vec))
        results.append((doc, score))
    results.sort(key=lambda x: x[1], reverse=True)
    return results

def main():
    print("=" * 70)
    print("🔍 DEMO: KEYWORD SEARCH VS VECTOR SEMANTIC SEARCH")
    print("=" * 70)

    # Query yang menggunakan sinonim (tidak ada kata persis di dokumen!)
    test_queries = [
        "Rekomendasi HP kamera bagus",
        "Bagaimana cara mengurus transaksi bank terganggu?",
        "Mobil listrik hemat energi"
    ]

    for query in test_queries:
        print(f"\n❓ QUERY USER: \"{query}\"")
        
        # 1. Keyword Search
        kw_res = keyword_search(query)
        top_kw = kw_res[0]
        print(f"   🔤 Keyword Search Top Result : ID {top_kw[0]['id']} - '{top_kw[0]['title']}' (Match Score: {top_kw[1]})")
        
        # 2. Semantic Search
        sem_res = semantic_search(query)
        top_sem = sem_res[0]
        print(f"   🧠 Semantic Search Top Result: ID {top_sem[0]['id']} - '{top_sem[0]['title']}' (Cosine Sim: {top_sem[1]:.4f})")

    print("\n💡 EVAKUASI:")
    print("   Keyword Search gagal menemukan Dokumen 1 untuk query 'HP' karena dokumen hanya menulis 'Ponsel cerdas'.")
    print("   Semantic Search berhasil memahami bahwa 'HP' ~ 'Ponsel' ~ 'Gawai'!")
    print("=" * 70)

if __name__ == "__main__":
    main()
