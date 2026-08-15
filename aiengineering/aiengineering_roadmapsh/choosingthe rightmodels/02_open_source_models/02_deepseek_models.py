#!/usr/bin/env python3
"""
02_deepseek_models.py
Modul analisis mendalam arsitektur DeepSeek V3 dan DeepSeek R1:
- Mixture-of-Experts (MoE) Architecture (671B Total / 37B Active)
- Reinforcement Learning Chain-of-Thought (R1 Reasoning)
- Distilled Models (1.5B, 7B, 8B, 14B, 32B, 70B)
"""

from typing import Dict, Any

def demonstrate_moe_efficiency(total_params_b: float, active_params_b: float) -> Dict[str, Any]:
    """Demonstrasi perhitungan efisiensi Mixture-of-Experts (MoE)."""
    saved_computation_percent = (1 - (active_params_b / total_params_b)) * 100
    return {
        "total_params": f"{total_params_b}B",
        "active_params_per_token": f"{active_params_b}B",
        "computation_reduction": f"{round(saved_computation_percent, 1)}%",
        "efficiency_note": f"Hanya {active_params_b}B parameter diaktifkan per token, memberikan performa model 671B dengan kecepatan 37B!"
    }

def main():
    print("=" * 65)
    print(" 🐳 DEEPSEEK V3 & R1 REASONING ARCHITECTURE EXPLORER")
    print("=" * 65)
    
    moe_stats = demonstrate_moe_efficiency(671.0, 37.0)
    print(f"\n⚡ MoE Architecture Advantage (DeepSeek V3 / R1):")
    print(f" • Total Parameters: {moe_stats['total_params']}")
    print(f" • Active Parameters: {moe_stats['active_params_per_token']}")
    print(f" • Hemat Komputasi: {moe_stats['computation_reduction']}")
    print(f" 💡 {moe_stats['efficiency_note']}")
    
    print("\n🧠 DeepSeek R1 Reasoning Innovations:")
    print(" 1. RL Murni (Pure Reinforcement Learning) tanpa SFT awal untuk mendorong Chain-of-Thought alami.")
    print(" 2. Distillation ke Open Weights kecil:")
    distilled_models = [
        ("DeepSeek-R1-Distill-Qwen-1.5B", "Mobile / Edge Device Reasoning"),
        ("DeepSeek-R1-Distill-Llama-8B", "Consumer Laptop / RTX 4060 GPU"),
        ("DeepSeek-R1-Distill-Qwen-14B / 32B", "Best Performance/Size Sweet Spot"),
        ("DeepSeek-R1-Distill-Llama-70B", "Enterprise On-Premises Frontier Reasoning")
    ]
    for d, target in distilled_models:
        print(f"   • {d:<35} ➔ Target: {target}")
        
    print("\n✅ Kesimpulan: DeepSeek R1 membuktikan bahwa model open-source dapat mencapai level reasoning o1 dengan biaya pelatihan & inferensi jauh lebih efisien.")

if __name__ == "__main__":
    main()
