"""
Modul 05: Evaluasi & Hyperparameters
Skrip 1: Metrik Evaluasi Model Fine-Tuned (Perplexity, BLEU/ROUGE, LLM-as-a-Judge)
"""

import math

def calculate_perplexity(cross_entropy_loss):
    """
    Perplexity (PPL) = exp(CrossEntropyLoss)
    """
    return math.exp(cross_entropy_loss)

def calculate_ngram_jaccard(reference, hypothesis, n=1):
    """
    Simulasi sederhana overlap n-gram (konsep dasar BLEU / ROUGE).
    """
    ref_words = reference.lower().split()
    hyp_words = hypothesis.lower().split()
    
    ref_ngrams = set(zip(*[ref_words[i:] for i in range(n)]))
    hyp_ngrams = set(zip(*[hyp_words[i:] for i in range(n)]))
    
    if not ref_ngrams or not hyp_ngrams:
        return 0.0
        
    intersection = ref_ngrams.intersection(hyp_ngrams)
    union = ref_ngrams.union(hyp_ngrams)
    
    return len(intersection) / len(union)

def demo_evaluation_metrics():
    print("=" * 60)
    print("MODUL 05 - SKRIP 1: Metrik Evaluasi Model Fine-Tuned")
    print("=" * 60)
    
    # 1. Perplexity
    sample_loss = 1.45
    ppl = calculate_perplexity(sample_loss)
    print(f"\n--- 1. Evaluasi Perplexity (PPL) ---")
    print(f"Validation Cross-Entropy Loss : {sample_loss:.2f}")
    print(f"Perplexity (exp(Loss))        : {ppl:.2f}")
    print("Prinsip: Semakin rendah nilai Perplexity, semakin akurat model memprediksi kata berikutnya.")
    
    # 2. Text Overlap (BLEU/ROUGE concept)
    print(f"\n--- 2. Evaluasi Overlap Teks (ROUGE / BLEU concept) ---")
    reference = "Supervised Fine-Tuning melatih LLM menggunakan data instruksi."
    hypothesis = "SFT melatih LLM menggunakan dataset berformat instruksi."
    
    unigram_score = calculate_ngram_jaccard(reference, hypothesis, n=1)
    bigram_score = calculate_ngram_jaccard(reference, hypothesis, n=2)
    
    print(f"Referensi : '{reference}'")
    print(f"Hasil Model: '{hypothesis}'")
    print(f"Unigram (1-gram) Similarity Score : {unigram_score * 100:.1f}%")
    print(f"Bigram (2-gram) Similarity Score  : {bigram_score * 100:.1f}%")
    
    # 3. LLM-as-a-Judge Concept
    print(f"\n--- 3. Metode Evaluasi Modern: LLM-as-a-Judge ---")
    print("Prompt Evaluasi ke Evaluator Model (misal GPT-4o):")
    prompt_judge = """
    [System: Anda adalah juri independen yang menilai respon AI.]
    [Pertanyaan: Jelaskan perbedaan LoRA dan Full Fine-Tuning.]
    [Respon Model: LoRA hanya melatih matriks adapter kecil, sedangkan Full FT melatih seluruh bobot.]
    
    Berikan skor (1-10) untuk Keakuratan, Kejelasan, dan Kelengkapan!
    """
    print(prompt_judge)

if __name__ == "__main__":
    demo_evaluation_metrics()
