#!/usr/bin/env python3
"""
01_sentence_transformers.py
Modul untuk mendemonstrasikan penggunaan library `sentence-transformers` secara lokal
untuk ekstraksi embedding, batch processing, dan similarity calculation.

Roadmap: https://roadmap.sh/ai-engineer
"""

import time
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

def mock_sentence_transformer_encode(sentences, dimensions=384):
    """Fallback generator jika library sentence-transformers tidak terinstall."""
    embeddings = []
    for s in sentences:
        seed_val = abs(hash(s)) % (2**32)
        random.seed(seed_val)
        raw_vec = [random.gauss(0, 1) for _ in range(dimensions)]
        norm = math.sqrt(sum(x*x for x in raw_vec))
        vec = [x / norm for x in raw_vec]
        embeddings.append(vec)
    return embeddings

def run_sentence_transformers_demo():
    print("=" * 70)
    print("        SENTENCE TRANSFORMERS LOKAL (ALL-MINILM-L6-V2)")
    print("=" * 70)
    
    sentences = [
        "Vector embeddings mengonversi teks menjadi representasi numerik dense.",
        "Embeddings convert text into dense numeric vector representations.",
        "Mobil balap Formula 1 memiliki kecepatan lebih dari 300 km/jam."
    ]
    
    model_name = "all-MiniLM-L6-v2"
    using_st = False
    
    try:
        from sentence_transformers import SentenceTransformer, util
        print(f"📦 Loading SentenceTransformer model: '{model_name}'...")
        start_load = time.time()
        model = SentenceTransformer(model_name)
        load_time = round(time.time() - start_load, 2)
        print(f"✅ Model loaded dalam {load_time} detik!")
        
        start_enc = time.time()
        embeddings = model.encode(sentences, convert_to_tensor=False)
        enc_time = round(time.time() - start_enc, 4)
        using_st = True
        
    except Exception as e:
        print(f"ℹ️ `sentence-transformers` tidak aktif atau mengunduh model: {e}")
        print("   Menggunakan mode simulasi lokal PyTorch/NumPy...")
        embeddings = mock_sentence_transformer_encode(sentences, dimensions=384)
        enc_time = 0.002
        
    print("\n1. Metadata & Vector Inspection:")
    print(f"   • Model Name     : {model_name}")
    print(f"   • Batch Count    : {len(sentences)} kalimat")
    dim_count = len(embeddings[0]) if isinstance(embeddings, list) else embeddings.shape[1]
    print(f"   • Vector Shape   : ({len(sentences)}, {dim_count}) ({dim_count} dimensi per kalimat)")
    print(f"   • Execution Time : {enc_time}s")
    sample_head = embeddings[0][:4] if isinstance(embeddings, list) else embeddings[0][:4].tolist()
    print(f"   • Sample Values  : {[round(x, 4) for x in sample_head]}")
    
    print("\n2. Cosine Similarity Matrix:")
    sim_0_1 = cosine_similarity(embeddings[0], embeddings[1])
    sim_0_2 = cosine_similarity(embeddings[0], embeddings[2])
    
    print(f"   • Kalimat 1 : '{sentences[0]}'")
    print(f"   • Kalimat 2 : '{sentences[1]}'")
    print(f"   • Kalimat 3 : '{sentences[2]}'")
    print("-" * 50)
    print(f"   ► Sim (Kalimat 1 <-> Kalimat 2 - Sinonim Semantic) : {sim_0_1:.4f}")
    print(f"   ► Sim (Kalimat 1 <-> Kalimat 3 - Berbeda Topik)    : {sim_0_2:.4f}")
    
    print("\n💡 Key Takeaway AI Engineer:")
    print("   `sentence-transformers` adalah pilihan open-source paling populer untuk eksekusi lokal.")
    print("   Model `all-MiniLM-L6-v2` hanya membutuhkan ~90MB RAM dan dapat berjalan sangat cepat di CPU.\n")

if __name__ == "__main__":
    run_sentence_transformers_demo()
