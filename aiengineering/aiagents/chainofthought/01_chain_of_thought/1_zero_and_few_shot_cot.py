#!/usr/bin/env python3
"""
SIMULASI MODUL 1.1: Zero-Shot CoT vs Few-Shot CoT vs Direct Generation
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents)

Modul ini mensimulasikan mekanisme pembuatan penalaran bertahap (Reasoning Trace)
menggunakan teknik Zero-Shot CoT ("Let's think step by step") dan Few-Shot CoT.
"""

import time
import random
from typing import Dict, List, Any

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Sample Complex Problems (Math & Reasoning Logic)
PROBLEMS = [
    {
        "id": "PROB-01",
        "question": "Sebuah toko komputer memiliki 15 laptop di stok awal. Pada hari Senin, mereka menjual 4 laptop. Hari Selasa, mereka menerima suplai baru sebanyak 10 laptop. Hari Rabu, mereka menjual setengah dari total stok laptop yang ada. Berapa sisa laptop pada hari Kamis?",
        "direct_answer": "Sisa 10 laptop.",
        "cot_steps": [
            "Langkah 1: Stok awal = 15 laptop.",
            "Langkah 2: Senin menjual 4 laptop -> 15 - 4 = 11 laptop.",
            "Langkah 3: Selasa terima suplai 10 laptop -> 11 + 10 = 21 laptop.",
            "Langkah 4: Rabu menjual 1/2 dari total stok -> 21 / 2 = 10.5 (Secara fisik dijual 10 laptop atau sisa 10.5, secara matematika 21 / 2 = 10.5). Sisa stok = 10.5 laptop.",
            "Kesimpulan: Sisa laptop adalah 10.5 (atau 10 laptop utuh jika dibulatkan)."
        ],
        "correct_value": 10.5
    },
    {
        "id": "PROB-02",
        "question": "Seorang pengembang AI agent memiliki budget $50 per hari. API LLM berbiaya $0.002 per 1.000 token input dan $0.006 per 1.000 token output. Jika setiap prompt rata-rata berisi 1.500 token input dan menghasilkan 500 token output, berapa maksimum eksekusi agent yang bisa dijalankan per hari?",
        "direct_answer": "Sekitar 8.333 eksekusi.",
        "cot_steps": [
            "Langkah 1: Biaya Input per eksekusi = (1.500 / 1.000) * $0.002 = $0.003.",
            "Langkah 2: Biaya Output per eksekusi = (500 / 1.000) * $0.006 = $0.003.",
            "Langkah 3: Total biaya per eksekusi = $0.003 + $0.003 = $0.006.",
            "Langkah 4: Maksimum eksekusi per hari = Total Budget / Biaya per eksekusi = $50 / $0.006.",
            "Langkah 5: $50 / 0.006 = 8.333.33 eksekusi.",
            "Kesimpulan: Maksimum eksekusi utuh yang bisa dijalankan adalah 8.333 kali."
        ],
        "correct_value": 8333
    }
]

def simulate_direct_prompting(problem: Dict[str, Any]):
    print(f"\n{BOLD}{RED}[ DIRECT PROMPTING (Tanpa CoT) ]{RESET}")
    print(f"Prompt: {problem['question']}")
    print(f"{YELLOW}Proses LLM: Memprediksi token jawaban langsung secara instantaneous...{RESET}")
    time.sleep(0.3)
    print(f"Jawaban LLM: \"{problem['direct_answer']}\"")
    print(f"{RED}⚠️ Risiko: Tidak ada langkah verifikasi logika intermediet, rentan salah kalkulasi pada masalah kompleks.{RESET}")

def simulate_zero_shot_cot(problem: Dict[str, Any]):
    print(f"\n{BOLD}{CYAN}[ ZERO-SHOT CoT ('Let\'s think step by step') ]{RESET}")
    print(f"Prompt: {problem['question']} \\n{BOLD}Let's think step by step.{RESET}")
    print(f"{CYAN}Proses LLM: Memicu pembentukan Reasoning Trace...{RESET}")
    time.sleep(0.4)
    
    print(f"\n{MAGENTA}--- REASONING TRACE GENERATION ---{RESET}")
    for step in problem["cot_steps"]:
        print(f"  🧠 {step}")
        time.sleep(0.2)
    print(f"{GREEN}✓ Hasil Akhir terverifikasi berdasarkan penalaran bertahap.{RESET}")

def simulate_few_shot_cot(problem: Dict[str, Any]):
    print(f"\n{BOLD}{GREEN}[ FEW-SHOT CoT (Dengan Contoh Penalaran) ]{RESET}")
    print("Prompt memuat pasang contoh (Exemplars):\n")
    print(f"{YELLOW}Exemplar 1:{RESET}")
    print("  Q: Ada 3 apel, beli 2 lagi, berapa totalnya?")
    print("  A: Mulai dengan 3 apel. Beli 2 lagi = 3 + 2 = 5 apel. Jawabannya 5.\n")
    print(f"Target Prompt: {problem['question']}")
    time.sleep(0.4)
    
    print(f"\n{GREEN}--- FEW-SHOT REASONING TRACE ---{RESET}")
    for step in problem["cot_steps"]:
        print(f"  📌 {step}")
        time.sleep(0.2)
    print(f"{GREEN}✓ Hasil Akhir berformat konsisten sesuai dengan exemplar prompt.{RESET}")

def main():
    print(f"\n{BOLD}{HEADER if 'HEADER' in globals() else MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   SIMULASI CHAIN OF THOUGHT (CoT): ZERO-SHOT VS FEW-SHOT VS DIRECT   {RESET}")
    print(f"{BOLD}{HEADER if 'HEADER' in globals() else MAGENTA}======================================================================{RESET}")
    print("Demonstrasi bagaimana teknik pengarahan penalaran (CoT) meningkatkan")
    print("akurasi dan transparansi logika AI Agent.\n")
    
    for problem in PROBLEMS:
        print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
        print(f"{BOLD}KASUS PENGUJIAN: {problem['id']}{RESET}")
        print(f"Masalah: {problem['question']}")
        print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
        
        simulate_direct_prompting(problem)
        simulate_zero_shot_cot(problem)
        simulate_few_shot_cot(problem)
        
        input(f"\n{YELLOW}Tekan [Enter] untuk melanjutkan ke masalah berikutnya...{RESET}")

    print(f"\n{BOLD}{GREEN}✓ Simulasi Zero-Shot & Few-Shot CoT Selesai!{RESET}\n")

if __name__ == "__main__":
    main()
