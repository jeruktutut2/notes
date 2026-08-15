#!/usr/bin/env python3
"""
01_model_comparison_benchmark.py
Benchmark runner interaktif untuk membandingkan Proprietary Models vs Open Source Models
berdasarkan dimensi, latensi, MTEB score, context length, dan biaya per 1M token.

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

MODELS_METADATA = [
    # Proprietary Models
    {
        "name": "OpenAI text-embedding-3-small",
        "category": "Proprietary",
        "provider": "OpenAI API",
        "dimensions": 1536,
        "context_window": 8191,
        "cost_per_1m": "$0.02",
        "mteb_score": 62.3,
        "latency_ms": 45,
        "deploy_type": "Cloud API"
    },
    {
        "name": "Google Gemini text-embedding-004",
        "category": "Proprietary",
        "provider": "Google GenAI API",
        "dimensions": 768,
        "context_window": 2048,
        "cost_per_1m": "$0.025",
        "mteb_score": 63.8,
        "latency_ms": 52,
        "deploy_type": "Cloud API"
    },
    {
        "name": "Cohere embed-multilingual-v3.0",
        "category": "Proprietary",
        "provider": "Cohere API",
        "dimensions": 1024,
        "context_window": 512,
        "cost_per_1m": "$0.10",
        "mteb_score": 64.1,
        "latency_ms": 60,
        "deploy_type": "Cloud API / VPC"
    },
    
    # Open Source Models
    {
        "name": "Sentence-Transformers all-MiniLM-L6-v2",
        "category": "Open Source",
        "provider": "UKPLab (Local)",
        "dimensions": 384,
        "context_window": 256,
        "cost_per_1m": "$0.00 (Self-Host)",
        "mteb_score": 56.3,
        "latency_ms": 4,
        "deploy_type": "CPU / Local"
    },
    {
        "name": "Hugging Face BAAI/bge-small-en-v1.5",
        "category": "Open Source",
        "provider": "BAAI (Hugging Face)",
        "dimensions": 384,
        "context_window": 512,
        "cost_per_1m": "$0.00 (Self-Host)",
        "mteb_score": 62.1,
        "latency_ms": 8,
        "deploy_type": "Local / GPU Server"
    },
    {
        "name": "Jina AI jina-embeddings-v2-base-en",
        "category": "Open Source",
        "provider": "Jina AI",
        "dimensions": 768,
        "context_window": 8192,
        "cost_per_1m": "$0.00 (Self-Host)",
        "mteb_score": 60.4,
        "latency_ms": 18,
        "deploy_type": "Docker / Local"
    }
]

def run_model_comparison_benchmark():
    print("=" * 90)
    print("        COMPREHENSIVE EMBEDDING MODEL BENCHMARK & SELECTION MATRIX")
    print("=" * 90)
    
    sample_text = "Optimasi pencarian semantik menggunakan Vector Database dan Embedding Models."
    print(f"\n📝 Sample Test Query: '{sample_text}'\n")
    
    # Render Output Table Header
    header = f"{'Model Name':<38} | {'Category':<12} | {'Dim':<5} | {'Context':<8} | {'MTEB':<5} | {'Cost/1M':<15}"
    print(header)
    print("-" * len(header))
    
    for m in MODELS_METADATA:
        row = f"{m['name']:<38} | {m['category']:<12} | {m['dimensions']:<5} | {m['context_window']:<8} | {m['mteb_score']:<5} | {m['cost_per_1m']:<15}"
        print(row)
        
    print("-" * len(header))
    
    print("\n⚡ Simulasi Latensi Eksekusi (1,000 Documents Batch Inference):")
    print("-------------------------------------------------------------------------")
    for m in MODELS_METADATA:
        # 1000 docs batch estimate
        batch_lat = (m['latency_ms'] * 1000) / (10 if m['category'] == "Open Source" else 20)
        bar = "█" * int(m['latency_ms'] / 3)
        print(f" • {m['name']:<38} : {m['latency_ms']:>3} ms/req | Batch Est: {batch_lat/1000:.2f}s  {bar}")
        
    print("\n💡 Panduan Pemilihan Berdasarkan Kasus Penggunaan (Use Cases):")
    print("   1. Private Data / On-Premise  -> BAAI/bge-small-en-v1.5 (Akurasi MTEB setara OpenAI)")
    print("   2. Long PDF / Legal Contracts  -> Jina AI jina-embeddings-v2 (8,192 Context Window)")
    print("   3. Ultra-Fast CPU Mobile/Edge  -> Sentence-Transformers all-MiniLM-L6-v2 (Latensi 4ms)")
    print("   4. Scale Fast Without Server   -> OpenAI text-embedding-3-small ($0.02 / 1M Token)")
    print("   5. Multilingual Enterprise RAG -> Cohere embed-multilingual-v3.0 (Int8 Compression)\n")

if __name__ == "__main__":
    run_model_comparison_benchmark()
