#!/usr/bin/env python3
"""
Modul 03: Matriks Trade-Off & Simulator Benchmark Biaya vs Performa
Menyediakan simulator kalkulasi Total Cost of Ownership (TCO)
antara memanggil Closed Proprietary API vs Sewa GPU Self-Hosted Open Weights.
"""

def simulate_tco_comparison(
    monthly_token_volume_millions: float,
    input_ratio: float = 0.7,
    output_ratio: float = 0.3
):
    """
    Menghitung estimasi biaya bulanan untuk volume token tertentu.
    """
    total_tokens = monthly_token_volume_millions * 1_000_000
    input_tokens = total_tokens * input_ratio
    output_tokens = total_tokens * output_ratio

    # 1. Closed API Costs (OpenAI GPT-4o-mini & GPT-4o)
    # GPT-4o-mini: $0.15 / 1M in, $0.60 / 1M out
    cost_gpt4o_mini = (input_tokens / 1e6 * 0.15) + (output_tokens / 1e6 * 0.60)
    
    # GPT-4o: $2.50 / 1M in, $10.00 / 1M out
    cost_gpt4o = (input_tokens / 1e6 * 2.50) + (output_tokens / 1e6 * 10.00)

    # 2. Self-Hosted GPU Costs (vLLM di Dedicated Server GPU Cloud)
    # 1x RTX 4090 (24GB VRAM) ~ $250 / bulan (dapat menangani ~20M token/bulan)
    # 1x A100 (80GB VRAM) ~ $1,200 / bulan (dapat menangani ~150M token/bulan)
    if monthly_token_volume_millions <= 20:
        gpu_setup = "1x RTX 4090 (24GB)"
        gpu_cost = 250.0
    elif monthly_token_volume_millions <= 150:
        gpu_setup = "1x A100 (80GB)"
        gpu_cost = 1200.0
    else:
        gpu_nodes = int(monthly_token_volume_millions // 150) + 1
        gpu_setup = f"{gpu_nodes}x A100 (80GB Cluster)"
        gpu_cost = gpu_nodes * 1200.0

    return {
        "volume_m": monthly_token_volume_millions,
        "gpt4o_mini_cost": round(cost_gpt4o_mini, 2),
        "gpt4o_cost": round(cost_gpt4o, 2),
        "self_hosted_gpu": gpu_setup,
        "self_hosted_cost": round(gpu_cost, 2),
        "cheapest_option": "Self-Hosted GPU" if gpu_cost < cost_gpt4o else "Closed API"
    }

def print_tradeoff_matrix():
    print("\nMATRIKS VALUASI STRATEGIS (CLOSED API VS OPEN WEIGHTS):")
    print("=" * 80)
    print(f"{'Kriteria':<22} | {'Closed Proprietary API':<26} | {'Self-Hosted Open Weights'}")
    print("-" * 80)
    print(f"{'Kecepatan Setup':<22} | {'Sangat Cepat (< 5 Menit)':<26} | {'Butuh Setup Infra (1-3 Hari)'}")
    print(f"{'Biaya Awal (CapEx)':<22} | {'$0 (Tanpa Sewa Hardware)':<26} | {'Perlu Deposit / Sewa GPU'}")
    print(f"{'Biaya Skala Besar':<22} | {'Mahal (Linier per Token)':<26} | {'Sangat Murah (Fixed GPU Rate)'}")
    print(f"{'Kepatuhan Privasi':<22} | {'Bergantung Vendor SLA':<26} | {'100% Data Internal (On-Prem)'}")
    print(f"{'Fine-Tuning Control':<22} | {'Terbatas (API Hyperparameters)':<26} | {'Akses Bobot Penuh (LoRA/SFT)'}")
    print("=" * 80)

def main():
    print("=" * 75)
    print("      SIMULATOR TOTAL COST OF OWNERSHIP (TCO) LLM DEPLOYMENT")
    print("=" * 75)
    
    test_volumes = [2.0, 15.0, 50.0, 200.0, 1000.0]
    
    print("\nSimulasi Biaya Bulanan Berdasarkan Volume Token (Input 70%, Output 30%):\n")
    print(f"{'Volume Token / Bulan':<22} | {'GPT-4o-mini':<13} | {'GPT-4o':<13} | {'Self-Hosted GPU (vLLM)'}")
    print("-" * 80)
    
    for v in test_volumes:
        res = simulate_tco_comparison(v)
        print(f"{v:6.1f} Juta Token       | ${res['gpt4o_mini_cost']:<11.2f} | ${res['gpt4o_cost']:<11.2f} | ${res['self_hosted_cost']:<8.2f} ({res['self_hosted_gpu']})")

    print_tradeoff_matrix()

    print("\n💡 KESIMPULAN TCO:")
    print("• Di bawah 20 Juta Token/bulan: Closed API (seperti GPT-4o-mini) jauh lebih hemat.")
    print("• Di atas 100 Juta Token/bulan: Self-Hosted GPU (Open Weights) menghemat ribuan Dolar.")

if __name__ == "__main__":
    main()
