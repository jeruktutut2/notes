#!/usr/bin/env python3
"""
MODUL 2: Context Compression & Pruning
Skrip 1: Selective Token Compression (LLMLingua Mechanism)

Mendemonstrasikan:
1. Perhitungan Information Density / Entropi Kata untuk Mengidentifikasi Filler Tokens.
2. Pemangkasan Token Redundan Tanpa Merusak Makna Semantik Utama.
3. Mengukur Token Compression Ratio (%) & Penghematan Biaya.
"""

import math
import re
from typing import List, Tuple, Dict, Any

class LLMLinguaCompressor:
    """Simulasi Kompresi Context berbasis Kepadatan Informasi (LLMLingua approach)."""

    # Kata sambung/filler umum dengan information density rendah (high frequency / low surprise)
    LOW_INFORMATION_WORDS = {
        "bahwa", "yang", "dan", "atau", "adalah", "merupakan", "tersebut", "dapat", "secara",
        "untuk", "pada", "dalam", "dengan", "ke", "dari", "ini", "itu", "juga", "akan", "telah",
        "bisa", "harus", "maka", "sehingga", "serta", "oleh", "karena", "sebagai"
    }

    def __init__(self, target_compression_ratio: float = 0.5):
        """target_compression_ratio: 0.5 berarti target kompresi memotong ~50% token."""
        self.target_compression_ratio = target_compression_ratio

    def _calculate_word_score(self, word: str, context_words: List[str]) -> float:
        """
        Menghitung Skor Kepadatan Informasi (Surprisal/Entropy Score).
        Kata bermakna spesifik (nama entitas, angka, terminologi teknis) memiliki skor tinggi.
        """
        clean_word = re.sub(r"[^\w]", "", word.lower())
        
        if not clean_word:
            return 0.0

        # High priority if number or capitalized/technical code
        if clean_word.isdigit() or any(char.isupper() for char in word):
            return 3.0

        # Low priority for common filler words
        if clean_word in self.LOW_INFORMATION_WORDS:
            return 0.2

        # IDF-like length heuristic (kata panjang cenderung membawa informasi lebih banyak)
        length_score = min(2.0, len(clean_word) / 4.0)
        return 1.0 + length_score

    def compress_text(self, text: str) -> Dict[str, Any]:
        """Memangkas teks berdasarkan urutan skor kepadatan informasi."""
        words = text.split()
        if not words:
            return {"compressed_text": "", "ratio": 0.0}

        scored_words = []
        for idx, word in enumerate(words):
            score = self._calculate_word_score(word, words)
            scored_words.append((idx, word, score))

        # Urutkan berdasarkan skor tertinggi
        sorted_by_score = sorted(scored_words, key=lambda x: x[2], reverse=True)

        # Ambil sejumlah target token terbanyak
        target_count = max(1, int(len(words) * (1.0 - self.target_compression_ratio)))
        selected = sorted_by_score[:target_count]

        # Urutkan kembali berdasarkan indeks posisi asli agar kalimat tetap koheren
        selected_in_original_order = sorted(selected, key=lambda x: x[0])

        compressed_words = [item[1] for item in selected_in_original_order]
        compressed_text = " ".join(compressed_words)

        original_tokens = len(words)
        compressed_tokens = len(compressed_words)
        actual_ratio = (1.0 - (compressed_tokens / original_tokens)) * 100

        return {
            "original_text": text,
            "compressed_text": compressed_text,
            "original_tokens": original_tokens,
            "compressed_tokens": compressed_tokens,
            "tokens_saved": original_tokens - compressed_tokens,
            "compression_ratio_percent": actual_ratio
        }

def demo():
    print("=" * 70)
    print("DEMO 1: SELECTIVE TOKEN COMPRESSION (LLMLINGUA APPROACH)")
    print("=" * 70)

    compressor = LLMLinguaCompressor(target_compression_ratio=0.40)

    sample_context = (
        "Dapat diketahui bahwa arsitektur dari Transformer adalah merupakan arsitektur yang sangat efisien "
        "untuk pemrosesan bahasa alami. Pada sistem ini, mekanisme Self-Attention yang digunakan mampu "
        "secara langsung mengkalkulasi hubungan antara token A dan token B dengan biaya waktu O(N^2). "
        "Oleh karena itu, penggunaan kompresi token LLMLingua adalah sangat penting untuk menghemat biaya API."
    )

    result = compressor.compress_text(sample_context)

    print("\n--- TEKS ASLI ---")
    print(result["original_text"])
    print(f"Jumlah Token/Kata Asli: {result['original_tokens']}")

    print("\n--- HASIL KOMPRESI TERSELEKSI (LLMLINGUA) ---")
    print(result["compressed_text"])
    print(f"Jumlah Token/Kata Setelah Kompresi: {result['compressed_tokens']}")

    print("\n--- METRIK PENGHEMATAN ---")
    print(f"  • Token Dihemat        : {result['tokens_saved']} token")
    print(f"  • Rasio Pemangkasan    : {result['compression_ratio_percent']:.2f}% dihemat")
    print(f"  • Estimasi Penghematan : ~{result['compression_ratio_percent']:.1f}% pengurangan biaya input API!")
    print("=" * 70)

if __name__ == "__main__":
    demo()
