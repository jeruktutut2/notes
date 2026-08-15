"""
Modul 02: PEFT & LoRA Architecture
Skrip 2: Implementasi LoRA menggunakan Hugging Face `peft`
"""

import sys

def demo_hf_peft():
    print("=" * 60)
    print("MODUL 02 - SKRIP 2: Hugging Face `peft` Integration")
    print("=" * 60)
    
    try:
        from peft import LoraConfig, get_peft_model, TaskType
        import torch.nn as nn
        
        # Simulasikan Model Sederhana
        class ToyLLM(nn.Module):
            def __init__(self):
                super().__init__()
                self.q_proj = nn.Linear(512, 512)
                self.v_proj = nn.Linear(512, 512)
                self.out_proj = nn.Linear(512, 512)
            def forward(self, x):
                return self.out_proj(self.q_proj(x) + self.v_proj(x))
                
        model = ToyLLM()
        
        # Konfigurasi LoRA
        config = LoraConfig(
            r=8,
            lora_alpha=16,
            target_modules=["q_proj", "v_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type=TaskType.FEATURE_EXTRACTION
        )
        
        peft_model = get_peft_model(model, config)
        
        print("\n--- Summary Model setelah dibungkus PEFT ---")
        peft_model.print_trainable_parameters()
        
        print("\n[OK] Berhasil mengonfigurasi LoraConfig dan menerapkan target_modules=['q_proj', 'v_proj'].")
        
    except ImportError:
        print("[INFO] Package 'peft' belum terinstall. Menampilkan prinsip LoraConfig HF:")
        print("""
        from peft import LoraConfig, get_peft_model, TaskType
        
        peft_config = LoraConfig(
            r=16,
            lora_alpha=32,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            lora_dropout=0.1,
            bias="none",
            task_type=TaskType.CAUSAL_LM
        )
        model = get_peft_model(base_model, peft_config)
        """)

if __name__ == "__main__":
    demo_hf_peft()
