"""
=================================================================
2. COST & LATENCY TRACKING
=================================================================
Di production, 3 hal yang HARUS dimonitor:
1. BIAYA  — berapa cost per request/hari/bulan?
2. LATENSI — seberapa cepat model merespons?
3. THROUGHPUT — berapa request bisa dilayani per detik?

Tanpa monitoring ini, Anda bisa:
- Kehabisan budget tanpa sadar
- Memberikan pengalaman user yang buruk (lambat)
- Gagal scale saat traffic meningkat
=================================================================
"""

import time
import random
import statistics
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime


# ─────────────────────────────────────────────────────
# SIMULASI COST TRACKING
# ─────────────────────────────────────────────────────

@dataclass
class InferenceLog:
    """Log untuk setiap request inference."""
    timestamp: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    latency_ms: float
    cost_usd: float
    status: str  # "success" atau "error"


class CostTracker:
    """Melacak biaya inference per model."""
    
    # Harga per 1M token (estimasi)
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        "claude-3.5-sonnet": {"input": 3.00, "output": 15.00},
        "claude-3-haiku": {"input": 0.25, "output": 1.25},
        "llama-3.1-70b (self-hosted)": {"input": 0.0, "output": 0.0},
    }

    def __init__(self):
        self.logs: list[InferenceLog] = []

    def hitung_biaya(self, model: str, prompt_tokens: int, completion_tokens: int) -> float:
        """Hitung biaya berdasarkan model dan jumlah token."""
        if model not in self.PRICING:
            return 0.0
        pricing = self.PRICING[model]
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost

    def log_request(self, model, prompt_tokens, completion_tokens, latency_ms, status="success"):
        """Catat setiap request inference."""
        cost = self.hitung_biaya(model, prompt_tokens, completion_tokens)
        log = InferenceLog(
            timestamp=datetime.now().isoformat(),
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            latency_ms=latency_ms,
            cost_usd=cost,
            status=status
        )
        self.logs.append(log)
        return log

    def ringkasan(self):
        """Menghasilkan ringkasan cost & performance."""
        if not self.logs:
            return "Belum ada log."

        success_logs = [l for l in self.logs if l.status == "success"]
        
        total_cost = sum(l.cost_usd for l in self.logs)
        total_tokens = sum(l.total_tokens for l in self.logs)
        total_requests = len(self.logs)
        error_rate = (total_requests - len(success_logs)) / total_requests * 100

        latencies = [l.latency_ms for l in success_logs]
        latencies.sort()

        p50 = latencies[len(latencies) // 2] if latencies else 0
        p95 = latencies[int(len(latencies) * 0.95)] if latencies else 0
        p99 = latencies[int(len(latencies) * 0.99)] if latencies else 0

        # Per-model breakdown
        model_stats = defaultdict(lambda: {"count": 0, "tokens": 0, "cost": 0.0})
        for log in self.logs:
            model_stats[log.model]["count"] += 1
            model_stats[log.model]["tokens"] += log.total_tokens
            model_stats[log.model]["cost"] += log.cost_usd

        return {
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_cost_usd": total_cost,
            "error_rate_pct": error_rate,
            "latency": {"p50": p50, "p95": p95, "p99": p99, "avg": statistics.mean(latencies) if latencies else 0},
            "per_model": dict(model_stats)
        }


def demo_cost_tracking():
    """Demo pelacakan biaya inference."""
    print("=" * 60)
    print("DEMO 1: Cost Tracking")
    print("=" * 60)

    tracker = CostTracker()

    # Harga per model
    print("\n💰 Harga per 1M Token:")
    print(f"   {'Model':<35} | {'Input':>8} | {'Output':>8}")
    print(f"   {'-'*35}-+-{'-'*8}-+-{'-'*8}")
    for model, prices in CostTracker.PRICING.items():
        print(f"   {model:<35} | ${prices['input']:>7.2f} | ${prices['output']:>7.2f}")

    # Simulasi 100 requests
    print(f"\n📊 Simulasi 100 Requests (campuran model):")

    models = ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
    for _ in range(100):
        model = random.choice(models)
        prompt_tokens = random.randint(100, 2000)
        completion_tokens = random.randint(50, 500)
        latency = random.uniform(200, 3000)
        status = "success" if random.random() > 0.02 else "error"

        tracker.log_request(model, prompt_tokens, completion_tokens, latency, status)

    summary = tracker.ringkasan()

    print(f"\n   📈 Ringkasan:")
    print(f"   Total requests : {summary['total_requests']}")
    print(f"   Total tokens   : {summary['total_tokens']:,}")
    print(f"   Total cost     : ${summary['total_cost_usd']:.4f}")
    print(f"   Error rate     : {summary['error_rate_pct']:.1f}%")

    print(f"\n   ⏱️ Latensi:")
    lat = summary['latency']
    print(f"   P50 : {lat['p50']:.0f} ms")
    print(f"   P95 : {lat['p95']:.0f} ms")
    print(f"   P99 : {lat['p99']:.0f} ms")
    print(f"   Avg : {lat['avg']:.0f} ms")

    print(f"\n   📋 Per Model:")
    for model, stats in summary['per_model'].items():
        print(f"   {model}: {stats['count']} requests, "
              f"{stats['tokens']:,} tokens, ${stats['cost']:.4f}")


def demo_estimasi_biaya_bulanan():
    """Estimasi biaya bulanan berdasarkan pola penggunaan."""
    print("\n" + "=" * 60)
    print("DEMO 2: Estimasi Biaya Bulanan")
    print("=" * 60)

    skenario = [
        {
            "nama": "Startup Kecil",
            "requests_per_day": 1000,
            "avg_prompt_tokens": 500,
            "avg_completion_tokens": 200,
            "model": "gpt-4o-mini"
        },
        {
            "nama": "Perusahaan Medium",
            "requests_per_day": 10000,
            "avg_prompt_tokens": 800,
            "avg_completion_tokens": 300,
            "model": "gpt-4o"
        },
        {
            "nama": "Enterprise",
            "requests_per_day": 100000,
            "avg_prompt_tokens": 1000,
            "avg_completion_tokens": 500,
            "model": "gpt-4o"
        },
        {
            "nama": "Self-Hosted (Llama)",
            "requests_per_day": 100000,
            "avg_prompt_tokens": 1000,
            "avg_completion_tokens": 500,
            "model": "llama-3.1-70b (self-hosted)"
        },
    ]

    tracker = CostTracker()

    print(f"\n📊 Estimasi Biaya Bulanan (30 hari):")
    print(f"   {'Skenario':<25} | {'Req/Day':>10} | {'Model':<20} | {'Biaya/Bulan':>12}")
    print(f"   {'-'*25}-+-{'-'*10}-+-{'-'*20}-+-{'-'*12}")

    for s in skenario:
        daily_cost = tracker.hitung_biaya(
            s['model'],
            s['requests_per_day'] * s['avg_prompt_tokens'],
            s['requests_per_day'] * s['avg_completion_tokens']
        )
        monthly_cost = daily_cost * 30

        print(f"   {s['nama']:<25} | {s['requests_per_day']:>10,} | {s['model']:<20} | ${monthly_cost:>11,.2f}")

    print(f"""
    💡 Tips Menghemat Biaya:
    1. Gunakan model kecil untuk task sederhana (gpt-4o-mini)
    2. Cache response untuk query yang sering diulang
    3. Optimalkan prompt (kurangi token yang tidak perlu)
    4. Pertimbangkan self-hosting untuk volume tinggi
    5. Gunakan batch API untuk non-real-time tasks (50% lebih murah)
    """)


def demo_latency_monitoring():
    """Penjelasan tentang monitoring latensi."""
    print("=" * 60)
    print("DEMO 3: Latency Monitoring Best Practices")
    print("=" * 60)

    print("""
    ⏱️ METRIK LATENSI YANG PENTING:

    1. P50 (Median)
       - 50% requests selesai dalam waktu ini
       - Menunjukkan "pengalaman tipikal"
       - Target: <1000ms untuk chat

    2. P95
       - 95% requests selesai dalam waktu ini
       - Menunjukkan "pengalaman worst-case yang umum"
       - Target: <3000ms

    3. P99
       - 99% requests selesai dalam waktu ini
       - Menunjukkan tail latency (outlier)
       - Target: <5000ms

    4. TTFT (Time to First Token)
       - Khusus streaming — waktu sampai token pertama muncul
       - Target: <500ms

    📊 DASHBOARD MONITORING:
    ┌─────────────────────────────────────────────┐
    │  Model Performance Dashboard                │
    ├─────────────────────────────────────────────┤
    │  Latency (ms)        │ Throughput (req/s)   │
    │  P50: ███████ 450    │ Current: ████ 45     │
    │  P95: █████████ 1200 │ Peak:    ██████ 120  │
    │  P99: ██████████ 2500│ Min:     ██ 12       │
    ├─────────────────────────────────────────────┤
    │  Error Rate: 0.3%    │ Cost Today: $12.45   │
    │  Uptime: 99.97%      │ Cost MTD:   $234.50  │
    └─────────────────────────────────────────────┘

    🛠️ TOOLS UNTUK MONITORING:
    - Prometheus + Grafana (open-source)
    - Datadog, New Relic (SaaS)
    - LangSmith (khusus LLM)
    - Helicone (proxy + analytics untuk OpenAI)
    """)


def main():
    demo_cost_tracking()
    demo_estimasi_biaya_bulanan()
    demo_latency_monitoring()

    print("\n✅ Selesai! Lanjut ke: 3_logging_tracing.py")

if __name__ == "__main__":
    main()
