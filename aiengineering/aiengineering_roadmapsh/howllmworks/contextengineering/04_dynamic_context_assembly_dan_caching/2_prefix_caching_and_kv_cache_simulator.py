#!/usr/bin/env python3
"""
MODUL 4: Dynamic Context Assembly & Caching
Skrip 2: Prefix Caching & KV-Cache Reuse Simulator

Mendemonstrasikan:
1. Prinsip Match Byte-for-Byte pada Prefix Context (Anthropic / OpenAI Context Caching).
2. Perhitungan Simulasi Penghematan Latensi TTFT (Time to First Token) & Biaya Token.
3. Simulasi Cache Hit vs Cache Miss pada Arsitektur VRAM KV-Cache LLM.
"""

import hashlib
import time
from typing import Dict, Tuple, Any

class KVCacheSimulator:
    """Simulator KV-Cache VRAM & Prefix Caching untuk LLM."""

    def __init__(self, cost_per_1k_uncached: float = 0.003, cost_per_1k_cached: float = 0.0005):
        self.cost_per_1k_uncached = cost_per_1k_uncached
        self.cost_per_1k_cached = cost_per_1k_cached
        self.kv_cache_store: Dict[str, Dict[str, Any]] = {}

    def _hash_prefix(self, prefix_text: str) -> str:
        """Menghasilkan MD5 hash untuk identifikasi prefix exact match."""
        return hashlib.md5(prefix_text.encode("utf-8")).hexdigest()

    def process_request(self, prefix_system_prompt: str, dynamic_user_query: str) -> Dict[str, Any]:
        """Proses request dengan mengecek keberadaan KV-Cache untuk prefix_system_prompt."""
        prefix_hash = self._hash_prefix(prefix_system_prompt)
        
        prefix_words = len(prefix_system_prompt.split())
        query_words = len(dynamic_user_query.split())
        total_words = prefix_words + query_words

        cache_hit = prefix_hash in self.kv_cache_store

        if cache_hit:
            # Cache Hit: Tidak perlu re-compute Key-Value Attention Matrix untuk prefix
            compute_time_ms = 15.0 + (query_words * 2.0)  # Sangat cepat!
            cached_tokens = prefix_words
            uncached_tokens = query_words
            status = "CACHE_HIT (KV-Cache Reused)"
        else:
            # Cache Miss: Wajib melakukan komputasi full attention matrix pada GPU
            compute_time_ms = (prefix_words * 1.5) + (query_words * 2.0)
            cached_tokens = 0
            uncached_tokens = total_words
            # Simpan ke Cache Store
            self.kv_cache_store[prefix_hash] = {
                "created_at": time.time(),
                "token_count": prefix_words
            }
            status = "CACHE_MISS (Full Computation)"

        # Perhitungan Biaya
        cost_cached = (cached_tokens / 1000.0) * self.cost_per_1k_cached
        cost_uncached = (uncached_tokens / 1000.0) * self.cost_per_1k_uncached
        total_cost = cost_cached + cost_uncached

        # Estimasi biaya jika tanpa caching sama sekali
        cost_without_cache = (total_words / 1000.0) * self.cost_per_1k_uncached

        return {
            "status": status,
            "cache_hit": cache_hit,
            "ttft_latency_ms": compute_time_ms,
            "total_tokens": total_words,
            "cached_tokens": cached_tokens,
            "uncached_tokens": uncached_tokens,
            "cost_usd": total_cost,
            "cost_saved_usd": max(0.0, cost_without_cache - total_cost),
            "savings_percent": ((cost_without_cache - total_cost) / cost_without_cache * 100) if cost_without_cache > 0 else 0
        }

def demo():
    print("=" * 70)
    print("DEMO 2: PREFIX CACHING & KV-CACHE REUSE SIMULATOR")
    print("=" * 70)

    simulator = KVCacheSimulator()

    large_system_prefix = (
        " Anda adalah Asisten Kode Utama Enterprise. Ikuti panduan keamanan OWASP Top 10, "
        "gunakan standar penulisan PEP8 untuk Python, sertakan tipe data terstruktur (type hinting), "
        "dan patuhi seluruh aturan lisensi open-source berikut: [Dokumentasi 500 Kata Regulasi Enterprise] " * 5
    )

    print(f"Ukuran Prefix System Prompt: ~{len(large_system_prefix.split())} kata/token.")

    # Request 1: Sesi Pertama (Cache Miss)
    print("\n--- REQUEST 1 (Sesi Pengguna Pertama) ---")
    query_1 = "Bagaimana cara membuat fungsi hash di Python?"
    res1 = simulator.process_request(large_system_prefix, query_1)
    print(f"Status        : {res1['status']}")
    print(f"TTFT Latency  : {res1['ttft_latency_ms']:.2f} ms")
    print(f"Biaya Request : ${res1['cost_usd']:.6f}")

    # Request 2: Sesi Kedua dengan Prefix Identik (Cache Hit)
    print("\n--- REQUEST 2 (Sesi Pengguna Kedua dengan System Prompt Identik) ---")
    query_2 = "Bagaimana cara mengoptimalkan kueri SQL di PostgreSQL?"
    res2 = simulator.process_request(large_system_prefix, query_2)
    print(f"Status        : {res2['status']}")
    print(f"TTFT Latency  : {res2['ttft_latency_ms']:.2f} ms (Sangat Cepat!)")
    print(f"Biaya Request : ${res2['cost_usd']:.6f}")
    print(f"Penghematan   : ${res2['cost_saved_usd']:.6f} ({res2['savings_percent']:.1f}% Dihemat!)")
    print("=" * 70)

if __name__ == "__main__":
    demo()
