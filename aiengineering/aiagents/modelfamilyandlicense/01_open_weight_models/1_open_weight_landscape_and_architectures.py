#!/usr/bin/env python3
"""
Modul 1.1: Open Weight Model Landscape & Architectures
Visualisasi & Simulasi Komputasi Model Open Weight (Dense vs Mixture of Experts / MoE)
Berdasarkan Roadmap.sh / AI Agents - Model Families and Licences
"""

import sys
import math
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
class OpenWeightModelInfo:
    name: str
    developer: str
    architecture_type: str  # "Dense" or "MoE"
    total_params_b: float   # in Billions
    active_params_b: float  # in Billions
    context_length_k: int   # in Thousands
    license_type: str
    primary_strengths: List[str]

OPEN_WEIGHT_CATALOG: List[OpenWeightModelInfo] = [
    OpenWeightModelInfo(
        name="Llama 3.1 8B",
        developer="Meta AI",
        architecture_type="Dense",
        total_params_b=8.0,
        active_params_b=8.0,
        context_length_k=128,
        license_type="Llama 3 Community License",
        primary_strengths=["General Reasoning", "Tool Calling", "Multilingual Support", "Low Resource Serving"]
    ),
    OpenWeightModelInfo(
        name="Llama 3.3 70B",
        developer="Meta AI",
        architecture_type="Dense",
        total_params_b=70.0,
        active_params_b=70.0,
        context_length_k=128,
        license_type="Llama 3 Community License",
        primary_strengths=["Enterprise Reasoning", "SOTA Code Generation", "Instruction Following"]
    ),
    OpenWeightModelInfo(
        name="Mixtral 8x7B v0.1",
        developer="Mistral AI",
        architecture_type="MoE",
        total_params_b=46.7,
        active_params_b=12.9,
        context_length_k=32,
        license_type="Apache 2.0",
        primary_strengths=["High Speed Inference", "Low Active Params FLOPs", "Strong Math/Code"]
    ),
    OpenWeightModelInfo(
        name="Qwen 2.5 72B",
        developer="Alibaba Cloud",
        architecture_type="Dense",
        total_params_b=72.0,
        active_params_b=72.0,
        context_length_k=128,
        license_type="Qwen License / Apache 2.0 (for smaller models)",
        primary_strengths=["State-of-the-Art Coding", "Math Reasoning", "Agent Structured Output"]
    ),
    OpenWeightModelInfo(
        name="DeepSeek V3 / R1",
        developer="DeepSeek",
        architecture_type="MoE",
        total_params_b=671.0,
        active_params_b=37.0,
        context_length_k=128,
        license_type="MIT License",
        primary_strengths=["Advanced Chain-of-Thought", "Multi-Head Latent Attention", "Unmatched MoE Cost Efficiency"]
    ),
    OpenWeightModelInfo(
        name="Gemma 2 27B",
        developer="Google",
        architecture_type="Dense",
        total_params_b=27.0,
        active_params_b=27.0,
        context_length_k=8,
        license_type="Gemma Terms of Use",
        primary_strengths=["High Efficiency per Parameter", "Safety Filter Alignment", "On-Device Friendly"]
    ),
    OpenWeightModelInfo(
        name="Phi-4 14B",
        developer="Microsoft",
        architecture_type="Dense",
        total_params_b=14.0,
        active_params_b=14.0,
        context_length_k=16,
        license_type="MIT License",
        primary_strengths=["Synthetic Data Trained", "Math & Logic Puzzles", "Compact Footprint"]
    )
]

def calculate_vram_and_throughput(params_b: float, active_params_b: float, precision_bits: int = 16, batch_size: int = 1):
    """
    Menghitung estimasi VRAM & throughput berdasarkan arsitektur model
    """
    bytes_per_param = precision_bits / 8.0
    # Base VRAM untuk bobot model
    weights_vram_gb = params_b * bytes_per_param
    # KV Cache + Overhead ~ 20%
    overhead_vram_gb = weights_vram_gb * 0.20
    total_vram_gb = weights_vram_gb + overhead_vram_gb
    
    # Estimasi Memory Bandwidth bottleneck (misal GPU H100 ~ 3.35 TB/s vs RTX 4090 ~ 1.0 TB/s)
    rtx4090_bw = 1008.0  # GB/s
    # Token generation time ~ (Active Bytes Transferred) / Memory Bandwidth
    active_bytes_gb = active_params_b * bytes_per_param
    tok_per_sec_4090 = rtx4090_bw / active_bytes_gb if active_bytes_gb > 0 else 0
    
    return {
        "weights_vram_gb": weights_vram_gb,
        "total_vram_gb": total_vram_gb,
        "active_bytes_gb": active_bytes_gb,
        "estimated_tok_sec_rtx4090": tok_per_sec_4090
    }

def print_model_catalog():
    print(f"\n{BOLD}{HEADER}=== KATALOG MODEL OPEN WEIGHT UTAMA UNTUK AI AGENTS ==={RESET}\n")
    print(f"{'Nama Model':<22} | {'Developer':<14} | {'Tipe':<6} | {'Total P':<8} | {'Active P':<8} | {'Lisensi':<25}")
    print("-" * 95)
    for m in OPEN_WEIGHT_CATALOG:
        print(f"{CYAN}{m.name:<22}{RESET} | {m.developer:<14} | {YELLOW}{m.architecture_type:<6}{RESET} | {m.total_params_b:>6.1f}B | {m.active_params_b:>6.1f}B | {GREEN}{m.license_type:<25}{RESET}")

def run_architectural_comparison():
    print(f"\n{BOLD}{HEADER}=== SIMULASI KOMPUTASI: DENSE VS MIXTURE OF EXPERTS (MoE) ==={RESET}\n")
    print("Membandingkan efisiensi Serving dua model kelas berat:")
    print(f" 1. {BOLD}Llama 3.3 70B{RESET} (Dense Model - 70B parameter aktif per token)")
    print(f" 2. {BOLD}DeepSeek V3 (671B MoE){RESET} (MoE Model - 671B Total, 37B Aktif per token)\n")

    l3 = calculate_vram_and_throughput(70.0, 70.0, precision_bits=16)
    ds = calculate_vram_and_throughput(671.0, 37.0, precision_bits=16)

    l3_q4 = calculate_vram_and_throughput(70.0, 70.0, precision_bits=4)
    ds_q4 = calculate_vram_and_throughput(671.0, 37.0, precision_bits=4)

    print(f"{BOLD}{CYAN}1. Perhitungan Presisi FP16 (16-bit):{RESET}")
    print(f"   • Llama 3.3 70B (Dense):")
    print(f"     - VRAM Bobot    : {l3['weights_vram_gb']:.1f} GB (Butuh ~2x GPU A100 80GB)")
    print(f"     - Active Memory : {l3['active_bytes_gb']:.1f} GB per token")
    print(f"     - Est. Speed 4090: {l3['estimated_tok_sec_rtx4090']:.1f} tok/s (jika muat)")
    
    print(f"   • DeepSeek V3 (MoE 671B):")
    print(f"     - VRAM Bobot    : {ds['weights_vram_gb']:.1f} GB (Butuh Cluster Multi-GPU VRAM)")
    print(f"     - Active Memory : {ds['active_bytes_gb']:.1f} GB per token ({BOLD}{GREEN}hanya ~53% dari Llama 70B!{RESET})")
    print(f"     - Est. Speed 4090: {ds['estimated_tok_sec_rtx4090']:.1f} tok/s")

    print(f"\n{BOLD}{CYAN}2. Perhitungan Presisi Kuantisasi GGUF INT4 (4-bit):{RESET}")
    print(f"   • Llama 3.3 70B (INT4) : VRAM ~{l3_q4['total_vram_gb']:.1f} GB -> {GREEN}Muat dalam 1x Mac Studio M2 Ultra (64GB/192GB RAM)!{RESET}")
    print(f"   • DeepSeek V3 (INT4)   : VRAM ~{ds_q4['total_vram_gb']:.1f} GB -> Memerlukan server multi-socket / multi-GPU.")

def interactive_calculator():
    print(f"\n{BOLD}{HEADER}=== KALKULATOR Serving VRAM & BANDWIDTH AI AGENT ==={RESET}")
    try:
        params = float(input("\nMasukkan total parameter model (dalam Miliar, misal 8 atau 70): ").strip())
        is_moe = input("Apakah arsitektur MoE? (y/n): ").strip().lower() == 'y'
        active = params
        if is_moe:
            active = float(input("Masukkan parameter AKTIF per token (dalam Miliar, misal 13 atau 37): ").strip())
        
        bits = int(input("Pilih presisi (16 untuk FP16, 8 untuk INT8, 4 untuk INT4): ").strip())
        res = calculate_vram_and_throughput(params, active, bits)
        
        print(f"\n{BOLD}{GREEN}--- HASIL KALKULASI INFRASTRUKTUR ---{RESET}")
        print(f"• VRAM Minimum Bobot Model : {res['weights_vram_gb']:.2f} GB")
        print(f"• VRAM Direkomendasikan    : {res['total_vram_gb']:.2f} GB (Termasuk KV Cache)")
        print(f"• Active Transfer per Token: {res['active_bytes_gb']:.2f} GB")
        print(f"• Est. Generation Throughput: ~{res['estimated_tok_sec_rtx4090']:.1f} tokens/detik (Memory-Bandwidth-bound)")
    except ValueError:
        print(f"{RED}Input tidak valid. Menggunakan estimasi standar.{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 1.1: OPEN WEIGHT MODEL LANDSCAPE & ARCHITECTURES{RESET}")
    print(f"{CYAN}Berdasarkan roadmap.sh/ai-agents (Model Families and Licences){RESET}")
    print("█" * 75)

    print_model_catalog()
    run_architectural_comparison()
    
    print("\nApakah Anda ingin mencoba Kalkulator VRAM kustom?")
    ans = input("Jawab (y/n): ").strip().lower()
    if ans == 'y':
        interactive_calculator()
    
    print(f"\n{GREEN}✔ Modul 1.1 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
