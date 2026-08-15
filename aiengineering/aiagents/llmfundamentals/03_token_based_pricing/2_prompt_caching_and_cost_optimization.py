#!/usr/bin/env python3
"""
Modul 3.2: Prompt Caching & Cost Optimization Mechanics
Simulasi Prefix Matching Prompt Caching (Anthropic, Gemini, OpenAI) dan perhitungan efisiensi latency/biaya.
"""

from typing import Tuple, Dict

def simulate_prompt_caching():
    print("\n" + "="*70)
    print(" 1. MEKANISME PREFIX MATCHING PROMPT CACHING")
    print("="*70)
    print("Prompt Caching menyimpan KV-Cache dari prefix prompt yang konstan (System Prompt & RAG Document).")
    print("Jika request berikutnya memiliki prefix identik, LLM tidak perlu memproses ulang token tersebut!\n")
    
    system_prompt = "SYS_PROMPT_AGENT_DEFINITIONS_AND_TOOLS_V1" # 5,000 tokens
    rag_document = "DOCUMENT_KNOWLEDGE_BASE_COMPLIANCE_2026"  # 20,000 tokens
    user_query_1 = "Bagaimana kebijakan pengembalian dana?"       # 100 tokens
    user_query_2 = "Apa syarat klaim garansi produk?"           # 120 tokens
    
    prefix_block = system_prompt + " + " + rag_document
    prefix_tokens = 25_000
    
    print(f"Prefix Teridentifikasi (Constant Block): {prefix_tokens:,} tokens")
    print(f"  • {system_prompt} (5,000 tokens)")
    print(f"  • {rag_document} (20,000 tokens)\n")
    
    # Request 1 (Cache Miss / Write Cache)
    print("\033[93m[Call 1]\033[0m User Query 1: '" + user_query_1 + "'")
    print("  -> Status Cache: \033[91mCACHE WRITE (CACHE MISS)\033[0m")
    print("  -> Token Diproses: 25,000 Read/Write + 100 Input = 25,100 tokens")
    print("  -> Latency TTFT : ~1.8 Detik (Slow)\n")

    # Request 2 (Cache Hit)
    print("\033[92m[Call 2]\033[0m User Query 2: '" + user_query_2 + "'")
    print("  -> Status Cache: \033[92mCACHE HIT (100% Prefix Matched)\033[0m")
    print("  -> Token Diproses: 25,000 Cached (Diskon 90%) + 120 Uncached Input")
    print("  -> Latency TTFT : ~0.2 Detik (\033[92m9x Lebih Cepat!\033[0m)\n")


def calculate_caching_savings():
    print("="*70)
    print(" 2. SIMULASI SAVINGS BIAYA PROMPT CACHING (CLAUDE 3.5 SONNET)")
    print("="*70)
    
    # Pricing Claude 3.5 Sonnet
    standard_input_rate = 3.00       # $3.00 / 1M
    cache_write_rate = 3.75          # $3.75 / 1M (Write ke cache +25%)
    cache_read_rate = 0.30           # $0.30 / 1M (Diskon 90%!)
    output_rate = 15.00              # $15.00 / 1M
    
    prefix_tokens = 50_000           # 50K System + RAG
    query_tokens = 500
    output_tokens = 1_000
    num_requests = 100               # 100 Request percakapan berturut-turut
    
    # Scenario A: Tanpa Prompt Caching
    cost_without_cache = num_requests * (
        ((prefix_tokens + query_tokens) / 1_000_000 * standard_input_rate) +
        (output_tokens / 1_000_000 * output_rate)
    )
    
    # Scenario B: Dengan Prompt Caching
    # 1st request = Cache Write
    first_req_cost = (
        (prefix_tokens / 1_000_000 * cache_write_rate) +
        (query_tokens / 1_000_000 * standard_input_rate) +
        (output_tokens / 1_000_000 * output_rate)
    )
    # Remaining 99 requests = Cache Read
    remaining_req_cost = (num_requests - 1) * (
        (prefix_tokens / 1_000_000 * cache_read_rate) +
        (query_tokens / 1_000_000 * standard_input_rate) +
        (output_tokens / 1_000_000 * output_rate)
    )
    cost_with_cache = first_req_cost + remaining_req_cost
    
    savings = cost_without_cache - cost_with_cache
    savings_pct = (savings / cost_without_cache) * 100
    
    print(f"Simulasi 100 API Calls dengan Prefix Konstan {prefix_tokens:,} Tokens:")
    print(f" • Biaya TANPA Caching : ${cost_without_cache:.2f} USD")
    print(f" • Biaya DENGAN Caching: \033[92m${cost_with_cache:.2f} USD\033[0m")
    print(f" • \033[93mTotal Penghematan    : ${savings:.2f} USD ({savings_pct:.1f}% SAVED!)\033[0m\n")


def main():
    print("\n" + "█"*70)
    print("  MODUL 3.2: PROMPT CACHING & COST OPTIMIZATION")
    print("█"*70)
    
    simulate_prompt_caching()
    calculate_caching_savings()
    
    print("="*70)
    print(" Syarat Agar Prompt Caching Aktif:")
    print(" 1. Minimum Token Prefix Threshold (misal: minimum 1,024 token di Anthropic / OpenAI).")
    print(" 2. Prefix teks harus 100% identik dari karakter pertama sampai batas cache breakpoint.")
    print(" 3. Tempatkan bagian statis (System Prompt / Docs) di ATAS, bagian dinamis (User Prompt) di BAWAH.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
