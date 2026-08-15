"""
02_latency_profiler.py
-----------------------
Lab runnable untuk menganalisis dan memprofilkan metrik latensi LLM:
Time-to-First-Token (TTFT), Tokens-per-Second (TPS), serta pembagian latensi per komponen.
"""

import time
import random
from typing import Dict, Any

class LatencyProfiler:
    """Profiler untuk mengukur TTFT, TPS, dan Breakdown Latensi"""

    def profile_simulated_stream(
        self,
        prompt_tokens: int,
        target_completion_tokens: int,
        model_name: str = "gpt-4o"
    ) -> Dict[str, Any]:
        
        start_time = time.time()

        # Step 1: Preprocessing & Retrieval phase (e.g., Vector DB)
        time.sleep(random.uniform(0.05, 0.15))
        retrieval_end_time = time.time()

        # Step 2: Model Prefill & Time-to-First-Token (TTFT)
        # Prefill time scales slightly with prompt token length
        prefill_delay = 0.10 + (prompt_tokens / 10_000) * 0.05
        time.sleep(prefill_delay)
        first_token_time = time.time()

        # Step 3: Token Streaming Generation Phase
        # Simulating ~40-60 TPS generation
        generated_tokens = 0
        for _ in range(target_completion_tokens):
            time.sleep(random.uniform(0.015, 0.025))  # ~40-60ms per token chunk
            generated_tokens += 1

        end_time = time.time()

        # Calculation Metrics
        retrieval_ms = round((retrieval_end_time - start_time) * 1000, 2)
        ttft_ms = round((first_token_time - start_time) * 1000, 2)
        generation_duration_sec = end_time - first_token_time
        total_duration_sec = end_time - start_time
        total_duration_ms = round(total_duration_sec * 1000, 2)
        
        tps = round(generated_tokens / generation_duration_sec, 2) if generation_duration_sec > 0 else 0

        return {
            "model_name": model_name,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": generated_tokens,
            "retrieval_duration_ms": retrieval_ms,
            "ttft_ms": ttft_ms,
            "generation_duration_sec": round(generation_duration_sec, 3),
            "total_duration_ms": total_duration_ms,
            "tokens_per_second": tps,
            "latency_breakdown": {
                "retrieval_pct": round((retrieval_ms / total_duration_ms) * 100, 1),
                "ttft_pct": round(((ttft_ms - retrieval_ms) / total_duration_ms) * 100, 1),
                "generation_pct": round(((generation_duration_sec * 1000) / total_duration_ms) * 100, 1)
            }
        }

def main():
    print(f"\n=======================================================")
    print(f"⏱️ LLM LATENCY PROFILER (TTFT, TPS & BREAKDOWN)")
    print(f"=======================================================\n")

    profiler = LatencyProfiler()

    print("Memulai profiling request streaming (Prompt Tokens: 2,400 | Completion Tokens: 50)...")
    res = profiler.profile_simulated_stream(
        prompt_tokens=2400,
        target_completion_tokens=50,
        model_name="gpt-4o"
    )

    print("\n--- HASIL METRIK LATENSI ---")
    print(f"🤖 Model              : {res['model_name']}")
    print(f"🔢 Tokens In / Out     : {res['prompt_tokens']} / {res['completion_tokens']}")
    print(f"🔍 Retrieval Latency   : {res['retrieval_duration_ms']} ms ({res['latency_breakdown']['retrieval_pct']}%)")
    print(f"🚀 Time-To-First-Token : {res['ttft_ms']} ms ({res['latency_breakdown']['ttft_pct']}%)")
    print(f"⚡ Tokens Per Second   : {res['tokens_per_second']} tokens/sec")
    print(f"⏱️ Total Latency (E2E) : {res['total_duration_ms']} ms")
    print("----------------------------\n")

    print("📊 Visualisasi Breakdown Latensi:")
    ret_bar = "█" * int(res['latency_breakdown']['retrieval_pct'] / 5)
    ttft_bar = "█" * int(res['latency_breakdown']['ttft_pct'] / 5)
    gen_bar = "█" * int(res['latency_breakdown']['generation_pct'] / 5)
    print(f"  Retrieval  [{ret_bar:<20}] {res['latency_breakdown']['retrieval_pct']}%")
    print(f"  TTFT       [{ttft_bar:<20}] {res['latency_breakdown']['ttft_pct']}%")
    print(f"  Generation [{gen_bar:<20}] {res['latency_breakdown']['generation_pct']}%")

    print("\n✅ Latency profiling selesai!")

if __name__ == "__main__":
    main()
