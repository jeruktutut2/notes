"""
03_vector_database_storage.py
Penyimpanan Embeddings & Payload Metadata ke dalam Index Vector Database (In-Memory Vector Store / FAISS / Chroma)
"""

import math
import random
from typing import List, Dict, Any

class MockEmbeddingEngine:
    def __init__(self, dim: int = 16):
        self.dim = dim
    def embed_text(self, text: str) -> List[float]:
        rng = random.Random(abs(hash(text)) % (2**32))
        vec = [rng.gauss(0, 1) for _ in range(self.dim)]
        norm = math.sqrt(sum(x*x for x in vec))
        return [x / norm if norm != 0 else x for x in vec]

class InMemoryVectorStore:
    """Implementasi Sederhana Vector DB dengan Payload Storage & Cosine Similarity Indexing"""
    def __init__(self, dim: int = 16):
        self.dim = dim
        self.vectors = []
        self.payloads = []
        
    def add(self, text: str, vector: List[float], metadata: Dict[str, Any]):
        self.vectors.append(vector)
        self.payloads.append({"text": text, **metadata})
        
    def search(self, query_vector: List[float], top_k: int = 2) -> List[Dict[str, Any]]:
        if not self.vectors:
            return []
        
        scores = []
        for idx, vec in enumerate(self.vectors):
            dot_product = sum(a * b for a, b in zip(vec, query_vector))
            scores.append((dot_product, idx))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        top_items = scores[:top_k]
        
        results = []
        for score, idx in top_items:
            results.append({
                "score": float(score),
                "payload": self.payloads[idx]
            })
        return results

def run_vector_db_demo():
    print("=" * 70)
    print("🗄️ DEMONSTRASI VECTOR DATABASE STORAGE & INDEXING")
    print("=" * 70)
    
    engine = MockEmbeddingEngine(dim=12)
    db = InMemoryVectorStore(dim=12)

    
    documents = [
        {"text": "Kebijakan Garansi Laptop: Garansi berlaku 2 tahun untuk sparepart utama.", "doc_id": "DOC-001", "category": "garansi"},
        {"text": "Pengembalian Dana: Process refund membutuhkan 3-5 hari kerja ke rekening bank.", "doc_id": "DOC-002", "category": "finance"},
        {"text": "Pusat Bantuan Laptop: Buka setiap hari Senin - Jumat pukul 08.00 - 17.00.", "doc_id": "DOC-003", "category": "support"}
    ]
    
    print("📥 Mengindeks dokumen ke Vector Database...")
    for doc in documents:
        vec = engine.embed_text(doc["text"])
        db.add(text=doc["text"], vector=vec, metadata={"doc_id": doc["doc_id"], "category": doc["category"]})
        print(f"   [Indexed] {doc['doc_id']} | Category: {doc['category']}")
        
    query = "Berapa lama garansi sparepart laptop?"
    query_vec = engine.embed_text(query)
    
    print(f"\n🔍 Melakukan Search Query: \"{query}\"")
    results = db.search(query_vec, top_k=2)
    
    print("-" * 50)
    print("🏆 Hasil Retrieval Top-K:")
    for rank, res in enumerate(results, 1):
        print(f"   Rank #{rank} [Similarity Score: {res['score']:.4f}]")
        print(f"     Doc ID  : {res['payload']['doc_id']}")
        print(f"     Category: {res['payload']['category']}")
        print(f"     Teks    : \"{res['payload']['text']}\"")
        print()
    print("=" * 70)

if __name__ == "__main__":
    run_vector_db_demo()
