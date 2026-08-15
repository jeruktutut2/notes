#!/usr/bin/env python3
"""
Modul 03: Hardware & GPU Sizing Assistant untuk Self-Hosting
Rekomendasi spesifikasi server GPU (NVIDIA RTX 4090, A100, H100)
dan Apple Silicon Unified Memory berdasarkan estimasi target Throughput & Concurrent Users.
"""

def recommend_hardware_spec(
    model_family: str,
    param_size_b: float,
    concurrent_users: int = 10,
    target_tps_per_user: int = 25
) -> dict:
    """
    Menghitung kebutuhan hardware server berdasarkan target performa.
    """
    total_tps_required = concurrent_users * target_tps_per_user
    
    if param_size_b <= 8.0:
        base_vram = 8.0 # 4-bit INT4
        if concurrent_users <= 5:
            gpu_option = "1x NVIDIA RTX 4090 (24GB VRAM) atau Apple Mac Studio M3 Ultra (64GB)"
            cost_est = "~$250/bln (Cloud GPU) / $1,999 (Buy)"
        else:
            gpu_option = "2x NVIDIA RTX 4090 (24GB) atau 1x NVIDIA A10G (24GB)"
            cost_est = "~$500/bln (Cloud GPU)"
    elif param_size_b <= 22.0:
        base_vram = 18.0
        if concurrent_users <= 10:
            gpu_option = "1x NVIDIA A100 (80GB VRAM) atau Apple Mac Studio M2/M3 Max (96GB)"
            cost_est = "~$1,200/bln (Cloud GPU)"
        else:
            gpu_option = "2x NVIDIA A100 (80GB VRAM)"
            cost_est = "~$2,400/bln (Cloud GPU)"
    elif param_size_b <= 70.0:
        base_vram = 45.0
        if concurrent_users <= 20:
            gpu_option = "2x NVIDIA A100 (80GB VRAM) (Tensor Parallelism = 2)"
            cost_est = "~$2,400/bln (Cloud GPU)"
        else:
            gpu_option = "4x NVIDIA H100 (80GB VRAM) (Tensor Parallelism = 4)"
            cost_est = "~$8,000/bln (Cloud GPU)"
    else: # 405B+
        gpu_option = "8x NVIDIA H100 (80GB VRAM) (Tensor Parallelism = 8)"
        cost_est = "~$18,000/bln (Cloud GPU)"

    return {
        "model": f"{model_family} {param_size_b}B",
        "concurrent_users": concurrent_users,
        "total_tps_target": total_tps_required,
        "recommended_hardware": gpu_option,
        "est_monthly_cost": cost_est
    }

def main():
    print("=" * 80)
    print("      HARDWARE & GPU SIZING ASSISTANT UNTUK SELF-HOSTING LLM")
    print("=" * 80)
    
    scenarios = [
        {"name": "Internal Company Chatbot", "model": "Llama-3.1", "params": 8.0, "users": 5, "tps": 30},
        {"name": "Customer Support RAG Bot", "model": "Qwen-2.5", "params": 14.0, "users": 25, "tps": 20},
        {"name": "Enterprise Reasoning Engine", "model": "Llama-3.1", "params": 70.0, "users": 15, "tps": 25},
        {"name": "Frontier Open Model Engine", "model": "Llama-3.1", "params": 405.0, "users": 50, "tps": 20},
    ]
    
    print("\nRekomendasi Hardware Server berdasarkan Target Beban:\n")
    
    for sc in scenarios:
        res = recommend_hardware_spec(sc["model"], sc["params"], sc["users"], sc["tps"])
        print(f"📌 Scenario     : {sc['name']} ({res['model']})")
        print(f"   Beban Target : {res['concurrent_users']} Concurrent Users -> Target {res['total_tps_target']} Tokens/sec")
        print(f"   Opsi Hardware: {res['recommended_hardware']}")
        print(f"   Est. Biaya   : {res['est_monthly_cost']}\n")

    print("💡 SYARAT NETWORK & MEMORY BANDWIDTH:")
    print("• Kecepatan inferensi LLM didominasi oleh **GPU Memory Bandwidth** (GB/s).")
    print("• NVIDIA H100 memikili ~3,350 GB/s bandwidth (3x lebih cepat dari RTX 4090 ~1,000 GB/s).")

if __name__ == "__main__":
    main()
