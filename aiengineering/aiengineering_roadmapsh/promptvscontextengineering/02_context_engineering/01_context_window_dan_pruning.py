#!/usr/bin/env python3
"""
Modul 02: Context Window & Token Pruning
Membahas Context Window Budgeting, Lost-in-the-Middle (U-Shape Effect), dan Token Information Density Compression.
"""

import math
import json
import re
from typing import List, Dict, Any

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class ContextWindowAndPruningSimulator:
    """Simulasi Pengelolaan Context Window & Kompresi Token"""

    @staticmethod
    def calculate_context_budget(
        total_window: int = 128000,
        system_prompt_tokens: int = 2000,
        chat_history_tokens: int = 25000,
        retrieved_docs_tokens: int = 80000,
        output_reserve_tokens: int = 4000
    ) -> Dict[str, Any]:
        """Menghitung alokasi dan sisa budget Context Window"""
        used = system_prompt_tokens + chat_history_tokens + retrieved_docs_tokens + output_reserve_tokens
        remaining = total_window - used
        overflow = max(0, -remaining)
        
        return {
            "total_context_limit": total_window,
            "used_tokens": used,
            "breakdown": {
                "system_prompt": system_prompt_tokens,
                "chat_history": chat_history_tokens,
                "retrieved_docs": retrieved_docs_tokens,
                "output_reserve": output_reserve_tokens
            },
            "remaining_budget": remaining,
            "status": "OVERFLOW_WARNING" if overflow > 0 else "OPTIMAL",
            "overflow_amount": overflow
        }

    @staticmethod
    def simulate_lost_in_the_middle(documents: List[str], target_needle_index: int) -> Dict[str, Any]:
        """
        Simulasi U-shaped Attention Retrieval Accuracy.
        Informasi di awal (Beginning) dan akhir (End) prompt memiliki recall tinggi (~95%).
        Informasi di tengah (Middle) mengalami degredasi recall hingga (~40-50%).
        """
        n = len(documents)
        position_ratio = target_needle_index / (n - 1) if n > 1 else 0.5
        
        # Formula U-Shape Attention Recall: 1.0 - 0.5 * sin(pi * position_ratio)
        recall_probability = 1.0 - 0.48 * math.sin(math.pi * position_ratio)
        
        return {
            "total_docs": n,
            "needle_index": target_needle_index,
            "position": "Awal (Beginning)" if position_ratio < 0.25 else ("Akhir (End)" if position_ratio > 0.75 else "Tengah (Middle)"),
            "estimated_recall_accuracy": f"{recall_probability * 100:.1f}%",
            "recommendation": "Tempatkan informasi paling kritikal di bagian paling awal (<system_context>) atau di akhir prompt."
        }

    @staticmethod
    def token_density_pruning(text: str, compression_ratio: float = 0.5) -> Dict[str, Any]:
        """
        Simulasi Selective Token Information Density Compression (LLMLingua style).
        Menghapus kata-kata stop-word / pengisi yang memiliki surprisal / informasi entropy rendah.
        """
        words = text.split()
        original_count = len(words)
        
        # Stopwords & filler tokens to prune first
        low_info_words = {"dan", "atau", "adalah", "yang", "untuk", "pada", "di", "dengan", "secara", "bahwa", "ini", "itu", "tersebut"}
        
        pruned_words = []
        for word in words:
            clean_w = re.sub(r"[^\w]", "", word.lower())
            if clean_w in low_info_words and len(pruned_words) > original_count * compression_ratio:
                continue
            pruned_words.append(word)
            
        compressed_text = " ".join(pruned_words)
        new_count = len(pruned_words)
        saved_tokens_pct = (1.0 - (new_count / original_count)) * 100
        
        return {
            "original_word_count": original_count,
            "compressed_word_count": new_count,
            "saved_tokens_percentage": f"{saved_tokens_pct:.1f}%",
            "compressed_text": compressed_text
        }

def main():
    print_header("MODUL 02: CONTEXT WINDOW & TOKEN PRUNING")

    # 1. Context Budget Allocation
    print(color("\n1. Visualisasi Budget Context Window (128K Limits):", "1;33"))
    budget = ContextWindowAndPruningSimulator.calculate_context_budget(
        total_window=128000,
        system_prompt_tokens=3000,
        chat_history_tokens=30000,
        retrieved_docs_tokens=90000, # Large RAG context
        output_reserve_tokens=8000
    )
    print(json.dumps(budget, indent=2))

    # 2. Lost-in-the-Middle Effect Demonstration
    print(color("\n2. Simulasi Lost-in-the-Middle (U-Shape Curve Effect):", "1;33"))
    docs = [f"Dokumen Pendukung #{i}: Detail operasional bisnis..." for i in range(1, 11)]
    print(f"Menempatkan informasi kunci ('Needle') di berbagai posisi dalam 10 dokumen RAG:")
    
    positions_to_test = [0, 4, 9] # Beginning, Middle, End
    for pos in positions_to_test:
        res = ContextWindowAndPruningSimulator.simulate_lost_in_the_middle(docs, pos)
        print(f"   • Dokumen Posisi [{pos}] ({res['position']}): Recall Accuracy = " + color(res['estimated_recall_accuracy'], "32" if pos != 4 else "31"))
    print(f"   Note: {res['recommendation']}")

    # 3. Token Compression & Density Pruning
    print(color("\n3. Selective Token Density Compression (LLMLingua Style):", "1;33"))
    sample_corpus = ("Laporan keuangan perusahaan PT Maju Bersama adalah bahwa pada kuartal ketiga ini "
                     "pendapatan secara signifikan mengalami peningkatan yang cukup tajam untuk sektor manufaktur.")
    
    prune_res = ContextWindowAndPruningSimulator.token_density_pruning(sample_corpus, compression_ratio=0.4)
    print(f"Teks Asli ({prune_res['original_word_count']} kata):")
    print(f"  \"{sample_corpus}\"")
    print(color(f"\nTeks Terkompresi ({prune_res['compressed_word_count']} kata, Hemat {prune_res['saved_tokens_percentage']}):", "32"))
    print(f"  \"{prune_res['compressed_text']}\"")

    print_header("RANGKUMAN CONTEXT WINDOW & PRUNING")
    print("✓ Menghindari Context Overflow dengan menghitung alokasi Token Budget sebelum memanggil LLM.")
    print("✓ Lost-in-the-Middle menurunkan akurasi RAG; informasi paling kritis harus ditempatkan di U-curve peaks.")
    print("✓ Token Pruning membuang low-surprisal tokens tanpa mengurangi fakta inti, menghemat biaya & latensi.")

if __name__ == "__main__":
    main()
