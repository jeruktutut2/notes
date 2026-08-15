"""
==============================================================================
MODULE MONITORING & OBSERVABILITY AI
==============================================================================
Memantau performa, latensi, penggunaan token, dan estimasi biaya operasional API
secara real-time (Telemetri AI).

DOKUMENTASI OBSERVABILITY:
    - Estimasi Biaya Token (misal model Gemini Flash / GPT-4o)
    - P95 / P99 Latensi eksekusi
    - Log Tracing audit trail per request ID
==============================================================================
"""

import time
import logging
from typing import Dict, Any

# Konfigurasi Logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("AIObservability")

# Tarif estimasi (USD per 1K Token)
HARGA_PER_1K_INPUT = 0.00015   # Est: $0.15 / 1M token
HARGA_PER_1K_OUTPUT = 0.00060  # Est: $0.60 / 1M token


class AIMonitor:
    def __init__(self):
        self.total_requests = 0
        self.total_tokens_input = 0
        self.total_tokens_output = 0
        self.total_cost_usd = 0.0
        self.latency_records = []

    def catat_request(self, prompt_text: str, response_text: str, duration_sec: float) -> Dict[str, Any]:
        """
        Mencatat telemetri satu kali transaksi request AI.
        """
        self.total_requests += 1
        
        # Estimasi kasar jumlah token (1 token ≈ 4 karakter)
        input_tokens = max(1, len(prompt_text) // 4)
        output_tokens = max(1, len(response_text) // 4)

        biaya_input = (input_tokens / 1000) * HARGA_PER_1K_INPUT
        biaya_output = (output_tokens / 1000) * HARGA_PER_1K_OUTPUT
        biaya_total = biaya_input + biaya_output

        self.total_tokens_input += input_tokens
        self.total_tokens_output += output_tokens
        self.total_cost_usd += biaya_total
        self.latency_records.append(duration_sec)

        telemetri = {
            "request_id": self.total_requests,
            "duration_sec": round(duration_sec, 3),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "estimated_cost_usd": round(biaya_total, 6)
        }

        logger.info(
            f"REQ #{self.total_requests} | Latency: {duration_sec:.2f}s | "
            f"Tokens: {input_tokens}in/{output_tokens}out | Cost: ${biaya_total:.6f}"
        )

        return telemetri

    def get_summary_metrics(self) -> Dict[str, Any]:
        """Mengembalikan data ringkasan kesehatan server AI."""
        avg_latency = (sum(self.latency_records) / len(self.latency_records)) if self.latency_records else 0.0
        return {
            "total_requests": self.total_requests,
            "total_tokens_used": self.total_tokens_input + self.total_tokens_output,
            "total_cost_usd": round(self.total_cost_usd, 4),
            "avg_latency_sec": round(avg_latency, 3)
        }


# Global Single Instance Monitor
monitor_global = AIMonitor()
