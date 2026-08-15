#!/usr/bin/env python3
"""
02_gemini_embedding_api.py
Modul untuk mendemonstrasikan Google Gemini Embeddings API (text-embedding-004)
dan penyesuaian tipe tugas (Task-Aware Embeddings).

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

def mock_gemini_embedding(text: str, task_type: str = "SEMANTIC_SIMILARITY", dimensions: int = 768) -> list:
    """Simulasi generator vektor embedding Google Gemini."""
    seed_val = abs(hash(f"{text}_{task_type}")) % (2**32)
    random.seed(seed_val)
    raw_vec = [random.gauss(0, 1) for _ in range(dimensions)]
    norm = math.sqrt(sum(x*x for x in raw_vec))
    return [x / norm for x in raw_vec]

def run_gemini_embedding_demo():
    print("=" * 70)
    print("       GOOGLE GEMINI EMBEDDINGS API & TASK-AWARE ENCODING")
    print("=" * 70)
    
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    using_mock = False
    
    doc_text = "Google Gemini menyediakan arsitektur multimodal dan context window hingga 2 juta token."
    query_text = "Berapa kapasitas konteks maksimal model Gemini?"
    unrelated_text = "Jadwal pertandingan sepak bola Liga Champions malam ini."
    
    task_types = ["RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY", "SEMANTIC_SIMILARITY", "CLASSIFICATION"]
    
    if api_key:
        try:
            from google import genai
            from google.genai import types
            client = genai.Client(api_key=api_key)
            print("🔑 API Key terdeteksi. Menggunakan Google GenAI SDK...")
            
            res_doc = client.models.embed_content(
                model="text-embedding-004",
                contents=doc_text,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT", title="Gemini Specs")
            )
            vec_doc = res_doc.embedding.values
            
            res_query = client.models.embed_content(
                model="text-embedding-004",
                contents=query_text,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
            )
            vec_query = res_query.embedding.values
            
            res_unrelated = client.models.embed_content(
                model="text-embedding-004",
                contents=unrelated_text,
                config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY")
            )
            vec_unrelated = res_unrelated.embedding.values
            
        except Exception as e:
            print(f"⚠️ Error saat memanggil Gemini API ({e}). Mengalihkan ke mode simulasi.")
            using_mock = True
    else:
        print("ℹ️ GEMINI_API_KEY tidak ditemukan. Menggunakan mode simulasi (Mocking).")
        using_mock = True
        
    if using_mock:
        vec_doc = mock_gemini_embedding(doc_text, task_type="RETRIEVAL_DOCUMENT")
        vec_query = mock_gemini_embedding(query_text, task_type="RETRIEVAL_QUERY")
        vec_unrelated = mock_gemini_embedding(unrelated_text, task_type="RETRIEVAL_QUERY")
        
    print("\n1. Visualisasi Task Types Google Gemini:")
    for t_type in task_types:
        sample_v = mock_gemini_embedding(doc_text, task_type=t_type)
        print(f"   • Task Type: {t_type:<22} -> Dimensi: {len(sample_v)} | Sample Head: {[round(x, 3) for x in sample_v[:3]]}")
        
    print("\n2. Evaluasi Retrieval Matching (Document vs Query):")
    print(f"   • Document : '{doc_text}'")
    print(f"   • User Query: '{query_text}'")
    print(f"   • Unrelated  : '{unrelated_text}'")
    print("-" * 50)
    
    sim_match = cosine_similarity(vec_doc, vec_query)
    sim_unrelated = cosine_similarity(vec_doc, vec_unrelated)
    
    print(f"   ► Similarity (Doc vs Query Matching)   : {sim_match:.4f}")
    print(f"   ► Similarity (Doc vs Unrelated Query)  : {sim_unrelated:.4f}")
    
    print("\n💡 Key Takeaway AI Engineer:")
    print("   Google Gemini `text-embedding-004` mengoptimalkan vektor berdasarkan `task_type`.")
    print("   Menggunakan `RETRIEVAL_DOCUMENT` untuk dokumen DB dan `RETRIEVAL_QUERY` untuk query user")
    print("   meningkatkan akurasi RAG retrieval secara signifikan.\n")

if __name__ == "__main__":
    run_gemini_embedding_demo()
