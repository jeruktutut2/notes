#!/usr/bin/env python3
"""
03_hybrid_search_bm25_dense.py
------------------------------
Implementasi Hybrid Search menggabungkan Lexical Score & Dense Vector Score
menggunakan Reciprocal Rank Fusion (RRF).
"""

import numpy as np

DOCS = [
    {"id": 1, "text": "Dokumen garansi produk laptop ASUS ROG Strix GTX-4090 serial #88219."},
    {"id": 2, "text": "Panduan perbaikan masalah komputasi lambat dan laptop mengalami overheat."},
    {"id": 3, "text": "Kebijakan pengembalian dana transaksi toko komputer dan komponen hardware."},
    {"id": 4, "text": "Cara mengajukan klaim garansi hardware komputer yang rusak atau gagal fungsi."},
]

def lexical_rank(query: str):
    q_tokens = query.lower().split()
    scores = []
    for doc in DOCS:
        text = doc["text"].lower()
        score = sum(2.0 if t in text else 0.0 for t in q_tokens)
        scores.append((doc["id"], score))
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def mock_vector_rank(query: str):
    # Pseudo vector sim simulation
    seed = sum(ord(c) for c in query)
    np.random.seed(seed)
    scores = [(doc["id"], float(np.random.uniform(0.3, 0.95))) for doc in DOCS]
    # Make ID 4 and ID 1 have high semantic relevance for warranty queries
    if "garansi" in query.lower() or "klaim" in query.lower():
        scores = [(1, 0.88), (4, 0.94), (2, 0.45), (3, 0.50)]
    scores.sort(key=lambda x: x[1], reverse=True)
    return scores

def rrf_fusion(lex_ranks, vec_ranks, k: int = 60):
    """Reciprocal Rank Fusion Score: 1/(k + rank_lex) + 1/(k + rank_vec)"""
    doc_rrf = {}

    for rank, (doc_id, score) in enumerate(lex_ranks, 1):
        doc_rrf[doc_id] = doc_rrf.get(doc_id, 0.0) + (1.0 / (k + rank))

    for rank, (doc_id, score) in enumerate(vec_ranks, 1):
        doc_rrf[doc_id] = doc_rrf.get(doc_id, 0.0) + (1.0 / (k + rank))

    sorted_rrf = sorted(doc_rrf.items(), key=lambda x: x[1], reverse=True)
    return sorted_rrf

def main():
    print("=" * 70)
    print("⚡ DEMO: HYBRID SEARCH WITH RECIPROCAL RANK FUSION (RRF)")
    print("=" * 70)

    query = "klaim garansi laptop ASUS serial #88219"
    print(f"\n❓ QUERY SPESIFIK & SEMANTIS: \"{query}\"")

    lex_res = lexical_rank(query)
    vec_res = mock_vector_rank(query)
    rrf_res = rrf_fusion(lex_res, vec_res)

    print("\n1. Hasil Lexical Search (Penting untuk exact serial #88219):")
    for doc_id, sc in lex_res:
        doc_text = next(d['text'] for d in DOCS if d['id'] == doc_id)
        print(f"   • Doc #{doc_id} (Score: {sc:.2f}) -> {doc_text[:60]}...")

    print("\n2. Hasil Vector Search (Penting untuk arti semantis garansi/klaim):")
    for doc_id, sc in vec_res:
        doc_text = next(d['text'] for d in DOCS if d['id'] == doc_id)
        print(f"   • Doc #{doc_id} (Cosine: {sc:.4f}) -> {doc_text[:60]}...")

    print("\n3. Hasil HYBRID SEARCH (RRF Combined Fusion Ranking):")
    for rank, (doc_id, rrf_score) in enumerate(rrf_res, 1):
        doc_text = next(d['text'] for d in DOCS if d['id'] == doc_id)
        print(f"   🏆 Rank {rank}: Doc #{doc_id} (RRF Score: {rrf_score:.5f}) -> {doc_text}")

    print("=" * 70)

if __name__ == "__main__":
    main()
