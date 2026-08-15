"""
MODUL 6.2: Prompt Compression, Token Estimation & Cost Optimization
=====================================================================
Penjelasan:
Biaya API LLM (seperti OpenAI GPT-4, Anthropic Claude, Gemini) dihitung berdasarkan jumlah token.
- Token Estimator: Memperkirakan jumlah token (secara kasar 1 token ~ 4 karakter atau 0.75 kata Bahasa Indonesia/Inggris).
- Compression Strategy: Menghapus filler words, redundansi, dan menyederhanakan instruksi tanpa mengurangi makna.
"""

import re

def estimate_tokens(text: str) -> int:
    """Estimasi jumlah token secara heuristik (~4 karakter per token)."""
    return math.ceil(len(text) / 4)


import math

def compress_prompt(verbose_prompt: str) -> str:
    """Strategi kompresi prompt untuk memangkas kata filler & redundansi."""
    compressed = verbose_prompt
    
    # Hapus kata-kata filler yang tidak menambah instruksi
    fillers = [
        r"\bmohon\s+bantuannya\s+untuk\b",
        r"\bkalau\s+bisa\b",
        r"\bsekiranya\b",
        r"\bdengan\s+sangat\s+jelas\s+dan\s+detail\b",
        r"\btolong\s+jelaskan\b"
    ]
    
    for f in fillers:
        compressed = re.sub(f, "", compressed, flags=re.IGNORECASE)
        
    # Bersihkan spasi ganda
    compressed = re.sub(r'\s+', ' ', compressed).strip()
    return compressed


def calculate_cost(num_prompt_tokens: int, num_completion_tokens: int, price_per_1k_input: float = 0.0015, price_per_1k_output: float = 0.002) -> float:
    """Kalkulasi biaya pemanggilan API."""
    cost_input = (num_prompt_tokens / 1000) * price_per_1k_input
    cost_output = (num_completion_tokens / 1000) * price_per_1k_output
    return cost_input + cost_output


def main():
    print("==========================================================")
    print(" DEMO 6.2: Prompt Compression & Cost Optimization")
    print("==========================================================\n")

    verbose_prompt = (
        "Halo AI, mohon bantuannya untuk tolong jelaskan dengan sangat jelas dan detail "
        "sekiranya apa saja keuntungan penggunaan cloud computing untuk startup lokal di Indonesia "
        "kalau bisa berikan 3 poin utama."
    )

    compressed_prompt = compress_prompt(verbose_prompt)
    
    tokens_before = estimate_tokens(verbose_prompt)
    tokens_after = estimate_tokens(compressed_prompt)
    
    cost_before = calculate_cost(tokens_before, 200)
    cost_after = calculate_cost(tokens_after, 200)

    print("[1] PROMPT SEBELUM KOMPRESI (VERBOSE):")
    print(f"Text: \"{verbose_prompt}\"")
    print(f"Estimasi Token: {tokens_before} token")
    print(f"Estimasi Biaya (1x Call): ${cost_before:.6f}")

    print("\n" + "="*60 + "\n")

    print("[2] PROMPT SETELAH KOMPRESI (TEROPTIMASI):")
    print(f"Text: \"{compressed_prompt}\"")
    print(f"Estimasi Token: {tokens_after} token")
    print(f"Estimasi Biaya (1x Call): ${cost_after:.6f}")
    
    savings_percent = ((tokens_before - tokens_after) / tokens_before) * 100
    print(f"\nPenghematan Token & Biaya: {savings_percent:.1f}%!")
    print("==========================================================")

if __name__ == "__main__":
    main()
