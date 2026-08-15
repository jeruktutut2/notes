#!/usr/bin/env python3
"""
Modul 4.1: Attention Mechanism & Transformer Variants (MHA, MQA, GQA)
Simulasi matematika Scaled Dot-Product Attention dan perbandingan arsitektur MHA vs MQA vs GQA.
"""

import math
from typing import List, Tuple

def softmax(scores: List[float]) -> List[float]:
    exp_scores = [math.exp(s) for s in scores]
    sum_exp = sum(exp_scores)
    return [e / sum_exp for e in exp_scores]

def calculate_scaled_dot_product_attention():
    print("\n" + "="*70)
    print(" 1. SIMULASI MATEMATIKA SCALED DOT-PRODUCT ATTENTION")
    print("="*70)
    print("Rumus Attention: Attention(Q, K, V) = softmax( (Q * K^T) / sqrt(d_k) ) * V\n")
    
    # Simple 2-token sequence example with Query and Key vectors of dimension d_k = 4
    d_k = 4
    scale = math.sqrt(d_k)
    
    # Simulated Q and K vectors for 2 tokens: "AI", "Agent"
    Q = [1.0, 0.5, -0.2, 0.8]      # Query token "Agent"
    K_tokens = [
        ("AI", [0.8, 0.6, -0.1, 0.7]),
        ("Agent", [1.0, 0.4, -0.3, 0.9])
    ]
    
    raw_scores = []
    print("Perhitungan Dot-Product (Q · K):")
    for name, K in K_tokens:
        dot_prod = sum(q * k for q, k in zip(Q, K))
        scaled_score = dot_prod / scale
        raw_scores.append(scaled_score)
        print(f"  • Q('Agent') · K('{name:<5}') = {dot_prod:.4f} | Scaled (/ {scale:.2f}): {scaled_score:.4f}")
    
    attn_weights = softmax(raw_scores)
    print("\nHasil Skor Attention (Softmax Weights):")
    for (name, _), w in zip(K_tokens, attn_weights):
        print(f"  • Attention Weight ke '{name:<5}': \033[92m{w*100:.1f}%\033[0m")
    print()


def compare_attention_variants():
    print("="*70)
    print(" 2. PERBANDINGAN ARSITEKTUR: MHA vs MQA vs GQA")
    print("="*70)
    
    variants = [
        ("Multi-Head Attention (MHA)", "GPT-3, Original Transformer", "Setiap Head memiliki Key & Value tersendiri.", "Memori KV-Cache paling besar (100% baseline)."),
        ("Multi-Query Attention (MQA)", "Falcon, PaLM", "Seluruh Head berbagi 1 pasang Key & Value yang sama.", "Sangat hemat KV-Cache (96% lebih hemat), namun kualitas model dapat turun."),
        ("Grouped-Query Attention (GQA)", "LLaMA-3, Mistral, Qwen-2", "Head dikelompokkan ke N grup (misal 8 Query Head per 1 KV Head).", "\033[92mStandard Industri Ideal!\033[0m Menggabungkan throughput MQA dengan kualitas MHA.")
    ]
    
    for name, models, mechanism, kv_impact in variants:
        print(f" • \033[93m{name}\033[0m")
        print(f"   Model          : {models}")
        print(f"   Mekanisme KV   : {mechanism}")
        print(f"   Dampak Memori  : {kv_impact}")
        print("-" * 65)
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 4.1: ATTENTION MECHANISM & TRANSFORMER VARIANTS")
    print("█"*70)
    
    calculate_scaled_dot_product_attention()
    compare_attention_variants()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Scaled dot-product scaling (/ sqrt(d_k)) mencegah vanishing gradient pada softmax.")
    print(" 2. GQA (Grouped-Query Attention) adalah standar arsitektur modern karena sangat menghemat VRAM.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
