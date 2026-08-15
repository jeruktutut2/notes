#!/usr/bin/env python3
"""
Modul 03: Perbandingan Paradigma & Trade-offs (Prompt vs Context Engineering)
Membahas perbedaan fundamental, perbandingan performa, biaya, latensi, dan batas skalabilitas.
"""

import json
from typing import Dict, Any

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class PromptVsContextComparison:
    """Benchmark & Simulator Perbandingan Prompt vs Context Engineering"""

    @staticmethod
    def compare_paradigms() -> Dict[str, Dict[str, Any]]:
        """Mata kuliah perbandingan 6 dimensi teknis"""
        return {
            "Prompt Engineering": {
                "Fokus Utama": "Formulasi instruksi, format output, CoT, dan framing persona",
                "Sifat Data": "Statis & Terstruktur (Instruksi sistem bawaan)",
                "Ukuran Token": "Kecil hingga Menengah (100 - 4,000 tokens)",
                "Sensitivitas Latensi": "Sangat Cepat / Low TTFT (Latensi rendah)",
                "Biaya Per Eksekusi": "Sangat Murah ($0.0001 - $0.005 per call)",
                "Tantangan Utama": "Prompt Injection, Hallucination jika data luar tidak ada",
                "Kasus Penggunaan Terbaik": "Task-specific instructions, reasoning, formatting JSON, sentiment analysis"
            },
            "Context Engineering": {
                "Fokus Utama": "Pengelolaan environment state, memory buffer, pruning, RAG, KV Caching",
                "Sifat Data": "Dinamis, Stateful, Multi-Tenant & Real-time Knowledge",
                "Ukuran Token": "Besar hingga Sangat Besar (8,000 - 128,000+ tokens)",
                "Sensitivitas Latensi": "Membutuhkan Caching / Higher TTFT tanpa optimization",
                "Biaya Per Eksekusi": "Bervariasi (Dapat membengkak tanpa pruning & caching)",
                "Tantangan Utama": "Lost-in-the-middle, Context Overflow, Memory Leak, Token Cost Scaling",
                "Kasus Penggunaan Terbaik": "Multi-turn Chatbots, Enterprise Knowledge Base RAG, Long-document Q&A"
            }
        }

    @staticmethod
    def simulate_cost_and_latency_tradeoff(
        query_type: str,
        num_requests: int = 1000
    ) -> Dict[str, Any]:
        """Simulasi kalkulasi biaya & latensi 1000 request"""
        # Price per 1M tokens: Input $2.50, Output $10.00 (Standard GPT-4o style model)
        
        # Scenario A: Pure Prompt Engineering (Static knowledge inside prompt)
        prompt_input_tokens = 800
        prompt_output_tokens = 200
        
        cost_prompt = num_requests * ((prompt_input_tokens / 1e6) * 2.50 + (prompt_output_tokens / 1e6) * 10.00)
        latency_prompt_ms = 450 # Fast TTFT
        
        # Scenario B: Pure Context Engineering (Large dynamic context 32K tokens)
        context_input_tokens = 32000
        context_output_tokens = 350
        
        cost_context_raw = num_requests * ((context_input_tokens / 1e6) * 2.50 + (context_output_tokens / 1e6) * 10.00)
        latency_context_raw_ms = 2800 # Slow TTFT without caching
        
        # Scenario C: Optimized Context Engineering (With Prefix Caching 80% discount + Pruning 50%)
        cached_input_tokens = 8000 # Pruned
        cost_context_opt = num_requests * ((cached_input_tokens * 0.2 / 1e6) * 2.50 + (context_output_tokens / 1e6) * 10.00)
        latency_context_opt_ms = 650 # Fast with KV cache hit
        
        return {
            "query_type": query_type,
            "requests_simulated": num_requests,
            "pure_prompt_engineering": {
                "total_cost_usd": f"${cost_prompt:.2f}",
                "avg_latency": f"{latency_prompt_ms} ms",
                "scalability_index": "High (Stateless)"
            },
            "unoptimized_context_engineering": {
                "total_cost_usd": f"${cost_raw:.2f}" if 'cost_raw' in locals() else f"${cost_context_raw:.2f}",
                "avg_latency": f"{latency_context_raw_ms} ms",
                "scalability_index": "Low (Expensive & High TTFT Latency)"
            },
            "optimized_context_engineering": {
                "total_cost_usd": f"${cost_context_opt:.2f}",
                "avg_latency": f"{latency_context_opt_ms} ms",
                "scalability_index": "Very High (Prefix Caching + Density Pruning)"
            }
        }

def main():
    print_header("MODUL 03: PERBANDINGAN PARADIGMA & TRADEOFFS")

    print(color("\n1. Perbandingan Karakteristik 6 Dimensi Utama:", "1;33"))
    comparison = PromptVsContextComparison.compare_paradigms()
    
    for paradigm, details in comparison.items():
        print(color(f"\n=== {paradigm.upper()} ===", "1;32" if paradigm == "Prompt Engineering" else "1;36"))
        for k, v in details.items():
            print(f"  • {k:<25}: {v}")

    print(color("\n2. Simulasi Benchmark Biaya & Latensi (1.000 Transaksi Production):", "1;33"))
    sim_res = PromptVsContextComparison.simulate_cost_and_latency_tradeoff("Enterprise Customer Support Query")
    
    print(color("\n  [A] Pure Prompt Engineering Approach:", "33"))
    print(f"      Total Biaya : {sim_res['pure_prompt_engineering']['total_cost_usd']}")
    print(f"      Rata Latensi: {sim_res['pure_prompt_engineering']['avg_latency']}")
    
    print(color("\n  [B] Unoptimized Context Engineering (32K Raw Window):", "31"))
    print(f"      Total Biaya : {sim_res['unoptimized_context_engineering']['total_cost_usd']}")
    print(f"      Rata Latensi: {sim_res['unoptimized_context_engineering']['avg_latency']}")

    print(color("\n  [C] Optimized Context Engineering (Prefix Caching + Pruning):", "32"))
    print(f"      Total Biaya : {sim_res['optimized_context_engineering']['total_cost_usd']}")
    print(f"      Rata Latensi: {sim_res['optimized_context_engineering']['avg_latency']}")

    print_header("RANGKUMAN TRADEOFF PARADIGMA")
    print("✓ Prompt Engineering fokus pada *Instruksi & Format*, efisien untuk tugas yang tidak butuh data eksternal.")
    print("✓ Context Engineering fokus pada *State & Data Environment*, mengelola ingatan dinamis & knowledge.")
    print("✓ Tanpa optimasi (Caching & Pruning), Context Engineering dapat 30x lebih mahal daripada Prompt saja.")

if __name__ == "__main__":
    main()
