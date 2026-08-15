"""
==============================================================================
MODULE CACHING AI (EXACT MATCH & SEMANTIC CACHING ENGINE)
==============================================================================
Menjawab request AI dengan LLM membutuhkan waktu (latensi 1-10 detik) dan
biaya token API yang mahal.

DENGAN CACHING ENGINE:
    1. Exact Match Caching: Menyimpan hasil jawaban berdasarkan Hash MD5 prompt yang persis sama.
       (Respon instan < 0.01 detik & Hemat Biaya 100%).
    2. Semantic Caching (Konsep): Menyimpan jawaban berdasarkan kemiripan vektor makna prompt.

SKENARIO:
    Digunakan oleh FastAPI Server di app.py untuk menyaring request berulang.
==============================================================================
"""

import hashlib
import time


class ExactMatchCache:
    """
    Engine Caching Sederhana berbasis MD5 Hash dari String Prompt.
    """
    def __init__(self, ttl_seconds: int = 3600):
        self.cache_store = {}
        self.ttl = ttl_seconds
        self.total_hits = 0
        self.total_misses = 0

    def _generate_key(self, prompt: str, system_prompt: str = "") -> str:
        gabungan = f"{system_prompt}||{prompt.strip().lower()}"
        return hashlib.md5(gabungan.encode("utf-8")).hexdigest()

    def get(self, prompt: str, system_prompt: str = "") -> str:
        """Mengambil data dari cache jika belum kedaluwarsa."""
        key = self._generate_key(prompt, system_prompt)
        entry = self.cache_store.get(key)

        if entry:
            waktu_dibuat = entry["timestamp"]
            if time.time() - waktu_dibuat < self.ttl:
                self.total_hits += 1
                return entry["response"]
            else:
                # Expired
                del self.cache_store[key]

        self.total_misses += 1
        return None

    def set(self, prompt: str, response_text: str, system_prompt: str = ""):
        """Menyimpan respon AI ke dalam cache."""
        key = self._generate_key(prompt, system_prompt)
        self.cache_store[key] = {
            "response": response_text,
            "timestamp": time.time()
        }

    def stats() -> dict:
        pass

    def get_stats(self) -> dict:
        total_req = self.total_hits + self.total_misses
        hit_rate = (self.total_hits / total_req * 100) if total_req > 0 else 0.0
        return {
            "total_items_cached": len(self.cache_store),
            "hits": self.total_hits,
            "misses": self.total_misses,
            "hit_rate_percent": round(hit_rate, 2)
        }
