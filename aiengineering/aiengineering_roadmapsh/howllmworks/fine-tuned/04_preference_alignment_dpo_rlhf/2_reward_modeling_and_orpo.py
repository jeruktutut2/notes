"""
Modul 04: Preference Alignment (DPO & RLHF)
Skrip 2: Reward Model Scoring & Concept Odds Ratio Policy Optimization (ORPO)
"""

import torch

def reward_model_score(chosen_score, rejected_score):
    """
    Reward Model Margin: r(x, y_w) - r(x, y_l) > 0
    """
    margin = chosen_score - rejected_score
    return margin

def demo_reward_and_orpo():
    print("=" * 60)
    print("MODUL 04 - SKRIP 2: Reward Modeling & ORPO Alignment")
    print("=" * 60)
    
    print("\n--- 1. Prinsip Reward Model (RLHF Klasik) ---")
    # Simulasikan output skor scalar dari Reward Model
    chosen_score = torch.tensor(2.45)
    rejected_score = torch.tensor(-1.12)
    margin = reward_model_score(chosen_score, rejected_score)
    
    print(f"Skor Respon Chosen   : {chosen_score.item():.2f}")
    print(f"Skor Respon Rejected : {rejected_score.item():.2f}")
    print(f"Reward Margin        : {margin.item():.2f}")
    
    print("\n--- 2. Odds Ratio Policy Optimization (ORPO) ---")
    print("ORPO menggabungkan Supervised Fine-Tuning (SFT) dan Preference Alignment secara langsung dalam SATU tahap training, tanpa membutuhkan Reference Model terpisah!")
    print("\nORPO Loss = Loss_SFT + lambda * Loss_OddsRatio")
    print("  - Loss_SFT       : Standar Cross-Entropy Loss pada respon Chosen.")
    print("  - Loss_OddsRatio : Memperbesar rasio odds p(y_chosen|x) / (1 - p(y_chosen|x)) relatif terhadap p(y_rejected|x).")
    
    print("\n[REKOMENDASI PRAKTIS] Gunakan SFT + DPO untuk kemudahan modularitas, atau gunakan ORPO jika ingin menghemat VRAM (karena tidak memuat Reference Model di VRAM).")

if __name__ == "__main__":
    demo_reward_and_orpo()
