#!/usr/bin/env python3
"""
Modul 02: Hyperparameters & Configuration Simulator
Mensimulasikan eksperimen parameter sampling (Temperature, Top-P, Max Tokens, Stop Sequences, Penalties).
"""

import math
import random

def softmax(logits, temperature=1.0):
    """Menghitung probabilitas Softmax dengan penyesuaian Temperature."""
    if temperature == 0.0:
        # Greedy selection
        max_idx = logits.index(max(logits))
        return [1.0 if i == max_idx else 0.0 for i in range(len(logits))]
    
    scaled_logits = [l / temperature for l in logits]
    max_l = max(scaled_logits)
    exp_logits = [math.exp(l - max_l) for l in scaled_logits]
    sum_exp = sum(exp_logits)
    return [e / sum_exp for e in exp_logits]

def apply_top_p(tokens, probs, top_p=0.9):
    """Menyaring token berdasarkan kumulatif probabilitas Nucleus Sampling (Top-P)."""
    sorted_pairs = sorted(zip(tokens, probs), key=lambda x: x[1], reverse=True)
    cum_sum = 0.0
    filtered = []
    for token, prob in sorted_pairs:
        filtered.append((token, prob))
        cum_sum += prob
        if cum_sum >= top_p:
            break
    return filtered

def run_hyperparameter_simulation():
    print("🎛️  LLM CONFIGURATION & SAMPLING SIMULATOR")
    print("=" * 60)
    
    vocabulary = ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "PHP", "Ruby"]
    raw_logits = [4.5,      3.8,          3.2,    2.9,   2.7,  2.5,   1.1,   0.8]
    
    temperatures = [0.0, 0.2, 0.7, 1.5]
    
    print("\n1. EFEK TEMPERATURE PADA DISTRIBUSI PROBABILITAS:")
    print("-" * 60)
    print(f"{'Token':<12} | " + " | ".join([f"T={t:<4}" for t in temperatures]))
    print("-" * 60)
    
    prob_matrix = [softmax(raw_logits, temp) for temp in temperatures]
    
    for i, token in enumerate(vocabulary):
        row_str = f"{token:<12} | "
        row_str += " | ".join([f"{prob_matrix[t_idx][i]*100:5.1f}%" for t_idx in range(len(temperatures))])
        print(row_str)
    print("-" * 60)
    
    print("\n2. EFEK TOP-P (NUCLEUS SAMPLING) PADA T=0.7:")
    print("-" * 60)
    probs_t07 = softmax(raw_logits, temperature=0.7)
    
    for p_val in [0.5, 0.85, 0.98]:
        filtered = apply_top_p(vocabulary, probs_t07, top_p=p_val)
        tokens_kept = [item[0] for item in filtered]
        print(f"Top-P = {p_val:<4} -> Token Tersisa ({len(tokens_kept)}): {', '.join(tokens_kept)}")
    
    print("=" * 60)

if __name__ == "__main__":
    run_hyperparameter_simulation()
