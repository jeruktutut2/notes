import hashlib
import numpy as np

def mock_embedding(text: str, dim: int = 64) -> np.ndarray:
    """Fungsi embedding deterministik lokal untuk simulasi dense retrieval."""
    seed = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    vec = np.random.randn(dim)
    return vec / np.linalg.norm(vec)

def dense_retrieval(query: str, corpus: list, top_k: int = 3) -> list:
    query_vec = mock_embedding(query)
    corpus_vecs = np.array([mock_embedding(doc) for doc in corpus])

    scores = np.dot(corpus_vecs, query_vec)

    results = []
    for idx, score in enumerate(scores):
        results.append({
            "doc_id": idx + 1,
            "document": corpus[idx],
            "score": float(score)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]

def main():
    print("=== 01. Dense Semantic Retrieval ===")

    corpus = [
        "Pengembangan perangkat lunak berbasis AI dan kecerdasan buatan.",
        "Model GPT-4o dan Claude 3.5 Sonnet adalah LLM terkini.",
        "Panduan membuat masakan rendang daging sapi pedas gurih.",
        "Arsitektur Microservices dan Cloud Native pada AWS GCP.",
        "Manajemen memori pada bahasa pemrograman C dan Rust."
    ]

    query = "Bagaimana perkembangan model LLM terbaru saat ini?"

    print(f"Query  : '{query}'")
    print(f"Corpus : {len(corpus)} dokumen\n")

    results = dense_retrieval(query, corpus, top_k=3)

    print("Hasil Dense Retrieval (Top-3 Similarity Score):")
    for r in results:
        print(f"  - [Doc #{r['doc_id']}] Score: {r['score']:.4f}")
        print(f"    Content: \"{r['document']}\"\n")

if __name__ == "__main__":
    main()
