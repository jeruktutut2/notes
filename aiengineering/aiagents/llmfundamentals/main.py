#!/usr/bin/env python3
"""
CLI Runner Interaktif - LLM Fundamentals AI Agent Learning Workspace
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) - Model Mechanisms
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
        print(f"{BOLD}{HEADER}=== AI AGENTS: LLM FUNDAMENTALS & MODEL MECHANISMS WORKSPACE ==={RESET}")
        print("█"*70)
        print(f"{CYAN}Berdasarkan Roadmap.sh (Transformer Models & LLMs -> Model Mechanisms){RESET}")
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print(f"{BOLD}[ Modul 1: Tokenization Mechanics ]{RESET}")
        print("  11. Tokenization Algorithms (BPE, WordPiece, SentencePiece & Special Tokens)")
        print("  12. Tiktoken & Byte-level BPE Tokenizer Efficiency Analysis")
        print("  13. Tokenizer Security, Prompt Injection & Special Token Smuggling")
        
        print(f"\n{BOLD}[ Modul 2: Context Windows & Attention Mechanics ]{RESET}")
        print("  21. Context Window Anatomy & KV-Cache VRAM Calculator")
        print("  22. Positional Embeddings & Context Length Scaling (RoPE, ALiBi, YaRN)")
        print("  23. Effective Context Window, Lost in the Middle & Attention Sinks (NIAH)")

        print(f"\n{BOLD}[ Modul 3: Token-Based Pricing & Cost Optimization ]{RESET}")
        print("  31. Token Cost Calculator & Multi-Turn Agent Loop Estimation")
        print("  32. Prompt Caching Simulator (Prefix Matching, Cost & TTFT Latency)")
        print("  33. Token Budgeting & Rate Limiting (Token Bucket & Agent Guardrails)")

        print(f"\n{BOLD}[ Modul 4: Transformer Architecture & Decoding ]{RESET}")
        print("  41. Attention Mechanism & Transformer Variants (MHA vs MQA vs GQA)")
        print("  42. Autoregressive Sampling (Temp, Top-P, Top-K) & Speculative Decoding")

        print(f"\n{BOLD}[ Modul 5: Model Selection & Kuantisasi ]{RESET}")
        print("  51. Open Weight vs Closed API Model Selection Matrix")
        print("  52. Quantization & Local Execution (GGUF, AWQ, VRAM Calculator)")

        print(f"\n{BOLD}[ Modul 6: Evaluasi & Benchmarks LLM ]{RESET}")
        print("  61. Standard Benchmarks & Pass@k Coding Metrics")
        print("  62. LLM-as-a-Judge Pattern & Bias Mitigation (Position/Verbosity)")

        print(f"\n  {BOLD}0. Keluar{RESET}")

        try:
            choice = input(f"\n{YELLOW}Masukkan nomor pilihan (e.g. 11, 21, 31): {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nKeluar dari program.")
            sys.exit(0)

        if choice == '0':
            print("\nTerima kasih telah belajar LLM Fundamentals!")
            sys.exit(0)

        script_map = {
            '11': os.path.join(base_dir, '01_tokenization', '1_bpe_wordpiece_sentencepiece.py'),
            '12': os.path.join(base_dir, '01_tokenization', '2_tiktoken_and_tokenizer_mechanics.py'),
            '13': os.path.join(base_dir, '01_tokenization', '3_tokenizer_security_and_edge_cases.py'),
            '21': os.path.join(base_dir, '02_context_windows', '1_context_window_anatomy_and_kv_cache.py'),
            '22': os.path.join(base_dir, '02_context_windows', '2_positional_embeddings_and_scaling.py'),
            '23': os.path.join(base_dir, '02_context_windows', '3_effective_context_window_and_attention_sinks.py'),
            '31': os.path.join(base_dir, '03_token_based_pricing', '1_token_cost_calculator_and_estimation.py'),
            '32': os.path.join(base_dir, '03_token_based_pricing', '2_prompt_caching_and_cost_optimization.py'),
            '33': os.path.join(base_dir, '03_token_based_pricing', '3_token_budgeting_and_rate_limiting.py'),
            '41': os.path.join(base_dir, '04_transformer_architecture', '1_attention_mechanism_and_transformers.py'),
            '42': os.path.join(base_dir, '04_transformer_architecture', '2_autoregressive_generation_and_decoding.py'),
            '51': os.path.join(base_dir, '05_model_selection_and_quantization', '1_open_vs_closed_source_models.py'),
            '52': os.path.join(base_dir, '05_model_selection_and_quantization', '2_quantization_and_local_execution.py'),
            '61': os.path.join(base_dir, '06_evaluasi_dan_benchmarks', '1_standard_benchmarks_and_metrics.py'),
            '62': os.path.join(base_dir, '06_evaluasi_dan_benchmarks', '2_llm_as_a_judge_and_eval_frameworks.py'),
        }

        if choice in script_map:
            run_script(script_map[choice])
        else:
            print(f"\n{RED}Pilihan tidak valid. Silakan coba lagi.{RESET}")

if __name__ == "__main__":
    main()
