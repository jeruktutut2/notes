#!/usr/bin/env python3
"""
Modul: Closed vs Open Source Models
Kalkulator Perbandingan Biaya TCO (Total Cost of Ownership) & Analisis Privasi.
"""

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def calculate_tco(daily_requests: int, avg_input_tokens: int, avg_output_tokens: int):
    # Closed Source API (GPT-4o rates): $2.50 / 1M Input, $10.00 / 1M Output
    monthly_input_tok = daily_requests * 30 * avg_input_tokens
    monthly_output_tok = daily_requests * 30 * avg_output_tokens
    
    cost_closed_usd = (monthly_input_tok / 1e6 * 2.50) + (monthly_output_tok / 1e6 * 10.00)
    
    # Open Source Self-Hosted (1x A100 GPU Cloud Instance ~$1,400/month fixed)
    gpu_instances_needed = max(1, int(daily_requests / 50000))
    cost_open_source_usd = gpu_instances_needed * 1400.0

    return {
        "monthly_requests": daily_requests * 30,
        "closed_source_api_cost": f"${cost_closed_usd:,.2f}",
        "open_source_gpu_cost": f"${cost_open_source_usd:,.2f}",
        "break_even_point": "Open-Source lebih hemat jika request > 30.000 / hari" if cost_open_source_usd < cost_closed_usd else "Closed-Source API lebih hemat untuk volume kecil/sedang"
    }

def main():
    print("=" * 70)
    print(color("  MODUL: CLOSED-SOURCE VS OPEN-SOURCE TCO CALCULATOR", "1;34"))
    print("=" * 70)

    # Test Scenarios
    scenarios = [
        ("Skenario Startup (1,000 req/hari)", 1000, 2000, 300),
        ("Skenario Enterprise (100,000 req/hari)", 100000, 2000, 300)
    ]

    for name, reqs, in_tok, out_tok in scenarios:
        print(color(f"\n{name}:", "1;33"))
        res = calculate_tco(reqs, in_tok, out_tok)
        print(f"  • Total Request/Bulan : {res['monthly_requests']:,}")
        print(f"  • Biaya Closed API    : {res['closed_source_api_cost']}")
        print(f"  • Biaya Open GPU Host : {res['open_source_gpu_cost']}")
        print(color(f"  ► Rekomendasi TCO     : {res['break_even_point']}", "1;32"))

    print("\n" + "=" * 70)
    print("✓ Closed-Source API unggul di awal (zero infra cost), Open-Source unggul di skala besar & privasi 100%.")

if __name__ == "__main__":
    main()
