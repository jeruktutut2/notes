#!/usr/bin/env python3
"""
SIMULASI MODUL 2.2: State Evaluation, Pruning & Backtracking di Tree of Thought (ToT)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents)

Modul ini mensimulasikan mekanisme penilaian cabang (Self-Evaluation / Heuristic Scorer),
pemotongan cabang mati (Pruning score < threshold), dan gerakan kembali (Backtracking)
ketika jalur yang ditempuh menemui jalan buntu.
"""

import time
from dataclasses import dataclass, field
from typing import List, Optional

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

PRUNING_THRESHOLD = 0.60

@dataclass
class StateNode:
    name: str
    action_thought: str
    score: float  # Evaluator confidence score
    children: List['StateNode'] = field(default_factory=list)
    parent: Optional['StateNode'] = None

def evaluate_and_backtrack_sim():
    print(f"\n{BOLD}{CYAN}=== TO T STATE EVALUATION & PRUNING SIMULATOR ==={RESET}")
    print(f"Pruning Threshold Score: {BOLD}{RED}{PRUNING_THRESHOLD}{RESET} (Cabang dengan score < {PRUNING_THRESHOLD} akan dipotong/pruned)\n")
    
    # Root
    root = StateNode("Root", "Tugas: Memperbaiki bug Memory Leak pada aplikasi Python Backend", 1.0)
    
    # Level 1 Branches
    n1 = StateNode("Branch-1", "Hipotesis A: Garbage Collection (gc) tidak berjalan otomatis", 0.35)
    n2 = StateNode("State-2", "Hipotesis B: Ada global array yang menyimpan reference objek secara konstan", 0.88)
    n3 = StateNode("Branch-3", "Hipotesis C: Kerusakan pada CPU Hardware server", 0.10)
    
    root.children = [n1, n2, n3]
    n1.parent = root
    n2.parent = root
    n3.parent = root
    
    # Level 2 Sub-branches for State-2
    n2_1 = StateNode("Branch-2.1", "Tindakan: Hapus global array tanpa unit test", 0.40)
    n2_2 = StateNode("State-2.2", "Tindakan: Profiling memori dengan tracemalloc & perbaiki event listener release", 0.95)
    
    n2.children = [n2_1, n2_2]
    n2_1.parent = n2
    n2_2.parent = n2
    
    print(f"{BOLD}{YELLOW}[ LANGKAH 1: EVALUASI KANDIDAT CABANG PADA LEVEL 1 ]{RESET}")
    time.sleep(0.3)
    for child in root.children:
        if child.score < PRUNING_THRESHOLD:
            print(f"  ❌ {BOLD}{child.name}{RESET} (Score: {RED}{child.score:.2f}{RESET}) -> {RED}[PRUNED / DIPOTONG]{RESET} jalur pemikiran: '{child.action_thought}'")
        else:
            print(f"  ✅ {BOLD}{child.name}{RESET} (Score: {GREEN}{child.score:.2f}{RESET}) -> {GREEN}[DILANJUTKAN]{RESET} jalur pemikiran: '{child.action_thought}'")
        time.sleep(0.2)
        
    print(f"\n{BOLD}{MAGENTA}[ LANGKAH 2: EKSPLORASI CABANG TERBAIK ({n2.name}) DENGAN SUB-STATE ]{RESET}")
    time.sleep(0.3)
    for sub in n2.children:
        if sub.score < PRUNING_THRESHOLD:
            print(f"  ❌ {BOLD}{sub.name}{RESET} (Score: {RED}{sub.score:.2f}{RESET}) -> {RED}[BACKTRACKING / PRUNED]{RESET}: '{sub.action_thought}'")
        else:
            print(f"  🏆 {BOLD}{sub.name}{RESET} (Score: {GREEN}{sub.score:.2f}{RESET}) -> {GREEN}[SOLUSI OPTIMAL TERPILIH]{RESET}: '{sub.action_thought}'")
        time.sleep(0.2)
        
    print(f"\n{BOLD}{GREEN}======================================================================{RESET}")
    print(f"{BOLD}{GREEN}                    RINGKASAN SOLUSI SOLUSI OPTIMAL                    {RESET}")
    print(f"{BOLD}{GREEN}======================================================================{RESET}")
    print(f"Jalur Pemikiran Terpilih:\n  {root.name} ➔ {n2.name} ➔ {n2_2.name}")
    print(f"Skor Akhir Kepastian: {BOLD}{GREEN}95% (0.95){RESET}")
    print(f"Status Pruning: {RED}3 Cabang Buruk Berhasil Dipangkas Mencegah Waktu/Token Terbuang.{RESET}\n")

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  SIMULASI TOT: STATE EVALUATION, PRUNING & BACKTRACKING MECHANISM    {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    evaluate_and_backtrack_sim()

if __name__ == "__main__":
    main()
