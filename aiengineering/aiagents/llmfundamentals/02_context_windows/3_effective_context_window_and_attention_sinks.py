#!/usr/bin/env python3
"""
Modul 2.3: Effective Context Window & Streaming Attention Sinks
Simulasi fenomena 'Lost in the Middle', Attention Sinks (StreamingLLM), dan Needle In A Haystack (NIAH).
"""

import random
from typing import List, Dict

def simulate_lost_in_the_middle():
    print("\n" + "="*70)
    print(" 1. FENOMENA 'LOST IN THE MIDDLE' (U-SHAPE ATTENTION DEGRADATION)")
    print("="*70)
    print("Studi membuktikan LLM sangat mengingat informasi di AWAL dan AKHIR konteks,")
    print("namun sering ALPA/LUPA pada informasi yang diletakkan di TENGAH dokumen.\n")
    
    positions = [0, 10, 25, 50, 75, 90, 100]  # Posisi fakta dalam % dokumen
    
    print(f"{'Posisi Fakta dalam Dokumen (%)':<32} | {'Visual Attention Weight':<25} | {'Akurasi Retrieval':<18}")
    print("-" * 80)
    
    for pos in positions:
        if pos <= 10:
            accuracy = 98.5
            bar = "████████████████████"
        elif pos >= 90:
            accuracy = 96.0
            bar = "███████████████████ "
        elif pos == 50:
            accuracy = 52.0  # Titik terendah (titik lembah U-shape)
            bar = "██████████          "
        else:
            accuracy = 70.0
            bar = "██████████████      "
            
        pos_str = f"Awal ({pos}%)" if pos < 20 else (f"Akhir ({pos}%)" if pos > 80 else f"Tengah ({pos}%)")
        print(f"{pos_str:<32} | {bar:<25} | \033[93m{accuracy:>5.1f}%\033[0m")
    
    print("\n\033[96mStrategi Mitigasi untuk AI Agent:\033[0m")
    print(" • Letakkan instruksi paling penting (System Prompt / Tool Guidelines) di paling atas.")
    print(" • Tempatkan query/jawaban yang diharapkan di paling bawah (paling dekat dengan token generasi).")
    print()


def simulate_attention_sinks():
    print("="*70)
    print(" 2. STREAMING ATTENTION SINKS (StreamingLLM)")
    print("="*70)
    print("Pada percakapan agent tanpa batas, jika token lama dihapus begitu saja (sliding window),")
    print("kinerja LLM runtuh total karena hilangnya 'Attention Sink' (token awal seperti <BOS>).\n")
    
    context_tokens = ["<BOS>", "System", "Prompt", "User_1", "Resp_1", "User_2", "Resp_2", "User_3", "Resp_3", "User_4"]
    
    print("Skema Memori StreamingLLM:")
    print(" [Attention Sink Tokens (4 Token Awal)] + [Sliding Window (N Token Terakhir)]\n")
    
    sinks = context_tokens[:2]      # Always keep initial tokens
    window = context_tokens[-4:]     # Keep sliding window
    
    print(f"Token Asli Lengkap : {context_tokens}")
    print(f"Token Dipertahankan: \033[92m{sinks}\033[0m (Attention Sinks) + \033[94m{window}\033[0m (Sliding Window)")
    print("\nHasil: Model mempertahankan kemampuan generasi stabil tanpa crash perplexity!")
    print()


def demonstrate_niah_benchmark_matrix():
    print("="*70)
    print(" 3. NEEDLE IN A HAYSTACK (NIAH) BENCHMARK MATRIX SIMULATOR")
    print("="*70)
    print("Menguji kemampuan LLM menemukan satu kalimat kunci ('Needle') di dalam teks raksasa ('Haystack').\n")
    
    doc_lengths = [4000, 16000, 32000, 64000, 128000]
    depth_percents = [10, 30, 50, 70, 90]
    
    print(f"{'Panjang Dokumen':<18} | " + " | ".join([f"Kedalaman {d}%" for d in depth_percents]))
    print("-" * 80)
    
    for length in doc_lengths:
        row = [f"{length//1000:>3}k Tokens      "]
        for depth in depth_percents:
            # Degrade score slightly at higher length & middle depth
            if length > 32000 and depth in [50, 70]:
                score = random.choice(["\033[91m 65% \033[0m", "\033[93m 78% \033[0m"])
            else:
                score = "\033[92m100% \033[0m"
            row.append(score)
        print(" | ".join(row))
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 2.3: EFFECTIVE CONTEXT WINDOW & ATTENTION SINKS")
    print("█"*70)
    
    simulate_lost_in_the_middle()
    simulate_attention_sinks()
    demonstrate_niah_benchmark_matrix()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Selalu waspadai efek Lost-in-the-Middle saat menyusun prompt RAG.")
    print(" 2. Gunakan teknik Attention Sinks untuk eksekusi agent yang membutuhkan percakapan continuous.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
