#!/usr/bin/env python3
"""
01_openai_embeddings_api.py
Modul untuk mendemonstrasikan penggunaan OpenAI Embeddings API (text-embedding-3-small/large)
serta pemotongan dimensi vektor (Matryoshka Embeddings).

Roadmap: https://roadmap.sh/ai-engineer
"""

import os
import sys
import math
import random

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

def cosine_similarity(v1, v2):
    """Menghitung cosine similarity antara dua vektor."""
    if HAS_NUMPY:
        dot = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        return float(dot / (norm1 * norm2))
    else:
        dot = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        return float(dot / (norm1 * norm2))

def mock_openai_embedding(text: str, dimensions: int = 1536) -> list:
    """Simulasi generator vektor embedding OpenAI dengan Matryoshka scaling."""
    seed_val = abs(hash(text)) % (2**32)
    random.seed(seed_val)
    raw_vec = [random.gauss(0, 1) for _ in range(1536)]
    norm1 = math.sqrt(sum(x*x for x in raw_vec))
    base_vec = [x / norm1 for x in raw_vec]
    
    truncated = base_vec[:dimensions]
    norm2 = math.sqrt(sum(x*x for x in truncated))
    truncated = [x / norm2 for x in truncated]
    return truncated

def run_openai_embeddings_demo():
    print("=" * 70)
    print("      OPENAI EMBEDDINGS API & MATRYOSHKA DIMENSION TRUNCATION")
    print("=" * 70)
    
    api_key = os.environ.get("OPENAI_API_KEY")
    using_mock = False
    
    sample_texts = [
        "Pembelajaran Mesin dan Kecerdasan Buatan dalam AI Engineering",
        "Machine Learning and Artificial Intelligence concepts",
        "Resep memasak nasi goreng spesial pedas manis"
    ]
    
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            print("🔑 API Key terdeteksi. Menggunakan OpenAI API langsung...")
            
            res_1536 = client.embeddings.create(
                model="text-embedding-3-small",
                input=sample_texts[0]
            )
            vec_1536 = res_1536.data[0].embedding
            
            res_512 = client.embeddings.create(
                model="text-embedding-3-small",
                input=sample_texts[0],
                dimensions=512
            )
            vec_512 = res_512.data[0].embedding
            
            vecs_all = []
            for t in sample_texts:
                r = client.embeddings.create(model="text-embedding-3-small", input=t, dimensions=512)
                vecs_all.append(r.data[0].embedding)
                
        except Exception as e:
            print(f"⚠️ Error saat memanggil OpenAI API ({e}). Mengalihkan ke mode simulasi.")
            using_mock = True
    else:
        print("ℹ️ OPENAI_API_KEY tidak ditemukan. Menggunakan mode simulasi (Mocking).")
        using_mock = True
        
    if using_mock:
        vec_1536 = mock_openai_embedding(sample_texts[0], dimensions=1536)
        vec_512 = mock_openai_embedding(sample_texts[0], dimensions=512)
        vecs_all = [mock_openai_embedding(t, dimensions=512) for t in sample_texts]
        
    print("\n1. Inspection Dimensi Vektor:")
    print(f"   • Standard Dimension (text-embedding-3-small) : {len(vec_1536)} float elements")
    print(f"   • Truncated Dimension (dimensions=512)      : {len(vec_512)} float elements")
    print(f"   • Sample Vector Head (5 dimensi pertama)    : {[round(x, 4) for x in vec_512[:5]]}")
    
    print("\n2. Evaluasi Cosine Similarity Antar Teks (Dimensi 512):")
    sim_0_1 = cosine_similarity(vecs_all[0], vecs_all[1])
    sim_0_2 = cosine_similarity(vecs_all[0], vecs_all[2])
    
    print(f"   • Teks 1: '{sample_texts[0]}'")
    print(f"   • Teks 2: '{sample_texts[1]}'")
    print(f"   • Teks 3: '{sample_texts[2]}'")
    print("-" * 50)
    print(f"   ► Similarity (Teks 1 <-> Teks 2 - Semantik Serupa) : {sim_0_1:.4f}")
    print(f"   ► Similarity (Teks 1 <-> Teks 3 - Topik Berbeda)   : {sim_0_2:.4f}")
    
    print("\n💡 Key Takeaway AI Engineer:")
    print("   OpenAI `text-embedding-3-small` memungkinkan pemotongan dimensi dari 1536 ke 512")
    print("   tanpa kehilangan performa signifikan, menghemat penyimpanan Vector DB hingga 66%!\n")

if __name__ == "__main__":
    run_openai_embeddings_demo()
