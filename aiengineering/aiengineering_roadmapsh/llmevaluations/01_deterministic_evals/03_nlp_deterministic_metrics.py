"""
03_nlp_deterministic_metrics.py
--------------------------------
Demonstrasi Evaluasi Deterministik N-Gram:
1. BLEU-4 Score (Precision N-Gram dengan Brevity Penalty)
2. ROUGE-1, ROUGE-2, & ROUGE-L Score (Recall N-Gram & Longest Common Subsequence)
3. METEOR Approximation
"""

import math
from collections import Counter

def get_ngrams(tokens: list[str], n: int) -> Counter:
    """Mengambil frekuensi n-gram dari daftar token."""
    return Counter([tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)])

def calculate_bleu(candidate: str, reference: str, max_n: int = 4) -> float:
    """
    Kalkulator BLEU Score murni (Bilingual Evaluation Understudy).
    """
    cand_tokens = candidate.lower().split()
    ref_tokens = reference.lower().split()
    
    if len(cand_tokens) == 0:
        return 0.0

    precisions = []
    for n in range(1, max_n + 1):
        cand_ngrams = get_ngrams(cand_tokens, n)
        ref_ngrams = get_ngrams(ref_tokens, n)
        
        if not cand_ngrams:
            precisions.append(0.0)
            continue
            
        clipped_count = 0
        for ngram, count in cand_ngrams.items():
            clipped_count += min(count, ref_ngrams.get(ngram, 0))
            
        total_cand_ngrams = sum(cand_ngrams.values())
        precisions.append(clipped_count / total_cand_ngrams if total_cand_ngrams > 0 else 0.0)

    # Brevity Penalty
    c = len(cand_tokens)
    r = len(ref_tokens)
    bp = 1.0 if c > r else math.exp(1.0 - (r / c)) if c > 0 else 0.0

    # Geometric mean of precisions
    if any(p == 0 for p in precisions):
        return 0.0
        
    log_sum = sum(math.log(p) for p in precisions) / max_n
    bleu = bp * math.exp(log_sum)
    return round(bleu, 4)

def calculate_rouge_n(candidate: str, reference: str, n: int = 1) -> dict:
    """Menghitung ROUGE-N (Precision, Recall, F1)."""
    cand_tokens = candidate.lower().split()
    ref_tokens = reference.lower().split()
    
    cand_ngrams = get_ngrams(cand_tokens, n)
    ref_ngrams = get_ngrams(ref_tokens, n)
    
    overlap = sum(min(count, ref_ngrams.get(ngram, 0)) for ngram, count in cand_ngrams.items())
    
    total_cand = sum(cand_ngrams.values())
    total_ref = sum(ref_ngrams.values())
    
    precision = overlap / total_cand if total_cand > 0 else 0.0
    recall = overlap / total_ref if total_ref > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4)
    }

def longest_common_subsequence(seq1: list, seq2: list) -> int:
    """Menghitung panjang Longest Common Subsequence untuk ROUGE-L."""
    m, n = len(seq1), len(seq2)
    L = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif seq1[i - 1] == seq2[j - 1]:
                L[i][j] = L[i - 1][j - 1] + 1
            else:
                L[i][j] = max(L[i - 1][j], L[i][j - 1])
    return L[m][n]

def calculate_rouge_l(candidate: str, reference: str) -> dict:
    """Menghitung ROUGE-L berbasis Longest Common Subsequence."""
    cand_tokens = candidate.lower().split()
    ref_tokens = reference.lower().split()
    
    lcs = longest_common_subsequence(cand_tokens, ref_tokens)
    
    precision = lcs / len(cand_tokens) if len(cand_tokens) > 0 else 0.0
    recall = lcs / len(ref_tokens) if len(ref_tokens) > 0 else 0.0
    f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    
    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4)
    }

if __name__ == "__main__":
    print("=== LAB 03: NLP DETERMINISTIC N-GRAM METRICS ===")
    
    cand = "Kecerdasan Buatan adalah bidang ilmu komputer yang mengembangkan sistem pintar."
    ref  = "Kecerdasan Buatan merupakan cabang ilmu komputer untuk membuat sistem cerdas."
    
    print(f"\nCandidate : '{cand}'")
    print(f"Reference : '{ref}'")
    
    # BLEU calculation
    bleu_score = calculate_bleu(cand, ref)
    print(f"\n[1] BLEU-4 Score : {bleu_score}")
    
    # ROUGE-1 & ROUGE-2
    rouge1 = calculate_rouge_n(cand, ref, n=1)
    rouge2 = calculate_rouge_n(cand, ref, n=2)
    rougel = calculate_rouge_l(cand, ref)
    
    print(f"\n[2] ROUGE Metrics:")
    print(f"    ROUGE-1 (Unigram) -> Precision: {rouge1['precision']}, Recall: {rouge1['recall']}, F1: {rouge1['f1']}")
    print(f"    ROUGE-2 (Bigram)  -> Precision: {rouge2['precision']}, Recall: {rouge2['recall']}, F1: {rouge2['f1']}")
    print(f"    ROUGE-L (LCS)     -> Precision: {rougel['precision']}, Recall: {rougel['recall']}, F1: {rougel['f1']}")
