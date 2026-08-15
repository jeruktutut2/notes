#!/usr/bin/env python3
"""
01_meta_llama.py
Modul eksplorasi keluarga Meta Llama 3.1 & 3.2:
- Llama 3.2 (1B/3B Lightweight & Edge)
- Llama 3.1 (8B Standard, 70B Enterprise, 405B Frontier Open Weight)
- Licensip & Hardware VRAM Calculator
"""

from typing import Dict, Any

def calculate_llama_hardware_req(param_billions: float, quant_bits: int = 4) -> Dict[str, Any]:
    """Menghitung estimasi VRAM GPU yang dibutuhkan untuk meng-host Llama model."""
    bytes_per_param = quant_bits / 8.0
    model_weight_gb = (param_billions * 1e9 * bytes_per_param) / (1024**3)
    kv_cache_overhead = model_weight_gb * 0.20 # 20% overhead context KV Cache & CUDA context
    total_vram_gb = model_weight_gb + kv_cache_overhead
    
    # Rekomendasi Hardware
    if total_vram_gb <= 8:
        hardware = "MacBook M1/M2/M3 (8GB RAM) / RTX 3060 (12GB)"
    elif total_vram_gb <= 24:
        hardware = "1x NVIDIA RTX 4090 (24GB VRAM) / Mac Studio (32GB)"
    elif total_vram_gb <= 80:
        hardware = "1x NVIDIA A100 (80GB VRAM) / 2x RTX 4090"
    else:
        hardware = "8x NVIDIA H100 (8x80GB VRAM cluster)"
        
    return {
        "params_b": param_billions,
        "quant_bits": f"INT{quant_bits}" if quant_bits < 16 else f"FP{quant_bits}",
        "weights_size_gb": round(model_weight_gb, 2),
        "recommended_vram_gb": round(total_vram_gb, 2),
        "hardware_recommendation": hardware
    }

def main():
    print("=" * 65)
    print(" 🦙 META LLAMA 3.1 / 3.2 ECOSYSTEM & VRAM HARDWARE SIZING")
    print("=" * 65)
    
    llama_family = [
        {"model": "Llama 3.2 1B / 3B", "use_case": "On-Device Mobile, Microcontrollers, Fast Edge NLP", "params": 3.0},
        {"model": "Llama 3.1 8B", "use_case": "General Chatbot, Local Dev, Efficient RAG", "params": 8.0},
        {"model": "Llama 3.1 70B", "use_case": "Enterprise Grade Reasoning, Complex Data Extraction", "params": 70.0},
        {"model": "Llama 3.1 405B", "use_case": "Frontier-level Open Weight Model (menyaingi GPT-4o)", "params": 405.0}
    ]
    
    print("\n📋 Meta Llama Model Lineup:")
    for l in llama_family:
        print(f"• {l['model']:<18} | Target: {l['use_case']}")
        
    print("\n🧮 Hardware & VRAM Estimation (Quantization INT4 / GGUF Q4_K_M):")
    for l in llama_family:
        req = calculate_llama_hardware_req(l["params"], quant_bits=4)
        print(f"  [{l['model']}] Size: {req['weights_size_gb']} GB ➔ Min VRAM: {req['recommended_vram_gb']} GB | Hardware: {req['hardware_recommendation']}")

    print("\n📜 Llama Community License Note:")
    print("  Bebas komersial hingga 700 Juta Monthly Active Users (MAU). Mendukung fine-tuning & deployment internal.")

if __name__ == "__main__":
    main()
