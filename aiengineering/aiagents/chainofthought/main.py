#!/usr/bin/env python3
"""
CLI Runner Interaktif - Chain of Thought (CoT), Tree of Thought (ToT) & Tools Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Diagram Visual Architecture
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: CHAIN OF THOUGHT (CoT) & TOOLS WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (AI Agents -> CoT, ToT, Tool Definition & Examples){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Chain of Thought (CoT) Fundamentals ]{RESET}")
        print("  11. Zero-Shot CoT vs Few-Shot CoT vs Direct Prompting")
        print("  12. Self-Consistency CoT (Majority Voting & Sampling)")
        print("  13. Thought Execution & Action Parsing (<thought> & <action>)")
        
        print(f"\n{BOLD}[ Modul 2: Tree of Thought (ToT) & Multi-Path Reasoning ]{RESET}")
        print("  21. ToT Branching & Search Algorithms (BFS vs DFS)")
        print("  22. ToT State Evaluation, Pruning & Backtracking")

        print(f"\n{BOLD}[ Modul 3: Tool Definition & Schema Standardisation ]{RESET}")
        print("  31. Name, Description, Input & Output Schema Standard")
        print("  32. Tool Error Handling, Validation & Feedback Loop")
        print("  33. Tool Usage Examples & Few-Shot Demonstrations")

        print(f"\n{BOLD}[ Modul 4: Examples of Tools (6 Pilar Contoh Tool) ]{RESET}")
        print("  41. Web Search & Database Queries (Tools 1 & 3)")
        print("  42. Code Execution / REPL & File System Access (Tools 2 & 6)")
        print("  43. API Requests & Email / Slack / SMS Dispatcher (Tools 4 & 5)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31, 41): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Chain of Thought & Tools!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_chain_of_thought', '1_zero_and_few_shot_cot.py'),
            '12': os.path.join(base_dir, '01_chain_of_thought', '2_self_consistency_cot.py'),
            '13': os.path.join(base_dir, '01_chain_of_thought', '3_thought_execution_parsing.py'),
            '21': os.path.join(base_dir, '02_tree_of_thought', '1_tot_branching_and_search.py'),
            '22': os.path.join(base_dir, '02_tree_of_thought', '2_tot_evaluation_and_backtracking.py'),
            '31': os.path.join(base_dir, '03_tool_definition', '1_tool_schema_and_metadata.py'),
            '32': os.path.join(base_dir, '03_tool_definition', '2_tool_error_handling_validation.py'),
            '33': os.path.join(base_dir, '03_tool_definition', '3_tool_usage_examples_fewshot.py'),
            '41': os.path.join(base_dir, '04_examples_of_tools', '1_web_search_and_db_queries.py'),
            '42': os.path.join(base_dir, '04_examples_of_tools', '2_code_exec_and_filesystem.py'),
            '43': os.path.join(base_dir, '04_examples_of_tools', '3_api_requests_and_messaging.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

if __name__ == "__main__":
    main()
