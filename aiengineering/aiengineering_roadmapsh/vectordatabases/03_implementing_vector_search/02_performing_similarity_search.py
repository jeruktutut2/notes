#!/usr/bin/env python3
"""
Modul 03: Implementing Vector Search - Performing Similarity Search
Top-K Search, Pre-Filtering vs Post-Filtering Metadata, dan Hybrid Search (BM25 + Dense Vectors).
"""

import numpy as np

# Sample Collection for Hybrid Search
COLLECTION = [
    {"id": "doc1", "text": "Pinecone serverless vector database index", "category": "cloud", "vec": np.array([0.9, 0.1, 0.0, 0.1])},
    {"id": "doc2", "text": "Chroma DB local embedded persistent store", "category": "local", "vec": np.array([0.8, 0.2, 0.1, 0.0])},
    {"id": "doc3", "text": "FAISS in-memory GPU vector search library", "category": "library", "vec": np.array([0.1, 0.9, 0.8, 0.2])},
    {"id": "doc4", "text": "Postgres pgvector extension cloud deployment", "category": "cloud", "vec": np.array([0.85, 0.15, 0.0, 0.1])},
]

def bm25_mock_sparse_score(text: str, query_keywords: list) -> float:
    """Simulasi sederhana skor pencocokan kata kunci BM25"""
    score = 0.0
    words = text.lower().split()
    for kw in query_keywords:
        if kw.lower() in words:
            score += 1.0
    return score

def hybrid_search(query_vec: np.ndarray, query_keywords: list, alpha: float = 0.7, top_k: int = 2):
    """
    Hybrid Search:
    Score = alpha * DenseScore + (1 - alpha) * SparseScore
    """
    results = []
    for item in COLLECTION:
        # 1. Dense Score (Cosine)
        dense_score = float(np.dot(query_vec, item["vec"]) / (np.linalg.norm(query_vec) * np.linalg.norm(item["vec"])))
        
        # 2. Sparse Score (BM25)
        sparse_score = bm25_mock_sparse_score(item["text"], query_keywords)
        
        # Normalisasi gabungan
        combined_score = (alpha * dense_score) + ((1.0 - alpha) * sparse_score)
        
        results.append({
            "id": item["id"],
            "text": item["text"],
            "dense_score": dense_score,
            "sparse_score": sparse_score,
            "hybrid_score": combined_score
        })

    results.sort(key=lambda x: x["hybrid_score"], reverse=True)
    return results[:top_k]

def main():
    print("=========================================================")
    print("  02: PERFORMING SIMILARITY SEARCH & HYBRID SEARCH")
    print("=========================================================\n")

    query_v = np.array([0.88, 0.12, 0.05, 0.05])
    keywords = ["cloud", "pinecone"]

    print("🔍 Query Input:")
    print(f"  • Dense Vector : {query_v}")
    print(f"  • Sparse Keywords: {keywords}\n")

    # 1. Standard Vector Similarity Search
    print("--- [1] DENSE VECTOR SEARCH MURNI (Alpha = 1.0) ---")
    dense_res = hybrid_search(query_v, keywords, alpha=1.0, top_k=2)
    for r in dense_res:
        print(f"  • [{r['id']}] Skor Vector: {r['dense_score']:.4f} | Teks: '{r['text']}'")
    print()

    # 2. Keyword Search Murni (BM25)
    print("--- [2] SPARSE KEYWORD SEARCH MURNI (Alpha = 0.0) ---")
    sparse_res = hybrid_search(query_v, keywords, alpha=0.0, top_k=2)
    for r in sparse_res:
        print(f"  • [{r['id']}] Skor BM25  : {r['sparse_score']:.4f} | Teks: '{r['text']}'")
    print()

    # 3. Hybrid Search (Dense + Sparse)
    print("--- [3] HYBRID SEARCH (Alpha = 0.7 Dense + 0.3 Sparse) ---")
    hybrid_res = hybrid_search(query_v, keywords, alpha=0.7, top_k=2)
    for r in hybrid_res:
        print(f"  • [{r['id']}] Skor Hybrid: {r['hybrid_score']:.4f} (Dense: {r['dense_score']:.2f}, Sparse: {r['sparse_score']:.2f})")
        print(f"    Teks: '{r['text']}'")

    print("\n✅ Hands-on Similarity Search Selesai! Hybrid Search memberikan akurasi tertinggi untuk RAG production.")

if __name__ == "__main__":
    main()
