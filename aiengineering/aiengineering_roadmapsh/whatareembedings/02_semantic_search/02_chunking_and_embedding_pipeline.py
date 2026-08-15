#!/usr/bin/env python3
"""
02_chunking_and_embedding_pipeline.py
------------------------------------
Pipeline pemotongan dokumen panjang (Chunking) dan indexing vektor semantik.
"""

import re
import numpy as np

LONG_TEXT = """
Kecerdasan Buatan (Artificial Intelligence / AI) telah berkembang pesat dalam dekade terakhir.
Salah satu inovasi terbesar adalah penggunaan Large Language Models (LLM) yang didukung oleh arsitektur Transformer.
Transformer memungkinkan pemrosesan bahasa alami secara parallel dengan mekanisme Self-Attention.

Untuk memanfaatkan pengetahuan spesifik enterprise, sistem Retrieval-Augmented Generation (RAG) diperkenalkan.
RAG mengombinasikan kekuatan pencarian dokumen berbasis Vector Database dengan kemampuan pemahaman teks dari LLM.
Dengan RAG, LLM dapat menjawab pertanyaan berdasarkan dokumen internal tanpa perlu melakukan fine-tuning ulang yang mahal.

Embeddings memainkan peran krusial dalam RAG. Dokumen panjang pertama-tama dipotong menjadi potongan kecil (chunks).
Setiap chunk diubah menjadi vektor numerik kontinu menggunakan model embedding seperti OpenAI text-embedding-3.
Saat pengguna mengajukan pertanyaan, query di-embed dan dicocokkan dengan chunk terdekat menggunakan Cosine Similarity.
"""

def chunk_text_fixed_size(text: str, chunk_size: int = 200, overlap: int = 40):
    """Fixed-size character chunking dengan overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += (chunk_size - overlap)
    return chunks

def chunk_text_by_sentence(text: str):
    """Sentence-based chunking."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s for s in sentences if s]

def mock_embed_text(text: str, dim: int = 16) -> np.ndarray:
    """Deterministic embedding mock."""
    seed = sum(ord(c) for c in text[:30])
    np.random.seed(seed)
    vec = np.random.uniform(-1, 1, size=dim)
    return vec / np.linalg.norm(vec)

def main():
    print("=" * 70)
    print("📦 DEMO: DOCUMENT CHUNKING & VECTOR EMBEDDING PIPELINE")
    print("=" * 70)

    print("\n1. Fixed-Size Chunking Strategy (Size=200, Overlap=40):")
    chunks = chunk_text_fixed_size(LONG_TEXT)
    for i, ch in enumerate(chunks, 1):
        print(f"\n   [Chunk #{i}] ({len(ch)} chars):")
        print(f"   \"{ch[:90]}...\"")

    print(f"\n2. Meng-generate Vector Index ({len(chunks)} chunks)...")
    vector_index = []
    for i, ch in enumerate(chunks):
        v = mock_embed_text(ch)
        vector_index.append({"id": i+1, "chunk": ch, "vector": v})

    # Search Simulation
    query = "Bagaimana cara kerja RAG dengan Vector Database?"
    q_vec = mock_embed_text(query)

    print(f"\n3. Pencarian Query User: \"{query}\"")
    scores = []
    for item in vector_index:
        sim = float(np.dot(q_vec, item["vector"]))
        scores.append((item, sim))
    
    scores.sort(key=lambda x: x[1], reverse=True)

    print("\n   🏆 Top 2 Chunks Terdekat:")
    for item, sim in scores[:2]:
        print(f"   • Chunk #{item['id']} (Score: {sim:.4f}):")
        print(f"     \"{item['chunk'][:100]}...\"")

    print("=" * 70)

if __name__ == "__main__":
    main()
