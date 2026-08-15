#!/usr/bin/env python3
"""
MODUL 2: Context Compression & Pruning
Skrip 3: Needle In A Haystack (NIAH) Benchmark Simulator

Mendemonstrasikan:
1. Pembuatan Haystack Synthesizer (teks bertema acak berukuran ribuan token).
2. Penyisipan "Needle" (fakta tersembunyi) pada berbagai variasi kedalaman (0% - 100%).
3. Evaluasi Ketepatan Retrieval In-Context (Heatmap Data Matrix Simulation).
"""

import random
from typing import List, Dict, Tuple

class NeedleInHaystackSimulator:
    """Simulator Benchmark NIAH untuk menguji ketahanan retrieval LLM."""

    # Paragraf pengisi (haystack)
    FILLER_PARAGRAPHS = [
        "Pemrosesan data terdistribusi menggunakan Apache Spark memfasilitasi analisis komputasi skala besar secara efisien di kluster server.",
        "Protokol komunikasi HTTPS memanfaatkan enkripsi TLS untuk mengamankan pertukaran data antara web browser dan web server.",
        "Struktur data Binary Search Tree memberikan performa pencarian rata-rata O(log N) dalam skenario terbaik.",
        "Prinsip desain Microservices memisahkan aplikasi monolitik menjadi layanan-layanan kecil yang independen dan terisolasi.",
        "Penggunaan indeks B-Tree pada database relasional mempercepat eksekusi kueri SELECT pada kolom berukuran besar."
    ]

    def __init__(self, needle: str, secret_answer: str):
        self.needle = needle
        self.secret_answer = secret_answer

    def generate_haystack(self, target_word_count: int, depth_percent: float) -> Tuple[str, int]:
        """
        Menghasilkan haystack sepanjang `target_word_count` kata,
        dan menyisipkan needle pada `depth_percent` (0% awal, 100% akhir).
        """
        paragraphs = []
        current_words = 0

        # Buat daftar paragraf pengisi
        while current_words < target_word_count:
            p = random.choice(self.FILLER_PARAGRAPHS)
            paragraphs.append(p)
            current_words += len(p.split())

        # Hitung posisi indeks penyisipan needle
        insertion_idx = int((depth_percent / 100.0) * len(paragraphs))
        insertion_idx = max(0, min(len(paragraphs), insertion_idx))

        paragraphs.insert(insertion_idx, f"*** [NEEDLE]: {self.needle} ***")
        
        final_text = "\n\n".join(paragraphs)
        actual_words = len(final_text.split())

        return final_text, actual_words

    def evaluate_retrieval_sim(self, depth_percent: float, total_words: int) -> bool:
        """
        Menyimulasikan apakah LLM berhasil menemukan jawaban berdasarkan kedalaman dan ukuran context.
        Akurasi turun di tengah-tengah (Lost in the middle) dan pada context yang sangat besar.
        """
        # Base probability
        base_prob = 0.98

        # Penalty untuk context berukuran besar (> 500 kata)
        length_penalty = min(0.40, (total_words / 2000.0) * 0.3)

        # U-Shape penalty (kedalaman 30%-70% paling rentan gagal)
        if 20.0 <= depth_percent <= 80.0:
            depth_penalty = 0.35 * (1.0 - abs(depth_percent - 50.0) / 30.0)
        else:
            depth_penalty = 0.05

        success_prob = max(0.10, base_prob - length_penalty - depth_penalty)
        return random.random() < success_prob

def demo():
    print("=" * 70)
    print("DEMO 3: NEEDLE IN A HAYSTACK (NIAH) BENCHMARK SIMULATOR")
    print("=" * 70)

    needle_fact = "Warna rahasia dari server produksi nomor 42 adalah KUNING VIOLET."
    secret_answer = "KUNING VIOLET"

    simulator = NeedleInHaystackSimulator(needle=needle_fact, secret_answer=secret_answer)

    print(f"FACT NEEDLE    : '{needle_fact}'")
    print(f"TARGET ANSWER  : '{secret_answer}'\n")

    # Grid Pengujian NIAH: Context Length vs Depth Percent
    context_lengths = [300, 600, 1200]
    depths = [0.0, 25.0, 50.0, 75.0, 100.0]

    print("--- BENCHMARK HEATMAP MATRIX SIMULATION (NIAH) ---")
    header = f"{'Context Size':<15} | " + " | ".join([f"Depth {d:4.0f}%" for d in depths])
    print(header)
    print("-" * len(header))

    random.seed(42) # Deterministic for clean demo presentation

    for length in context_lengths:
        row_str = f"{length:<11} kata | "
        results = []
        for depth in depths:
            _, actual_words = simulator.generate_haystack(length, depth)
            success = simulator.evaluate_retrieval_sim(depth, actual_words)
            symbol = "  ✅ PASS " if success else "  ❌ FAIL "
            results.append(symbol)
        print(row_str + " | ".join(results))

    print("\nCatatan Analisis NIAH:")
    print("• ✅ PASS  : LLM berhasil mengambil fakta needle tanpa halusinasi.")
    print("• ❌ FAIL  : LLM mengalami distraction/halusinasi akibat efek Lost in the Middle.")
    print("=" * 70)

if __name__ == "__main__":
    demo()
