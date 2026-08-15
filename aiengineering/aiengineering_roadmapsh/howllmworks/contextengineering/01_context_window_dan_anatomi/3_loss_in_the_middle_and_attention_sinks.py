#!/usr/bin/env python3
"""
MODUL 1: Context Window & Anatomi Context
Skrip 3: Lost in the Middle & Attention Sinks Simulator

Mendemonstrasikan:
1. Simulasi Kurva Performa LLM Recall berdasarkan posisi fakta (Lost in the Middle Effect).
2. Efek Attention Sinks (StreamingLLM) untuk menjaga token awal (System Prompt) dari truncation.
3. Strategi Re-ordering Context (Sandwich Positioning) untuk memaksimalkan recall.
"""

import math
import random
from typing import List, Dict, Tuple

class LostInTheMiddleSimulator:
    """Metrik visualisasi efek Lost in the Middle pada LLM."""

    @staticmethod
    def calculate_recall_probability(depth_percent: float) -> float:
        """
        Menghitung estimasi probabilitas recall LLM berdasarkan kedalaman posisi fakta (0% = awal, 50% = tengah, 100% = akhir).
        Menggunakan kurva U-Shape khas (Liu et al., 2023).
        """
        # Model matematis U-shape: Primacy high (0%), Middle low (50%), Recency high (100%)
        # P(recall) = 0.95 - 0.70 * sin(pi * depth)
        prob = 0.95 - 0.50 * math.sin(math.pi * (depth_percent / 100.0))
        return max(0.20, min(0.99, prob))

    @staticmethod
    def reorder_chunks_sandwich(chunks: List[str]) -> List[str]:
        """
        Mengurutkan ulang dokumen RAG dengan strategi 'Sandwich' / Primacy-Recency Optimization:
        Dokumen paling relevan ditaruh di awal (0%) dan di akhir (100%), dokumen kurang relevan di tengah.
        """
        if len(chunks) <= 2:
            return chunks

        # Anggap chunks sudah terurut dari paling relevan ke kurang relevan
        reordered = []
        left = True
        
        # Masukkan selang-seling ke depan dan ke belakang
        start_list = []
        end_list = []

        for idx, chunk in enumerate(chunks):
            if idx % 2 == 0:
                start_list.append(chunk)
            else:
                end_list.insert(0, chunk)

        return start_list + end_list

class StreamingAttentionSinkSimulator:
    """Simulasi mekanisme Attention Sinks untuk context window yang sangat panjang."""

    def __init__(self, sink_size: int = 4, recent_size: int = 16):
        self.sink_tokens: List[str] = []      # Initial tokens (Attention Sinks)
        self.recent_tokens: List[str] = []    # Sliding window recent tokens
        self.sink_size = sink_size
        self.recent_size = recent_size

    def push_tokens(self, tokens: List[str]):
        """Menambahkan token baru dengan mempertahankan Attention Sinks & Recent Window."""
        for token in tokens:
            if len(self.sink_tokens) < self.sink_size:
                self.sink_tokens.append(token)
            else:
                self.recent_tokens.append(token)
                if len(self.recent_tokens) > self.recent_size:
                    self.recent_tokens.pop(0)

    def get_active_context(self) -> List[str]:
        """Penggabungan Attention Sinks + Recent Window."""
        return self.sink_tokens + ["... [COMPRESSED_MIDDLE_TOKENS] ..."] + self.recent_tokens

def demo():
    print("=" * 70)
    print("DEMO 3: LOST IN THE MIDDLE & ATTENTION SINKS SIMULATOR")
    print("=" * 70)

    # 1. Visualisasi U-Shape Curve (Lost in the Middle)
    print("\n--- SIMULASI KURVA U-SHAPE RECALL (LOST IN THE MIDDLE) ---")
    print(f"{'Kedalaman Position (%)':<25} | {'Estimasi Accuracy Recall':<25} | Visualisasi Bar")
    print("-" * 75)

    for depth in range(0, 101, 10):
        prob = LostInTheMiddleSimulator.calculate_recall_probability(depth)
        bar_len = int(prob * 30)
        bar = "█" * bar_len
        print(f"{depth:^23}% | {prob * 100:6.1f}%                    | {bar}")

    # 2. Re-ordering Sandwich Optimization
    rag_documents = [
        "[Doc 1 - Top Relevant]: Kunci API berada di server 10.0.0.1.",
        "[Doc 2 - High Relevant]: Port yang digunakan adalah 8080.",
        "[Doc 3 - Mid Relevant]: Versi sistem operasi adalah Linux Ubuntu 22.04.",
        "[Doc 4 - Low Relevant]: Server dibeli pada tahun 2021.",
        "[Doc 5 - Lowest Relevant]: Warna casing server adalah hitam."
    ]

    print("\n--- OPTIMASI SANDWICH RE-ORDERING (RAG CONTEXT) ---")
    print("Urutan Asal (Skor Relevansi Menurun):")
    for doc in rag_documents:
        print(f"  • {doc}")

    reordered = LostInTheMiddleSimulator.reorder_chunks_sandwich(rag_documents)
    print("\nUrutan Setelah Sandwich Re-ordering (Menghindari Lost in the Middle):")
    for doc in reordered:
        print(f"  • {doc}")

    # 3. Attention Sinks Streaming Simulation
    print("\n--- SIMULASI ATTENTION SINKS (STREAMING LLM CONTEXT) ---")
    sink_sim = StreamingAttentionSinkSimulator(sink_size=2, recent_size=4)
    tokens_stream = ["<SYS>", "ROLE:AI", "Turn1", "Turn2", "Turn3", "Turn4", "Turn5", "Turn6", "Turn7", "Turn8"]
    
    sink_sim.push_tokens(tokens_stream)
    active_ctx = sink_sim.get_active_context()

    print(f"Stream Token Input Total: {tokens_stream}")
    print(f"Context Aktif yang Dipertahankan oleh Attention Sink:")
    print(f"  -> {active_ctx}")
    print("\nCatatan: Token '<SYS>' & 'ROLE:AI' dipertahankan sebagai Attention Sink agar LLM tidak kehilangan orientasi instruksi dasar.")
    print("=" * 70)

if __name__ == "__main__":
    demo()
