#!/usr/bin/env python3
"""
Modul: Streaming Responses
Simulasi Server-Sent Events (SSE) Streaming token demi token di terminal.
"""

import sys
import time

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: STREAMING RESPONSES (SSE SIMULATION)", "1;34"))
    print("=" * 70)

    sample_llm_response = (
        "Halo! Terima kasih telah menghubungi layanan AI Engineering. "
        "Streaming response memungkinkan token pertama langsung ditampilkan ke layar pengguna "
        "tanpa harus menunggu seluruh jawaban selesai digenerasi oleh server LLM."
    )

    print(color("\n[Simulasi Real-Time SSE Token Stream]:\n", "1;33"))
    tokens = sample_llm_response.split(" ")
    
    start_time = time.time()
    for idx, tok in enumerate(tokens):
        # Simulate token delivery delay
        time.sleep(0.08)
        sys.stdout.write(tok + " ")
        sys.stdout.flush()

    total_time = time.time() - start_time
    print(color(f"\n\n✓ Stream selesai dalam {total_time:.2f} detik (Average TTFT: ~80ms per token).", "1;32"))

if __name__ == "__main__":
    main()
