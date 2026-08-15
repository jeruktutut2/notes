"""
=================================================================
1. EVALUASI OUTPUT MODEL
=================================================================
Mengevaluasi kualitas output model AI sangat penting karena:
- Model bisa menghasilkan output yang salah/menyesatkan
- Perlu standar objektif untuk membandingkan model
- Monitoring degradasi kualitas di production

3 Pendekatan Evaluasi:
1. Deterministik → Metrik terukur (BLEU, ROUGE, F1)
2. Model-based  → Pakai model lain sebagai evaluator
3. Human eval   → Manusia menilai kualitas output
=================================================================
"""

from collections import Counter
import math


# ─────────────────────────────────────────────────────
# IMPLEMENTASI METRIK EVALUASI (Tanpa Library Eksternal)
# ─────────────────────────────────────────────────────

def hitung_bleu_sederhana(reference, hypothesis, max_n=4):
    """
    BLEU Score — mengukur kualitas terjemahan/generasi teks
    dengan membandingkan n-gram overlap antara output dan referensi.
    
    Skor: 0.0 (buruk) - 1.0 (sempurna)
    Dipakai untuk: Machine Translation, Text Generation
    """
    ref_tokens = reference.lower().split()
    hyp_tokens = hypothesis.lower().split()

    scores = []
    for n in range(1, max_n + 1):
        # Hitung n-gram
        ref_ngrams = Counter([tuple(ref_tokens[i:i+n]) for i in range(len(ref_tokens)-n+1)])
        hyp_ngrams = Counter([tuple(hyp_tokens[i:i+n]) for i in range(len(hyp_tokens)-n+1)])

        # Hitung overlap
        overlap = sum((hyp_ngrams & ref_ngrams).values())
        total = sum(hyp_ngrams.values())

        if total == 0:
            scores.append(0)
        else:
            scores.append(overlap / total)

    # Brevity penalty (penalti jika terlalu pendek)
    bp = min(1.0, math.exp(1 - len(ref_tokens) / max(len(hyp_tokens), 1)))

    # Geometric mean dari semua n-gram scores
    if all(s > 0 for s in scores):
        log_avg = sum(math.log(s) for s in scores) / len(scores)
        bleu = bp * math.exp(log_avg)
    else:
        bleu = 0.0

    return bleu


def hitung_rouge_l(reference, hypothesis):
    """
    ROUGE-L — mengukur Longest Common Subsequence (LCS) antara
    output dan referensi.
    
    Dipakai untuk: Summarization, Text Generation
    """
    ref_tokens = reference.lower().split()
    hyp_tokens = hypothesis.lower().split()

    # Dynamic programming untuk LCS
    m, n = len(ref_tokens), len(hyp_tokens)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if ref_tokens[i-1] == hyp_tokens[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])

    lcs_length = dp[m][n]

    # Precision, Recall, F1
    precision = lcs_length / n if n > 0 else 0
    recall = lcs_length / m if m > 0 else 0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0

    return {"precision": precision, "recall": recall, "f1": f1, "lcs_length": lcs_length}


def hitung_exact_match(reference, hypothesis):
    """Exact Match — apakah output PERSIS sama dengan referensi."""
    return 1.0 if reference.strip().lower() == hypothesis.strip().lower() else 0.0


def hitung_f1_token(reference, hypothesis):
    """Token-level F1 — overlap token antara output dan referensi."""
    ref_tokens = set(reference.lower().split())
    hyp_tokens = set(hypothesis.lower().split())

    common = ref_tokens & hyp_tokens
    if len(common) == 0:
        return 0.0

    precision = len(common) / len(hyp_tokens)
    recall = len(common) / len(ref_tokens)
    f1 = 2 * precision * recall / (precision + recall)

    return f1


def demo_evaluasi_metrik():
    """Demo berbagai metrik evaluasi."""
    print("=" * 60)
    print("DEMO 1: Metrik Evaluasi Deterministik")
    print("=" * 60)

    # Contoh: Evaluasi terjemahan
    reference = "The cat sat on the mat in the living room"
    
    hypotheses = [
        ("Sempurna", "The cat sat on the mat in the living room"),
        ("Baik", "The cat was sitting on the mat in the room"),
        ("Cukup", "A cat is on the mat"),
        ("Buruk", "The dog ran in the park yesterday afternoon"),
    ]

    print(f"\n📖 Referensi: \"{reference}\"")
    print(f"\n📊 Evaluasi berbagai output:")
    print(f"   {'Kualitas':<10} | {'BLEU':>6} | {'ROUGE-L F1':>10} | {'Token F1':>8} | {'EM':>4}")
    print(f"   {'-'*10}-+-{'-'*6}-+-{'-'*10}-+-{'-'*8}-+-{'-'*4}")

    for label, hyp in hypotheses:
        bleu = hitung_bleu_sederhana(reference, hyp)
        rouge = hitung_rouge_l(reference, hyp)
        f1 = hitung_f1_token(reference, hyp)
        em = hitung_exact_match(reference, hyp)

        print(f"   {label:<10} | {bleu:>6.4f} | {rouge['f1']:>10.4f} | {f1:>8.4f} | {em:>4.1f}")

    print(f"\n   💡 Interpretasi:")
    print(f"   - BLEU: Mengukur n-gram overlap (presisi-oriented)")
    print(f"   - ROUGE-L: Mengukur subsequence terpanjang (recall-oriented)")
    print(f"   - Token F1: Overlap token level")
    print(f"   - Exact Match: Hanya 1.0 jika persis sama")


def demo_evaluasi_summarization():
    """Demo evaluasi untuk task summarization."""
    print("\n" + "=" * 60)
    print("DEMO 2: Evaluasi Summarization")
    print("=" * 60)

    reference_summary = "AI transforms healthcare finance and education but raises concerns about jobs and privacy"

    model_summaries = [
        ("Model A", "AI is transforming healthcare finance and education raising concerns about jobs privacy and ethics"),
        ("Model B", "Artificial intelligence has many applications in various industries"),
        ("Model C", "The weather today is sunny and warm with a chance of rain"),
    ]

    print(f"\n📖 Reference Summary:")
    print(f"   \"{reference_summary}\"")

    print(f"\n📊 Evaluasi Model Summaries:")
    for nama, summary in model_summaries:
        rouge = hitung_rouge_l(reference_summary, summary)
        f1 = hitung_f1_token(reference_summary, summary)
        print(f"\n   {nama}: \"{summary}\"")
        print(f"   → ROUGE-L: P={rouge['precision']:.3f} R={rouge['recall']:.3f} F1={rouge['f1']:.3f}")
        print(f"   → Token F1: {f1:.3f}")


def demo_model_based_eval():
    """Penjelasan evaluasi berbasis model (LLM-as-Judge)."""
    print("\n" + "=" * 60)
    print("DEMO 3: Model-Based Evaluation (LLM-as-Judge)")
    print("=" * 60)

    print("""
    💡 LLM-as-Judge: Menggunakan model LLM besar (GPT-4, Claude)
       untuk mengevaluasi output model lain.

    📝 Contoh Prompt Evaluator:

    ```
    Kamu adalah evaluator yang menilai kualitas jawaban AI.
    
    Pertanyaan: {question}
    Jawaban yang dinilai: {answer}
    Referensi (jika ada): {reference}
    
    Nilai jawaban berdasarkan kriteria berikut (1-5):
    1. Akurasi: Apakah informasi benar?
    2. Relevansi: Apakah menjawab pertanyaan?
    3. Kelengkapan: Apakah cukup detail?
    4. Kejelasan: Apakah mudah dipahami?
    
    Format output:
    {
        "akurasi": <1-5>,
        "relevansi": <1-5>,
        "kelengkapan": <1-5>,
        "kejelasan": <1-5>,
        "rata_rata": <1-5>,
        "alasan": "<penjelasan singkat>"
    }
    ```

    📋 KAPAN PAKAI METODE APA:
    ┌──────────────────┬────────────────────────────────┐
    │ Metode           │ Kapan Dipakai                  │
    ├──────────────────┼────────────────────────────────┤
    │ Deterministik    │ Ada ground truth yang jelas     │
    │ (BLEU, ROUGE)    │ Translation, QA, Summarization │
    ├──────────────────┼────────────────────────────────┤
    │ Model-based      │ Output open-ended, kreatif     │
    │ (LLM-as-Judge)   │ Chat, creative writing, advice │
    ├──────────────────┼────────────────────────────────┤
    │ Human eval       │ Use case kritis, final check   │
    │                  │ Healthcare, legal, education   │
    └──────────────────┴────────────────────────────────┘
    """)


def main():
    demo_evaluasi_metrik()
    demo_evaluasi_summarization()
    demo_model_based_eval()

    print("\n✅ Selesai! Lanjut ke: 2_cost_latency_tracking.py")

if __name__ == "__main__":
    main()
