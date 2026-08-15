#!/usr/bin/env python3
"""
Modul: Prompt Caching
Simulasi Cache Hit/Miss, Penghematan Biaya Token, dan Pengurangan TTFT Latency.
"""

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: PROMPT CACHING (KV CACHE OPTIMIZATION)", "1;34"))
    print("=" * 70)

    # Static System Policy (4000 tokens simulation)
    system_prefix = "[STATIC SYSTEM PROMPT v2.4 - BANK POLICY & ENTERPRISE RULES] " * 150
    user_query_1 = "Berapa batas transfer harian?"
    user_query_2 = "Bagaimana cara reset PIN ATM?"

    print(color("\n1. REQUEST 1 (COLD START - CACHE MISS):", "1;33"))
    print(f"System Prefix Token Count: ~3,600 tokens")
    print(f"User Query              : '{user_query_1}'")
    print(color("Status                  : CACHE MISS (Writing to KV Cache Store)", "31"))
    print("Metrics                 : Input Tokens = 3,615 | TTFT Latency = 1,450 ms | Total Cost = $0.0090")

    print(color("\n2. REQUEST 2 (WARM HIT - SAME PREFIX):", "1;33"))
    print(f"System Prefix Token Count: ~3,600 tokens (Identical Prefix)")
    print(f"User Query              : '{user_query_2}'")
    print(color("Status                  : CACHE HIT (Reading from GPU KV Memory)", "1;32"))
    print(color("Metrics                 : Cached Tokens = 3,600 (80% Discount) | TTFT Latency = 180 ms | Total Cost = $0.0018", "1;32"))

    print("\n" + "=" * 70)
    print("✓ Prompt Caching menekan biaya hingga 80% dan memotong latensi hingga 8x lipat.")
    print("✓ Syarat utama: Seluruh komponen statis harus diletakkan di bagian awal (prefix) prompt.")

if __name__ == "__main__":
    main()
