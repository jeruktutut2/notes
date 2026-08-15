#!/usr/bin/env python3
"""
03_jina_embeddings.py
Modul untuk mendemonstrasikan Jina AI Embeddings (jina-embeddings-v2-base-en / v3),
kapasitas 8,192 long-context window, dan Late Chunking.

Roadmap: https://roadmap.sh/ai-engineer
"""

import math
import random

def mock_jina_embedding(text: str, context_length: int = 8192, dimensions: int = 768) -> list:
    """Simulasi Jina AI Long-Context Embedding Generator."""
    seed_val = abs(hash(text)) % (2**32)
    random.seed(seed_val)
    raw_vec = [random.gauss(0, 1) for _ in range(dimensions)]
    norm = math.sqrt(sum(x*x for x in raw_vec))
    return [x / norm for x in raw_vec]

def run_jina_embeddings_demo():
    print("=" * 70)
    print("        JINA AI EMBEDDINGS (8K LONG-CONTEXT & LATE CHUNKING)")
    print("=" * 70)
    
    long_pdf_text = "DOKUMEN KONTRAK HUKUM AI ENTERPRISE... " + "Syarat dan Ketentuan Layanan AI. " * 300
    short_query = "Apakah kontrak mencakup SLA layanan 99.9%?"
    
    model_name = "jina-embeddings-v2-base-en"
    
    vec_long_doc = mock_jina_embedding(long_pdf_text)
    vec_query = mock_jina_embedding(short_query)
    
    print("\n1. Spesifikasi Model Jina Embeddings:")
    print(f"   • Model Identifier   : {model_name}")
    print(f"   • Max Context Window : 8,192 Tokens (Setara ~10-15 Halaman PDF!)")
    print(f"   • Standard Models    : 512 Tokens (Akan terpotong / Truncated!)")
    print(f"   • Vector Dimensions  : {len(vec_long_doc)}")
    
    print("\n2. Perbandingan Tradisional vs Late Chunking:")
    print("   • Standard RAG Pipeline:")
    print("     [Dokumen 8k] --Chunk 512--> [Chunk 1, Chunk 2...] --Embed--> [Vector 1, Vector 2]")
    print("     ❌ Kelemahan: Terjadi Boundary Loss (konteks antar paragraf terputus).")
    print("\n   • Jina Late Chunking Pipeline:")
    print("     [Dokumen 8k] --Full Encoder (8k)--> [Full Token States] --Mean Pool per Chunk--> [Vectors]")
    print("     ✅ Keunggulan: Setiap vektor chunk mempertahankan memori seluruh dokumen!")
    
    print("\n3. Visualisasi Vektor Dokumen Panjang:")
    print(f"   • Length Teks Dokumen : {len(long_pdf_text)} Karakter (~4,200 Token)")
    print(f"   • Vector Status       : Extracted Full without Truncation ✅")
    print(f"   • Sample Vector Head  : {[round(x, 4) for x in vec_long_doc[:4]]}")
    
    print("\n💡 Key Takeaway AI Engineer:")
    print("   Jina AI Embeddings sangat ideal untuk RAG dokumen panjang (PDF, Laporan Keuangan, Kontrak).")
    print("   Dengan 8k context window dan Late Chunking, hilangnya konteks akibat pemotongan teks terhindari.\n")

if __name__ == "__main__":
    run_jina_embeddings_demo()
