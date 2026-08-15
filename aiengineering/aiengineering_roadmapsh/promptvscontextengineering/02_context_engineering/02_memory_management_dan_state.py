#!/usr/bin/env python3
"""
Modul 02: In-Context Memory Management & State Architecture
Membahas Summarization Buffer, Tripartite Memory (Episodic, Semantic, Procedural), dan Working Memory Scratchpad.
"""

import json
from typing import List, Dict, Any

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class InContextMemoryManager:
    """Simulasi Arsitektur Memori LLM Multi-Turn"""

    def __init__(self, max_recent_messages: int = 3):
        self.max_recent_messages = max_recent_messages
        self.episodic_memory: List[Dict[str, str]] = [] # Raw chat logs
        self.semantic_memory: Dict[str, str] = {} # Entity & User Facts (Long-term)
        self.procedural_memory: List[str] = [ # System Rules & Workflow Steps
            "Aturan 1: Verifikasi identitas user sebelum transaksi.",
            "Aturan 2: Gunakan Bahasa Indonesia formal dan ramah."
        ]
        self.summary_buffer: str = "" # Summarized history

    def add_turn(self, role: str, content: str):
        """Menambahkan turn baru dan mengekstraksi fakta ke memori terdistribusi"""
        self.episodic_memory.append({"role": role, "content": content})
        
        # Simple entity extraction simulation (Semantic Memory)
        if "nama saya" in content.lower():
            name = content.split("nama saya")[-1].strip().split()[0]
            self.semantic_memory["user_name"] = name
        if "rekening" in content.lower():
            self.semantic_memory["account_type"] = "Bank Transfer Preferred"

        # Check if conversation needs summarization
        if len(self.episodic_memory) > self.max_recent_messages * 2:
            self._update_summary_buffer()

    def _update_summary_buffer(self):
        """Merangkum pesan lama menjadi Summary Buffer ringkas"""
        old_turns = self.episodic_memory[:-self.max_recent_messages]
        summarized_facts = [f"{t['role']}: {t['content'][:30]}..." for t in old_turns]
        self.summary_buffer += " | " + " ".join(summarized_facts)
        # Keep only recent messages in episodic active window
        self.episodic_memory = self.episodic_memory[-self.max_recent_messages:]

    def assemble_working_memory_context(self, current_user_query: str) -> str:
        """Menggabungkan Tripartite Memory & Summary Buffer menjadi Working Memory Prompt"""
        procedural_str = "\n".join(self.procedural_memory)
        semantic_str = json.dumps(self.semantic_memory)
        recent_history = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in self.episodic_memory])

        working_context = f"""<procedural_rules>
{procedural_str}
</procedural_rules>

<semantic_user_profile>
{semantic_str}
</semantic_user_profile>

<summarized_past_history>
{self.summary_buffer if self.summary_buffer else 'Belum ada percakapan lampau yang dirangkum.'}
</summarized_past_history>

<active_recent_dialogue>
{recent_history}
</active_recent_dialogue>

<current_user_query>
{current_user_query}
</current_user_query>"""
        return working_context

def main():
    print_header("MODUL 02: IN-CONTEXT MEMORY & STATE MANAGEMENT")

    mem_mgr = InContextMemoryManager(max_recent_messages=2)
    
    print(color("\n1. Simulasi Percakapan Multi-Turn & Extraction into Tripartite Memory:", "1;33"))
    
    turns = [
        ("user", "Halo, nama saya Budi Hartono. Saya mau tanya tentang fitur transfer."),
        ("assistant", "Halo Pak Budi! Selamat datang. Ada yang bisa saya bantu terkait fitur transfer?"),
        ("user", "Saya sering pakai rekening BCA untuk transaksi bisnis."),
        ("assistant", "Baik Pak Budi, informasi rekening BCA Bapak telah kami catat."),
        ("user", "Berapa limit harian transfer antar bank?"),
    ]

    for role, content in turns:
        print(f"[{role.upper()}]: {content}")
        mem_mgr.add_turn(role, content)

    print(color("\n2. Status Tripartite Memory Terkini:", "1;33"))
    print(color("  [A] Semantic Memory (User Facts Extracted):", "36"))
    print(f"      {json.dumps(mem_mgr.semantic_memory, indent=2)}")
    
    print(color("  [B] Summary Buffer (Rangkuman Pesan Lampau):", "36"))
    print(f"      \"{mem_mgr.summary_buffer.strip()}\"")
    
    print(color("  [C] Episodic Active Window (Sliding Messages):", "36"))
    for msg in mem_mgr.episodic_memory:
        print(f"      • {msg['role']}: {msg['content']}")

    # 3. Working Memory Assembly
    print(color("\n3. Dynamic Working Memory Scratchpad untuk Request Terakhir:", "1;33"))
    current_q = "Berapa biayanya jika saya transfer 50 juta dari BCA?"
    working_prompt = mem_mgr.assemble_working_memory_context(current_q)
    print(color(working_prompt, "32"))

    print_header("RANGKUMAN MEMORY & STATE MANAGEMENT")
    print("✓ Summary Buffer mendeduksi riwayat percakapan panjang tanpa melebihi batas Token Window.")
    print("✓ Tripartite Memory memisahkan aturan (Procedural), profil user (Semantic), dan riwayat (Episodic).")
    print("✓ Dynamic Working Memory Scratchpad menjamin model tetap memiliki konteks stateful yang bersih.")

if __name__ == "__main__":
    main()
