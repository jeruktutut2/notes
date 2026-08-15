"""
Modul 05: Evaluasi & Hyperparameters
Skrip 2: Hyperparameter Tuning Guidelines & Learning Rate Schedules
"""

import math

def simulate_cosine_warmup_lr(step, total_steps=100, warmup_steps=10, base_lr=2e-4, min_lr=1e-5):
    """
    Simulasi Learning Rate Schedule: Linear Warmup -> Cosine Decay
    """
    if step < warmup_steps:
        # Linear Warmup
        return base_lr * (step / warmup_steps)
    else:
        # Cosine Decay
        progress = (step - warmup_steps) / (total_steps - warmup_steps)
        cosine_decay = 0.5 * (1.0 + math.cos(math.pi * progress))
        return min_lr + (base_lr - min_lr) * cosine_decay

def demo_hyperparameters():
    print("=" * 60)
    print("MODUL 05 - SKRIP 2: Hyperparameter Tuning for Fine-Tuning")
    print("=" * 60)
    
    print("\n--- 1. Visualisasi Learning Rate Schedule (Warmup + Cosine Decay) ---")
    base_lr = 2e-4
    total_steps = 100
    warmup_steps = 10
    
    sample_steps = [0, 5, 10, 25, 50, 75, 100]
    for st in sample_steps:
        lr_now = simulate_cosine_warmup_lr(st, total_steps, warmup_steps, base_lr)
        print(f"Step {st:03d} / {total_steps} | Learning Rate: {lr_now:.6f}")
        
    print("\n--- 2. Rekomendasi Hyperparameter LoRA / QLoRA ---")
    print("| Hyperparameter    | Nilai Standar Rekomendasi | Catatan |")
    print("|-------------------|---------------------------|---------|")
    print("| Learning Rate (LR)| 2e-4 s/d 1e-4             | Lebih besar 10x dibanding Full FT |")
    print("| LoRA Rank (r)     | 8, 16, 32, 64             | r=16 umum digunakan untuk sebagian besar kasus |")
    print("| LoRA Alpha        | 2 * r (misal r=16 -> alpha=32)| Scaling factor kestabilan gradien |")
    print("| LoRA Dropout      | 0.05 s/d 0.1              | Mencegah overfitting pada dataset kecil |")
    print("| Warmup Ratio      | 0.03 (3% dari total step) | Menjaga stabilitas bobot awal |")
    print("| LR Scheduler      | 'cosine' atau 'constant'  | Cosine decay memberikan hasil lebih smooth |")

if __name__ == "__main__":
    demo_hyperparameters()
