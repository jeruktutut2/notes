#!/usr/bin/env python3
"""
Modul 02: Episodic vs Semantic Memory
Skrip 1: Episodic Memory (Event Sequence & Execution Trajectories)

Simulasi Episodic Memory (Memori Episodis / Pengalaman Spesifik).
Fitur utama:
- Pencatatan log urutan kejadian berbasis waktu (Timestamped Trajectory Logs).
- Struktur Agent Action Loop: (State, Action, Observation, Outcome).
- Retrieval episode masa lalu untuk introspeksi & pembetulan kesalahan (Reflective Learning).
"""

import time
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
@dataclass
class EpisodeEntry:
    """Struktur data satu episode pengalaman agen."""
    timestamp: float
    session_id: str
    task_goal: str
    action_taken: str
    observation: str
    success: bool
    reflection_notes: str


class EpisodicMemoryStore:
    """Penyimpanan Memori Episodis untuk merekam jejak tindakan (Trajectories)."""

    def __init__(self):
        self.episodes: List[EpisodeEntry] = []

    def record_episode(self, session_id: str, goal: str, action: str, observation: str, success: bool, reflection: str):
        """Merekam episode baru ke dalam episodic log."""
        entry = EpisodeEntry(
            timestamp=time.time(),
            session_id=session_id,
            task_goal=goal,
            action_taken=action,
            observation=observation,
            success=success,
            reflection_notes=reflection
        )
        self.episodes.append(entry)

    def search_similar_past_episodes(self, query_keyword: str) -> List[EpisodeEntry]:
        """Mencari episode masa lalu berdasarkan kata kunci tugas."""
        results = [ep for ep in self.episodes if query_keyword.lower() in ep.task_goal.lower()]
        return results


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 02.1: EPISODIC MEMORY (EVENT SEQUENCES & TRAJECTORY LOGS)    {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    episodic_memory = EpisodicMemoryStore()

    # Episode 1: Kegagalan masa lalu saat mengakses Database Postgres
    print(f"{BOLD}{RED}=== MEMORIZING EPISODE 1 (Masa Lalu: 2 Hari Yang Lalu) ==={RESET}")
    goal_1 = "Hubungkan agen ke Postgres Database Produksi"
    action_1 = "Menjalankan psycopg2.connect(host='localhost', port=5432)"
    obs_1 = "ConnectionRefusedError: port 5432 closed"
    reflection_1 = "Gagal karena Service Postgres lokal mati, harus menggunakan host 'prod-db.internal' port 5433."
    
    episodic_memory.record_episode(
        session_id="sess_001",
        goal=goal_1,
        action=action_1,
        observation=obs_1,
        success=False,
        reflection=reflection_1
    )
    print(f"Goal: {goal_1}")
    print(f"Hasil: {RED}FAILED{RESET} -> Reflection Saved: '{reflection_1}'\n")

    # Episode 2: Keberhasilan eksekusi ulang
    print(f"{BOLD}{GREEN}=== MEMORIZING EPISODE 2 (Masa Lalu: Kemarin) ==={RESET}")
    goal_2 = "Hubungkan agen ke Postgres Database Produksi"
    action_2 = "Menjalankan psycopg2.connect(host='prod-db.internal', port=5433)"
    obs_2 = "Connection successful. Returned 100 rows."
    reflection_2 = "Berhasil terkoneksi via host prod-db.internal port 5433."

    episodic_memory.record_episode(
        session_id="sess_002",
        goal=goal_2,
        action=action_2,
        observation=obs_2,
        success=True,
        reflection=reflection_2
    )
    print(f"Goal: {goal_2}")
    print(f"Hasil: {GREEN}SUCCESS{RESET} -> Reflection Saved: '{reflection_2}'\n")

    # Sesi Sekarang: Agen diminta menjalankan tugas database Postgres lagi
    print(f"{BOLD}{YELLOW}=== SESI SEKARANG: AGENT MENERIMA TUGAS DATABASE POSTGRES ==={RESET}")
    current_task = "Koneksi ke Postgres Database dan ambil tabel pengguna"
    print(f"Task Saat Ini: '{current_task}'")
    print("Mencari Episodic Memory terkait tugas serupa...")

    matched_episodes = episodic_memory.search_similar_past_episodes("Postgres")

    print(f"\n{BOLD}[EPISODIC MEMORY RETRIEVED ({len(matched_episodes)} Episodes)]{RESET}")
    for idx, ep in enumerate(matched_episodes, 1):
        status_color = GREEN if ep.success else RED
        status_text = "BERHASIL" if ep.success else "GAGAL"
        print(f"  {idx}. [Sesi: {ep.session_id}] Status: {status_color}{status_text}{RESET}")
        print(f"     Action: {ep.action_taken}")
        print(f"     Observation: {ep.observation}")
        print(f"     Catatan Refleksi: {ep.reflection_notes}\n")

    print(f"{GREEN}[REFLECTIVE DECISION]{RESET} Berdasarkan Episodic Memory, agent langsung memilih port 5433 & host 'prod-db.internal' tanpa mengulangi kesalahan port 5432!")


if __name__ == "__main__":
    run_demo()
