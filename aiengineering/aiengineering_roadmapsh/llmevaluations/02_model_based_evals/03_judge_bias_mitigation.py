"""
03_judge_bias_mitigation.py
---------------------------
Demonstrasi Teknik Mitigasi Bias LLM-as-a-Judge:
1. Position Swapping & Swap Aggregation (Menghilangkan Position Bias)
2. Normalisasi Verbosity (Menghilangkan Verbosity Bias)
3. Multi-Judge Consensus Aggregation
"""

import json

def raw_judge_call_biased(prompt: str) -> str:
    """
    Simulasi LLM Judge yang menderita 'Position Bias'
    (cenderung memenangkan kandidat pertama yang muncul di prompt).
    """
    if "kandidat pertama: model a" in prompt.lower():
        return "Model A"
    elif "kandidat pertama: model b" in prompt.lower():
        return "Model B"
    return "Tie"

def evaluate_pairwise_biased(model_a_text: str, model_b_text: str, position_order: str = "A_first") -> str:
    """Evaluasi satu arah (rentan bias)."""
    if position_order == "A_first":
        prompt = f"Bandingkan dua jawaban berikut:\nKandidat Pertama: Model A -> {model_a_text}\nKandidat Kedua: Model B -> {model_b_text}"
    else:
        prompt = f"Bandingkan dua jawaban berikut:\nKandidat Pertama: Model B -> {model_b_text}\nKandidat Kedua: Model A -> {model_a_text}"
    return raw_judge_call_biased(prompt)

def evaluate_pairwise_unbiased_position_swap(model_a_text: str, model_b_text: str) -> dict:
    """
    Position Swapping Mitigation Technique:
    Menjalankan 2 ronde evaluasi dengan membalik urutan opsi A dan B.
    """
    # Round 1: Model A diposisikan di awal
    winner_round1 = evaluate_pairwise_biased(model_a_text, model_b_text, position_order="A_first")
    
    # Round 2: Model B diposisikan di awal
    winner_round2 = evaluate_pairwise_biased(model_a_text, model_b_text, position_order="B_first")

    # Agregasi Konsistensi
    # Round 1 memenangkan Model A. Round 2 memenangkan Model B (karena bias urutan).
    if winner_round1 == "Model A" and winner_round2 == "Model A":
        final_winner = "Model A"
        is_biased = False
    elif winner_round1 == "Model B" and winner_round2 == "Model B":
        final_winner = "Model B"
        is_biased = False
    else:
        # Pemenang berubah saat urutan dibalik = Terdeteksi Position Bias!
        final_winner = "Tie (Position Bias Detected)"
        is_biased = True

    return {
        "round1_order_A_first_winner": winner_round1,
        "round2_order_B_first_winner": winner_round2,
        "final_unbiased_winner": final_winner,
        "bias_detected": is_biased
    }

def normalize_verbosity_penalty(length_a: int, length_b: int, judge_preferred_winner: str, threshold_ratio: float = 1.5) -> str:
    """
    Mitigasi Verbosity Bias: Menghukum respons yang menang hanya karena terlalu panjang.
    """
    ratio = length_a / length_b if length_b > 0 else 1.0
    if judge_preferred_winner == "Model A" and ratio > threshold_ratio:
        return "Tie (Penalty Applied: Model A won due to verbosity)"
    elif judge_preferred_winner == "Model B" and (1.0 / ratio) > threshold_ratio:
        return "Tie (Penalty Applied: Model B won due to verbosity)"
    return judge_preferred_winner

if __name__ == "__main__":
    print("=== LAB 06: MITIGATING LLM-AS-A-JUDGE BIASES ===")

    resp_a = "Karakteristik RAG: 1. Retriever 2. Vector DB 3. Prompt Augmentation 4. LLM Generation."
    resp_b = "RAG adalah Retrieval Augmented Generation. RAG sangat berguna untuk AI modern."

    print("\n[1] Evaluasi Biased Single-Pass (Rentang Position Bias):")
    res_biased = evaluate_pairwise_biased(resp_a, resp_b, position_order="A_first")
    print(f"    Single-pass Winner (A First): {res_biased}")

    print("\n[2] Evaluasi Unbiased via Position Swapping:")
    unbiased_res = evaluate_pairwise_unbiased_position_swap(resp_a, resp_b)
    print(f"    Round 1 (A First Winner): {unbiased_res['round1_order_A_first_winner']}")
    print(f"    Round 2 (B First Winner): {unbiased_res['round2_order_B_first_winner']}")
    print(f"    Final Unbiased Winner   : 🛡️ {unbiased_res['final_unbiased_winner']}")
    print(f"    Bias Detected           : {unbiased_res['bias_detected']}")

    print("\n[3] Verbosity Bias Normalization Test:")
    long_verbose_a = resp_a * 5  # Resp A 5x lebih panjang
    normal_b = resp_b
    raw_win = "Model A"
    normalized_win = normalize_verbosity_penalty(len(long_verbose_a), len(normal_b), raw_win)
    print(f"    Raw Winner              : {raw_win}")
    print(f"    Length Ratio (A / B)    : {len(long_verbose_a) / len(normal_b):.1f}x")
    print(f"    Post-Normalization Win  : {normalized_win}")
