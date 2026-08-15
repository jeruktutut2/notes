"""
Modul 02: PEFT & LoRA Architecture
Skrip 1: Custom LoRA (Low-Rank Adaptation) dari Dasar dengan PyTorch
"""

import torch
import torch.nn as nn

class CustomLoRALinear(nn.Module):
    """
    Implementasi kustom LoRA Layer di PyTorch.
    Matriks bobot asli W_0 dibekukan (frozen).
    Menambahkan matriks A dan B berukuran rank r kecil.
    
    Formula: output = x @ W_0.T + (alpha / r) * (x @ A.T @ B.T)
    """
    def __init__(self, in_features, out_features, r=8, lora_alpha=16):
        super().__init__()
        # Matriks bobot linear asli W_0 (dibekukan)
        self.linear = nn.Linear(in_features, out_features)
        self.linear.weight.requires_grad = False
        if self.linear.bias is not None:
            self.linear.bias.requires_grad = False
            
        self.r = r
        self.lora_alpha = lora_alpha
        self.scaling = lora_alpha / r
        
        # Matriks LoRA A (r x in_features) dan B (out_features x r)
        self.lora_A = nn.Parameter(torch.zeros(r, in_features))
        self.lora_B = nn.Parameter(torch.zeros(out_features, r))
        
        # Inisialisasi: A ~ Gaussian Random, B = 0
        nn.init.kaiming_uniform_(self.lora_A, a=5**0.5)
        nn.init.zeros_(self.lora_B)
        
    def forward(self, x):
        # Base Linear pass
        base_out = self.linear(x)
        # LoRA Adaption pass: (x @ A^T) @ B^T * scaling
        lora_out = (x @ self.lora_A.T) @ self.lora_B.T * self.scaling
        return base_out + lora_out

def demo_custom_lora():
    print("=" * 60)
    print("MODUL 02 - SKRIP 1: Custom LoRA Layer dari Scratch (PyTorch)")
    print("=" * 60)
    
    in_dim = 4096
    out_dim = 4096
    r = 8
    alpha = 16
    
    # Base Layer biasa
    base_layer = nn.Linear(in_dim, out_dim)
    base_params = sum(p.numel() for p in base_layer.parameters())
    
    # Custom LoRA Layer
    lora_layer = CustomLoRALinear(in_dim, out_dim, r=r, lora_alpha=alpha)
    trainable_params = sum(p.numel() for p in lora_layer.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in lora_layer.parameters())
    
    print(f"\nDimensi Layer : {in_dim} -> {out_dim}")
    print(f"Rank r         : {r}")
    print(f"Alpha          : {alpha}")
    print(f"Scaling Factor : {alpha / r}")
    print("-" * 50)
    print(f"Jumlah Parameter Asli (Full Weight)   : {base_params:,}")
    print(f"Jumlah Parameter Trainable (LoRA A+B) : {trainable_params:,}")
    print(f"Penghematan Parameter                 : {(1 - trainable_params / base_params) * 100:.2f}%")
    
    # Dummy Forward Pass Test
    x = torch.randn(2, 128, in_dim)  # Batch 2, Seq 128, Dim 4096
    out = lora_layer(x)
    print(f"\n[OK] Forward Pass Berhasil! Shape Output: {out.shape}")

if __name__ == "__main__":
    demo_custom_lora()
