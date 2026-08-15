#!/usr/bin/env python3
"""
Modul 1: Streamed vs Unstreamed Responses Simulator
Mengilustrasikan perbedaan transmisi token, Time-to-First-Token (TTFT), Total Latency,
dan aspek User Experience (UX) antara HTTP Blocking (Batch) vs Server-Sent Events (SSE).
"""

import time
import sys
from dataclasses import dataclass
from typing import List, Generator

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class ResponseMetrics:
    mode: str
    ttft_seconds: float
    total_time_seconds: float
    token_count: int
    itl_seconds: float  # Inter-Token Latency

SAMPLE_RESPONSE_TOKENS = [
    "AI", " Agents", " memerlukan", " strategi", " transmisi", " data", " yang",
    " responsif.", " Dengan", " menggunakan", " Streaming", " (SSE),", " pengguna",
    " dapat", " membaca", " hasil", " generasi", " secara", " seketika", " tanpa",
    " harus", " menunggu", " seluruh", " respon", " selesai", " dibuat."
]

def simulate_llm_inference_unstreamed(tokens: List[str], prefill_delay: float = 0.3, per_token_delay: float = 0.08) -> tuple[str, ResponseMetrics]:
    """Simulasi unstreamed (blocking response): Menunggu seluruh token selesai diproses."""
    start_time = time.time()
    
    # 1. Prefill / Prompt Processing phase
    time.sleep(prefill_delay)
    
    # 2. Generation phase (blocking backend)
    for _ in tokens:
        time.sleep(per_token_delay)
        
    total_time = time.time() - start_time
    full_text = "".join(tokens)
    
    # Unstreamed: TTFT adalah TOTAL wkt karena client tidak menerima data sampai akhir
    metrics = ResponseMetrics(
        mode="Unstreamed (Blocking Batch)",
        ttft_seconds=total_time,
        total_time_seconds=total_time,
        token_count=len(tokens),
        itl_seconds=per_token_delay
    )
    return full_text, metrics

def simulate_llm_inference_streamed(tokens: List[str], prefill_delay: float = 0.3, per_token_delay: float = 0.08) -> Generator[str, None, ResponseMetrics]:
    """Simulasi streamed response (SSE): Memancar token demi token secara real-time."""
    start_time = time.time()
    
    # 1. Prefill / Prompt Processing phase
    time.sleep(prefill_delay)
    
    # 2. Token Pertama (TTFT)
    ttft = time.time() - start_time
    yield tokens[0]
    first_token_time = time.time()
    
    # 3. Generating sisa token
    for token in tokens[1:]:
        time.sleep(per_token_delay)
        yield token
        
    total_time = time.time() - start_time
    avg_itl = (total_time - ttft) / (len(tokens) - 1) if len(tokens) > 1 else 0
    
    metrics = ResponseMetrics(
        mode="Streamed (Server-Sent Events / SSE)",
        ttft_seconds=ttft,
        total_time_seconds=total_time,
        token_count=len(tokens),
        itl_seconds=avg_itl
    )
    return metrics

def run_demo():
    print(f"\n{BOLD}{HEADER}=== SIMULASI STREAMED VS UNSTREAMED RESPONSES ==={RESET}\n")
    print(f"{CYAN}Skenario: LLM menghasilkan {len(SAMPLE_RESPONSE_TOKENS)} token respon.{RESET}\n")

    # -------------------------------------------------------------
    # 1. SIMULASI UNSTREAMED (BLOCKING BATCH)
    # -------------------------------------------------------------
    print(f"{BOLD}[ 1. UNSTREAMED RESPONSE (BLOCKING HTTP POST) ]{RESET}")
    print(f"{YELLOW}Status: Mengirim Request... Menunggu server menyelesaikan seluruh generasi...{RESET}")
    
    sys.stdout.flush()
    text_unstreamed, metrics_unstreamed = simulate_llm_inference_unstreamed(SAMPLE_RESPONSE_TOKENS)
    
    print(f"{GREEN}▶ Respon Diterima Sekaligus (Blocking Done):{RESET}")
    print(f"{BOLD}\"{text_unstreamed}\"{RESET}\n")
    
    print(f"  • Time-to-First-Token (TTFT) : {RED}{metrics_unstreamed.ttft_seconds:.3f} s{RESET} (User menunggu layar kosong!)")
    print(f"  • Total Generation Time       : {GREEN}{metrics_unstreamed.total_time_seconds:.3f} s{RESET}")
    print(f"  • Average Inter-Token Latency : {metrics_unstreamed.itl_seconds:.3f} s/token\n")

    time.sleep(1)

    # -------------------------------------------------------------
    # 2. SIMULASI STREAMED (SSE / CHUNKED TRANSFER)
    # -------------------------------------------------------------
    print(f"{BOLD}[ 2. STREAMED RESPONSE (SERVER-SENT EVENTS / SSE) ]{RESET}")
    print(f"{YELLOW}Status: Mengirim Request... Stream dimulai seketika:{RESET}\n")
    print(f"{GREEN}▶ Respon Streamed (Live Chunking):{RESET}\n  ", end="")
    sys.stdout.flush()
    
    stream_gen = simulate_llm_inference_streamed(SAMPLE_RESPONSE_TOKENS)
    
    tokens_received = []
    try:
        while True:
            chunk = next(stream_gen)
            tokens_received.append(chunk)
            print(f"{CYAN}{chunk}{RESET}", end="")
            sys.stdout.flush()
    except StopIteration as e:
        metrics_streamed = e.value

    print("\n")
    print(f"  • Time-to-First-Token (TTFT) : {GREEN}{metrics_streamed.ttft_seconds:.3f} s{RESET} (⚡ Instant Perceived UX!)")
    print(f"  • Total Generation Time       : {GREEN}{metrics_streamed.total_time_seconds:.3f} s{RESET}")
    print(f"  • Average Inter-Token Latency : {metrics_streamed.itl_seconds:.3f} s/token\n")

    # -------------------------------------------------------------
    # 3. TABEL COMPARISON & UX SUMMARY
    # -------------------------------------------------------------
    print(f"{BOLD}{HEADER}=== ANALISIS PERBANDINGAN PERFORMA ==={RESET}")
    ttft_improvement = ((metrics_unstreamed.ttft_seconds - metrics_streamed.ttft_seconds) / metrics_unstreamed.ttft_seconds) * 100
    
    print(f"• TTFT Improvement (Perceived Latency Reduksi): {BOLD}{GREEN}{ttft_improvement:.1f}% LEBIH CEPAT!{RESET}")
    print(f"• Total Latency: {BOLD}Sama ({metrics_streamed.total_time_seconds:.2f}s vs {metrics_unstreamed.total_time_seconds:.2f}s){RESET} karena kecepatan inferensi model identik.")
    
    print(f"\n{BOLD}[ KAPAN MENGGUNAKAN MASING-MASING MODE? ]{RESET}")
    print(f" 1. {BOLD}Gunakan Streamed (SSE){RESET}:")
    print("    - User-Facing Chat Interface, Live Writing Assistant, CLI Terminal Stream.")
    print("    - Membutuhkan Perceived Latency sangat kecil agar pengguna tidak merasa aplikasi membeku.")
    print(f" 2. {BOLD}Gunakan Unstreamed (Blocking){RESET}:")
    print("    - Backend Agent Steps, Function Calling (Tool Loop), Structured Outputs (JSON Parsing).")
    print("    - Membutuhkan validasi JSON utuh sebelum memanggil API eksternal.")

if __name__ == "__main__":
    run_demo()
