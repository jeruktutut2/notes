#!/usr/bin/env python3
"""
CLI Runner Interaktif - Agent Loop AI Agent Learning Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) - Agent Loop Architecture & Example Usecases
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: AGENT LOOP WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (AI Agents -> Agent Loop & Example Usecases){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Perception / User Input ]{RESET}")
        print("  11. Perception & User Input Parsing")
        print("  12. Input Sanitization, Prompt Injection & Guardrails")
        
        print(f"\n{BOLD}[ Modul 2: Reason and Plan ]{RESET}")
        print("  21. ReAct Reasoning (Thought-Action-Observation) & CoT")
        print("  22. Task Decomposition & DAG Planning")

        print(f"\n{BOLD}[ Modul 3: Acting / Tool Invocation ]{RESET}")
        print("  31. Tool Definition (JSON Schema) & Function Calling")
        print("  32. Action Execution, Retry Logic & Fallback Error Handling")

        print(f"\n{BOLD}[ Modul 4: Observation & Reflection ]{RESET}")
        print("  41. Observation Processing & Working Memory (Sliding Window)")
        print("  42. Reflection, Self-Correction & Termination Criteria")

        print(f"\n{BOLD}[ Modul 5: Agent Loop Architecture ]{RESET}")
        print("  51. End-to-End Autonomous Agent Loop Engine")

        print(f"\n{BOLD}[ Modul 6: Example Usecases (Sesuai Diagram) ]{RESET}")
        print("  61. Personal Assistant Agent (Calendar & Agenda Manager)")
        print("  62. Code Generation Agent (Write, Test & Auto-Debug Loop)")
        print("  63. Data Analysis Agent (Tabular Data Aggregation & Insights)")
        print("  64. Web Scraping / Crawling Agent (URL Scraping & Link Extraction)")
        print("  65. NPC / Game AI Agent (RPG World State, Perception & Action)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 51, 61): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Agent Loop!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_perception_user_input', '1_perception_and_input_parsing.py'),
            '12': os.path.join(base_dir, '01_perception_user_input', '2_input_sanitization_and_guardrails.py'),
            '21': os.path.join(base_dir, '02_reason_and_plan', '1_react_reasoning_and_cot.py'),
            '22': os.path.join(base_dir, '02_reason_and_plan', '2_planning_and_task_decomposition.py'),
            '31': os.path.join(base_dir, '03_acting_tool_invocation', '1_tool_definition_and_function_calling.py'),
            '32': os.path.join(base_dir, '03_acting_tool_invocation', '2_action_execution_and_error_handling.py'),
            '41': os.path.join(base_dir, '04_observation_reflection', '1_observation_processing_and_memory.py'),
            '42': os.path.join(base_dir, '04_observation_reflection', '2_reflection_self_correction_and_termination.py'),
            '51': os.path.join(base_dir, '05_agent_loop_architecture', '1_full_agent_loop_engine.py'),
            '61': os.path.join(base_dir, '06_example_usecases', '1_personal_assistant_agent.py'),
            '62': os.path.join(base_dir, '06_example_usecases', '2_code_generation_agent.py'),
            '63': os.path.join(base_dir, '06_example_usecases', '3_data_analysis_agent.py'),
            '64': os.path.join(base_dir, '06_example_usecases', '4_web_scraping_crawling_agent.py'),
            '65': os.path.join(base_dir, '06_example_usecases', '5_npc_game_ai_agent.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

if __name__ == "__main__":
    main()
