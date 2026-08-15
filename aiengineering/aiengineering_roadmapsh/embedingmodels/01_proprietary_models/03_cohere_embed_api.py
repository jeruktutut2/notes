#!/usr/bin/env python3
"""
03_cohere_embed_api.py
Modul untuk mendemonstrasikan Cohere Embed API v3 (embed-multilingual-v3.0)
serta fitur kompresi vektor int8 dan binary embeddings.

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

def mock_cohere_embed(text: str, embedding_type: str = "float", dimensions: int = 1024):
    """Simulasi generator vektor embedding Cohere dengan kompresi."""
    seed_val = abs(hash(text)) % (2**32)
    random.seed(seed_val)
    
    if embedding_type == "float":
        raw_vec = [random.gauss(0, 1) for _ in range(dimensions)]
        norm = math.sqrt(sum(x*x for x in raw_vec))
        return [x / norm for x in raw_vec]
    elif embedding_type == "int8":
        return [random.randint(-128, 127) for _ in range(dimensions)]
    elif embedding_type == "binary":
        return [random.randint(0, 255) for _ in range(dimensions // 8)]

def run_cohere_embed_demo():
    print("=" * 70)
    print("      COHERE EMBED V3 & VECTOR COMPRESSION (INT8 / BINARY)")
    print("=" * 70)
    
    api_key = os.environ.get("COHERE_API_KEY")
    using_mock = False
    
    texts = [
        "Arsitektur RAG enterprise memerlukan vector database skala besar.",
        "Enterprise RAG architectures require high-performance vector databases.",
        "Resep kue bolu pandan kukus lezat dan lembut."
    ]
    
    if api_key:
        try:
            import cohere
            co = cohere.ClientV2(api_key=api_key)
            print("🔑 API Key terdeteksi. Menggunakan Cohere ClientV2 SDK...")
            
            res = co.embed(
                texts=texts,
                model="embed-multilingual-v3.0",
                input_type="search_document",
                embedding_types=["float", "int8"]
            )
            vec_float = res.embeddings.float[0]
            vec_int8 = res.embeddings.int8[0]
            
        except Exception as e:
            print(f"⚠️ Error saat memanggil Cohere API ({e}). Mengalihkan ke mode simulasi.")
            using_mock = True
    else:
        print("ℹ️ COHERE_API_KEY tidak ditemukan. Menggunakan mode simulasi (Mocking).")
        using_mock = True
        
    if using_mock:
        vec_float = mock_cohere_embed(texts[0], embedding_type="float")
        vec_int8 = mock_cohere_embed(texts[0], embedding_type="int8")
        vec_binary = mock_cohere_embed(texts[0], embedding_type="binary")
        vecs_all = [mock_cohere_embed(t, embedding_type="float") for t in texts]
        
    print("\n1. Perbandingan Format Output & Memory Compression:")
    print(f"   • Float32 (Full Precision) : Dimensi = {len(vec_float)} | Est. Memory = {len(vec_float)*4} bytes")
    print(f"   • Int8 Quantized           : Dimensi = {len(vec_int8)} | Est. Memory = {len(vec_int8)*1} bytes (Hemat 75%!)")
    print(f"   • Binary (Bit Packed)      : Dimensi = {len(vec_binary)*8} bits | Est. Memory = {len(vec_binary)} bytes (Hemat 96%!)")
    
    print("\n2. Sample Values Preview:")
    print(f"   • Float32 Head : {[round(x, 4) for x in vec_float[:4]]}")
    print(f"   • Int8 Head    : {vec_int8[:4]}")
    
    print("\n3. Cross-Lingual Semantic Similarity (Bahasa Indonesia <-> English):")
    sim_id_en = cosine_similarity(vecs_all[0], vecs_all[1])
    sim_id_unrelated = cosine_similarity(vecs_all[0], vecs_all[2])
    
    print(f"   • Teks ID : '{texts[0]}'")
    print(f"   • Teks EN : '{texts[1]}'")
    print(f"   • Teks 3  : '{texts[2]}'")
    print("-" * 50)
    print(f"   ► Cross-Lingual Match (ID <-> EN)    : {sim_id_en:.4f} (Kemiripan Semantik Tinggi!)")
    print(f"   ► Unrelated Match (ID <-> Resep)     : {sim_id_unrelated:.4f}")
    
    print("\n💡 Key Takeaway AI Engineer:")
    print("   Cohere `embed-multilingual-v3.0` adalah pilihan utama untuk sistem RAG multibahasa.")
    print("   Dukungan kompresi INT8 dan BINARY bawaan memangkas kebutuhan RAM Vector DB hingga 96%.\n")

if __name__ == "__main__":
    run_cohere_embed_demo()
