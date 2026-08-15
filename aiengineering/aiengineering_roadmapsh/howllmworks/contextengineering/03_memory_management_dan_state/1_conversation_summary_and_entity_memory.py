#!/usr/bin/env python3
"""
MODUL 3: In-Context Memory & State Management
Skrip 1: Conversation Summary & Entity Memory Store

Mendemonstrasikan:
1. Summary Buffer Memory: Meringkas percakapan lama ketika token percakapan melampaui ambang batas.
2. Entity Memory Extractor: Menjaga variabel kunci (pengguna, entitas) dalam bentuk Key-Value JSON.
3. Integrasi Memory Buffer ke dalam System Prompt.
"""

import json
from typing import List, Dict, Any

class EntityMemoryStore:
    """Penyimpan memori entitas (Key-Value State)."""
    def __init__(self):
        self.entities: Dict[str, str] = {}

    def update_entity(self, key: str, value: str):
        self.entities[key] = value

    def get_formatted_entities(self) -> str:
        if not self.entities:
            return "(Tidak ada entitas terdeteksi)"
        return json.dumps(self.entities, ensure_ascii=False, indent=2)

class ConversationSummaryBuffer:
    """Buffer percakapan berbasis ringkasan otomatis saat token membengkak."""

    def __init__(self, max_token_limit: int = 150):
        self.max_token_limit = max_token_limit
        self.summary: str = ""
        self.history: List[Dict[str, str]] = []
        self.entity_store = EntityMemoryStore()

    def _estimate_tokens(self, text: str) -> int:
        return max(len(text.split()), len(text) // 4)

    def add_turn(self, role: str, content: str):
        """Menambah turn percakapan dan mengekstrak entitas sederhana."""
        self.history.append({"role": role, "content": content})

        # Deteksi entitas sederhana (Simulasi)
        if "nama saya" in content.lower():
            name = content.split("nama saya")[-1].strip().split()[0].capitalize()
            self.entity_store.update_entity("user_name", name)
        if "projek" in content.lower():
            self.entity_store.update_entity("active_project", "Context Engineering AI")

        # Periksa apakah total token melampaui limit
        total_tokens = sum(self._estimate_tokens(h["content"]) for h in self.history)
        if total_tokens > self.max_token_limit:
            self._summarize_oldest_turns()

    def _summarize_oldest_turns(self):
        """Meringkas turn percakapan tertua dan mengosongkannya dari history mentah."""
        turns_to_summarize = self.history[:2]
        self.history = self.history[2:]

        summary_snippets = []
        for t in turns_to_summarize:
            summary_snippets.append(f"{t['role']}: {t['content']}")

        new_summary_text = " | ".join(summary_snippets)
        if self.summary:
            self.summary += " " + new_summary_text
        else:
            self.summary = f"Ringkasan Percakapan Sebelumnya: {new_summary_text}"

    def build_memory_context(self) -> str:
        """Menyusun context memori lengkap untuk dimasukkan ke prompt."""
        formatted_history = "\n".join([f"{h['role'].upper()}: {h['content']}" for h in self.history])

        return (
            f"=== MEMORI ENTITAS PENGGUNA ===\n{self.entity_store.get_formatted_entities()}\n\n"
            f"=== RINGKASAN PERCAKAPAN LAMA ===\n{self.summary if self.summary else '(Kosong)'}\n\n"
            f"=== RIWAYAT PERCAKAPAN AKTIF ===\n{formatted_history}"
        )

def demo():
    print("=" * 70)
    print("DEMO 1: CONVERSATION SUMMARY & ENTITY MEMORY STORE")
    print("=" * 70)

    memory_buffer = ConversationSummaryBuffer(max_token_limit=40)

    # Tambahkan beberapa turn
    print("-> Menambahkan Turn 1 & Turn 2...")
    memory_buffer.add_turn("user", "Halo, nama saya Budi dan saya sedang mengerjakan projek AI Engineering.")
    memory_buffer.add_turn("assistant", "Halo Budi! Senang membantu Anda di projek AI Engineering. Ada yang bisa dibantu?")

    print("-> Menambahkan Turn 3 & Turn 4 (Memicu Summarization)...")
    memory_buffer.add_turn("user", "Saya ingin tahu bagaimana cara kerja Summary Buffer Memory agar token tidak habis.")
    memory_buffer.add_turn("assistant", "Summary Buffer meringkas percakapan lama menjadi bentuk eksekutif dan hanya menyimpan turn terbaru di buffer aktif.")

    print("\n--- HASIL STRUCTURAL MEMORY CONTEXT ---")
    print(memory_buffer.build_memory_context())
    print("=" * 70)

if __name__ == "__main__":
    demo()
