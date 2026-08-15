#!/usr/bin/env python3
"""
Modul 4.2: Autoregressive Generation & Decoding Strategies
Simulasi sampling parameters (Temperature, Top-P, Top-K) dan teknik percepatan Speculative Decoding.
"""

import math
import random
from typing import List, Tuple

def simulate_sampling_parameters():
    print("\n" + "="*70)
    print(" 1. SIMULASI AUTOREGRESSIVE SAMPLING: TEMPERATURE, TOP-K, TOP-P")
    print("="*70)
    
    vocab_logits = [
        ("Agent", 4.5),
        ("Model", 3.8),
        ("System", 3.1),
        ("Kucing", 0.2),
        ("Mobil", -1.0)
    ]
    
    print("Logits Mentah Kosakata: " + ", ".join([f"'{k}': {v}" for k, v in vocab_logits]) + "\n")
    
    # 1. Effect of Temperature
    temperatures = [0.1, 0.7, 1.5]
    print("A. Pengaruh Temperature (Softmax Scaling T):\n")
    
    for T in temperatures:
        scaled_logits = [v / T for _, v in vocab_logits]
        exp_vals = [math.exp(v) for v in scaled_logits]
        sum_exp = sum(exp_vals)
        probs = [e / sum_exp for e in exp_vals]
        
        prob_str = ", ".join([f"'{vocab_logits[i][0]}': {probs[i]*100:.1f}%" for i in range(len(probs))])
        print(f"  • Temp {T:<3} -> {prob_str}")
    
    print("\n  \033[90m-> Temperature 0.1 (Greedy / Deterministic), Temp 1.5 (Kreatif / Random)\033[0m\n")

    # 2. Top-K Sampling
    print("B. Top-K Sampling (Misal K=2):")
    top_k = 2
    top_k_candidates = vocab_logits[:top_k]
    print(f"  • Hanya memilih {top_k} kandidat dengan logit tertinggi: {[c[0] for c in top_k_candidates]}\n")

    # 3. Top-P (Nucleus) Sampling
    print("C. Top-P (Nucleus) Sampling (Misal P=0.85):")
    print("  • Memilih kandidat kumulatif hingga probabilitas mencapai 85% (membuang kata berisiko/absurd).")
    print()


def simulate_speculative_decoding():
    print("="*70)
    print(" 2. SPECULATIVE DECODING (PERCEPATAN INFERENCE 2X-3X)")
    print("="*70)
    print("Speculative Decoding menggunakan Small Draft Model (e.g. 1B) untuk menembak K token cepat,")
    print("lalu diverifikasi sekaligus secara paralel oleh Large Target Model (e.g. 70B).\n")
    
    draft_tokens = ["AI", "Agent", "dapat", "memproses", "data"]
    verification_results = [True, True, True, False, False] # Large model rejects token 4
    
    print(f"Draft Model (Small 1B) Menghasilkan : {draft_tokens}")
    print("Target Model (Large 70B) Verifikasi Parallel...")
    
    accepted = []
    for tok, valid in zip(draft_tokens, verification_results):
        if valid:
            accepted.append(f"\033[92m{tok}\033[0m")
        else:
            accepted.append(f"\033[91m{tok} (REJECTED & RESAMPLED)\033[0m")
            break
            
    print(f"Hasil Eksekusi Step : {' '.join(accepted)}")
    print("\nKeuntungan: Memangkas waktu latensi eksekusi dari 5 forward pass GPU menjadi 1 forward pass saja!")
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 4.2: AUTOREGRESSIVE GENERATION & DECODING")
    print("█"*70)
    
    simulate_sampling_parameters()
    simulate_speculative_decoding()
    
    print("="*70)
    print(" Rekomendasi Parameter Agent:")
    print(" 1. Tool Call / Structured Output / Coding : Temp = 0.0 s/d 0.2 (Deterministik)")
    print(" 2. Creative Writing / Brainstorming       : Temp = 0.7 s/d 0.9, Top-P = 0.9")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
