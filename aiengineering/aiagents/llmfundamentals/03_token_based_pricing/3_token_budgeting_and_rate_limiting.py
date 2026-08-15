#!/usr/bin/env python3
"""
Modul 3.3: Token Budgeting & Rate Limiting (Token Bucket & Guardrails)
Simulasi Token Bucket Algorithm untuk TPM/RPM limiter dan Guardrail pembatas biaya Agent.
"""

import time
from typing import Tuple

class TokenBucketRateLimiter:
    """
    Simulasi Token Bucket Algorithm untuk mengontrol TPM (Tokens Per Minute) API Limit.
    """
    def __init__(self, tpm_limit: int, rpm_limit: int):
        self.tpm_limit = tpm_limit
        self.rpm_limit = rpm_limit
        self.available_tokens = tpm_limit
        self.available_requests = rpm_limit
        self.last_refill_time = time.time()

    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill_time
        if elapsed >= 60.0:
            self.available_tokens = self.tpm_limit
            self.available_requests = self.rpm_limit
            self.last_refill_time = now

    def consume(self, token_cost: int) -> Tuple[bool, str]:
        self._refill()
        if self.available_requests <= 0:
            return False, "429 Rate Limit Exceeded: RPM (Requests Per Minute) Limit Reached!"
        if self.available_tokens < token_cost:
            return False, f"429 Rate Limit Exceeded: TPM Limit Reached! (Perlu {token_cost} tokens, tersisa {self.available_tokens})"
        
        self.available_requests -= 1
        self.available_tokens -= token_cost
        return True, f"Request Approved. Sisa Token Bucket: {self.available_tokens:,} TPM | Sisa Request: {self.available_requests} RPM"


class AgentTokenGuardrail:
    """
    Guardrail pemantau akumulasi biaya agent untuk mencegah infinite loop token drain.
    """
    def __init__(self, max_token_budget: int = 50_000, max_usd_budget: float = 0.50):
        self.max_token_budget = max_token_budget
        self.max_usd_budget = max_usd_budget
        self.used_tokens = 0
        self.used_usd = 0.0

    def record_usage(self, input_tokens: int, output_tokens: int, price_per_1m_in: float = 2.50, price_per_1m_out: float = 10.00) -> bool:
        call_tokens = input_tokens + output_tokens
        call_cost = ((input_tokens / 1_000_000) * price_per_1m_in) + ((output_tokens / 1_000_000) * price_per_1m_out)
        
        self.used_tokens += call_tokens
        self.used_usd += call_cost
        
        if self.used_tokens > self.max_token_budget or self.used_usd > self.max_usd_budget:
            print(f"\033[91m[GUARDRAIL TRIGGERED!] Agent dihentikan secara paksa!\033[0m")
            print(f"  Penggunaan: {self.used_tokens:,} / {self.max_token_budget:,} Tokens | ${self.used_usd:.4f} / ${self.max_usd_budget:.2f} USD")
            return False
        
        print(f"\033[92m[Guardrail Status]\033[0m Usage: {self.used_tokens:,} / {self.max_token_budget:,} Tokens (${self.used_usd:.4f} USD)")
        return True


def demonstrate_rate_limiter():
    print("\n" + "="*70)
    print(" 1. SIMULASI TOKEN BUCKET RATE LIMITER (TPM / RPM)")
    print("="*70)
    
    limiter = TokenBucketRateLimiter(tpm_limit=30_000, rpm_limit=3)
    
    requests = [
        ("Agent Step 1", 10_000),
        ("Agent Step 2", 15_000),
        ("Agent Step 3", 8_000),   # Will breach TPM
        ("Agent Step 4", 2_000)    # Will breach RPM
    ]
    
    for req_name, tokens in requests:
        success, msg = limiter.consume(tokens)
        status = "\033[92m[SUCCESS]\033[0m" if success else "\033[91m[BLOCKED]\033[0m"
        print(f"Request: {req_name:<15} ({tokens:>6,} tokens) -> {status} {msg}")
    print()


def demonstrate_guardrail():
    print("="*70)
    print(" 2. SIMULASI AGENT TOKEN BUDGET GUARDRAIL")
    print("="*70)
    
    guardrail = AgentTokenGuardrail(max_token_budget=40_000, max_usd_budget=0.20)
    
    # Simulate agent infinite loop
    loop_step = 0
    while True:
        loop_step += 1
        print(f"\nExcuting Agent ReAct Step {loop_step}...")
        # Every step consumes more context
        input_t = 10_000 + (loop_step * 5_000)
        output_t = 800
        
        is_safe = guardrail.record_usage(input_t, output_t)
        if not is_safe:
            print(f"\033[93mPencegahan Berhasil: Infinite loop agent terdeteksi dan dihentikan di Step {loop_step}!\033[0m")
            break
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 3.3: TOKEN BUDGETING & RATE LIMITING")
    print("█"*70)
    
    demonstrate_rate_limiter()
    demonstrate_guardrail()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Selalu pasang Rate Limiter client-side untuk menangani HTTP 429 dari API provider.")
    print(" 2. Setiap produksi AI Agent WAJIB dipasangi Max Budget Guardrail (Hard Limit USD & Token Count).")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
