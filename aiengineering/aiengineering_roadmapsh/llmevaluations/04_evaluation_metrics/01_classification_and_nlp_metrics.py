"""
01_classification_and_nlp_metrics.py
------------------------------------
Kalkulator Metrik Klasik NLP & Klasifikasi:
1. Precision, Recall, F1 Score & Accuracy Matrix
2. Perplexity (PPL) Calculation & Evaluation
3. Confusion Matrix Generator
"""

import math

def calculate_classification_metrics(tp: int, fp: int, fn: int, tn: int) -> dict:
    """Menghitung metrik klasifikasi dasar."""
    total = tp + fp + fn + tn
    accuracy = (tp + tn) / total if total > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "confusion_matrix": {"TP": tp, "FP": fp, "FN": fn, "TN": tn}
    }

def calculate_perplexity(log_probabilities: list[float]) -> float:
    """
    Menghitung Perplexity dari daftar log probabilitas token.
    PPL = exp(-1/N * sum(log P(w_i)))
    Nilai PPL semakin rendah = Model semakin percaya diri & tidak bingung.
    """
    if not log_probabilities:
        return 0.0
    
    n = len(log_probabilities)
    avg_neg_log_prob = -sum(log_probabilities) / n
    perplexity = math.exp(avg_neg_log_prob)
    return round(perplexity, 4)

if __name__ == "__main__":
    print("=== LAB 10: CLASSIFICATION & PERPLEXITY METRICS ===")

    # 1. Classification Metrics Test
    # Scenario: Evaluating LLM intent classifier (TP=85, FP=10, FN=15, TN=190)
    metrics = calculate_classification_metrics(tp=85, fp=10, fn=15, tn=190)
    print("\n[1] Classification Metrics Output:")
    print(f"    Confusion Matrix : {metrics['confusion_matrix']}")
    print(f"    Accuracy         : {metrics['accuracy'] * 100:.1f}%")
    print(f"    Precision        : {metrics['precision'] * 100:.1f}%")
    print(f"    Recall           : {metrics['recall'] * 100:.1f}%")
    print(f"    F1 Score         : {metrics['f1_score']:.4f}")

    # 2. Perplexity Test
    # High confidence token logprobs (closer to 0) vs low confidence (very negative)
    confident_logprobs = [-0.15, -0.05, -0.10, -0.08, -0.12]
    uncertain_logprobs = [-2.50, -3.10, -1.90, -4.00, -2.80]

    ppl_confident = calculate_perplexity(confident_logprobs)
    ppl_uncertain = calculate_perplexity(uncertain_logprobs)

    print("\n[2] Perplexity (PPL) Evaluation:")
    print(f"    Confident Model PPL  : {ppl_confident} (Sangat Baik)")
    print(f"    Uncertain Model PPL  : {ppl_uncertain} (Tinggi / Bingung)")
