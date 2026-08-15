#!/usr/bin/env python3
"""
CLI Runner Interaktif - Agent Architecture Workspace
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: AGENT ARCHITECTURE WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (AI Agents -> Common Architectures, Building Agents, Frameworks, Eval & Monitoring){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Common Architectures ]{RESET}")
        print("  11. RAG Agent & ReAct (Reason + Act) Agent Loop")
        print("  12. Planner-Executor Agent & DAG (Directed Acyclic Graph) Engine")
        print("  13. Multi-Agent Systems & Self-Critique / Reflection Loop")
        
        print(f"\n{BOLD}[ Modul 2: Building Agents ]{RESET}")
        print("  21. Manual Agent Construction (From Scratch: Loop, Parsing, Retries)")
        print("  22. LLM Native Function Calling (OpenAI, Gemini, Anthropic, Assistant API)")

        print(f"\n{BOLD}[ Modul 3: Building Using Frameworks ]{RESET}")
        print("  31. Frameworks Overview & Abstractions (LangChain, LangGraph, CrewAI, AutoGen, Smolagents, Agno)")

        print(f"\n{BOLD}[ Modul 4: Evaluation, Testing, Debugging & Monitoring ]{RESET}")
        print("  41. Agent Evaluation Metrics, Unit/Integration Testing & HITL")
        print("  42. Structured Logging, Tracing & Observability Formatters (LangSmith, LangFuse, Helicone, OpenLLMetry)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31, 41): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Agent Architecture!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_common_architectures', '1_rag_and_react_agents.py'),
            '12': os.path.join(base_dir, '01_common_architectures', '2_planner_executor_and_dag.py'),
            '13': os.path.join(base_dir, '01_common_architectures', '3_multi_agent_and_self_critique.py'),
            '21': os.path.join(base_dir, '02_building_agents', '1_manual_from_scratch.py'),
            '22': os.path.join(base_dir, '02_building_agents', '2_llm_native_function_calling.py'),
            '31': os.path.join(base_dir, '03_building_using_frameworks', '1_frameworks_overview.py'),
            '41': os.path.join(base_dir, '04_eval_testing_debugging_monitoring', '1_evaluation_and_testing.py'),
            '42': os.path.join(base_dir, '04_eval_testing_debugging_monitoring', '2_debugging_and_monitoring.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")


if __name__ == "__main__":
    main()
