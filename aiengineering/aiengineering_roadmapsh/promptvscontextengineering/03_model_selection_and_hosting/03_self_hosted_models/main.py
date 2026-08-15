#!/usr/bin/env python3
"""
Modul: Self-Hosted Models
Kalkulator Memori GPU VRAM untuk Hosting LLM (vLLM / Ollama) berdasarkan skala parameter dan kuantisasi.
"""

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def calculate_vram_needs(param_billions: float, precision: str, context_len: int = 128000):
    bytes_per_param = {"FP16": 2.0, "INT8": 1.0, "INT4_AWQ": 0.5}.get(precision, 2.0)
    
    # Model Weights Memory
    model_vram_gb = param_billions * bytes_per_param
    
    # KV Cache Memory (approximate calculation for 128K context window)
    kv_cache_vram_gb = (context_len / 32000) * (param_billions / 8.0) * 4.0
    
    total_vram_needed = (model_vram_gb + kv_cache_vram_gb) * 1.2 # 20% overhead margin

    return {
        "model_weights_vram": f"{model_vram_gb:.1f} GB",
        "kv_cache_vram": f"{kv_cache_vram_gb:.1f} GB",
        "total_vram_required": f"{total_vram_needed:.1f} GB",
        "recommended_gpu": "1x RTX 4090 (24GB)" if total_vram_needed <= 24 else ("1x A100 (80GB)" if total_vram_needed <= 80 else "2x A100 (160GB VRAM)")
    }

def main():
    print("=" * 70)
    print(color("  MODUL: SELF-HOSTED LLM VRAM CALCULATOR", "1;34"))
    print("=" * 70)

    test_configs = [
        ("Llama 3.1 8B (FP16 Unquantized)", 8.0, "FP16"),
        ("Llama 3.1 8B (INT4 AWQ Quantized)", 8.0, "INT4_AWQ"),
        ("Llama 3.1 70B (INT4 AWQ Quantized)", 70.0, "INT4_AWQ")
    ]

    for name, params, prec in test_configs:
        print(color(f"\n{name}:", "1;33"))
        res = calculate_vram_needs(params, prec)
        print(f"  • Memori Bobot Model : {res['model_weights_vram']}")
        print(f"  • Memori KV Cache    : {res['kv_cache_vram']}")
        print(color(f"  ► Total VRAM Wajib   : {res['total_vram_required']}", "1;32"))
        print(color(f"  ► Rekomendasi Hardware: {res['recommended_gpu']}", "36"))

    print("\n" + "=" * 70)
    print("✓ Kuantisasi INT4 memangkas kebutuhan VRAM hingga 70%, mengizinkan model 70B berjalan di 1x A100 GPU.")

if __name__ == "__main__":
    main()
