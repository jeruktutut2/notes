#!/usr/bin/env python3
"""
Modul 04: Kalkulator Interaktif VRAM & Parameter Model LLM
Perhitungan matematis presisi kebutuhan VRAM GPU untuk berbagai ukuran model LLM
(7B, 13B, 70B, 405B) berdasarkan bit precision, context length, dan batch size.
"""

def calculate_vram(
    params_in_billions: float,
    bits_per_param: int,
    context_length: int = 4096,
    batch_size: int = 1,
    num_layers: int = 32,
    hidden_size: int = 4096,
    num_heads: int = 32
) -> dict:
    """
    Menghitung estimasi kebutuhan memory GPU:
    1. Weight Memory
    2. KV Cache Memory
    3. Activation & Overhead Memory
    """
    # 1. Weight memory
    bytes_per_param = bits_per_param / 8.0
    weight_memory_gb = params_in_billions * bytes_per_param
    
    # 2. KV Cache Memory (approx formula: 2 * num_layers * num_heads * head_dim * context * batch * bytes)
    head_dim = hidden_size // num_heads
    kv_cache_bytes = 2 * num_layers * num_heads * head_dim * context_length * batch_size * 2 # FP16 KV cache
    kv_cache_gb = kv_cache_bytes / (1024 ** 3)
    
    # 3. CUDA & Runtime Overhead (10-20% margin)
    overhead_gb = max(1.5, weight_memory_gb * 0.15)
    
    total_vram_gb = weight_memory_gb + kv_cache_gb + overhead_gb
    
    return {
        "params_b": params_in_billions,
        "bits": bits_per_param,
        "weight_memory_gb": round(weight_memory_gb, 2),
        "kv_cache_gb": round(kv_cache_gb, 2),
        "overhead_gb": round(overhead_gb, 2),
        "total_vram_gb": round(total_vram_gb, 2),
        "rec_gpu": recommend_gpu(total_vram_gb)
    }

def recommend_gpu(vram_gb: float) -> str:
    if vram_gb <= 8.0:
        return "NVIDIA RTX 3060 / 4060 8GB atau Apple Mac M-Series 16GB"
    elif vram_gb <= 16.0:
        return "NVIDIA RTX 4070 / 4080 16GB atau Apple Mac M-Series 24GB"
    elif vram_gb <= 24.0:
        return "NVIDIA RTX 3090 / 4090 24GB atau Apple Mac M-Series 32GB"
    elif vram_gb <= 48.0:
        return "NVIDIA RTX 6000 Ada / A6000 48GB"
    elif vram_gb <= 80.0:
        return "1x NVIDIA A100 / H100 80GB"
    elif vram_gb <= 160.0:
        return "2x NVIDIA A100 80GB (Tensor Parallelism = 2)"
    else:
        return f"Cluster Multi-GPU ({int(vram_gb // 80) + 1}x NVIDIA H100 80GB)"

def main():
    print("=" * 75)
    print("      KALKULATOR VRAM GPU & PARAMETER MODEL LLM INTERAKTIF")
    print("=" * 75)
    
    models = [
        {"name": "Small Model (Llama-3.2 3B)", "params": 3.2, "bits": 4, "ctx": 8192},
        {"name": "Standard Local LLM (Llama-3.1 8B FP16)", "params": 8.0, "bits": 16, "ctx": 8192},
        {"name": "Standard Local LLM (Llama-3.1 8B INT4)", "params": 8.0, "bits": 4, "ctx": 8192},
        {"name": "Mid-tier Model (Mistral-Small 22B INT4)", "params": 22.0, "bits": 4, "ctx": 16384},
        {"name": "Enterprise Model (Llama-3.1 70B INT4)", "params": 70.0, "bits": 4, "ctx": 32768},
        {"name": "Frontier Model (Llama-3.1 405B INT8)", "params": 405.0, "bits": 8, "ctx": 16384},
    ]
    
    print(f"\n{'Nama Model & Konfigurasi':<36} | {'Weights':<8} | {'KV Cache':<9} | {'Total VRAM':<11} | {'Rekomendasi GPU'}")
    print("-" * 105)
    
    for m in models:
        res = calculate_vram(m["params"], m["bits"], context_length=m["ctx"])
        label = f"{m['name']} ({m['bits']}-bit)"
        print(f"{label:<36} | {res['weight_memory_gb']:5.1f} GB | {res['kv_cache_gb']:6.1f} GB | {res['total_vram_gb']:7.1f} GB  | {res['rec_gpu']}")

    print("\n💡 PETUNJUK VRAM:")
    print("1. Kuantisasi 4-bit menghemat ~75% VRAM dibanding FP16 tanpa penurunan penalaran drastis.")
    print("2. Panjang Konteks (Context Window) meningkatkan KV Cache secara linier terhadap batch size.")

if __name__ == "__main__":
    main()
