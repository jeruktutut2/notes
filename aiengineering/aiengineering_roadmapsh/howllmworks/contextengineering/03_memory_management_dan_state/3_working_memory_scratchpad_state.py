#!/usr/bin/env python3
"""
MODUL 3: In-Context Memory & State Management
Skrip 3: Working Memory & Scratchpad State Pattern

Mendemonstrasikan:
1. Pemeliharaan State Sementara (Working Memory Scratchpad) saat Agen Menjalankan Penalaran Bertahap.
2. Penjejak variabel aktif (Active Variables, Step Counter, Pending Actions).
3. Pembersihan Scratchpad setelah Tugas Selesai (State Transition Hygiene).
"""

import json
from typing import Dict, List, Any

class WorkingMemoryScratchpad:
    """Scratchpad Working Memory untuk agen pemroses tugas bertahap."""

    def __init__(self, task_id: str):
        self.task_id = task_id
        self.step_counter: int = 0
        self.active_variables: Dict[str, Any] = {}
        self.thought_history: List[str] = []
        self.pending_subtasks: List[str] = []

    def initialize_task(self, subtasks: List[str]):
        self.pending_subtasks = subtasks
        self.step_counter = 1

    def record_step(self, thought: str, action_taken: str, variable_updates: Dict[str, Any] = None):
        """Mencatat hasil dari satu langkah penalaran."""
        log_entry = f"Step {self.step_counter}: [THOUGHT] {thought} -> [ACTION] {action_taken}"
        self.thought_history.append(log_entry)

        if variable_updates:
            self.active_variables.update(variable_updates)

        if self.pending_subtasks:
            self.pending_subtasks.pop(0)

        self.step_counter += 1

    def get_scratchpad_formatted(self) -> str:
        """Format Scratchpad untuk disisipkan ke context window."""
        subtasks_str = "\n".join([f"  [ ] {st}" for st in self.pending_subtasks]) if self.pending_subtasks else "  [✓] Semua subtask selesai!"
        history_str = "\n".join([f"  • {th}" for th in self.thought_history]) if self.thought_history else "  (Belum ada langkah)"
        vars_str = json.dumps(self.active_variables, indent=2) if self.active_variables else "{}"

        return (
            f"<working_memory task_id=\"{self.task_id}\">\n"
            f"  <current_step>{self.step_counter}</current_step>\n"
            f"  <active_variables>\n{vars_str}\n  </active_variables>\n"
            f"  <pending_subtasks>\n{subtasks_str}\n  </pending_subtasks>\n"
            f"  <thought_scratchpad>\n{history_str}\n  </thought_scratchpad>\n"
            f"</working_memory>"
        )

def demo():
    print("=" * 70)
    print("DEMO 3: WORKING MEMORY & SCRATCHPAD STATE PATTERN")
    print("=" * 70)

    scratchpad = WorkingMemoryScratchpad(task_id="TASK_COMPRESSION_OPTIMIZATION")

    # Inisialisasi daftar subtask
    scratchpad.initialize_task([
        "Hitung total token awal dokumen input.",
        "Jalankan algoritma LLMLingua compression.",
        "Verifikasi akurasi informasi terkompresi."
    ])

    print("\n--- STATE SCRATCHPAD AWAL (Langkah 1) ---")
    print(scratchpad.get_scratchpad_formatted())

    # Eksekusi Langkah 1
    scratchpad.record_step(
        thought="Dokumen memiliki 1250 token. Perlu dikompresi hingga < 600 token.",
        action_taken="Menjalankan tokenizer estimator.",
        variable_updates={"raw_token_count": 1250, "target_limit": 600}
    )

    # Eksekusi Langkah 2
    scratchpad.record_step(
        thought="Membuang kata filler dengan entropi rendah.",
        action_taken="Menjalankan LLMLingua filter.",
        variable_updates={"compressed_token_count": 520, "compression_ratio": "58.4%"}
    )

    print("\n--- STATE SCRATCHPAD SETELAH LANGKAH 2 (STATE TERUPDATE) ---")
    print(scratchpad.get_scratchpad_formatted())
    print("=" * 70)

if __name__ == "__main__":
    demo()
