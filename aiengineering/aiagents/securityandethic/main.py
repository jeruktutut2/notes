#!/usr/bin/env python3
"""
CLI Runner Interaktif - AI Agent Security & Ethics Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Topik Security & Ethics:
1. Prompt Injection / Jailbreaks
2. Tool Sandboxing / Permissioning
3. Data Privacy + PII Redaction
4. Bias & Toxicity Guardrails
5. Safety + Red Team Testing
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: SECURITY & ETHICS WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (AI Agents -> Security & Ethic){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Prompt Injection / Jailbreaks ]{RESET}")
        print("  11. Direct & Indirect Prompt Injection Simulation")
        print("  12. Jailbreak Defense, Delimiters & Guardrail Filter")
        
        print(f"\n{BOLD}[ Modul 2: Tool Sandboxing / Permissioning ]{RESET}")
        print("  21. Tool Permissioning, RBAC & Human-in-the-Loop (HITL)")
        print("  22. Sandboxed Execution Environment (AST & Directory Jail)")

        print(f"\n{BOLD}[ Modul 3: Data Privacy + PII Redaction ]{RESET}")
        print("  31. PII Detection & Masking (Email, NIK, Phone, Credit Card)")
        print("  32. Privacy-Preserving Agent Memory (TTL & Right to be Forgotten)")

        print(f"\n{BOLD}[ Modul 4: Bias & Toxicity Guardrails ]{RESET}")
        print("  41. Input & Output Guardrails Pipeline")
        print("  42. Bias Mitigation & System Steering")

        print(f"\n{BOLD}[ Modul 5: Safety + Red Team Testing ]{RESET}")
        print("  51. Automated Red Teaming Harness")
        print("  52. Safety Evaluation & Benchmark Reporting (ASR / Precision / Recall)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31, 41, 51): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar AI Agent Security & Ethics!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_prompt_injection_jailbreaks', '1_direct_and_indirect_prompt_injection.py'),
            '12': os.path.join(base_dir, '01_prompt_injection_jailbreaks', '2_jailbreak_defense_and_delimiters.py'),
            '21': os.path.join(base_dir, '02_tool_sandboxing_permissioning', '1_tool_permission_and_rbac.py'),
            '22': os.path.join(base_dir, '02_tool_sandboxing_permissioning', '2_sandboxed_execution_environment.py'),
            '31': os.path.join(base_dir, '03_data_privacy_pii_redaction', '1_pii_detection_and_redaction.py'),
            '32': os.path.join(base_dir, '03_data_privacy_pii_redaction', '2_privacy_preserving_agent_memory.py'),
            '41': os.path.join(base_dir, '04_bias_toxicity_guardrails', '1_input_output_guardrails.py'),
            '42': os.path.join(base_dir, '04_bias_toxicity_guardrails', '2_bias_mitigation_and_steering.py'),
            '51': os.path.join(base_dir, '05_safety_red_team_testing', '1_automated_red_teaming.py'),
            '52': os.path.join(base_dir, '05_safety_red_team_testing', '2_safety_eval_and_benchmarks.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")


if __name__ == "__main__":
    main()
