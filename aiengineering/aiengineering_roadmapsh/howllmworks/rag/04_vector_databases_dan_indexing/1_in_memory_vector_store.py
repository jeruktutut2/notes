import hashlib
import numpy as np

class InMemoryVectorStore:
    def __init__(self, dim: int = 128):
        self.dim = dim
        self.vectors = []    # List of np.ndarray
        self.documents = []  # List of str
        self.metadata = []   # List of dict

    def _embed(self, text: str) -> np.ndarray:
        """Embedding deterministik sederhana untuk pengujian in-memory vector store."""
        seed = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % (2**32)
        np.random.seed(seed)
        vec = np.random.randn(self.dim)
        return vec / np.linalg.norm(vec)

    def add_documents(self, docs: list, metadatas: list = None):
        if metadatas is None:
            metadatas = [{} for _ in docs]

        for doc, meta in zip(docs, metadatas):
            vec = self._embed(doc)
            self.vectors.append(vec)
            self.documents.append(doc)
            self.metadata.append(meta)

    def search(self, query: str, top_k: int = 3, filter_meta: dict = None) -> list:
        if not self.vectors:
            return []

        query_vec = self._embed(query)
        matrix = np.array(self.vectors)
        # Cosine similarity (vektor sudah ternormalisasi)
        scores = np.dot(matrix, query_vec)

        results = []
        for idx, score in enumerate(scores):
            meta = self.metadata[idx]
            # Match filter metadata jika ada
            if filter_meta:
                match = all(meta.get(k) == v for k, v in filter_meta.items())
                if not match:
                    continue
            results.append({
                "score": float(score),
                "document": self.documents[idx],
                "metadata": meta
            })

        # Urutkan berdasarkan skor tertinggi
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]

def main():
    print("=== 01. Custom In-Memory Vector Store ===")

    store = InMemoryVectorStore(dim=64)

    documents = [
        "Python adalah bahasa yang sangat populer untuk Data Science dan AI.",
        "ChromaDB dan Qdrant adalah Vector Databases skala besar.",
        "Arsitektur RAG menggabungkan Vector Search dengan Large Language Models.",
        "Resep memasak rendang daging sapi khas Minangkabau."
    ]

    metadatas = [
        {"category": "programming", "year": 2024},
        {"category": "database", "year": 2024},
        {"category": "ai", "year": 2024},
        {"category": "kuliner", "year": 2023}
    ]

    store.add_documents(documents, metadatas)
    print(f"[OK] Memasukkan {len(documents)} dokumen ke Vector Store.\n")

    query = "Bagaimana arsitektur RAG bekerja dengan Vector DB?"
    print(f"Query: '{query}'")
    results = store.search(query, top_k=2)

    for i, res in enumerate(results, 1):
        print(f"\n  Hasil #{i} (Score: {res['score']:.4f}):")
        print(f"  Dokumen : \"{res['document']}\"")
        print(f"  Metadata: {res['metadata']}")

    # Demo Metadata Filtering
    print(f"\nQuery dengan Filter Metadata (category='programming'):")
    filtered_res = store.search(query, top_k=2, filter_meta={"category": "programming"})
    for res in filtered_res:
        print(f"  - Match: {res['document']} ({res['metadata']})")

if __name__ == "__main__":
    main()
