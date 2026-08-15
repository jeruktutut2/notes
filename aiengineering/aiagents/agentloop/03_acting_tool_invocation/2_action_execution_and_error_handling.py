#!/usr/bin/env python3
"""
Modul 3.2: Action Execution & Error Handling
Demonstrasi mekanisme eksekusi tindakan yang tangguh (resilient tool execution)
lengkap dengan strategi retry (percobaan ulang), fallback mechanism, dan penanganan timeout/error.
"""

import time
import random
from typing import Dict, Any, Callable

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

class FlakyAPIClient:
    """Simulasi API external yang kadang mengalami Network Timeout atau 500 Server Error."""
    def __init__(self):
        self.attempts = 0

    def query_external_api(self, endpoint: str) -> str:
        self.attempts += 1
        print(f"   [API Hit #{self.attempts}] Menghubungi {endpoint}...")
        
        if self.attempts < 3:
            # Simulasi Network Error pada 2 percobaan pertama
            raise TimeoutError("504 Gateway Timeout: Server tidak merespons dalam 2000ms")
        
        return json.dumps({"status": "SUCCESS", "data": "Data hasil query berhasil didapatkan pada percobaan ke-3"})

import json

class ResilientActionExecutor:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.5):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def execute_with_retry(self, action_func: Callable, *args, fallback_func: Callable = None, **kwargs) -> str:
        for attempt in range(1, self.max_retries + 1):
            try:
                result = action_func(*args, **kwargs)
                print(f"  {GREEN}✔ Eksekusi Sukses pada Percobaan #{attempt}!{RESET}")
                return result
            except Exception as e:
                print(f"  {RED}✘ Percobaan #{attempt} Gagal: {e}{RESET}")
                if attempt < self.max_retries:
                    sleep_time = self.backoff_factor * (2 ** (attempt - 1))
                    print(f"  {YELLOW}⌛ Menunggu {sleep_time:.1f} detik sebelum retry...{RESET}")
                    time.sleep(sleep_time)
                else:
                    print(f"  {RED}⚠ Batas maksimum retry ({self.max_retries}) tercapai.{RESET}")

        if fallback_func:
            print(f"  {CYAN}🔄 Menjalankan Fallback Mechanism...{RESET}")
            return fallback_func()
        
        return "Error: Action execution failed after maximum retries and no fallback available."

def fallback_local_cache() -> str:
    return json.dumps({"status": "FALLBACK_SUCCESS", "data": "Menggunakan data dari local cache terdekat."})

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 3.2: ACTION EXECUTION & ERROR HANDLING ==={RESET}\n")

    api_client = FlakyAPIClient()
    executor = ResilientActionExecutor(max_retries=3, backoff_factor=0.3)

    print(f"{BOLD}1. Menguji Eksekusi Tool dengan Retry Loop & Recovery:{RESET}")
    res = executor.execute_with_retry(
        api_client.query_external_api,
        "https://api.example.com/v1/data",
        fallback_func=fallback_local_cache
    )
    print(f"Hasil Akhir Observasi: {GREEN}{res}{RESET}\n")
    print("-" * 65)

    print(f"\n{BOLD}2. Menguji Eksekusi Tool yang Selalu Error (Menjalankan Fallback):{RESET}")
    def broken_api():
        raise ConnectionResetError("500 Internal Server Error: Database Down")

    res_fallback = executor.execute_with_retry(
        broken_api,
        fallback_func=fallback_local_cache
    )
    print(f"Hasil Akhir Observasi: {YELLOW}{res_fallback}{RESET}\n")

if __name__ == "__main__":
    main()
