#!/usr/bin/env python3
"""
PROMPT ENGINEERING LEARNING WORKSPACE - CLI LAUNCHER
=====================================================
Modul Pembelajaran Prompt Engineering Berdasarkan roadmap.sh/ai-agents & Diagram Visual "Writing Good Prompts".

Pilihan Modul:
1. Be specific in what you want & Role Prompting (01_be_specific_and_role_prompting)
2. Provide additional context & Grounding (02_provide_additional_context)
3. Use relevant technical terms & Attention Steering (03_technical_terms_and_domain_jargon)
4. Use Examples in your Prompt & Few-Shot Learning (04_use_examples_few_shot)
5. Iterate and Test your Prompts & Benchmark (05_iterate_and_test_prompts)
6. Specify Length, format etc. & Structured Output (06_specify_length_and_format)
7. Jalankan Seluruh Simulasi (Batch Runner)
8. Keluar
"""

import sys
import os
import subprocess
import time

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODULES = [
    ("01", "Be Specific in What You Want & Role Prompting", os.path.join(BASE_DIR, "01_be_specific_and_role_prompting", "main.py")),
    ("02", "Provide Additional Context & Grounding Data", os.path.join(BASE_DIR, "02_provide_additional_context", "main.py")),
    ("03", "Use Relevant Technical Terms & Attention Steering", os.path.join(BASE_DIR, "03_technical_terms_and_domain_jargon", "main.py")),
    ("04", "Use Examples in Your Prompt & Few-Shot Learning", os.path.join(BASE_DIR, "04_use_examples_few_shot", "main.py")),
    ("05", "Iterate and Test Your Prompts & Benchmark Suite", os.path.join(BASE_DIR, "05_iterate_and_test_prompts", "main.py")),
    ("06", "Specify Length, Format Etc. & Structured Output", os.path.join(BASE_DIR, "06_specify_length_and_format", "main.py")),
]

def print_banner():
    print(f"\n{BOLD}{CYAN}╔═════════════════════════════════════════════════════════════════════════╗")
    print(f"║{YELLOW}      PROMPT ENGINEERING FOR AI AGENTS - ROADMAP.SH LEARNING WORKSPACE   {CYAN}║")
    print(f"╠═════════════════════════════════════════════════════════════════════════╣")
    print(f"║ {GREEN}Berdasarkan diagram roadmap visual: Writing Good Prompts                 {CYAN}║")
    print(f"╚═════════════════════════════════════════════════════════════════════════╝{RESET}\n")

def print_menu():
    print_banner()
    print(f"{BOLD}Daftar Modul Pembelajaran Interaktif:{RESET}\n")
    for code, title, _ in MODULES:
        print(f"  {BOLD}{GREEN}[{code}]{RESET} {title}")
    print(f"  {BOLD}{YELLOW}[07]{RESET} Jalankan Seluruh Modul (Full Batch Test)")
    print(f"  {BOLD}{RED}[08]{RESET} Keluar\n")

def run_script(script_path: str):
    if not os.path.exists(script_path):
        print(f"{RED}Error: File skrip tidak ditemukan di {script_path}{RESET}")
        return
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"{RED}Eror saat menjalankan skrip {script_path}: {e}{RESET}")
    except KeyboardInterrupt:
        print(f"\n{YELLOW}Eksekusi dibatalkan oleh pengguna.{RESET}")

def run_all():
    print(f"\n{BOLD}{MAGENTA}🚀 MENJALANKAN SELURUH MODUL SIMULASI PROMPT ENGINEERING...{RESET}\n")
    for code, title, script_path in MODULES:
        print(f"\n{BOLD}{BLUE}========================================================================={RESET}")
        print(f"{BOLD}{YELLOW}>>> JALANKAN MODUL {code}: {title.upper()}{RESET}")
        print(f"{BOLD}{BLUE}========================================================================={RESET}")
        run_script(script_path)
        time.sleep(0.5)

def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ["--all", "-a", "all", "07", "7"]:
            run_all()
            return
        elif arg.isdigit() and 1 <= int(arg) <= 6:
            idx = int(arg) - 1
            run_script(MODULES[idx][2])
            return

    while True:
        print_menu()
        choice = input(f"{BOLD}Masukkan nomor pilihan (01-08): {RESET}").strip()
        
        if choice in ["01", "1"]:
            run_script(MODULES[0][2])
        elif choice in ["02", "2"]:
            run_script(MODULES[1][2])
        elif choice in ["03", "3"]:
            run_script(MODULES[2][2])
        elif choice in ["04", "4"]:
            run_script(MODULES[3][2])
        elif choice in ["05", "5"]:
            run_script(MODULES[4][2])
        elif choice in ["06", "6"]:
            run_script(MODULES[5][2])
        elif choice in ["07", "7"]:
            run_all()
        elif choice in ["08", "8", "exit", "quit", "q"]:
            print(f"\n{GREEN}Terima kasih telah belajar Prompt Engineering AI Agents! Sampai jumpa.{RESET}\n")
            break
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan masukkan nomor 01-08.{RESET}\n")
            time.sleep(0.8)

if __name__ == "__main__":
    main()
