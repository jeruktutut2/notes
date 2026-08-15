#!/usr/bin/env python3
"""
MODUL 3: In-Context Memory & State Management
Skrip 2: Episodic, Semantic, & Procedural Memory Architecture

Mendemonstrasikan:
1. Episodic Memory (Perekaman Riwayat Kejadian / Pengalaman Sesi Lampau).
2. Semantic Memory (Penyimpan Fakta Pengetahuan Konseptual).
3. Procedural Memory (Instruksi Langkah-demi-Langkah / SOP Agen).
4. Penyatuan Multi-Tier Memory ke dalam Single In-Context Memory Window.
"""

from typing import List, Dict, Any

class TripartiteAgentMemory:
    """Arsitektur Tiga Lapis Memori Agen AI (Episodic, Semantic, Procedural)."""

    def __init__(self):
        # 1. Procedural Memory: Aturan & Workflow Tetap
        self.procedural_memory: List[str] = [
            "Langkah 1: Verifikasi otentikasi identitas pengguna.",
            "Langkah 2: Periksa log error pada database sebelum melakukan restart service.",
            "Langkah 3: Dokumentasikan setiap aksi perubahan konfigurasi pada audit log."
        ]

        # 2. Semantic Memory: Pengetahuan Fakta yang Dipercaya
        self.semantic_memory: Dict[str, str] = {
            "DB_PORT": "5432",
            "STAGING_SERVER_IP": "192.168.1.100",
            "BACKUP_RETENTION_DAYS": "30 Hari",
            "SUPPORT_CONTACT": "devops-team@company.com"
        }

        # 3. Episodic Memory: Pengalaman Interaksi Sesi Sebelumnya
        self.episodic_memory: List[Dict[str, str]] = [
            {"timestamp": "2026-07-25 14:00", "event": "User Budi melakukan deployment versi v1.2.0 di Staging (Berhasil)."},
            {"timestamp": "2026-07-25 16:30", "event": "Koneksi database PostgreSQL terputus selama 2 menit karena High CPU spike."}
        ]

    def add_episode(self, timestamp: str, event_description: str):
        self.episodic_memory.append({"timestamp": timestamp, "event": event_description})

    def update_semantic_fact(self, fact_key: str, fact_value: str):
        self.semantic_memory[fact_key] = fact_value

    def assemble_full_memory_prompt(self, current_task: str) -> str:
        """Merakit ketiga lapis memori menjadi In-Context Memory terstruktur."""

        # Format Procedural
        proc_str = "\n".join([f"  • {step}" for step in self.procedural_memory])

        # Format Semantic
        sem_str = "\n".join([f"  • {k}: {v}" for k, v in self.semantic_memory.items()])

        # Format Episodic (3 kejadian terakhir)
        ep_str = "\n".join([f"  • [{e['timestamp']}] {e['event']}" for e in self.episodic_memory[-3:]])

        return (
            f"=== TRIPARTITE AGENT MEMORY SYSTEM ===\n\n"
            f"[1. PROCEDURAL MEMORY (Standard Operating Procedure)]\n{proc_str}\n\n"
            f"[2. SEMANTIC MEMORY (Fakta Pengetahuan Terverifikasi)]\n{sem_str}\n\n"
            f"[3. EPISODIC MEMORY (Pengalaman Sesi Lampau)]\n{ep_str}\n\n"
            f"=== TUGAS SAAT INI ===\n{current_task}"
        )

def demo():
    print("=" * 70)
    print("DEMO 2: TRIPARTITE MEMORY (EPISODIC, SEMANTIC, PROCEDURAL)")
    print("=" * 70)

    agent_memory = TripartiteAgentMemory()

    # Tambahkan pengalaman baru (Episodic)
    agent_memory.add_episode("2026-07-26 09:00", "User Budi meminta troubleshooting koneksi database staging.")

    current_task = "Tolong periksa mengapa koneksi database staging error dan berikan rekomendasi perbaikan sesuai SOP."

    in_context_prompt = agent_memory.assemble_full_memory_prompt(current_task)

    print("\n--- PERAKITAN CONTEXT MEMORI TRIPARTIT LENGKAP ---")
    print(in_context_prompt)
    print("\nRingkasan: Agen AI dapat membaca fakta teknis (Semantic), SOP kerja (Procedural), dan histori insiden (Episodic) secara bersamaan.")
    print("=" * 70)

if __name__ == "__main__":
    demo()
