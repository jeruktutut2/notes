#!/usr/bin/env python3
"""
Modul 4.1: Observation Processing & Memory Management
Demonstrasi pengolahan hasil observasi tool, pembaruan Working Memory Agent,
dan teknik kompresi memori (sliding window) untuk menjaga context window tidak meluap.
"""

from typing import List, Dict, Any
from dataclasses import dataclass, field
import json

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class MemoryEntry:
    turn_id: int
    role: str  # user, thought, action, observation
    content: str

class AgentWorkingMemory:
    def __init__(self, max_turns: int = 4):
        self.max_turns = max_turns
        self.entries: List[MemoryEntry] = []
        self.turn_counter = 0

    def add_entry(self, role: str, content: str):
        self.turn_counter += 1
        entry = MemoryEntry(turn_id=self.turn_counter, role=role, content=content)
        self.entries.append(entry)
        print(f"  {BLUE}[Memory Added]{RESET} Turn #{self.turn_counter} ({role}): {content[:60]}...")

    def get_compressed_context(self) -> str:
        """Mengompresi memori lama dan hanya mempertahankan N turn terakhir (Sliding Window)."""
        if len(self.entries) > self.max_turns:
            trimmed_entries = self.entries[-self.max_turns:]
            summary_header = f"[SYSTEM MEMORY SUMMARY: {len(self.entries) - self.max_turns} turn terdahulu telah dikompresi]\n"
        else:
            trimmed_entries = self.entries
            summary_header = ""

        formatted = [f"{e.role.upper()}: {e.content}" for e in trimmed_entries]
        return summary_header + "\n".join(formatted)

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 4.1: OBSERVATION PROCESSING & MEMORY MANAGEMENT ==={RESET}\n")

    memory = AgentWorkingMemory(max_turns=3)

    print(f"{BOLD}Simulasi Penambahan Riwayat Iterasi Agent Loop:{RESET}\n")

    interactions = [
        ("user", "Hitung rata-rata penjualan bulan Jan - Mar"),
        ("thought", "Saya perlu memanggil tool get_sales_data untuk bulan Jan-Mar"),
        ("action", "call get_sales_data(months=['Jan', 'Feb', 'Mar'])"),
        ("observation", "Data returned: Jan=100, Feb=150, Mar=200"),
        ("thought", "Saya perlu menghitung (100+150+200)/3"),
        ("action", "call calculate_avg(values=[100, 150, 200])"),
        ("observation", "Average result = 150.0")
    ]

    for role, text in interactions:
        memory.add_entry(role, text)

    print(f"\n{BOLD}Working Memory Context Window Saat Ini (Max 3 Turn Terakhir):{RESET}")
    print(f"{CYAN}--------------------------------------------------{RESET}")
    print(f"{YELLOW}{memory.get_compressed_context()}{RESET}")
    print(f"{CYAN}--------------------------------------------------{RESET}\n")

if __name__ == "__main__":
    main()
