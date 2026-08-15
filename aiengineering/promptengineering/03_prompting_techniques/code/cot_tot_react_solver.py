#!/usr/bin/env python3
"""
Modul 03: CoT, Tree of Thoughts (ToT), & ReAct Agent Solver
Simulasi langsung logika pemecahan masalah berbasis CoT, ToT, dan ReAct.
"""

import time

def solve_chain_of_thought(problem: str):
    """Simulasi Chain of Thought (CoT)."""
    print(f"\n🧠 [CHAIN OF THOUGHT (CoT)] Problem: {problem}")
    steps = [
        "Langkah 1: Identifikasi variabel yang diketahui dalam soal.",
        "Langkah 2: Tentukan rumus atau logika matematika yang berlaku.",
        "Langkah 3: Hitung hasil kalkulasi intermediate secara berurutan.",
        "Langkah 4: Tinjau kembali konsistensi logika dan tentukan jawaban akhir."
    ]
    for step in steps:
        print(f"  └─> {step}")
        time.sleep(0.1)

def solve_tree_of_thoughts(problem: str):
    """Simulasi Tree of Thoughts (ToT) dengan 3 Cabang Penalaran & Evaluasi."""
    print(f"\n🌳 [TREE OF THOUGHTS (ToT)] Problem: {problem}")
    branches = [
        {"id": "Cabang A", "strategy": "Pendekatan Brute-Force", "score": 4.5, "status": "Ditolak"},
        {"id": "Cabang B", "strategy": "Pendekatan Dynamic Programming", "score": 9.2, "status": "Terpilih (Optimal)"},
        {"id": "Cabang C", "strategy": "Pendekatan Heuristik Greedy", "score": 7.0, "status": "Cadangan"}
    ]
    
    for b in branches:
        print(f"  ├─ [{b['id']}] Strategi: {b['strategy']} | Score: {b['score']}/10 -> {b['status']}")
    print("  └─> Keputusan ToT: Menjalankan eksekusi berdasarkan Cabang B.")

def solve_react_agent(task: str):
    """Simulasi ReAct Loop (Thought -> Action -> Observation -> Final Answer)."""
    print(f"\n🤖 [ReAct AGENT LOOP] Task: {task}")
    trace = [
        ("Thought 1", "Saya perlu mencari kurs mata uang USD ke IDR hari ini."),
        ("Action 1", "SearchAPI['USD to IDR rate']"),
        ("Observation 1", "1 USD = 16.250 IDR"),
        ("Thought 2", "Sekarang saya akan mengalikan $150 dengan 16.250."),
        ("Action 2", "Calculator[150 * 16250]"),
        ("Observation 2", "2.437.500"),
        ("Final Answer", "Total $150 sama dengan Rp 2.437.500 IDR.")
    ]
    
    for step_type, content in trace:
        print(f"  [{step_type:<12}] {content}")
        time.sleep(0.1)

def main():
    print("🚀 ADVANCED REASONING SOLVER DEMO")
    print("=" * 60)
    problem = "Sebuah toko memberikan diskon 20% kemudian potongan tambahan 10%. Berapa total diskon efektif?"
    
    solve_chain_of_thought(problem)
    solve_tree_of_thoughts(problem)
    solve_react_agent("Hitung konversi $150 ke IDR dan tambahkan pajak 11%")
    print("=" * 60)

if __name__ == "__main__":
    main()
