#!/usr/bin/env python3
"""
Modul 6.2: Example Usecase - Code Generation & Auto-Debugging Agent
Simulasi AI Agent yang menulis kode Python, mengeksekusinya di Sandbox, mengevaluasi Stack Trace saat eror,
lalu melakukan perbaikan kode secara mandiri (Self-Correction Loop) hingga seluruh pengujian lulus.
"""

import time
import subprocess
import sys

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class CodeGenerationAgent:
    def __init__(self):
        # Draf kode v1 (mengandung sengaja ZeroDivisionError)
        self.code_v1 = """def calculate_average(numbers):
    return sum(numbers) / len(numbers) # Bug jika list kosong!

print(calculate_average([]))
"""
        # Kode v2 yang sudah diperbaiki (Self-Corrected)
        self.code_v2 = """def calculate_average(numbers):
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)

print(f"Avg empty: {calculate_average([])}")
print(f"Avg valid: {calculate_average([10, 20, 30])}")
"""

    def run_agent_loop(self):
        print(f"\n{BOLD}{CYAN}=== USECASE 2: CODE GENERATION & AUTO-DEBUGGING AGENT ==={RESET}")
        print(f"Goal: \"Buat fungsi Python calculate_average yang tahan terhadap edge case list kosong\"\n")

        # --- ITERASI 1: MENULIS KODE V1 & MENJALANKAN SANDBOX ---
        print(f"{BOLD}[Iterasi #1 - Generated Code V1]{RESET}")
        print(f"🧠 {BLUE}Thought    :{RESET} Saya akan menulis fungsi matematika dasar calculate_average.")
        print(f"⚡ {YELLOW}Action     :{RESET} Execute code in sandbox Python...")
        
        # Simulasi Eksekusi Sandbox & Stacktrace Error
        obs_1 = "ZeroDivisionError: division by zero at line 2 in calculate_average"
        print(f"👁 {RED}Observation: [FAIL] {obs_1}{RESET}")
        print(f"🧠 {RED}Reflection : Eror terjadi karena pembagian dengan len(numbers) = 0 pada list kosong.{RESET}")
        print(f"🛠 {CYAN}Correction : Tambahkan penanganan kondisi darurat 'if not numbers: return 0.0'{RESET}\n")

        time.sleep(0.3)

        # --- ITERASI 2: REVISI KODE V2 & RUNNING TEST ---
        print(f"{BOLD}[Iterasi #2 - Self-Corrected Code V2]{RESET}")
        print(f"🧠 {BLUE}Thought    :{RESET} Saya telah merevisi kode dengan guard clause penanganan list kosong.")
        print(f"⚡ {YELLOW}Action     :{RESET} Execute updated code in sandbox Python...")
        
        obs_2 = "Avg empty: 0.0 | Avg valid: 20.0\nProcess finished with exit code 0"
        print(f"👁 {GREEN}Observation: [PASS] {obs_2}{RESET}")
        print(f"🧠 {GREEN}Reflection : Seluruh unit test lulus dengan sukses tanpa exception!{RESET}")
        print(f"🏁 {GREEN}Decision   : TERMINATE LOOP (Goal Achieved){RESET}\n")

        print(f"{GREEN}{BOLD}✔ [KODE AKHIR YANG DIHASILKAN AGENT]:{RESET}")
        print(f"{CYAN}{self.code_v2}{RESET}")

if __name__ == "__main__":
    agent = CodeGenerationAgent()
    agent.run_agent_loop()
