"""
Modul 04: Preference Alignment (DPO & RLHF)
Skrip 1: Direct Preference Optimization (DPO) Loss & Pair Formatting
"""

import torch
import torch.nn.functional as F

def compute_dpo_loss(policy_chosen_logps, policy_rejected_logps,
                     ref_chosen_logps, ref_rejected_logps, beta=0.1):
    """
    Menghitung DPO Loss secara matematis.
    
    Formula DPO Loss:
    - L_DPO = - log_sigmoid( beta * ( (log p_policy(y_w|x) - log p_ref(y_w|x)) 
                                    - (log p_policy(y_l|x) - log p_ref(y_l|x)) ) )
    """
    pi_logratios = policy_chosen_logps - policy_rejected_logps
    ref_logratios = ref_chosen_logps - ref_rejected_logps
    
    logits = pi_logratios - ref_logratios
    loss = -F.logsigmoid(beta * logits)
    
    return loss.mean()

def demo_dpo():
    print("=" * 60)
    print("MODUL 04 - SKRIP 1: Direct Preference Optimization (DPO)")
    print("=" * 60)
    
    print("\n--- 1. Format Dataset Preference DPO (Chosen vs Rejected) ---")
    dpo_sample = {
        "prompt": "Tulis respon sopan untuk menolak permintaan diskon 90%.",
        "chosen": "Mohon maaf, kami tidak dapat memberikan diskon 90%. Namun, kami menawarkan diskon 10% untuk pembelian pertama Anda.",
        "rejected": "Gak bisa bro, 90% rugi dong kita! Mana ada diskon segitu!"
    }
    
    print(f"Prompt   : {dpo_sample['prompt']}")
    print(f"Chosen   : {dpo_sample['chosen']}")
    print(f"Rejected : {dpo_sample['rejected']}")
    
    print("\n--- 2. Perhitungan DPO Loss Matriks PyTorch ---")
    # Log-probabilities sintetis dari Policy Model (model yang sedang dilatih)
    policy_chosen_logps = torch.tensor([-1.2, -1.5])
    policy_rejected_logps = torch.tensor([-3.5, -4.0])
    
    # Log-probabilities sintetis dari Reference Model (model SFT asli)
    ref_chosen_logps = torch.tensor([-2.0, -2.1])
    ref_rejected_logps = torch.tensor([-2.5, -2.8])
    
    beta = 0.1
    dpo_loss = compute_dpo_loss(policy_chosen_logps, policy_rejected_logps,
                                ref_chosen_logps, ref_rejected_logps, beta=beta)
    
    print(f"Beta (KL Penalty Factor) : {beta}")
    print(f"DPO Loss Nilai Hitung     : {dpo_loss.item():.4f}")
    
    print("\n[KESIMPULAN] DPO Loss akan makin kecil jika Policy Model memperbesar probabilitas respon 'Chosen' dan memperkecil probabilitas respon 'Rejected' secara bersamaan.")

if __name__ == "__main__":
    demo_dpo()
