"""
01_token_cost_calculator.py
---------------------------
Lab runnable untuk menghitung biaya token LLM secara presisi across berbagai provider
(OpenAI, Anthropic, Gemini) serta mensimulasikan peringatan ambang batas anggaran (Budget Alerts).
"""

from typing import Dict, Any, List

# Standard Pricing per 1 Million Tokens (USD)
PRICING_TABLE = {
    "gpt-4o": {"input_per_1m": 2.50, "output_per_1m": 10.00},
    "gpt-4o-mini": {"input_per_1m": 0.15, "output_per_1m": 0.60},
    "claude-3-5-sonnet": {"input_per_1m": 3.00, "output_per_1m": 15.00},
    "gemini-1.5-flash": {"input_per_1m": 0.075, "output_per_1m": 0.30},
    "gemini-1.5-pro": {"input_per_1m": 1.25, "output_per_1m": 5.00},
}

class LLMCostCalculator:
    def __init__(self, daily_budget_usd: float = 10.0):
        self.daily_budget = daily_budget_usd
        self.total_spent = 0.0
        self.records: List[Dict[str, Any]] = []

    def calculate_cost(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        if model not in PRICING_TABLE:
            raise ValueError(f"Model '{model}' tidak ditemukan dalam tabel harga.")

        rates = PRICING_TABLE[model]
        input_cost = (prompt_tokens / 1_000_000) * rates["input_per_1m"]
        output_cost = (completion_tokens / 1_000_000) * rates["output_per_1m"]
        total_call_cost = input_cost + output_cost

        return total_call_cost

    def record_usage(self, model: str, prompt_tokens: int, completion_tokens: int, user_id: str):
        cost = self.calculate_cost(model, prompt_tokens, completion_tokens)
        self.total_spent += cost
        
        record = {
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "cost_usd": cost,
            "user_id": user_id
        }
        self.records.append(record)

        # Check Budget Alert
        percentage_used = (self.total_spent / self.daily_budget) * 100
        alert_flag = None
        if percentage_used >= 100:
            alert_flag = f"🚨 CRITICAL ALERT: Anggaran harian (${self.daily_budget}) terlampaui! Spent: ${self.total_spent:.4f}"
        elif percentage_used >= 80:
            alert_flag = f"⚠️ WARNING: Penggunaan telah mencapai {percentage_used:.1f}% dari anggaran (${self.daily_budget}). Spent: ${self.total_spent:.4f}"

        return record, alert_flag

def main():
    print(f"\n=======================================================")
    print(f"💰 LLM TOKEN COST CALCULATOR & BUDGET MONITOR")
    print(f"=======================================================\n")

    calculator = LLMCostCalculator(daily_budget_usd=0.05) # Budget kecil untuk demo alert

    # Simulasi batch eksekusi request
    simulated_requests = [
        {"model": "gpt-4o", "prompt_tokens": 4200, "completion_tokens": 850, "user": "usr_alpha"},
        {"model": "claude-3-5-sonnet", "prompt_tokens": 12000, "completion_tokens": 1500, "user": "usr_beta"},
        {"model": "gpt-4o-mini", "prompt_tokens": 50000, "completion_tokens": 8000, "user": "usr_gamma"},
        {"model": "gemini-1.5-flash", "prompt_tokens": 120000, "completion_tokens": 15000, "user": "usr_delta"},
    ]

    print(f"Daily Budget set to: ${calculator.daily_budget:.2f} USD\n")
    print(f"{'User':<12} | {'Model':<18} | {'Tokens (In/Out)':<18} | {'Cost (USD)':<12} | {'Status'}")
    print("-" * 80)

    for req in simulated_requests:
        rec, alert = calculator.record_usage(
            model=req["model"],
            prompt_tokens=req["prompt_tokens"],
            completion_tokens=req["completion_tokens"],
            user_id=req["user"]
        )
        tokens_str = f"{rec['prompt_tokens']} / {rec['completion_tokens']}"
        status_str = "OK" if not alert else alert.split(":")[0]
        print(f"{rec['user_id']:<12} | {rec['model']:<18} | {tokens_str:<18} | ${rec['cost_usd']:<11.6f} | {status_str}")

        if alert:
            print(f"   ↳ {alert}")

    print("-" * 80)
    print(f"\nTotal Akumulasi Biaya: ${calculator.total_spent:.6f} USD")
    print(f"Jumlah Request Dicatat: {len(calculator.records)}")

if __name__ == "__main__":
    main()
