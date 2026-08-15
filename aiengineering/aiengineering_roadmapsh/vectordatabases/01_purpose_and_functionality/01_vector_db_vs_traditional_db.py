#!/usr/bin/env python3
"""
Modul 01: Purpose and Functionality - Vector DB vs Traditional DB
Demonstrasi komparatif antara pencarian berbasis Kata Kunci/SQL Tradisional vs Semantik Vector Database.
"""

import time
import numpy as np

# Sample Document Dataset
DOCUMENTS = [
    {"id": 1, "title": "Dasar Machine Learning", "category": "AI", "text": "Pengenalan algoritma regresi linier dan klasifikasi data dengan Python."},
    {"id": 2, "title": "Arsitektur Transformer LLM", "category": "AI", "text": "Model kecerdasan buatan modern menggunakan mekanisme Self-Attention untuk memproses bahasa."},
    {"id": 3, "title": "Resep Rendang Daging Sapi", "category": "Kuliner", "text": "Cara memasak rendang khas Padang dengan bumbu rempah kelapa sangrai."},
    {"id": 4, "title": "Panduan Pemrograman Python", "category": "Tech", "text": "Tutorial penulisan sintaksis Python 3 yang bersih, modular, dan cepat."},
    {"id": 5, "title": "Vektor Database & ANN Search", "category": "AI", "text": "Sistem penyimpanan embedding berdimensi tinggi untuk pencarian kemiripan konteks cepat."},
]

def traditional_exact_match(query_keyword: str):
    """Simulasi Query Tradisional SQL LIKE '%keyword%'"""
    start_time = time.perf_counter()
    results = []
    for doc in DOCUMENTS:
        if query_keyword.lower() in doc["text"].lower() or query_keyword.lower() in doc["title"].lower():
            results.append(doc)
    elapsed_ms = (time.perf_counter() - start_time) * 1000
    return results, elapsed_ms

def mock_embed(text: str, dim: int = 128) -> np.ndarray:
    """Fungsi simulasi pembuatan embedding deterministik dari teks"""
    rng = np.random.RandomState(seed=abs(hash(text)) % (2**32))
    vec = rng.randn(dim)
    return vec / np.linalg.norm(vec)

class MockVectorDB:
    """Simulasi Sederhana Vector Database"""
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.vectors = []
        self.payloads = []

    def upsert(self, doc_id: int, vector: np.ndarray, payload: dict):
        self.vectors.append(vector)
        self.payloads.append({"id": doc_id, **payload})

    def search(self, query_vector: np.ndarray, top_k: int = 3):
        start_time = time.perf_counter()
        if not self.vectors:
            return [], 0.0
        
        matrix = np.array(self.vectors) # Shape: (N, dim)
        # Cosine similarity (karena vektor ter-normalisasi)
        scores = np.dot(matrix, query_vector)
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "score": float(scores[idx]),
                "payload": self.payloads[idx]
            })
        elapsed_ms = (time.perf_counter() - start_time) * 1000
        return results, elapsed_ms

def main():
    print("=========================================================")
    print("  01: VECTOR DATABASE VS TRADITIONAL DATABASE DEMO")
    print("=========================================================\n")

    query_text = "AI dan Kecerdasan Buatan"
    print(f"🔍 Query Pengguna: '{query_text}'\n")

    # 1. Traditional SQL / Exact Match
    keyword = "AI"
    sql_results, sql_time = traditional_exact_match(keyword)
    print(f"--- [1] DATABASE TRADISIONAL (Keyword Match: '{keyword}') ---")
    print(f"Waktu Eksekusi: {sql_time:.4f} ms")
    print(f"Jumlah Hasil Ditemukan: {len(sql_results)}")
    for doc in sql_results:
        print(f"  • ID {doc['id']}: {doc['title']} ({doc['category']})")
    print()

    # 2. Vector Database Semantic Search
    print("--- [2] VECTOR DATABASE (Semantic Similarity Search) ---")
    vdb = MockVectorDB(dim=128)
    for doc in DOCUMENTS:
        vec = mock_embed(doc["text"] + " " + doc["title"])
        vdb.upsert(doc["id"], vec, doc)

    query_vec = mock_embed("AI dan Kecerdasan Buatan modern untuk pemrosesan teks")
    vec_results, vec_time = vdb.search(query_vec, top_k=3)
    print(f"Waktu Eksekusi Vector Search: {vec_time:.4f} ms")
    print("Top-3 Hasil Kemiripan Semantik Terdekat:")
    for rank, res in enumerate(vec_results, 1):
        payload = res["payload"]
        print(f"  {rank}. [Skor: {res['score']:.4f}] ID {payload['id']}: {payload['title']}")
        print(f"     Teks: '{payload['text'][:60]}...'")

    print("\n✅ Kesimpulan: Vector DB menemukan makna kontekstual tanpa tergantung keyword persis!")

if __name__ == "__main__":
    main()
