#!/usr/bin/env python3
"""
Modul 2.1: Closed Weight API Ecosystems & Enterprise Capabilities
Katalog Provider API Komersial, Fitur Enterprise Privasi (ZDR), SLA & Pricing Multi-Provider
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

@dataclass
class ClosedApiModel:
    name: str
    provider: str
    input_price_per_m: float   # USD per Million Tokens
    output_price_per_m: float  # USD per Million Tokens
    cached_input_price_per_m: float
    max_context_window: int     # in Tokens
    supports_zdr: bool          # Zero Data Retention
    batch_api_discount: float   # Percentage (e.g. 0.50 for 50%)
    specialized_features: List[str]

CLOSED_MODELS: List[ClosedApiModel] = [
    ClosedApiModel(
        name="GPT-4o",
        provider="OpenAI",
        input_price_per_m=2.50,
        output_price_per_m=10.00,
        cached_input_price_per_m=1.25,
        max_context_window=128000,
        supports_zdr=True,
        batch_api_discount=0.50,
        specialized_features=["Native Multimodal", "Structured JSON Outputs", "High Tool Calling Accuracy"]
    ),
    ClosedApiModel(
        name="o3-mini",
        provider="OpenAI",
        input_price_per_m=1.10,
        output_price_per_m=4.40,
        cached_input_price_per_m=0.55,
        max_context_window=200000,
        supports_zdr=True,
        batch_api_discount=0.50,
        specialized_features=["Reasoning Tokens", "STEM & Coding SOTA", "Flexible Effort Parameter"]
    ),
    ClosedApiModel(
        name="Claude 3.5 Sonnet",
        provider="Anthropic",
        input_price_per_m=3.00,
        output_price_per_m=15.00,
        cached_input_price_per_m=0.30,  # Prompt Caching discount up to 90%
        max_context_window=200000,
        supports_zdr=True,
        batch_api_discount=0.50,
        specialized_features=["Best Agentic Coding", "Computer Use API", "Artifacts Generation"]
    ),
    ClosedApiModel(
        name="Claude 3.5 Haiku",
        provider="Anthropic",
        input_price_per_m=0.80,
        output_price_per_m=4.00,
        cached_input_price_per_m=0.08,
        max_context_window=200000,
        supports_zdr=True,
        batch_api_discount=0.50,
        specialized_features=["Ultra Fast Latency", "Cost-Effective Worker Agent", "Lightweight Agent Loop"]
    ),
    ClosedApiModel(
        name="Gemini 2.0 Flash",
        provider="Google Cloud",
        input_price_per_m=0.10,
        output_price_per_m=0.40,
        cached_input_price_per_m=0.025,
        max_context_window=1000000,
        supports_zdr=True,
        batch_api_discount=0.50,
        specialized_features=["1M Token Context", "Native Audio/Video Streaming", "Sub-second Latency"]
    ),
    ClosedApiModel(
        name="DeepSeek V3 API",
        provider="DeepSeek Cloud",
        input_price_per_m=0.14,
        output_price_per_m=0.28,
        cached_input_price_per_m=0.014,  # Context cache discount ~90%
        max_context_window=64000,
        supports_zdr=False,
        batch_api_discount=0.0,
        specialized_features=["Unbeatable Open API Price", "DeepSeek R1 Thinking", "OpenAI Compatible API"]
    )
]

def display_closed_models_catalog():
    print(f"\n{BOLD}{HEADER}=== KATALOG CLOSED WEIGHT MODEL API & ENTERPRISE PRICING ==={RESET}\n")
    print(f"{'Nama Model':<18} | {'Provider':<13} | {'Input $/M':<10} | {'Output $/M':<11} | {'Cached $/M':<11} | {'ZDR?':<5}")
    print("-" * 85)
    for m in CLOSED_MODELS:
        zdr_str = f"{GREEN}Ya{RESET}" if m.supports_zdr else f"{YELLOW}Tdk{RESET}"
        print(f"{CYAN}{m.name:<18}{RESET} | {m.provider:<13} | ${m.input_price_per_m:>8.2f} | ${m.output_price_per_m:>9.2f} | ${m.cached_input_price_per_m:>9.3f} | {zdr_str:<5}")

def run_enterprise_feature_explanation():
    print(f"\n{BOLD}{HEADER}=== SEKURITAS & ENTERPRISE DATA PRIVACY IN CLOSED APIS ==={RESET}\n")
    print(f"1. {BOLD}{CYAN}Zero Data Retention (ZDR):{RESET}")
    print("   • Provider API (seperti OpenAI Enterprise & Anthropic API) menjamin data prompt & output")
    print("     TIDAK disimpan di server provider dan TIDAK DUGUNAKAN untuk melatih model publik.")
    print("   • Esensial untuk sektor Perbankan, Kesehatan (HIPAA), dan Legal Compliance.")

    print(f"\n2. {BOLD}{CYAN}Batch API (Asynchronous Processing):{RESET}")
    print("   • Diskon biaya 50% untuk permintaan yang tidak membutuhkan latensi *real-time* (SLA 24 jam).")
    print("   • Sangat efektif untuk skenario background agent: Data scraping, dokumentasi otomatis, & offline evaluation.")

    print(f"\n3. {BOLD}{CYAN}Prompt Caching:{RESET}")
    print("   • Menyimpan prefix prompt (misal: System Prompt / RAG Context yang besar) di memori cache server.")
    print("   • Mengurangi biaya input token hingga 50% - 90% dan memangkas Time-To-First-Token (TTFT).")

def run_multi_agent_cost_simulator():
    print(f"\n{BOLD}{HEADER}=== SIMULATOR BIAYA AGENT VOLUME TINGGI (100,000 PERMINTAAN/HARI) ==={RESET}")
    print("Asumsi Skenario Agent Workflow:")
    print(" • Average Input Prompt  : 2,000 tokens (System prompt + Context)")
    print(" • Average Cached Tokens : 1,500 tokens (75% cache hit rate)")
    print(" • Average Output Tokens : 500 tokens\n")
    
    daily_requests = 100000
    avg_input_m = (daily_requests * 500) / 1000000.0          # Uncached (500 tokens)
    avg_cached_m = (daily_requests * 1500) / 1000000.0        # Cached (1500 tokens)
    avg_output_m = (daily_requests * 500) / 1000000.0         # Output (500 tokens)

    print(f"{'Nama Model':<18} | {'Biaya Input/Hari':<17} | {'Biaya Output/Hari':<17} | {'Total Biaya/Bulan':<20}")
    print("-" * 80)

    for m in CLOSED_MODELS:
        input_cost = (avg_input_m * m.input_price_per_m) + (avg_cached_m * m.cached_input_price_per_m)
        output_cost = avg_output_m * m.output_price_per_m
        daily_total = input_cost + output_cost
        monthly_total = daily_total * 30.0

        print(f"{CYAN}{m.name:<18}{RESET} | ${input_cost:>15.2f} | ${output_cost:>15.2f} | {BOLD}{GREEN}${monthly_total:>17.2f}{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 2.1: CLOSED WEIGHT API ECOSYSTEMS & ENTERPRISE CAPABILITIES{RESET}")
    print(f"{CYAN}Berdasarkan roadmap.sh/ai-agents (Model Families and Licences){RESET}")
    print("█" * 75)

    display_closed_models_catalog()
    run_enterprise_feature_explanation()
    run_multi_agent_cost_simulator()

    print(f"\n{GREEN}✔ Modul 2.1 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
