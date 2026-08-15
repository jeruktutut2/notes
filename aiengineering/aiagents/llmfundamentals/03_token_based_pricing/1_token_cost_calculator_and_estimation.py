#!/usr/bin/env python3
"""
Modul 3.1: Token Cost Calculator & Multi-Turn Estimation
Kalkulator estimasi biaya penggunaan API LLM berbasis token input & token output.
"""

from dataclasses import dataclass
from typing import Dict, List

@dataclass
class ModelPricing:
    name: str
    input_price_per_1m: float   # USD per 1 Juta Input Tokens
    output_price_per_1m: float  # USD per 1 Juta Output Tokens
    cached_input_price_per_1m: float = 0.0 # Prompt caching price

MODEL_PRICING_TABLE = {
    "gpt-4o": ModelPricing("OpenAI GPT-4o", input_price_per_1m=2.50, output_price_per_1m=10.00, cached_input_price_per_1m=1.25),
    "gpt-4o-mini": ModelPricing("OpenAI GPT-4o-Mini", input_price_per_1m=0.15, output_price_per_1m=0.60, cached_input_price_per_1m=0.075),
    "claude-3-5-sonnet": ModelPricing("Anthropic Claude 3.5 Sonnet", input_price_per_1m=3.00, output_price_per_1m=15.00, cached_input_price_per_1m=0.30),
    "gemini-1-5-pro": ModelPricing("Google Gemini 1.5 Pro", input_price_per_1m=1.25, output_price_per_1m=5.00, cached_input_price_per_1m=0.3125),
    "deepseek-r1": ModelPricing("DeepSeek R1 (API)", input_price_per_1m=0.55, output_price_per_1m=2.19, cached_input_price_per_1m=0.14)
}

def calculate_single_call_cost(model_key: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING_TABLE[model_key]
    input_cost = (input_tokens / 1_000_000) * pricing.input_price_per_1m
    output_cost = (output_tokens / 1_000_000) * pricing.output_price_per_1m
    return input_cost + output_cost


def demonstrate_single_call_comparison():
    print("\n" + "="*70)
    print(" 1. HARGA EKSEKUSI SINGLE CALL LLM (INPUT 10K TOKENS, OUTPUT 1K TOKENS)")
    print("="*70)
    
    input_tokens = 10_000
    output_tokens = 1_000
    
    print(f"Skenario: 1x Request Prompt RAG ({input_tokens:,} input tokens, {output_tokens:,} output tokens)\n")
    
    print(f"{'Model Provider':<28} | {'Input Cost':<12} | {'Output Cost':<12} | {'Total Cost (USD)':<18}")
    print("-" * 75)
    
    for key, p in MODEL_PRICING_TABLE.items():
        in_c = (input_tokens / 1_000_000) * p.input_price_per_1m
        out_c = (output_tokens / 1_000_000) * p.output_price_per_1m
        total = in_c + out_c
        print(f"{p.name:<28} | ${in_c:<11.4f} | ${out_c:<11.4f} | \033[92m${total:<16.4f}\033[0m")
    print()


def simulate_multiturn_agent_loop():
    print("="*70)
    print(" 2. AKUMULASI BIAYA PADA MULTI-TURN AI AGENT REASONING LOOP")
    print("="*70)
    print("Pada AI Agent (ReAct Loop), setiap langkah menyertakan ULANG seluruh histori percakapan.")
    print("Akibatnya, input token bertumbuh secara eksponensial/kuadratis di setiap turn!\n")
    
    base_system_prompt = 2_000  # System & Tools
    turn_added_tokens = 1_500   # User prompt + Tool output
    output_per_turn = 500       # Agent reasoning + Tool call payload
    num_turns = 5
    
    model_key = "claude-3-5-sonnet"
    p = MODEL_PRICING_TABLE[model_key]
    
    print(f"Model: {p.name} | ReAct Iterasi: {num_turns} Turns\n")
    
    cumulative_cost = 0.0
    accumulated_context = base_system_prompt
    
    print(f"{'Turn':<6} | {'Input Context Size':<20} | {'Output Tokens':<15} | {'Cost Turn (USD)':<16} | {'Akumulasi Total':<16}")
    print("-" * 80)
    
    for t in range(1, num_turns + 1):
        accumulated_context += turn_added_tokens
        turn_cost = calculate_single_call_cost(model_key, accumulated_context, output_per_turn)
        cumulative_cost += turn_cost
        
        print(f"Turn {t:<2} | {accumulated_context:>14,} tokens | {output_per_turn:>13,} | ${turn_cost:>14.4f} | \033[93m${cumulative_cost:>14.4f}\033[0m")
        accumulated_context += output_per_turn # include output in next turn history
    
    print(f"\n\033[91mPerhatian:\033[0m Total 5 Turn Agent menghabiskan ${cumulative_cost:.4f}.")
    print("Tanpa Caching atau Pruning, biaya Agent loop dapat membengkak hingga 10x-50x lipat!")
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 3.1: TOKEN COST CALCULATOR & ESTIMATION")
    print("█"*70)
    
    demonstrate_single_call_comparison()
    simulate_multiturn_agent_loop()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Token Output umumnya 4x lebih mahal dibandingkan Token Input.")
    print(" 2. Pengulangan context pada multi-turn agent adalah sumber pemborosan biaya utama.")
    print(" 3. Memilih model ringan (e.g. GPT-4o-mini / DeepSeek) untuk tool-routing sangat menghemat anggaran.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
