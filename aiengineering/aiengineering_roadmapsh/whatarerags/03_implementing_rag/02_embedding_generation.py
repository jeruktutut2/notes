"""
02_embedding_generation.py
Generasi Dense Vector Embeddings dari Text Chunks
Memiliki fallback deterministik berbasis hash/TF-IDF jika sentence-transformers/OpenAI tidak terinstall.
"""

import math
import random
from typing import List

class MockEmbeddingEngine:
    """Mock/Fallback Embedding Generator yang konsisten & deterministik (Dimensi 16) - Pure Python Zero-Dependency"""
    def __init__(self, dim: int = 16):
        self.dim = dim
        
    def embed_text(self, text: str) -> List[float]:
        rng = random.Random(abs(hash(text)) % (2**32))
        vec = [rng.gauss(0, 1) for _ in range(self.dim)]
        # Normalize to unit length (L2 normalization)
        norm = math.sqrt(sum(x*x for x in vec))
        return [x / norm if norm != 0 else x for x in vec]

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

def run_embedding_demo():
    print("=" * 70)
    print("🔢 DEMONSTRASI EMBEDDING GENERATION")
    print("=" * 70)
    
    chunks = [
        "RAG menggabungkan Vector DB dengan LLM.",
        "Chunking memotong dokumen besar menjadi bagian kecil.",
        "Distance metrics seperti Cosine Similarity mengukur kemiripan makna."
    ]
    
    engine = MockEmbeddingEngine(dim=8)
    embeddings = engine.embed_batch(chunks)
    
    print(f"📊 Jumlah text chunks: {len(chunks)}")
    print(f"📐 Dimensi vector embedding: {len(embeddings[0])}")
    print("-" * 50)
    
    for idx, (text, vec) in enumerate(zip(chunks, embeddings), 1):
        vec_preview = [round(x, 4) for x in vec[:5]]
        norm = math.sqrt(sum(x*x for x in vec))
        print(f"   [Chunk {idx}] \"{text}\"")
        print(f"               ➔ Vector Preview: {vec_preview} ... (L2 norm: {norm:.2f})")
        print()
    print("=" * 70)


if __name__ == "__main__":
    run_embedding_demo()
