#!/usr/bin/env python3
"""
MODUL 6: Evaluasi, Metrik & Biaya Context
Skrip 2: Cost, Latency, & Performance Degradation Benchmark

Mendemonstrasikan:
1. Pemodelan Biaya Token Input vs Output pada Skala Panjang Context (1k - 128k Tokens).
2. Estimasi TTFT (Time to First Token) & Generasi Latency Kuadratik/Linier.
3. Simulasi Benchmark Biaya Operasional Bulanan untuk Agen AI Berbasis Context Window.
"""

from typing import List, Dict, Any

class ContextCostAnalyzer:
    """Kalkulator & Benchmark Biaya Skalabilitas Context Window."""

    def __init__(
        self,
        cost_per_1m_input_usd: float = 2.50,   # Misal Claude 3.5 Sonnet / GPT-4o input
        cost_per_1m_output_usd: float = 10.00,
        cached_discount_factor: float = 0.50   # 50% Diskon untuk Cached Token
    ):
        self.cost_per_1m_input_usd = cost_per_1m_input_usd
        self.cost_per_1m_output_usd = cost_per_1m_output_usd
        self.cached_discount_factor = cached_discount_factor

    def calculate_single_request(
        self,
        input_tokens: int,
        output_tokens: int,
        cached_ratio: float = 0.0
    ) -> Dict[str, Any]:
        """Kalkulasi biaya satu request dengan opsi Context Caching."""

        cached_tokens = int(input_tokens * cached_ratio)
        uncached_tokens = input_tokens - cached_tokens

        input_cost_uncached = (uncached_tokens / 1_000_000.0) * self.cost_per_1m_input_usd
        input_cost_cached = (cached_tokens / 1_000_000.0) * (self.cost_per_1m_input_usd * self.cached_discount_factor)
        output_cost = (output_tokens / 1_000_000.0) * self.cost_per_1m_output_usd

        total_cost = input_cost_uncached + input_cost_cached + output_cost

        # Perkiraan Latensi TTFT (linier-kuadratik tergantung KV Cache)
        # Latensi uncached token: ~0.8ms per 1k token, cached token: ~0.1ms per 1k token
        ttft_latency_ms = 50.0 + (uncached_tokens / 1000.0 * 0.8) + (cached_tokens / 1000.0 * 0.1)

        return {
            "input_tokens": input_tokens,
            "cached_tokens": cached_tokens,
            "output_tokens": output_tokens,
            "total_cost_usd": total_cost,
            "ttft_latency_ms": round(ttft_latency_ms, 2)
        }

def demo():
    print("=" * 70)
    print("DEMO 2: COST, LATENCY, & PERFORMANCE DEGRADATION BENCHMARK")
    print("=" * 70)

    analyzer = ContextCostAnalyzer(cost_per_1m_input_usd=2.50, cost_per_1m_output_usd=10.00)

    context_scales = [1_000, 4_000, 16_000, 64_000, 128_000]
    output_tokens = 500
    daily_requests = 10_000

    print(f"Harga Model: ${analyzer.cost_per_1m_input_usd}/1M Input | ${analyzer.cost_per_1m_output_usd}/1M Output")
    print(f"Volume Pengujian: {daily_requests:,} Request/Hari ({daily_requests * 30:,} Request/Bulan)\n")

    print(f"{'Context Size':<15} | {'Cost/Req (USD)':<16} | {'Biaya Bulanan (No Cache)':<26} | {'Est. TTFT Latency'}")
    print("-" * 80)

    for ctx in context_scales:
        res = analyzer.calculate_single_request(ctx, output_tokens, cached_ratio=0.0)
        monthly_cost = res["total_cost_usd"] * daily_requests * 30
        print(f"{ctx:7,} tokens | ${res['total_cost_usd']:<14.5f} | ${monthly_cost:<24,.2f} | {res['ttft_latency_ms']} ms")

    print("\n--- SIMULASI PENGHEMATAN DENGAN CONTEXT CACHING (80% CACHED RATIO) ---")
    ctx = 64_000
    res_no_cache = analyzer.calculate_single_request(ctx, output_tokens, cached_ratio=0.0)
    res_with_cache = analyzer.calculate_single_request(ctx, output_tokens, cached_ratio=0.8)

    m_no_cache = res_no_cache["total_cost_usd"] * daily_requests * 30
    m_with_cache = res_with_cache["total_cost_usd"] * daily_requests * 30

    print(f"Context Size: 64,000 tokens")
    print(f"  • Tanpa Caching : Biaya Bulanan = ${m_no_cache:,.2f} | TTFT = {res_no_cache['ttft_latency_ms']} ms")
    print(f"  • Dengan Caching: Biaya Bulanan = ${m_with_cache:,.2f} | TTFT = {res_with_cache['ttft_latency_ms']} ms")
    print(f"  • Total Hemat   : ${m_no_cache - m_with_cache:,.2f} / Bulan ({(1 - m_with_cache/m_no_cache)*100:.1f}% Penghematan!)")
    print("=" * 70)

if __name__ == "__main__":
    demo()
