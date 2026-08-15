#!/usr/bin/env python3
"""
Modul 6.1: Standard Benchmarks & Pass@k Metrics
Penjelasan benchmark populer (MMLU, HumanEval, GSM8K) dan simulasi matematika metrik Pass@k.
"""

import math
from typing import List

def calculate_pass_at_k(n: int, c: int, k: int) -> float:
    """
    Menghitung metrik Pass@k untuk evaluasi coding (HumanEval).
    n = Total sampel percobaan generasi per problem
    c = Jumlah sampel yang lolos unit test (correct)
    k = Batas k sampel yang dievaluasi
    Rumus Unbiased: Pass@k = 1 - (comb(n-c, k) / comb(n, k))
    """
    if n - c < k:
        return 1.0
    
    # Formula perkalian kombinasi aman
    prob_fail = 1.0
    for i in range(k):
        prob_fail *= (n - c - i) / (n - i)
        
    return 1.0 - prob_fail


def demonstrate_pass_at_k():
    print("\n" + "="*70)
    print(" 1. KALKULASI METRIK PASS@K UNTUK EVALUASI AI AGENT CODING")
    print("="*70)
    print("Pass@k mengukur probabilitas minimal 1 sampel dari k percobaan lolos pengujian.\n")
    
    n_samples = 10 # Model menghasilkan 10 pilihan kode
    correct_counts = [1, 3, 5, 8]
    
    print(f"Total Sampel Dihasilkan (n) = {n_samples}\n")
    print(f"{'Jumlah Sampel Benar (c)':<25} | {'Pass@1':<12} | {'Pass@3':<12} | {'Pass@5':<12}")
    print("-" * 65)
    
    for c in correct_counts:
        p1 = calculate_pass_at_k(n_samples, c, k=1)
        p3 = calculate_pass_at_k(n_samples, c, k=3)
        p5 = calculate_pass_at_k(n_samples, c, k=5)
        print(f"{c:>3} dari {n_samples} kode benar           | {p1*100:>10.1f}% | {p3*100:>10.1f}% | {p5*100:>10.1f}%")
    print()


def overview_standard_benchmarks():
    print("="*70)
    print(" 2. DOKUMEN BENCHMARK STANDAR INDUSTRI LLM")
    print("="*70)
    
    benchmarks = [
        ("MMLU (Massive Multitask Language Understanding)", "Pengetahuan Umum / Akademik", "Multiple-choice 57 subjek (Hukum, Kedokteran, Sejarah)."),
        ("HumanEval / MBPP", "Kemampuan Pemrograman (Coding)", "Masalah pemrograman Python dengan Unit Test otomatis (Pass@1)."),
        ("GSM8K / MATH", "Penalaran Matematika & Logic", "Soal cerita matematika sekolah dasar hingga olimpiade."),
        ("GPQA (Google-Proof Q&A)", "Penalaran Tingkat Tinggi (PhD Level)", "Pertanyaan sains sangat sulit yang tidak bisa dicari instan di Google.")
    ]
    
    for name, domain, desc in benchmarks:
        print(f" • \033[93m{name}\033[0m")
        print(f"   Fokus : {domain}")
        print(f"   Detail: {desc}")
        print("-" * 65)
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 6.1: STANDARD BENCHMARKS & PASS@K METRICS")
    print("█"*70)
    
    demonstrate_pass_at_k()
    overview_standard_benchmarks()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Pass@1 mengukur efisiensi eksekusi pertama, sedangkan Pass@k mengukur batas potensi model.")
    print(" 2. Jangan percaya skor benchmark sintetis tunggal; selalu lakukan evaluasi kustom pada dataset Agent Anda.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
