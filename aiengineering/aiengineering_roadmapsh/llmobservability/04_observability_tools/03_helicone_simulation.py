"""
03_helicone_simulation.py
-------------------------
Simulasi arsitektur Proxy Gateway Helicone (Header tracking, Caching, Rate-limiting, & Cost Analytics).
"""

import time
import json
import hashlib
from typing import Dict, Any, Tuple

class HeliconeProxyGatewaySimulator:
    """Simulasi Reverse Proxy Smart Gateway Helicone"""

    def __init__(self):
        self.response_cache: Dict[str, Dict[str, Any]] = {}
        self.request_logs: List[Dict[str, Any]] = []

    def execute_proxy_request(
        self,
        headers: Dict[str, str],
        model: str,
        prompt: str
    ) -> Tuple[Dict[str, Any], bool]:
        """
        Mengirim request melalui Helicone Proxy:
        - Memeriksa custom headers (e.g. Helicone-Cache-Enabled, Helicone-User-Id)
        - Jika Cache Hit -> Kembalikan respons instan (0ms latency, $0 cost)
        - Jika Cache Miss -> Panggil provider & simpan ke cache jika diaktifkan
        """
        user_id = headers.get("Helicone-User-Id", "anonymous")
        cache_enabled = headers.get("Helicone-Cache-Enabled", "false").lower() == "true"
        
        # Calculate prompt hash for cache lookup
        cache_key = hashlib.md5(f"{model}:{prompt}".encode()).hexdigest()

        start_time = time.time()

        if cache_enabled and cache_key in self.response_cache:
            # CACHE HIT
            cached_data = self.response_cache[cache_key]
            latency_ms = round((time.time() - start_time) * 1000, 2)
            log_entry = {
                "user_id": user_id,
                "model": model,
                "cache_hit": True,
                "latency_ms": latency_ms,
                "cost_saved_usd": cached_data["cost_usd"]
            }
            self.request_logs.append(log_entry)
            return {
                "response": cached_data["response"],
                "cached": True,
                "latency_ms": latency_ms,
                "cost_usd": 0.0
            }, True

        # CACHE MISS (Simulate LLM Call)
        time.sleep(0.20) # Simulate LLM API latency
        latency_ms = round((time.time() - start_time) * 1000, 2)
        generated_text = f"[Generated response for: '{prompt[:30]}...']"
        simulated_cost = 0.0024

        res_body = {
            "response": generated_text,
            "cached": False,
            "latency_ms": latency_ms,
            "cost_usd": simulated_cost
        }

        if cache_enabled:
            self.response_cache[cache_key] = res_body

        self.request_logs.append({
            "user_id": user_id,
            "model": model,
            "cache_hit": False,
            "latency_ms": latency_ms,
            "cost_usd": simulated_cost
        })

        return res_body, False

def main():
    print(f"\n=======================================================")
    print(f"☀️ HELICONE PROXY GATEWAY SIMULATION LAB")
    print(f"=======================================================\n")

    proxy = HeliconeProxyGatewaySimulator()

    prompt_query = "Apa perbedaan antara Closed Model dan Open Source Model?"
    helicone_headers = {
        "Helicone-Auth": "Bearer HELICONE_KEY_9981",
        "Helicone-User-Id": "usr_dev_44",
        "Helicone-Cache-Enabled": "true"
    }

    print("--- 1. REQUEST PERTAMA (Cache Miss) ---")
    print(f"Prompt: \"{prompt_query}\"")
    res1, is_cache = proxy.execute_proxy_request(helicone_headers, "gpt-4o", prompt_query)
    print(f"Latency : {res1['latency_ms']} ms")
    print(f"Cost    : ${res1['cost_usd']:.4f}")
    print(f"Cached? : {res1['cached']}\n")

    print("--- 2. REQUEST KEDUA (Cache Hit dengan Prompt yang Sama) ---")
    print(f"Prompt: \"{prompt_query}\"")
    res2, is_cache2 = proxy.execute_proxy_request(helicone_headers, "gpt-4o", prompt_query)
    print(f"Latency : {res2['latency_ms']} ms ⚡ (Instan dari Cache)")
    print(f"Cost    : ${res2['cost_usd']:.4f} 💰 (Hemat 100% Biaya)")
    print(f"Cached? : {res2['cached']}\n")

    print("✅ Helicone proxy gateway simulation lab completed!")

if __name__ == "__main__":
    main()
