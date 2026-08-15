#!/usr/bin/env python3
"""
Master Interactive Launcher - Prompt Engineering Learning Workspace (roadmap.sh)
"""

import sys
import subprocess

def run_script(path: str):
    print(f"\n▶️ Running {path}...\n")
    subprocess.run([sys.executable, path])

def main():
    while True:
        print("\n" + "=" * 65)
        print(" 🧠 PROMPT ENGINEERING INTERACTIVE WORKSPACE (roadmap.sh)")
        print("=" * 65)
        print(" [1] Modul 01: Token & Context Window Calculator")
        print(" [2] Modul 02: LLM Configuration & Sampling Simulator (Temp/Top-P)")
        print(" [3] Modul 03: Zero-Shot vs Few-Shot Prompting Demo")
        print(" [4] Modul 03: CoT, Tree of Thoughts (ToT), & ReAct Solver")
        print(" [5] Modul 04: Structured Output & JSON Schema Enforcer")
        print(" [6] Modul 04: Automatic Prompt Engineering (APE) Generator")
        print(" [7] Modul 05: 14 Best Practices Auditor")
        print(" [8] Modul 05: Red Teaming & Prompt Injection Simulator")
        print(" [9] Modul 06: Reliability Suite & LLM-as-a-Judge Evaluation")
        print(" [0] Keluar")
        print("=" * 65)
        
        choice = input("Pilih menu (0-9): ").strip()
        
        if choice == "1":
            run_script("01_introduction_and_terminology/code/token_context_calculator.py")
        elif choice == "2":
            run_script("02_llm_configuration/code/hyperparameters_experiment.py")
        elif choice == "3":
            run_script("03_prompting_techniques/code/zero_few_shot_demo.py")
        elif choice == "4":
            run_script("03_prompting_techniques/code/cot_tot_react_solver.py")
        elif choice == "5":
            run_script("04_structured_outputs_and_auto_prompts/code/structured_output_enforcer.py")
        elif choice == "6":
            run_script("04_structured_outputs_and_auto_prompts/code/auto_prompt_generator.py")
        elif choice == "7":
            run_script("05_best_practices_and_red_teaming/code/best_practices_auditor.py")
        elif choice == "8":
            run_script("05_best_practices_and_red_teaming/code/red_teaming_simulator.py")
        elif choice == "9":
            run_script("06_improving_reliability/code/reliability_suite.py")
        elif choice == "0":
            print("Sampai jumpa! Selamat belajar Prompt Engineering.")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
