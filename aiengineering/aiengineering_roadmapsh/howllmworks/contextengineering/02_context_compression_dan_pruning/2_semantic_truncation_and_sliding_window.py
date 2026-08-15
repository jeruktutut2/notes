#!/usr/bin/env python3
"""
MODUL 2: Context Compression & Pruning
Skrip 2: Semantic Truncation & Sliding Window with Recency Decay

Mendemonstrasikan:
1. Sliding Window Truncation berbobot Recency Decay.
2. Semantic Sentence Truncation berdasarkan Kemiripan dengan Kueri.
3. Pemilihan Paragraf Terbaik untuk Tetap Berada dalam Token Budget.
"""

import math
from typing import List, Dict, Any

class SemanticTruncator:
    """Truncator cerdas berbasis skor relevansi semantik + recency decay."""

    @staticmethod
    def _jaccard_similarity(str1: str, str2: str) -> float:
        """Kalkulasi similarity sederhana berbasis kata jaccard index."""
        set1 = set(str1.lower().split())
        set2 = set(str2.lower().split())
        if not set1 or not set2:
            return 0.0
        intersection = set1.intersection(set2)
        union = set1.union(set2)
        return len(intersection) / len(union)

    def truncate_passages(
        self,
        passages: List[str],
        query: str,
        max_words_budget: int = 60,
        decay_factor: float = 0.9
    ) -> Dict[str, Any]:
        """
        Menilai setiap paragraf berdasarkan relevansi semantik terhadap query,
        dikalikan dengan recency decay factor (paragraf lebih baru = multiplier lebih tinggi).
        """
        scored_passages = []
        total_p = len(passages)

        for idx, passage in enumerate(passages):
            raw_sim = self._jaccard_similarity(passage, query)
            
            # Recency multiplier: Paragraf terakhir mendapat decay minimal (1.0), paragraf lama terdevaluasi
            position_from_end = total_p - 1 - idx
            recency_weight = math.pow(decay_factor, position_from_end)
            
            combined_score = raw_sim * recency_weight

            scored_passages.append({
                "index": idx,
                "text": passage,
                "words": len(passage.split()),
                "similarity": raw_sim,
                "recency_weight": recency_weight,
                "combined_score": combined_score
            })

        # Urutkan berdasarkan combined score tertinggi
        sorted_passages = sorted(scored_passages, key=lambda x: x["combined_score"], reverse=True)

        selected_passages = []
        used_words = 0

        for item in sorted_passages:
            if used_words + item["words"] <= max_words_budget:
                selected_passages.append(item)
                used_words += item["words"]

        # Kembalikan ke urutan teks asli
        selected_in_order = sorted(selected_passages, key=lambda x: x["index"])
        truncated_text = "\n\n".join([p["text"] for p in selected_in_order])

        return {
            "truncated_text": truncated_text,
            "used_words": used_words,
            "max_words_budget": max_words_budget,
            "included_passages_count": len(selected_passages),
            "total_passages_count": total_p,
            "passage_details": scored_passages
        }

def demo():
    print("=" * 70)
    print("DEMO 2: SEMANTIC TRUNCATION & RECENTY-DECAY SLIDING WINDOW")
    print("=" * 70)

    passages = [
        "Passage 0 (Lama): Pengenalan dasar Python dibuat oleh Guido van Rossum tahun 1991.",
        "Passage 1 (Lama): Konfigurasi database MySQL dapat diatur menggunakan file my.cnf di Linux.",
        "Passage 2 (Sedang): Arsitektur RAG membutuhkan Vector Database seperti Qdrant atau Milvus.",
        "Passage 3 (Baru): Penggunaan LLMLingua dan Context Compression dapat memotong token RAG secara drastis.",
        "Passage 4 (Paling Baru): Pilihan optimasi context window mencakup sliding window dan prompt caching."
    ]

    query = "Bagaimana cara melakukan optimasi context window pada RAG menggunakan compression?"
    truncator = SemanticTruncator()

    result = truncator.truncate_passages(passages, query, max_words_budget=45, decay_factor=0.85)

    print(f"\nKUERI PENGGUNA: '{query}'")
    print(f"BUDGET KATA MAKSIMUM: {result['max_words_budget']} kata\n")

    print("--- EVALUASI SKOR PARAGRAF (SEMANTIC SIMILARITY x RECENCY DECAY) ---")
    for detail in result["passage_details"]:
        print(f"  • Passage #{detail['index']}: Sim={detail['similarity']:.2f} | RecencyW={detail['recency_weight']:.2f} | Score={detail['combined_score']:.3f}")

    print("\n--- HASIL HASIL SELEKSI TEKS TERCOMPRESS ---")
    print(result["truncated_text"])

    print(f"\nRingkasan: Memilih {result['included_passages_count']} dari {result['total_passages_count']} paragraf ({result['used_words']} kata).")
    print("=" * 70)

if __name__ == "__main__":
    demo()
