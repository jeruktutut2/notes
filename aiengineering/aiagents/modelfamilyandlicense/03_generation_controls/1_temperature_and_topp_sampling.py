#!/usr/bin/env python3
"""
Modul 3.1: Generation Controls - Temperature & Top-P (Nucleus) Sampling
Simulasi Matematis & Visualisasi Softmax Logits Scaling & Probability Truncation
Berdasarkan Gambar 1 & Roadmap.sh / AI Agents - Generation Controls
"""

import sys
import math
import random
from typing import List, Tuple, Dict

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Sample Vocabulary & Unnormalized Logits (z_i)
SAMPLE_LOGITS: Dict[str, float] = {
    "Paris": 4.5,
    "London": 3.8,
    "Berlin": 3.2,
    "Tokyo": 2.1,
    "banana": -1.2,
    "robot": -2.5,
    "xyz_123": -4.0
}

def compute_softmax(logits: Dict[str, float], temperature: float) -> Dict[str, float]:
    """
    Menghitung Softmax dengan Temperature Scaling: P(y_i) = exp(z_i / T) / sum(exp(z_j / T))
    """
    if temperature <= 0.0001:
        # T -> 0 (Greedy / Argmax)
        max_token = max(logits, key=logits.get)
        return {k: (1.0 if k == max_token else 0.0) for k in logits}
    
    # Scale logits by Temperature
    scaled_logits = {k: v / temperature for k, v in logits.items()}
    # Max trick for numerical stability
    max_scaled = max(scaled_logits.values())
    exp_logits = {k: math.exp(v - max_scaled) for k, v in scaled_logits.items()}
    sum_exp = sum(exp_logits.values())
    
    return {k: exp_v / sum_exp for k, exp_v in exp_logits.items()}

def apply_top_p_nucleus(probs: Dict[str, float], top_p: float) -> Tuple[Dict[str, float], List[str]]:
    """
    Memotong token berprobabilitas rendah sampai kumulatif sum mencapai top_p.
    Menghasilkan probabilitas ternormalisasi ulang & daftar token yang tersisa.
    """
    # Urutkan berdasarkan probabilitas descending
    sorted_items = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    
    retained = {}
    cum_sum = 0.0
    kept_tokens = []
    
    for token, prob in sorted_items:
        if cum_sum < top_p or len(kept_tokens) == 0:
            retained[token] = prob
            cum_sum += prob
            kept_tokens.append(token)
        else:
            break
            
    # Renormalisasi probabilitas token yang tersimpan
    retained_sum = sum(retained.values())
    renormalized = {k: v / retained_sum for k, v in retained.items()} if retained_sum > 0 else retained
    
    return renormalized, kept_tokens

def draw_bar_chart(probs: Dict[str, float], title: str):
    print(f"\n{BOLD}{CYAN}--- {title} ---{RESET}")
    max_bar_width = 35
    for token, prob in probs.items():
        bar_len = int(prob * max_bar_width)
        bar = "█" * bar_len
        pct = prob * 100.0
        color = GREEN if prob > 0.3 else (YELLOW if prob > 0.05 else RED)
        print(f" {token:<10} | {color}{bar:<35}{RESET} | {pct:>5.1f}%")

def run_temperature_comparison_demo():
    print(f"\n{BOLD}{HEADER}=== DEMO 1: IMPACT SUHU (TEMPERATURE) TERHADAP SOFTMAX ==={RESET}")
    print("Logits Mentah (z_i) dari LLM untuk prompt 'The capital of France is ...':")
    for tok, logit in SAMPLE_LOGITS.items():
        print(f"  - '{tok}': logit = {logit}")

    temperatures = [0.01, 0.5, 1.0, 1.8]
    for t in temperatures:
        probs = compute_softmax(SAMPLE_LOGITS, temperature=t)
        label = f"Greedy Argmax (T={t})" if t < 0.1 else f"Sampling (T={t})"
        draw_bar_chart(probs, f"Temperature T = {t} ({label})")

def run_top_p_comparison_demo():
    print(f"\n{BOLD}{HEADER}=== DEMO 2: IMPACT TOP-P (NUCLEUS SAMPLING) ==={RESET}")
    probs_t1 = compute_softmax(SAMPLE_LOGITS, temperature=1.0)
    
    print(f"Probabilitas awal (T=1.0) sebelum Nucleus Truncation:")
    draw_bar_chart(probs_t1, "Probabilitas Awal (T=1.0)")

    top_ps = [0.95, 0.70, 0.40]
    for p in top_ps:
        renorm_probs, kept = apply_top_p_nucleus(probs_t1, top_p=p)
        draw_bar_chart(renorm_probs, f"Top-P = {p} (Token Terpilih: {kept})")

def interactive_sampling_simulator():
    print(f"\n{BOLD}{HEADER}=== INTERACTIVE SAMPLING SIMULATOR ==={RESET}")
    try:
        temp = float(input("\nMasukkan nilai Temperature (misal: 0.0 s.d. 2.0): ").strip())
        top_p = float(input("Masukkan nilai Top-P (misal: 0.1 s.d. 1.0): ").strip())
        
        raw_probs = compute_softmax(SAMPLE_LOGITS, temperature=temp)
        final_probs, kept = apply_top_p_nucleus(raw_probs, top_p=top_p)
        
        draw_bar_chart(final_probs, f"Hasil Akhir (Temperature={temp}, Top-P={top_p})")
        
        # Monte-Carlo simulation 1,000 sampling steps
        tokens = list(final_probs.keys())
        weights = list(final_probs.values())
        samples = random.choices(tokens, weights=weights, k=1000)
        
        counts = {t: samples.count(t) for t in SAMPLE_LOGITS.keys()}
        
        print(f"\n{BOLD}{GREEN}--- HASIL MONTE-CARLO SIMULATION (1,000 GENERATED TOKENS) ---{RESET}")
        for t, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            pct = (count / 1000.0) * 100.0
            print(f" • Token '{t:<10}': terpilih {count:>4} kali ({pct:>5.1f}%)")
            
    except ValueError:
        print(f"{RED}Input tidak valid.{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 3.1: GENERATION CONTROLS - TEMPERATURE & TOP-P SAMPLING{RESET}")
    print(f"{CYAN}Sesuai dengan Gambar 1 (Generation Controls: Temperature, Top-p){RESET}")
    print("█" * 75)

    run_temperature_comparison_demo()
    run_top_p_comparison_demo()
    
    print("\nIngin mencoba Simulator Interaktif?")
    ans = input("Jawab (y/n): ").strip().lower()
    if ans == 'y':
        interactive_sampling_simulator()

    print(f"\n{GREEN}✔ Modul 3.1 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
