#!/usr/bin/env python3
"""
CLI Runner Interaktif - Understand the Basics AI Agent Learning Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) - Understand the Basics
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: UNDERSTAND THE BASICS WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (roadmap.sh/ai-agents -> Understand the Basics){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Streamed vs Unstreamed Responses ]{RESET}")
        print("  11. Streamed (SSE / Chunked) vs Unstreamed (Blocking HTTP) Simulator & TTFT Analysis")
        
        print(f"\n{BOLD}[ Modul 2: Reasoning vs Standard Models ]{RESET}")
        print("  21. Reasoning Models (DeepSeek R1 / o1 / o3 CoT) vs Standard Models (GPT-4o / Claude 3.5)")

        print(f"\n{BOLD}[ Modul 3: Fine-Tuning vs Prompt Engineering ]{RESET}")
        print("  31. Decision Framework & ROI Simulator (Prompt Eng / Few-Shot / RAG vs LoRA Fine-Tuning)")

        print(f"\n{BOLD}[ Modul 4: Embeddings and Vector Search ]{RESET}")
        print("  41. Vector Embeddings, Cosine Similarity, Dot Product, & Lexical vs Semantic Search")

        print(f"\n{BOLD}[ Modul 5: Understand the Basics of RAG ]{RESET}")
        print("  51. End-to-End RAG Pipeline (Chunking -> Embedding -> Retrieval Top-K -> LLM Synthesis)")

        print(f"\n{BOLD}[ Modul 6: Pricing of Common Models ]{RESET}")
        print("  61. LLM Pricing Comparison (OpenAI, Anthropic, Gemini, DeepSeek), Caching, & Agent Loop Cost")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31, 41, 51, 61): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar Understand the Basics!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_streamed_vs_unstreamed', '1_streamed_vs_unstreamed_responses.py'),
            '21': os.path.join(base_dir, '02_reasoning_vs_standard', '1_reasoning_vs_standard_models.py'),
            '31': os.path.join(base_dir, '03_finetuning_vs_prompt_engineering', '1_finetuning_vs_prompt_engineering.py'),
            '41': os.path.join(base_dir, '04_embeddings_and_vector_search', '1_embeddings_and_vector_search.py'),
            '51': os.path.join(base_dir, '05_understand_basics_of_rag', '1_basics_of_rag.py'),
            '61': os.path.join(base_dir, '06_pricing_of_common_models', '1_pricing_of_common_models.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

if __name__ == "__main__":
    main()
