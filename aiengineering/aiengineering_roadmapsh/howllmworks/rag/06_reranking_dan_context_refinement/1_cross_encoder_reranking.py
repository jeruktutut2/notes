def simulate_cross_encoder_score(query: str, doc: str) -> float:
    """
    Simulasi Cross-Encoder Scoring Model.
    Berbeda dari Bi-Encoder yang meng-embed query & doc terpisah, Cross-Encoder menerima
    (query, doc) sekaligus dan menganalisis hubungan cross-attention penuh.
    """
    query_words = set(query.lower().split())
    doc_words = doc.lower().split()

    matches = sum(1 for w in doc_words if w in query_words)
    score = (matches / max(len(doc_words), 1)) * 5.0
    return float(min(score, 1.0))

def main():
    print("=== 01. Cross-Encoder Reranking Simulation ===")

    query = "Bagaimana cara melakukan deployment aplikasi Python ke Docker?"

    # Hasil pencarian awal dari Vector DB (Bi-Encoder Initial Retrieval)
    initial_retrieved_docs = [
        {"id": 1, "text": "Panduan umum bahasa pemrograman Python dan fitur barunya."},
        {"id": 2, "text": "Langkah demi langkah membuat Dockerfile dan containerize aplikasi Python."},
        {"id": 3, "text": "Konfigurasi server Nginx untuk load balancing web server."},
        {"id": 4, "text": "Perintah docker run dan docker build untuk deployment container Python."}
    ]

    print(f"Query: '{query}'\n")
    print("[Dokumen Sebelum Reranking (Bi-Encoder Order)]")
    for doc in initial_retrieved_docs:
        print(f"  - Doc #{doc['id']}: {doc['text']}")

    # Proses Reranking dengan Cross-Encoder
    reranked = []
    for doc in initial_retrieved_docs:
        ce_score = simulate_cross_encoder_score(query, doc['text'])
        reranked.append({
            "id": doc['id'],
            "text": doc['text'],
            "rerank_score": ce_score
        })

    reranked.sort(key=lambda x: x["rerank_score"], reverse=True)

    print("\n[Dokumen Setelah Cross-Encoder Reranking (Presisi Tinggi)]")
    for rank, doc in enumerate(reranked, 1):
        print(f"  #{rank} [Doc #{doc['id']}] Score: {doc['rerank_score']:.4f} -> {doc['text']}")

if __name__ == "__main__":
    main()
