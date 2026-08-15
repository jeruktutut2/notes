#!/usr/bin/env python3
"""
MODUL 1: Context Window & Anatomi Context
Skrip 1: Context Window Architecture & Token Budgeting

Mendemonstrasikan:
1. Pembagian Alokasi Token Window (System, History, RAG Context, Working Memory, User Query, Reserved Output).
2. Mekanisme Truncation Berbasis Prioritas saat Context Overflow.
3. Simulasi Token Manager & Visualisasi Budgeting Context Window.
"""

import json
from typing import Dict, List, Any

class TokenEstimator:
    """Estimator sederhana: ~1 token ≈ 4 karakter (untuk bahasa Indonesia/Inggris)."""
    @staticmethod
    def count_tokens(text: str) -> int:
        if not text:
            return 0
        words = text.split()
        # Perkiraan realistis token: kombinasi kata + karakter
        return max(len(words), len(text) // 4)

class ContextWindowManager:
    """Manager pengelola alokasi context window LLM."""
    def __init__(self, max_context_window: int = 4096, max_output_reserved: int = 1024):
        self.max_context_window = max_context_window
        self.max_output_reserved = max_output_reserved
        self.max_input_budget = max_context_window - max_output_reserved

        # Definisi Alokasi Target (Persentase dari input budget)
        self.allocation_targets = {
            "system_prompt": 0.15,      # 15% untuk System Instruction & Guardrails
            "rag_context": 0.40,        # 40% untuk Retrieval Augmented Context
            "history": 0.25,            # 25% untuk Riwayat Percakapan
            "working_memory": 0.10,     # 10% untuk Scratchpad / State
            "user_query": 0.10          # 10% untuk Kueri Pengguna
        }

    def allocate_and_assemble(
        self,
        system_prompt: str,
        rag_chunks: List[str],
        history: List[Dict[str, str]],
        working_memory: str,
        user_query: str
    ) -> Dict[str, Any]:
        """Merakit context window dengan enforcement token budget."""
        
        system_tokens = TokenEstimator.count_tokens(system_prompt)
        query_tokens = TokenEstimator.count_tokens(user_query)
        wm_tokens = TokenEstimator.count_tokens(working_memory)

        # 1. Alokasikan System Prompt & User Query lebih dulu (Priority 1)
        used_tokens = system_tokens + query_tokens + wm_tokens
        remaining_budget = self.max_input_budget - used_tokens

        if remaining_budget < 0:
            return {
                "status": "CRITICAL_OVERFLOW",
                "message": "System prompt + Query melebihi batas total input budget!",
                "used_tokens": used_tokens,
                "max_input_budget": self.max_input_budget
            }

        # 2. Alokasikan RAG Context (Priority 2)
        rag_budget = int(self.max_input_budget * self.allocation_targets["rag_context"])
        selected_rag_chunks = []
        rag_tokens = 0

        for chunk in rag_chunks:
            chunk_t = TokenEstimator.count_tokens(chunk)
            if rag_tokens + chunk_t <= min(rag_budget, remaining_budget):
                selected_rag_chunks.append(chunk)
                rag_tokens += chunk_t
            else:
                break

        remaining_budget -= rag_tokens

        # 3. Alokasikan History Percakapan (Priority 3 - Truncate dari yang terlama)
        selected_history = []
        history_tokens = 0
        
        # Iterasi dari percakapan terbaru
        for turn in reversed(history):
            turn_str = f"{turn['role']}: {turn['content']}"
            t_count = TokenEstimator.count_tokens(turn_str)
            if history_tokens + t_count <= remaining_budget:
                selected_history.insert(0, turn)
                history_tokens += t_count
            else:
                break

        total_input_tokens = system_tokens + query_tokens + wm_tokens + rag_tokens + history_tokens
        
        # Rakit Prompt Akhir
        formatted_rag = "\n".join([f"- [Dokumen]: {c}" for c in selected_rag_chunks])
        formatted_history = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in selected_history])

        assembled_prompt = (
            f"=== SYSTEM INSTRUCTION ===\n{system_prompt}\n\n"
            f"=== RETRIEVED CONTEXT (RAG) ===\n{formatted_rag if formatted_rag else '(Tidak ada)'}\n\n"
            f"=== CONVERSATION HISTORY ===\n{formatted_history if formatted_history else '(Tidak ada)'}\n\n"
            f"=== WORKING MEMORY SCRATCHPAD ===\n{working_memory}\n\n"
            f"=== USER QUERY ===\n{user_query}"
        )

        return {
            "status": "SUCCESS",
            "assembled_prompt": assembled_prompt,
            "token_breakdown": {
                "system_prompt": system_tokens,
                "user_query": query_tokens,
                "working_memory": wm_tokens,
                "rag_context": rag_tokens,
                "history": history_tokens,
                "total_input_tokens": total_input_tokens,
                "max_input_budget": self.max_input_budget,
                "remaining_input_budget": self.max_input_budget - total_input_tokens,
                "reserved_output_tokens": self.max_output_reserved,
                "total_context_window": self.max_context_window
            },
            "pruning_stats": {
                "rag_chunks_included": len(selected_rag_chunks),
                "rag_chunks_total": len(rag_chunks),
                "history_turns_included": len(selected_history),
                "history_turns_total": len(history)
            }
        }

def demo():
    print("=" * 70)
    print("DEMO 1: CONTEXT WINDOW ARCHITECTURE & TOKEN BUDGETING")
    print("=" * 70)

    # Inisialisasi Manager dengan Window 2048 token
    manager = ContextWindowManager(max_context_window=2048, max_output_reserved=512)

    system_prompt = (
        "Anda adalah AI Engineering Consultant berpengalaman. Jawab pertanyaan pengguna "
        "secara terstruktur, presisi, dan sertakan contoh implementasi teknis."
    )
    
    rag_chunks = [
        "Metode FlashAttention-2 mengoptimalkan urutan IO antara GPU HBM dan SRAM.",
        "RoPE (Rotary Position Embedding) memungkinkan perpanjangan context window hingga 128k token.",
        "LLMLingua menggunakan model bahasa kecil untuk memangkas token non-esensial dari prompt.",
        "Prefix caching memanfaatkan identitas byte-for-byte awal prompt untuk menghindari re-komputasi KV Cache."
    ]

    history = [
        {"role": "user", "content": "Halo, saya ingin belajar tentang optimasi LLM."},
        {"role": "assistant", "content": "Tentu! Ada beberapa topik utama: Context Engineering, RAG, dan Fine-Tuning."},
        {"role": "user", "content": "Apa bedanya Context Engineering dengan Prompt Engineering?"},
        {"role": "assistant", "content": "Prompt Engineering berfokus pada desain teks instruksi, sedangkan Context Engineering mengelola seluruh alokasi token window, memori, kompresi, dan caching."}
    ]

    working_memory = "Active Topic: Context Engineering Optimization; User Skill Level: Advanced."
    user_query = "Bagaimana cara menyusun alokasi token window agar tidak overflow saat dokumen RAG sangat panjang?"

    result = manager.allocate_and_assemble(system_prompt, rag_chunks, history, working_memory, user_query)

    print("\n--- BREAKDOWN ALOKASI TOKEN ---")
    for key, val in result["token_breakdown"].items():
        print(f"  • {key:<25}: {val}")

    print("\n--- STATISTIK PEMANGKASAN (PRUNING) ---")
    for key, val in result["pruning_stats"].items():
        print(f"  • {key:<25}: {val}")

    print("\n--- HASIL PERAKITAN CONTEXT WINDOW ---")
    print(result["assembled_prompt"][:400] + "\n... [Teks dipotong untuk tampilan CLI] ...")
    print("=" * 70)

if __name__ == "__main__":
    demo()
