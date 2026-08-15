#!/usr/bin/env python3
"""
Modul 03: Maintaining Memory
Skrip 4: Forgetting / Aging Strategies (Memory Decay & Eviction Policies)

Simulasi teknik peluruhan memori (Forgetting Curve) & pembersihan otomatis.
Fitur utama:
- Ebbinghaus Forgetting Curve formula: S(t) = S0 * exp(-lambda * delta_t) + alpha * AccessCount.
- Importance Score (Skor Kepentingan 1 - 10).
- Eviction Policies: Threshold Eviction & LRU (Least Recently Used) Cleanup.
"""

import math
import time
from dataclasses import dataclass
from typing import List, Dict

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


@dataclass
class MemoryNode:
    """Representasi satu entri memori dengan peluruhan usia."""
    id: str
    content: str
    initial_importance: float  # S0 (Scale 1.0 - 10.0)
    created_at: float
    last_accessed_at: float
    access_count: int = 1


class MemoryRetentionManager:
    """Pengelola Retensi & Peluruhan Memori Jangka Panjang."""

    def __init__(self, decay_rate: float = 0.1, access_amplification: float = 0.5, min_retention_threshold: float = 2.0):
        self.decay_rate = decay_rate  # lambda
        self.alpha = access_amplification  # alpha
        self.min_threshold = min_retention_threshold  # S_min threshold
        self.memory_store: Dict[str, MemoryNode] = {}

    def add_memory(self, mem_id: str, content: str, importance: float):
        """Menambahkan memori baru ke store."""
        now = time.time()
        node = MemoryNode(
            id=mem_id,
            content=content,
            initial_importance=importance,
            created_at=now,
            last_accessed_at=now,
            access_count=1
        )
        self.memory_store[mem_id] = node

    def access_memory(self, mem_id: str):
        """Mengakses memori (Memperkuat retensi memori)."""
        if mem_id in self.memory_store:
            node = self.memory_store[mem_id]
            node.last_accessed_at = time.time()
            node.access_count += 1

    def calculate_current_score(self, node: MemoryNode, simulated_now: float) -> float:
        """
        Menhitung skor retensi memori saat ini S(t):
        S(t) = S0 * e^(-lambda * delta_t) + alpha * access_count
        """
        delta_t = simulated_now - node.last_accessed_at  # Selisih waktu dalam detik / jam simulasi
        decay_factor = math.exp(-self.decay_rate * delta_t)
        score = (node.initial_importance * decay_factor) + (self.alpha * node.access_count)
        return score

    def run_garbage_collection(self, simulated_now: float) -> List[str]:
        """Daur ulang / hapus memori yang skor retensinya di bawah ambang batas (Forgetting Eviction)."""
        purged_ids = []
        for mem_id, node in list(self.memory_store.items()):
            score = self.calculate_current_score(node, simulated_now)
            if score < self.min_threshold:
                purged_ids.append(mem_id)
                del self.memory_store[mem_id]
        return purged_ids


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 03.4: FORGETTING / AGING STRATEGIES (EBBINGHAUS DECAY CURVE) {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    manager = MemoryRetentionManager(decay_rate=0.2, access_amplification=0.5, min_retention_threshold=2.5)

    now = time.time()

    # Menambahkan 3 jenis memori dengan tingkat kepentingan berbeda
    print(f"{GREEN}[INIT MEMORY STORE]{RESET} Menyimpan 3 memori awal:")
    
    # Memori 1: Catatan instruksi acak (Importance rendah: 3.0)
    manager.add_memory("mem_01", "Pengguna menyebutkan menyukai warna biru muda.", importance=3.0)
    print("  1. [mem_01] Importance: 3.0 | Content: 'Pengguna menyukai warna biru muda.'")

    # Memori 2: Kredensial DB (Importance sangat tinggi: 9.5)
    manager.add_memory("mem_02", "API Key Production: sk-prod-881923-secret", importance=9.5)
    print("  2. [mem_02] Importance: 9.5 | Content: 'API Key Production: sk-prod-881923-secret'")

    # Memori 3: Pertanyaan seputar cuaca kemarin (Importance sedang: 4.5, diakses 4 kali)
    manager.add_memory("mem_03", "Cuaca di Jakarta kemarin adalah cerah berawan.", importance=4.5)
    manager.access_memory("mem_03")
    manager.access_memory("mem_03")
    manager.access_memory("mem_03")
    print("  3. [mem_03] Importance: 4.5 | Content: 'Cuaca Jakarta' (Diakses 4 kali)")

    # Simulasi berlalunya waktu (Waktu berlalu: 10 satuan waktu simulasi)
    simulated_future_time = now + 10.0
    print(f"\n{BOLD}{YELLOW}=== SIMULASI WAKTU BERLALU (+10 Satuan Waktu Simulasi) ==={RESET}")
    print("Menghitung ulang Skor Retensi S(t) menggunakan kurva peluruhan eksponensial:\n")

    for mem_id, node in manager.memory_store.items():
        score = manager.calculate_current_score(node, simulated_future_time)
        print(f"  • Memori ID [{mem_id}]: Skor Retensi Saat Ini = {score:.2f} (Init S0: {node.initial_importance}, Accesses: {node.access_count})")

    # Jalankan Cleaning / Eviction Policy
    print(f"\n{BOLD}{RED}=== MENJALANKAN GARBAGE COLLECTION (Threshold Eviction < 2.5) ==={RESET}")
    purged = manager.run_garbage_collection(simulated_future_time)

    for p_id in purged:
        print(f"  {RED}[PURGED/FORGOTTEN]{RESET} Memori [{p_id}] telah dihapus dari memori agen karena dianggap usang & tidak penting.")

    print(f"\n{BOLD}[SISA MEMORI TERSEDIA DI STORE AGENT]{RESET}")
    for mem_id, node in manager.memory_store.items():
        score = manager.calculate_current_score(node, simulated_future_time)
        print(f"  • [{mem_id}] (Score: {score:.2f}): \"{node.content}\"")

    print(f"\n{GREEN}[KESIMPULAN]{RESET} Forgetting strategy mencegah memori agen penuh oleh sampah informasi yang tidak penting atau tidak pernah diakses kembali.")


if __name__ == "__main__":
    run_demo()
