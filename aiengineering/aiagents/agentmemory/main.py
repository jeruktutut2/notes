#!/usr/bin/env python3
"""
CLI Runner Interaktif - Agent Memory Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Diagram Visual Architecture Component
"""

import os
import sys
import subprocess

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


def run_script(script_path: str):
    print(f"\n{'='*70}")
    print(f"Menjalankan: {YELLOW}{os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}{RESET}")
    print(f"{'='*70}\n")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n{RED}[ERROR] Gagal menjalankan skrip: {e}{RESET}")
    except FileNotFoundError:
        print(f"\n{RED}[ERROR] File tidak ditemukan: {script_path}{RESET}")
    print(f"\n{'='*70}\n")


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "█"*70)
        print(f"{BOLD}{HEADER}=== AI AGENTS: AGENT MEMORY WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (AI Agents -> What is Agent Memory, Episodic vs Semantic, Maintaining Memory){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: What is Agent Memory? ]{RESET}")
        print("  11. Short-Term Memory (Within Prompt / Context Window)")
        print("  12. Long-Term Memory (Persistent Vector DB / SQL Store)")
        
        print(f"\n{BOLD}[ Modul 2: Episodic vs Semantic Memory ]{RESET}")
        print("  21. Episodic Memory (Event Sequence & Execution Trajectories)")
        print("  22. Semantic Memory (Factual Knowledge & Entity Stores)")

        print(f"\n{BOLD}[ Modul 3: Maintaining Memory ]{RESET}")
        print("  31. RAG and Vector Databases (Cosine Similarity Search)")
        print("  32. User Profile Storage (Structured Preferences)")
        print("  33. Summarization / Compression (Summary Buffer Memory)")
        print("  34. Forgetting / Aging Strategies (Decay Curve & Eviction)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Agent Memory!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_what_is_agent_memory', '1_short_term_memory_prompt.py'),
            '12': os.path.join(base_dir, '01_what_is_agent_memory', '2_long_term_memory_external.py'),
            '21': os.path.join(base_dir, '02_episodic_vs_semantic_memory', '1_episodic_memory_events.py'),
            '22': os.path.join(base_dir, '02_episodic_vs_semantic_memory', '2_semantic_memory_facts.py'),
            '31': os.path.join(base_dir, '03_maintaining_memory', '1_rag_and_vector_databases.py'),
            '32': os.path.join(base_dir, '03_maintaining_memory', '2_user_profile_storage.py'),
            '33': os.path.join(base_dir, '03_maintaining_memory', '3_summarization_and_compression.py'),
            '34': os.path.join(base_dir, '03_maintaining_memory', '4_forgetting_and_aging_strategies.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")


if __name__ == "__main__":
    main()
