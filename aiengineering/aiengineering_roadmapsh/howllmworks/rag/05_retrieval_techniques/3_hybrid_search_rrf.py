def reciprocal_rank_fusion(dense_results: list, sparse_results: list, k: int = 60) -> list:
    """
    Reciprocal Rank Fusion (RRF):
    RRF_Score(d) = sum(1 / (k + rank_i(d)))
    Menggabungkan hasil Dense + Sparse secara fair tanpa perlu normalisasi skala skor.
    """
    rrf_scores = {}
    doc_map = {}

    # Proses Dense Results
    for rank, res in enumerate(dense_results, 1):
        doc_id = res["doc_id"]
        doc_map[doc_id] = res["document"]
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # Proses Sparse Results
    for rank, res in enumerate(sparse_results, 1):
        doc_id = res["doc_id"]
        doc_map[doc_id] = res["document"]
        rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # Urutkan berdasarkan RRF Score terbanyak
    combined = [
        {"doc_id": doc_id, "document": doc_map[doc_id], "rrf_score": score}
        for doc_id, score in rrf_scores.items()
    ]
    combined.sort(key=lambda x: x["rrf_score"], reverse=True)
    return combined

def main():
    print("=== 03. Hybrid Search: Reciprocal Rank Fusion (RRF) ===")

    # Simulasi hasil Dense Search (Top-3)
    dense_results = [
        {"doc_id": 101, "document": "Panduan Instalasi Python dan Venv", "score": 0.89},
        {"doc_id": 102, "document": "Konfigurasi Virtual Environment Pip", "score": 0.82},
        {"doc_id": 103, "document": "Manajemen Package Conda & Poetry", "score": 0.75}
    ]

    # Simulasi hasil Sparse Keyword Search (Top-3)
    sparse_results = [
        {"doc_id": 102, "document": "Konfigurasi Virtual Environment Pip", "score": 4.12},
        {"doc_id": 104, "document": "Perintah pip install requirements.txt", "score": 3.85},
        {"doc_id": 101, "document": "Panduan Instalasi Python dan Venv", "score": 2.10}
    ]

    print("[Dense Search Results (Semantic)]")
    for r in dense_results:
        print(f"  - Doc #{r['doc_id']}: {r['document']}")

    print("\n[Sparse Search Results (BM25 Keyword)]")
    for r in sparse_results:
        print(f"  - Doc #{r['doc_id']}: {r['document']}")

    # Jalankan RRF Fusion
    fused_results = reciprocal_rank_fusion(dense_results, sparse_results, k=60)

    print("\n[Hasil Hybrid Search (RRF Score)]")
    for i, r in enumerate(fused_results, 1):
        print(f"  #{i} [Doc #{r['doc_id']}] RRF Score: {r['rrf_score']:.6f} -> \"{r['document']}\"")

if __name__ == "__main__":
    main()
