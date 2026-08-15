#!/usr/bin/env python3
"""
Modul 2.2: Tradeoff Matrix Open Weight vs Closed Weight
Matrix Keputusan Multi-Kriteria & Interactive Architecture Selector untuk AI Agent Systems
Berdasarkan Roadmap.sh / AI Agents - Model Families and Licences
"""

import sys
from dataclasses import dataclass
from typing import List, Dict

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_tradeoff_matrix():
    print(f"\n{BOLD}{HEADER}=== TRADEOFF MATRIX: OPEN WEIGHT VS CLOSED WEIGHT APIS ==={RESET}\n")
    
    matrix_data = [
        ("Privasi Data & Sekuritas", "100% Lokal / On-Prem. Data tidak pernah keluar dari jaringan.", "Tergantung Klausa ZDR (Zero Data Retention) Provider Cloud."),
        ("Struktur Biaya", "CapEx + Fixed OpEx (Listrik/GPU Rent). Murah pada volume tinggi.", "Variable OpEx (Pay-per-Token). Sangat murah untuk awal, mahal di skala raksasa."),
        ("Latensi & Throughput", "Sangat rendah & terprediksi (Edge/Local vLLM). Bebas Rate Limit API.", "Tergantung latensi jaringan API external & Rate Limit (RPM/TPM)."),
        ("Reasoning & SOTA Quality", "Tinggi (DeepSeek R1, Llama 3.3 70B), namun perlu GPU besar.", "State-of-the-Art Tertinggi (Claude 3.5 Sonnet, GPT-4o, o3-mini)."),
        ("Customizability & Weights", "Dapat di-fine-tune (LoRA/Full), bobot model milik penuh.", "Terbatas pada System Prompt & Fine-Tuning API berbayar yang terbatas."),
        ("Operasional Maintenance", "Tinggi (Memerlukan MLOps, vLLM, Health Checks, Cluster GPU).", "Nol (Zero Infra Overhead, Provider mengelola ketersediaan server).")
    ]

    print(f"{'Kriteria Evaluasi':<25} | {'Open Weight Models (Local/Self-Hosted)':<40} | {'Closed Weight Models (Proprietary API)':<40}")
    print("-" * 110)
    for kriteria, open_desc, closed_desc in matrix_data:
        print(f"{BOLD}{CYAN}{kriteria:<25}{RESET} | {YELLOW}{open_desc:<40}{RESET} | {GREEN}{closed_desc:<40}{RESET}")

def run_architectural_advisor():
    print(f"\n{BOLD}{HEADER}=== INTERACTIVE AI AGENT ARCHITECTURE SELECTOR ==={RESET}")
    print("Sistem ini membantu menentukan paduan model terbaik untuk skenario AI Agent Anda.\n")

    try:
        print(f"{BOLD}1. Apakah ada regulasi privasi ketat (misal: Data Medis/Bank dilarang keluar jaringan)?:{RESET}")
        print("   a) Ya, WAJIB 100% On-Premises / Offline Network")
        print("   b) Tidak, Cloud ZDR (Zero Data Retention) diperbolehkan")
        print("   c) Bebas (Public Cloud API biasa)")
        q_privacy = input("Pilihan (a/b/c): ").strip().lower()

        print(f"\n{BOLD}2. Berapa estimasi volume token harian AI Agent Anda?:{RESET}")
        print("   a) Low (< 1 Juta token / hari)")
        print("   b) Medium (1 - 50 Juta token / hari)")
        print("   c) Ultra-High (> 100 Juta token / hari)")
        q_volume = input("Pilihan (a/b/c): ").strip().lower()

        print(f"\n{BOLD}3. Seberapa kompleks kebutuhan Reasoning / Coding / Tool Calling?:{RESET}")
        print("   a) Sederhana (Ekstraksi data, RAG biasa, Summarization)")
        print("   b) Menengah (Multi-turn tool calling, JSON formatting)")
        print("   c) Sangat Kompleks (Autonomous Agent, SOTA Coding, Deep Reasoning)")
        q_complexity = input("Pilihan (a/b/c): ").strip().lower()

        print(f"\n{BOLD}{GREEN}================ REKOMENDASI ARSITEKTUR MODEL ================={RESET}\n")

        if q_privacy == 'a':
            print(f"🔒 {BOLD}STRATEGI RECOMMENDED: PURE OPEN WEIGHT ON-PREMISES{RESET}")
            print(" • Master Reasoner Agent : Llama 3.3 70B (INT4 GGUF) atau Qwen 2.5 72B pada Local GPU Node.")
            print(" • Task Worker / Router  : Llama 3.1 8B atau Phi-4 14B.")
            print(" • Engine Recommendation : vLLM / Ollama dengan Tensor Parallelism.")
            print(" • Keuntungan Key        : Data 100% aman dalam firewall perusahaan.")
        
        elif q_volume == 'c' and q_complexity != 'c':
            print(f"⚡ {BOLD}STRATEGI RECOMMENDED: HYBRID / LOCAL DEEPSEEK MOE COST OPTIMIZER{RESET}")
            print(" • Primary Model         : DeepSeek V3 / Mixtral 8x7B Self-Hosted atau DeepSeek Cloud API.")
            print(" • Fast Worker Model     : Gemini 2.0 Flash (untuk routing & prompt caching).")
            print(" • Keuntungan Key        : Efisiensi biaya hingga 90% pada volume 100M+ token.")

        else:
            print(f"🚀 {BOLD}STRATEGI RECOMMENDED: CLOSED API ORCHESTRATOR + HYBRID ROUTING{RESET}")
            print(" • Master Reasoner Agent : Claude 3.5 Sonnet / GPT-4o (Reasoning & Complex Tool Use).")
            print(" • Fast/Cheap Sub-Agent  : Gemini 2.0 Flash / Claude 3.5 Haiku / Llama 3.1 8B Local.")
            print(" • Keuntungan Key        : Kecepatan pengembangan maksimal dengan SOTA AI capabilities.")

    except ValueError:
        print(f"{RED}Input tidak valid.{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 2.2: TRADEOFF MATRIX OPEN WEIGHT VS CLOSED WEIGHT{RESET}")
    print(f"{CYAN}Berdasarkan roadmap.sh/ai-agents (Model Families and Licences){RESET}")
    print("█" * 75)

    print_tradeoff_matrix()
    run_architectural_advisor()

    print(f"\n{GREEN}✔ Modul 2.2 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
