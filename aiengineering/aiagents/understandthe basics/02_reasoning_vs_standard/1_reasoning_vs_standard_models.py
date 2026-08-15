#!/usr/bin/env python3
"""
Modul 2: Reasoning vs Standard Models Simulator
Mengilustrasikan perbedaan arsitektur model penalaran mendalam (Chain-of-Thought / Reasoning Tokens)
seperti DeepSeek R1 / o1 / o3-mini dibandingkan Standard Direct Models (GPT-4o, Claude 3.5 Sonnet).
"""

import time
from dataclasses import dataclass
from typing import List, Dict

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
class ModelExecutionResult:
    model_name: str
    model_type: str  # "Standard" atau "Reasoning"
    prompt: str
    reasoning_tokens: List[str]
    final_output_tokens: List[str]
    total_latency: float
    accuracy_score: float  # 0.0 - 1.0

# Skenario Soal Logika Kompleks
PROBLEM_PROMPT = "Sebuah agen AI harus mendistribusikan 5 tugas ke 3 pekerja dengan batasan: Pekerja A maksimal 2 tugas, Pekerja B tidak boleh mengerjakan tugas #3, dan Pekerja C harus mengerjakan minimal 1 tugas. Berapa banyak kombinasi valid yang mungkin?"

def run_standard_model_simulation(prompt: str) -> ModelExecutionResult:
    """Simulasi Standard Model (GPT-4o / Claude 3.5 Sonnet): Langsung menghasilkan jawaban."""
    start = time.time()
    time.sleep(0.4)  # Fast inference
    
    # Standard model mencoba menjawab langsung
    output_tokens = [
        "Untuk", " menyelesaikan", " masalah", " ini,", " ada", " 5", " tugas", " dan", " 3", " pekerja.\n",
        "Kombinasi", " total", " tanpa", " batasan", " adalah", " 3^5", " =", " 243.\n",
        "Setelah", " memperhitungkan", " batasan", " Pekerja", " A,", " B,", " dan", " C,", " jumlah", " kombinasi",
        " valid", " yang", " didapatkan", " adalah", " 42", " kombinasi."
    ]
    
    latency = time.time() - start
    return ModelExecutionResult(
        model_name="GPT-4o / Claude 3.5 (Standard)",
        model_type="Standard Direct Model",
        prompt=prompt,
        reasoning_tokens=[],  # Tanpa hidden reasoning tokens
        final_output_tokens=output_tokens,
        total_latency=latency,
        accuracy_score=0.75  # Terkadang tergelincir pada logika kombinatoriks rumit
    )

def run_reasoning_model_simulation(prompt: str) -> ModelExecutionResult:
    """Simulasi Reasoning Model (DeepSeek R1 / o3-mini): Menggunakan Internal CoT / Thinking Tokens."""
    start = time.time()
    
    # Phase 1: Internal Thinking / CoT Loop
    reasoning_tokens = [
        "1. Analisis Variabel: N=5 tugas (T1,T2,T3,T4,T5), Pekerja (A, B, C).\n",
        "2. Batasan 1: count(A) <= 2.\n",
        "3. Batasan 2: Pekerja B tidak boleh T3 -> Pilihan T3 hanya (A atau C) [2 pilihan].\n",
        "4. Batasan 3: count(C) >= 1.\n",
        "5. Metodologi: Gunakan Principle of Inclusion-Exclusion (PIE) atau Kasus per Kasus berdasarkan count(A).\n",
        "   - Kasus A=0: T3 punya 1 pilihan (C). T1,T2,T4,T5 punya 2 pilihan (B,C). Total = 1 * 2^4 = 16. Kurangi kasus C=0 -> 16 - 1 = 15.\n",
        "   - Kasus A=1: Pilih 1 tugas untuk A (5 cara). Jika A dapat T3, sisa 4 tugas ke (B,C) [2^4=16]. C=0 -> 1. Total = 15. Kombinasi: 1 * 15 = 15.\n",
        "     Jika A tidak dapat T3 (4 cara), T3 harus C (1 cara). Sisa 3 tugas ke (B,C) [2^3=8]. C=0 -> 1. Total = 7. Kombinasi: 4 * 7 = 28.\n",
        "   - Kasus A=2: Cek kombinasi sub-kasus A=2...\n",
        "6. Verifikasi ulang seluruh syarat -> Hasil persis: 49 kombinasi valid."
    ]
    
    # Simulasi durasi thinking
    time.sleep(1.2)
    
    # Phase 2: Final Clean Response
    output_tokens = [
        "Berdasarkan", " analisis", " penalaran", " langkah", " demi", " langkah:\n",
        "Jumlah", " kombinasi", " valid", " yang", " memenuhi", " seluruh", " batasan", " adalah",
        " tepat", " 49", " kombinasi."
    ]
    
    latency = time.time() - start
    return ModelExecutionResult(
        model_name="DeepSeek R1 / OpenAI o3-mini",
        model_type="Reasoning Model (Chain-of-Thought)",
        prompt=prompt,
        reasoning_tokens=reasoning_tokens,
        final_output_tokens=output_tokens,
        total_latency=latency,
        accuracy_score=1.0  # Akurasi sempurna pada logika terstruktur
    )

def run_demo():
    print(f"\n{BOLD}{HEADER}=== SIMULASI REASONING VS STANDARD MODELS ==={RESET}\n")
    print(f"{CYAN}Soal Uji Logika Kompleks:{RESET}\n\"{PROBLEM_PROMPT}\"\n")
    print(f"{'='*75}\n")

    # 1. Standard Model Execution
    print(f"{BOLD}[ 1. EKSEKUSI STANDARD MODEL (GPT-4o / Claude 3.5) ]{RESET}")
    res_std = run_standard_model_simulation(PROBLEM_PROMPT)
    print(f"{YELLOW}Model Type: {res_std.model_type}{RESET}")
    print(f"Internal Thinking: {RED}(Tidak Ada / Direct Inference){RESET}")
    print(f"{GREEN}▶ Respon Output ({len(res_std.final_output_tokens)} tokens):{RESET}")
    print(f"{BOLD}\"{''.join(res_std.final_output_tokens)}\"{RESET}")
    print(f"⏱️ Waktu Eksekusi : {GREEN}{res_std.total_latency:.2f} detik{RESET}")
    print(f"🎯 Skor Akurasi Logika : {YELLOW}{res_std.accuracy_score * 100:.0f}%{RESET}\n")

    print(f"{'='*75}\n")

    # 2. Reasoning Model Execution
    print(f"{BOLD}[ 2. EKSEKUSI REASONING MODEL (DeepSeek R1 / OpenAI o3-mini) ]{RESET}")
    res_reason = run_reasoning_model_simulation(PROBLEM_PROMPT)
    print(f"{YELLOW}Model Type: {res_reason.model_type}{RESET}")
    
    print(f"\n{CYAN}🧠 Internal Reasoning Tokens / Thinking Process ({len(res_reason.reasoning_tokens)} CoT steps):{RESET}")
    for step in res_reason.reasoning_tokens:
        print(f"  {BLUE}│{RESET} {step}")
        time.sleep(0.05)
        
    print(f"\n{GREEN}▶ Jawaban Final ({len(res_reason.final_output_tokens)} tokens):{RESET}")
    print(f"{BOLD}\"{''.join(res_reason.final_output_tokens)}\"{RESET}")
    print(f"⏱️ Waktu Eksekusi : {YELLOW}{res_reason.total_latency:.2f} detik{RESET} (Termasuk Thinking Overhead)")
    print(f"🎯 Skor Akurasi Logika : {GREEN}{res_reason.accuracy_score * 100:.0f}% (SOTA Precision){RESET}\n")

    # 3. Dynamic Comparison Matrix
    print(f"{BOLD}{HEADER}=== ANALISIS PERBANDINGAN STRATEGIS ==={RESET}")
    print(f"┌──────────────────────────────┬─────────────────────────┬─────────────────────────┐")
    print(f"│ Metrik                       │ Standard Model          │ Reasoning Model         │")
    print(f"├──────────────────────────────┼─────────────────────────┼─────────────────────────┤")
    print(f"│ Total Tokens Processed       │ {len(res_std.final_output_tokens):<23} │ {len(res_reason.reasoning_tokens) + len(res_reason.final_output_tokens):<23} │")
    print(f"│ Latensi Respon               │ {res_std.total_latency:.2f}s (Cepat)            │ {res_reason.total_latency:.2f}s (Lebih Lambat)    │")
    print(f"│ Akurasi Penalaran Rumit      │ ~{res_std.accuracy_score*100:.0f}%                     │ ~{res_reason.accuracy_score*100:.0f}% (Sempurna)       │")
    print(f"│ Penggunaan Token Overhead    │ Minimal (0 Token CoT)   │ Tinggi (Ratusan CoT)    │")
    print(f"└──────────────────────────────┴─────────────────────────┴─────────────────────────┘")

    print(f"\n{BOLD}[ REKOMENDASI PENGGUNAAN PADA AI AGENTS ]{RESET}")
    print(" • Gunakan Standard Model (GPT-4o / Gemini Flash) untuk: Chat UI umum, Router Agent, Function Calling, Summarization.")
    print(" • Gunakan Reasoning Model (DeepSeek R1 / o3-mini) untuk: Planning Agent, Math/Physics Engine, Multi-Step Code Refactoring.")

if __name__ == "__main__":
    run_demo()
