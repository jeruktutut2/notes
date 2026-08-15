#!/usr/bin/env python3
"""
Modul 01: Token & Context Window Calculator
Menghitung jumlah token, memperkirakan biaya API, dan mensimulasikan penggunaan Context Window LLM.
"""

import sys

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

def count_tokens(text: str, model_encoding: str = "cl100k_base") -> int:
    """Menghitung jumlah token dalam teks menggunakan tiktoken atau perkiraan BPE."""
    if HAS_TIKTOKEN:
        try:
            encoding = tiktoken.get_encoding(model_encoding)
            return len(encoding.encode(text))
        except Exception:
            pass
    # Fallback estimation for Indonesian / English text
    words = text.split()
    return int(len(words) * 1.3)

def analyze_context_window(prompt_text: str, max_context_limit: int = 128000):
    """Menganalisis penggunaan context window dan perkiraan biaya."""
    tokens_count = count_tokens(prompt_text)
    percentage_used = (tokens_count / max_context_limit) * 100
    
    # Biaya rata-rata GPT-4o ($2.50 per 1M input tokens)
    cost_usd = (tokens_count / 1_000_000) * 2.50
    cost_idr = cost_usd * 16000  # Estimasi kurs 1 USD = 16,000 IDR
    
    print("\n" + "=" * 60)
    print(" 📊 HASIL ANALISIS TOKEN & CONTEXT WINDOW")
    print("=" * 60)
    print(f"Panjang Teks (Karakter) : {len(prompt_text):,}")
    print(f"Jumlah Kata              : {len(prompt_text.split()):,}")
    print(f"Estimasi Jumlah Token    : {tokens_count:,} token")
    print(f"Context Window Used      : {percentage_used:.4f}% dari {max_context_limit:,} token")
    print(f"Estimasi Biaya API Input : ${cost_usd:.6f} USD (~Rp {cost_idr:,.2f})")
    print("=" * 60)

def main():
    print("🚀 Prompt Engineering Toolkit - Token & Context Window Calculator")
    sample_prompt = """
    [SYSTEM INSTRUCTION]
    Anda adalah seorang AI System Architect berpengalaman. Tugas Anda adalah memberikan analisis
    arsitektur mikroservis untuk aplikasi e-commerce berskala besar.
    
    [CONTEXT]
    Sistem saat ini mengalami kendala bottleneck pada database PostgreSQL saat event Flash Sale.
    Traffic melonjak dari 500 RPS menjadi 45.000 RPS dalam rentang waktu 30 detik.
    
    [TASK]
    Berikan 3 strategi konkret meliputi Caching Layer (Redis/Memcached), Database Read-Replicas,
    dan Message Queue (RabbitMQ/Kafka) untuk menanggulangi masalah ini.
    """
    
    analyze_context_window(sample_prompt.strip())

if __name__ == "__main__":
    main()
