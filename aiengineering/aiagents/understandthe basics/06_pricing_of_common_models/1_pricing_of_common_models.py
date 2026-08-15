#!/usr/bin/env python3
"""
Modul 6: Pricing of Common Models & Cost Optimization Simulator
Kalkulator dan simulator estimasi biaya operasional LLM populer (OpenAI, Anthropic, Google, DeepSeek),
Input vs Output Token Pricing, Prompt Caching Discounts, serta simulasi Multi-Turn Agent Loop.
"""

from dataclasses import dataclass
from typing import Dict, List

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
class ModelPricing:
    model_name: str
    provider: str
    input_usd_per_1m: float
    cached_input_usd_per_1m: float
    output_usd_per_1m: float

MODEL_CATALOG: Dict[str, ModelPricing] = {
    "gpt-4o": ModelPricing("GPT-4o", "OpenAI", 2.50, 1.25, 10.00),
    "o3-mini": ModelPricing("o3-mini (Reasoning)", "OpenAI", 1.10, 0.55, 4.40),
    "claude-3-5-sonnet": ModelPricing("Claude 3.5 Sonnet", "Anthropic", 3.00, 0.30, 15.00),
    "gemini-2-0-flash": ModelPricing("Gemini 2.0 Flash", "Google", 0.10, 0.025, 0.40),
    "deepseek-v3": ModelPricing("DeepSeek V3", "DeepSeek", 0.14, 0.014, 0.28),
    "deepseek-r1": ModelPricing("DeepSeek R1 (Reasoning)", "DeepSeek", 0.55, 0.14, 2.19),
}

def calculate_single_call_cost(model_key: str, input_tokens: int, output_tokens: int, is_cached: bool = False) -> float:
    p = MODEL_CATALOG[model_key]
    in_rate = p.cached_input_usd_per_1m if is_cached else p.input_usd_per_1m
    cost_in = (input_tokens / 1_000_000.0) * in_rate
    cost_out = (output_tokens / 1_000_000.0) * p.output_usd_per_1m
    return cost_in + cost_out

def simulate_agent_multi_turn_loop(model_key: str, turns: int = 5, base_prompt_tokens: int = 2000, new_input_per_turn: int = 500, output_per_turn: int = 300, use_caching: bool = True) -> tuple[float, int, int]:
    """Simulasi akumulasi biaya agent multi-step loop.
    Pada setiap turn, sejarah chat bertambah (accumulation), sehingga input token terus membengkak.
    """
    total_cost = 0.0
    total_input = 0
    total_output = 0
    current_history_tokens = base_prompt_tokens

    for turn in range(1, turns + 1):
        input_for_this_turn = current_history_tokens + new_input_per_turn
        
        # Turn pertama = fresh input. Turn berikutnya = cached jika caching enabled
        cached_this_turn = (turn > 1) and use_caching
        
        cost = calculate_single_call_cost(model_key, input_for_this_turn, output_per_turn, is_cached=cached_this_turn)
        total_cost += cost
        total_input += input_for_this_turn
        total_output += output_per_turn

        # Akumulasi riwayat untuk turn berikutnya
        current_history_tokens = input_for_this_turn + output_per_turn

    return total_cost, total_input, total_output

def run_demo():
    print(f"\n{BOLD}{HEADER}=== PRICING OF COMMON MODELS & COST ESTIMATOR ==={RESET}\n")
    print(f"{CYAN}Tabel Tarif Resmi Provider LLM (per 1 Juta Tokens / 1M Tokens):{RESET}\n")

    print(f"┌────────────────────────┬───────────┬──────────────────┬──────────────────┬──────────────────┐")
    print(f"│ Model                  │ Provider  │ Standard Input   │ Cached Input     │ Output Tokens    │")
    print(f"├────────────────────────┼───────────┼──────────────────┼──────────────────┼──────────────────┤")
    
    for key, p in MODEL_CATALOG.items():
        print(f"│ {p.model_name:<22} │ {p.provider:<9} │ ${p.input_usd_per_1m:<15.2f} │ ${p.cached_input_usd_per_1m:<16.3f} │ ${p.output_usd_per_1m:<15.2f} │")
    print(f"└────────────────────────┴───────────┴──────────────────┴──────────────────┴──────────────────┘")

    print(f"\n{'='*80}\n")
    print(f"{BOLD}[ SKENARIO 1: SINGLE REQUEST BIAYA STANDAR ]{RESET}")
    print("Permintaan: Prompt System + RAG (5,000 Input Tokens), Jawaban Agent (800 Output Tokens)\n")

    print(f"┌────────────────────────┬─────────────────────┬─────────────────────┐")
    print(f"│ Model                  │ Biaya Non-Cached    │ Biaya Prompt Cache  │")
    print(f"├────────────────────────┼─────────────────────┼─────────────────────┤")
    for key, p in MODEL_CATALOG.items():
        cost_normal = calculate_single_call_cost(key, 5000, 800, is_cached=False)
        cost_cached = calculate_single_call_cost(key, 5000, 800, is_cached=True)
        print(f"│ {p.model_name:<22} │ ${cost_normal:<19.5f} │ {GREEN}${cost_cached:<19.5f}{RESET} │")
    print(f"└────────────────────────┴─────────────────────┴─────────────────────┘")

    print(f"\n{'='*80}\n")
    print(f"{BOLD}[ SKENARIO 2: MULTI-STEP AGENT LOOP (5 ITERASI TURN) ]{RESET}")
    print("Skenario: ReAct Agent mengeksekusi 5 langkah pencarian & analisis kode.\n")

    for key in ["gpt-4o", "claude-3-5-sonnet", "gemini-2-0-flash", "deepseek-v3"]:
        m_name = MODEL_CATALOG[key].model_name
        cost_no_cache, in_tok, out_tok = simulate_agent_multi_turn_loop(key, turns=5, use_caching=False)
        cost_cache, _, _ = simulate_agent_multi_turn_loop(key, turns=5, use_caching=True)
        
        savings_pct = ((cost_no_cache - cost_cache) / cost_no_cache) * 100
        
        print(f"🔹 {BOLD}{m_name}{RESET}:")
        print(f"  • Total Input Tokens Accumulated : {in_tok:,} tokens")
        print(f"  • Total Output Tokens Generated  : {out_tok:,} tokens")
        print(f"  • Biaya Tanpa Prompt Caching     : {RED}${cost_no_cache:.4f}{RESET}")
        print(f"  • Biaya DENGAN Prompt Caching    : {GREEN}${cost_cache:.4f}{RESET} ({BOLD}{GREEN}Hemat {savings_pct:.1f}%!{RESET})\n")

    print(f"{BOLD}[ INSIGHT STRATEGI PENETAPAN BIAYA OPERASIONAL AI AGENTS ]{RESET}")
    print(" 1. Smart Model Routing: Gunakan Gemini 2.0 Flash / DeepSeek V3 untuk agent step intermediate, dan panggil Claude 3.5 Sonnet / GPT-4o HANYA untuk instruksi final.")
    print(" 2. Prompt Caching: Menyimpan System Prompt & skema Tools pada Caching API memotong biaya operasional agent hingga 50-80%!")
    print(" 3. Context Truncation: Ringkas riwayat percakapan lama di pertengahan loop agar input token tidak membengkak secara kuadratik.")

if __name__ == "__main__":
    run_demo()
