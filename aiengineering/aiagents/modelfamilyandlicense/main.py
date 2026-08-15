#!/usr/bin/env python3
"""
CLI Runner Interaktif - Model Families, Licenses & Generation Controls Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Referensi
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: MODEL FAMILIES, LICENSES & GENERATION CONTROLS ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (Model Families and Licences & Generation Controls){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Open Weight Models & Licensing ]{RESET}")
        print("  11. Open Weight Model Landscape & Architecture Calculator (Dense vs MoE)")
        print("  12. Open Weight Licensing & Compliance Audit (Apache 2.0, MIT, Llama 3)")
        
        print(f"\n{BOLD}[ Modul 2: Closed Weight Models & Decision Matrix ]{RESET}")
        print("  21. Closed Weight API Ecosystems & Enterprise Capabilities (ZDR, SLAs)")
        print("  22. Tradeoff Decision Matrix & Architecture Selector (Open vs Closed)")

        print(f"\n{BOLD}[ Modul 3: Generation Controls (Gambar Referensi 1) ]{RESET}")
        print("  31. Temperature & Top-P (Nucleus) Sampling Visualizer")
        print("  32. Frequency & Presence Penalties Logit Adjustment Simulator")
        print("  33. Stopping Criteria & Max Length Truncated JSON Repair Engine")

        print(f"\n{BOLD}[ Modul 4: License Compliance & Deployment Architecture ]{RESET}")
        print("  41. Commercial License Auditor & Risk Evaluation Tool")
        print("  42. AI Agent Deployment Topology Architecture Advisor")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31, 41): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Model Families, Licenses & Generation Controls!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_open_weight_models', '1_open_weight_landscape_and_architectures.py'),
            '12': os.path.join(base_dir, '01_open_weight_models', '2_open_weight_licensing_and_compliance.py'),
            '21': os.path.join(base_dir, '02_closed_weight_models', '1_closed_weight_api_ecosystems.py'),
            '22': os.path.join(base_dir, '02_closed_weight_models', '2_tradeoff_matrix_open_vs_closed.py'),
            '31': os.path.join(base_dir, '03_generation_controls', '1_temperature_and_topp_sampling.py'),
            '32': os.path.join(base_dir, '03_generation_controls', '2_frequency_and_presence_penalties.py'),
            '33': os.path.join(base_dir, '03_generation_controls', '3_stopping_criteria_and_max_length.py'),
            '41': os.path.join(base_dir, '04_license_and_commercial_rights', '1_license_checker_and_compliance_tool.py'),
            '42': os.path.join(base_dir, '04_license_and_commercial_rights', '2_agent_deployment_arch_advisor.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

if __name__ == "__main__":
    main()
