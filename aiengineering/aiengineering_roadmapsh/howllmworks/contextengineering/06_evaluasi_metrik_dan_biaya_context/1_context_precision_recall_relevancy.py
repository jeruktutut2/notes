#!/usr/bin/env python3
"""
MODUL 6: Evaluasi, Metrik & Biaya Context
Skrip 1: Context Precision, Recall, & Relevancy Metrics

Mendemonstrasikan:
1. Context Precision: Mengukur proporsi token/paragraf relevan dibanding total context.
2. Context Recall: Mengukur cakupan fakta ground truth yang berhasil ditangkap context.
3. Noise-to-Signal Ratio (NSR) & Information Density Score.
"""

from typing import List, Set, Dict, Any

class ContextEvaluator:
    """Evaluator Kualitas Context Window."""

    @staticmethod
    def _tokenize_set(text: str) -> Set[str]:
        # Filter kata sederhana
        stopwords = {"yang", "dan", "di", "ke", "dari", "ini", "itu", "adalah", "untuk", "pada"}
        words = text.lower().split()
        return {w.strip(".,!?()") for w in words if w not in stopwords and len(w) > 2}

    def evaluate_context(
        self,
        retrieved_context: str,
        ground_truth_facts: str,
        user_query: str
    ) -> Dict[str, float]:
        """Menghitung metrik Context Precision, Recall, Relevancy, dan NSR."""

        ctx_tokens = self._tokenize_set(retrieved_context)
        gt_tokens = self._tokenize_set(ground_truth_facts)
        query_tokens = self._tokenize_set(user_query)

        if not ctx_tokens:
            return {"precision": 0.0, "recall": 0.0, "relevancy": 0.0, "nsr": 1.0, "density": 0.0}

        # Token relevan = irisan context dengan ground truth / query
        relevant_in_ctx = ctx_tokens.intersection(gt_tokens.union(query_tokens))
        irrelevant_in_ctx = ctx_tokens - relevant_in_ctx

        # 1. Context Precision: (Token Relevan di Context) / (Total Token di Context)
        precision = len(relevant_in_ctx) / len(ctx_tokens)

        # 2. Context Recall: (Token Relevan di Context) / (Total Token di Ground Truth)
        recall = len(relevant_in_ctx) / len(gt_tokens) if gt_tokens else 1.0

        # 3. Noise-to-Signal Ratio (NSR): Token Irrelevan / Token Relevan
        nsr = len(irrelevant_in_ctx) / len(relevant_in_ctx) if relevant_in_ctx else 999.0

        # 4. Information Density Score: (Token Relevan per 100 token context)
        raw_word_count = len(retrieved_context.split())
        density_score = (len(relevant_in_ctx) / raw_word_count * 100) if raw_word_count > 0 else 0.0

        return {
            "context_precision": round(precision, 4),
            "context_recall": round(recall, 4),
            "noise_to_signal_ratio": round(nsr, 4),
            "information_density_per_100w": round(density_score, 2),
            "total_words": raw_word_count,
            "relevant_tokens_count": len(relevant_in_ctx),
            "noise_tokens_count": len(irrelevant_in_ctx)
        }

def demo():
    print("=" * 70)
    print("DEMO 1: CONTEXT PRECISION, RECALL, & RELEVANCY METRICS")
    print("=" * 70)

    evaluator = ContextEvaluator()

    user_query = "Berapa batas alokasi token untuk RAG context dan bagaimana cara mengompresinya?"
    ground_truth = "Alokasi RAG context idealnya 40% dari total input budget. Kompresi dapat dilakukan dengan LLMLingua."

    # Skenario A: Context Bersih (High Precision, High Recall)
    clean_context = (
        "Alokasi RAG context disarankan mengambil porsi 40% dari budget input window LLM. "
        "Untuk mengompresi token yang membengkak, teknik LLMLingua dapat digunakan untuk memangkas kata filler."
    )

    # Skenario B: Context Berisik / Noisy (Low Precision, High NSR)
    noisy_context = (
        "Perusahaan didirikan tahun 2015 di Jakarta. Cuaca hari ini sangat cerah. "
        "Alokasi RAG context disarankan mengambil porsi 40% dari budget input window LLM. "
        "Server Linux memerlukan restart mingguan. Kami juga menyajikan kopi gratis di kantin. "
        "Untuk mengompresi token, teknik LLMLingua digunakan."
    )

    res_clean = evaluator.evaluate_context(clean_context, ground_truth, user_query)
    res_noisy = evaluator.evaluate_context(noisy_context, ground_truth, user_query)

    print("--- KUERI PENGGUNA ---")
    print(f"Query : '{user_query}'")
    print(f"Ground Truth Facts: '{ground_truth}'\n")

    print(f"{'Metrik Evaluasi Context':<30} | {'Skenario A (Clean Context)':<25} | {'Skenario B (Noisy Context)'}")
    print("-" * 85)
    print(f"{'Context Precision (0-1)':<30} | {res_clean['context_precision']:^25} | {res_noisy['context_precision']:^25}")
    print(f"{'Context Recall (0-1)':<30} | {res_clean['context_recall']:^25} | {res_noisy['context_recall']:^25}")
    print(f"{'Noise-to-Signal Ratio (NSR)':<30} | {res_clean['noise_to_signal_ratio']:^25} | {res_noisy['noise_to_signal_ratio']:^25}")
    print(f"{'Info Density (Token/100w)':<30} | {res_clean['information_density_per_100w']:^25} | {res_noisy['noise_tokens_count']:^25}")
    print("-" * 85)

    print("\nCatatan Analisis Metrik:")
    print("• Precision tinggi menunjukkan bahwa context bersih dari informasi yang tidak relevan (bebas dari noise).")
    print("• Noise-to-Signal Ratio (NSR) yang tinggi pada Skenario B meningkatkan risiko halusinasi dan pemborosan biaya token!")
    print("=" * 70)

if __name__ == "__main__":
    demo()
