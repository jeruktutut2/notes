#!/usr/bin/env python3
"""
Modul 01: What is Agent Memory?
Skrip 1: Short-Term Memory (Within Prompt / Context Window)

Simulasi pengelolaan Short-Term Memory (STM) yang disimpan langsung di dalam prompt context window.
Fitur utama:
- Conversation Scratchpad (System, User, Assistant, Observation).
- Sliding Window Context Buffer.
- Simulasi Token Budgeting & Management.
"""

import json
from typing import List, Dict, Any

# ANSI Colors untuk output visual CLI
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class ShortTermMemoryManager:
    """Pengelola Short-Term Memory yang beroperasi di dalam Prompt Context Window."""
    
    def __init__(self, system_prompt: str, max_token_budget: int = 150):
        self.system_prompt = system_prompt
        self.max_token_budget = max_token_budget
        self.messages: List[Dict[str, str]] = []
        self.scratchpad: List[str] = []  # Internal CoT / working memory

    def estimate_tokens(self, text: str) -> int:
        """Estimasi sederhana jumlah token (pendekatan: ~4 karakter per token)."""
        return max(1, len(text) // 4)

    def add_message(self, role: str, content: str):
        """Menambahkan pesan baru ke conversation history."""
        self.messages.append({"role": role, "content": content})

    def add_scratchpad_thought(self, thought: str):
        """Menambahkan langkah CoT / pemikiran agen ke scratchpad."""
        self.scratchpad.append(thought)

    def get_total_context_tokens(self) -> int:
        """Menghitung total token dalam seluruh prompt aktif."""
        total = self.estimate_tokens(self.system_prompt)
        for msg in self.messages:
            total += self.estimate_tokens(msg['content'])
        for thought in self.scratchpad:
            total += self.estimate_tokens(thought)
        return total

    def enforce_sliding_window(self):
        """
        Menjaga total token agar tidak melebihi token budget.
        Pesan paling tua (setelah system prompt) akan dipangkas jika budget terlampaui.
        """
        while self.get_total_context_tokens() > self.max_token_budget and len(self.messages) > 1:
            removed = self.messages.pop(0)
            print(f"{YELLOW}[STM TRIMMING]{RESET} Menghapus pesan terlama dari prompt STM: ({removed['role']}): '{removed['content'][:30]}...'")

    def assemble_full_prompt(self) -> str:
        """Menggabungkan seluruh elemen short-term memory menjadi prompt siap-kirim ke LLM."""
        prompt = f"=== SYSTEM INSTRUCTION ===\n{self.system_prompt}\n\n"
        
        if self.scratchpad:
            prompt += "=== AGENT SCRATCHPAD (WORKING MEMORY) ===\n"
            for idx, thought in enumerate(self.scratchpad, 1):
                prompt += f"[Step {idx}] {thought}\n"
            prompt += "\n"

        prompt += "=== CONVERSATION HISTORY (SHORT-TERM CONTEXT) ===\n"
        for msg in self.messages:
            prompt += f"[{msg['role'].upper()}]: {msg['content']}\n"
            
        return prompt


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 01.1: SHORT-TERM MEMORY (WITHIN PROMPT / CONTEXT WINDOW)     {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    system_instruction = "Anda adalah AI Assistant layanan keuangan. Bantu pengguna dengan ramah & akurat."
    stm = ShortTermMemoryManager(system_prompt=system_instruction, max_token_budget=120)

    print(f"{GREEN}[INIT]{RESET} Menginisialisasi Short-Term Memory dengan Max Token Budget = 120 Tokens.\n")

    # Skenario Interaksi Percakapan
    conversations = [
        ("user", "Halo, nama saya Budi santoso. Saya ingin menanyakan suku bunga tabungan."),
        ("assistant", "Halo Pak Budi! Suku bunga tabungan harian kami saat ini adalah 2.5% per tahun."),
        ("user", "Baik, lalu berapa syarat minimum saldo pembukaan rekening baru?"),
        ("assistant", "Minimum pembukaan rekening baru adalah Rp 500.000, Pak Budi."),
        ("user", "Bagus sekali. Bisakah Anda sebutkan nama saya dan berapa minimum depositnya?"),
    ]

    for role, content in conversations:
        print(f"{BOLD}---> Input Pesan Baru ({role}):{RESET} \"{content}\"")
        stm.add_message(role, content)
        
        # Tambah scratchpad internal agent
        if role == "user":
            stm.add_scratchpad_thought(f"User bertanya: '{content}'. Memeriksa riwayat konteks di STM.")
            
        # Pangkas jika melebihi context limit
        stm.enforce_sliding_window()

        current_tokens = stm.get_total_context_tokens()
        print(f"     [Status STM] Jumlah Pesan: {len(stm.messages)} | Total Token: {current_tokens}/{stm.max_token_budget}\n")

    print(f"{BOLD}{YELLOW}--- PROMPT LENGKAP YANG AKAN DIKIRIM KE LLM (IN-PROMPT STM) ---{RESET}")
    print(stm.assemble_full_prompt())
    print(f"{GREEN}[KESIMPULAN]{RESET} Short-Term Memory hidup di dalam prompt (RAM LLM). Pesan tua terpotong saat memori penuh.")


if __name__ == "__main__":
    run_demo()
