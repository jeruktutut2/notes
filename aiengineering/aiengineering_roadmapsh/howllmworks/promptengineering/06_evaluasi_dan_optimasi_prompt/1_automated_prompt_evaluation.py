"""
MODUL 6.1: Automated Prompt Evaluation & Benchmarking (LLM-as-a-Judge)
=====================================================================
Penjelasan:
Mengevaluasi kualitas prompt memerlukan metrik otomatis:
1. Exact Match / Regex Match (Kesesuaian format).
2. Cosine Similarity (Kesesuaian makna berbasis vektor kata).
3. LLM-as-a-Judge: Menggunakan LLM terpisah untuk menilai kualitas respon berdasarkan rubrik (Skor 1-5).
"""

import math

def calculate_exact_match(predicted: str, ground_truth: str) -> float:
    """Mengukur persentase kesamaan kata persis (Exact Match / Word Jaccard)."""
    p_words = set(predicted.lower().split())
    g_words = set(ground_truth.lower().split())
    intersection = p_words.intersection(g_words)
    union = p_words.union(g_words)
    return len(intersection) / len(union) if union else 0.0


def llm_judge_evaluation(prompt_variant: str, response: str, rubrik: str) -> dict:
    """Simulasi LLM-as-a-Judge yang menilai respon berdasarkan rubrik evaluasi."""
    # Skor simulatif berdasarkan kejelasan respon
    score = 4.5 if "terstruktur" in prompt_variant.lower() or "lengkap" in response.lower() else 2.5
    
    return {
        "score": score,
        "max_score": 5.0,
        "evaluasi_hakim": "Respon sangat akurat, mematuhi format JSON, dan tidak mengandung halusinasi.",
        "kelayakan_produksi": score >= 4.0
    }


def main():
    print("==========================================================")
    print(" DEMO 6.1: Automated Prompt Evaluation & LLM-as-a-Judge")
    print("==========================================================\n")

    ground_truth = "PT Solusi Digital bergerak di bidang cloud computing dan AI."
    
    response_prompt_v1 = "PT Solusi Digital adalah perusahaan cloud computing dan AI."
    response_prompt_v2 = "Perusahaan ini sangat bagus dan melayani banyak klien di Indonesia."

    print("Ground Truth (Target):", ground_truth)
    print("\n" + "-"*50)

    # 1. Exact Match Evaluation
    score_v1 = calculate_exact_match(response_prompt_v1, ground_truth)
    score_v2 = calculate_exact_match(response_prompt_v2, ground_truth)

    print(f"Prompt Variant 1 Jaccard Similarity Score: {score_v1:.2f}")
    print(f"Prompt Variant 2 Jaccard Similarity Score: {score_v2:.2f}")

    print("\n" + "="*60 + "\n")

    # 2. LLM-as-a-Judge Benchmarking
    rubrik = "Nilai keakuratan informasi (1-5) dan kepatuhan terhadap format."
    judge_res = llm_judge_evaluation("Prompt Terstruktur V1", response_prompt_v1, rubrik)

    print("[LLM-AS-A-JUDGE EVALUATION REPORT]:")
    print(f" - Skor: {judge_res['score']} / {judge_res['max_score']}")
    print(f" - Ulasan Hakim: {judge_res['evaluasi_hakim']}")
    print(f" - Lolos Kualifikasi Produksi: {judge_res['kelayakan_produksi']}")
    print("==========================================================")

if __name__ == "__main__":
    main()
