"""
Modul 03: Supervised Fine-Tuning (SFT)
Skrip 3: Memory Efficient Training (Gradient Accumulation, FP16/BF16 & Checkpointing)
"""

import torch

def calculate_effective_batch_size(micro_batch_size, grad_accum_steps, num_gpus=1):
    """
    Hitung Effective Batch Size = Micro Batch * Grad Accum Steps * GPU Count
    """
    return micro_batch_size * grad_accum_steps * num_gpus

def demo_memory_efficiency():
    print("=" * 60)
    print("MODUL 03 - SKRIP 3: Teknik Efisiensi Memori Training LLM")
    print("=" * 60)
    
    # 1. Gradient Accumulation Simulation
    micro_batch = 2
    grad_accum = 8
    gpus = 1
    eff_batch = calculate_effective_batch_size(micro_batch, grad_accum, gpus)
    
    print("\n--- 1. Gradient Accumulation ---")
    print(f"Micro Batch Size per GPU : {micro_batch}")
    print(f"Gradient Accumulation    : {grad_accum} langkah")
    print(f"Effective Batch Size      : {eff_batch} sampel")
    print("Keuntungan: Hemat VRAM GPU seolah-olah menggunakan Batch Size besar!")
    
    # 2. Mixed Precision Check (FP32 vs FP16 vs BF16)
    print("\n--- 2. Kemampuan Hardware Mixed Precision ---")
    cuda_available = torch.cuda.is_available()
    print(f"CUDA Available          : {cuda_available}")
    
    if cuda_available:
        bf16_supported = torch.cuda.is_bf16_supported()
        print(f"bfloat16 (BF16) Support : {bf16_supported}")
    else:
        print("Running on CPU. Tipe data rekomendasi pada Apple Silicon/CPU: FP32 atau MPS Float16.")
        
    # 3. Memory Calculation Rule-of-Thumb
    print("\n--- 3. Estimasi Kebutuhan VRAM Model 7B Parameter ---")
    print("| Metode Training    | Weights VRAM | Optimizer VRAM | Total Min VRAM |")
    print("|--------------------|--------------|----------------|----------------|")
    print("| Full FT (FP16)     | ~14 GB       | ~56 GB         | ~80+ GB        |")
    print("| LoRA 16-bit        | ~14 GB       | ~0.5 GB        | ~18-24 GB      |")
    print("| QLoRA 4-bit (NF4)  | ~3.5 GB      | ~0.5 GB        | ~6-8 GB        |")

if __name__ == "__main__":
    demo_memory_efficiency()
