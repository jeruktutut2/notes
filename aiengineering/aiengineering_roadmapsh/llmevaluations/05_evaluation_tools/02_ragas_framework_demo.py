"""
02_ragas_framework_demo.py
--------------------------
Demonstrasi Framework RAGAS (Retrieval Augmented Generation Assessment):
1. Evaluasi Komponen RAG (Faithfulness, Answer Relevance, Context Precision, Context Recall)
2. Batch Evaluation pada Dataset RAG
3. Pembuatan Laporan Evaluasi RAGAS (Evaluation Matrix)
"""

class RagasEvaluatorSimulated:
    """Simulator RAGAS Dataset Evaluation Framework."""

    def evaluate_dataset(self, dataset: list[dict]) -> dict:
        """
        Evaluasi kumpulan sampel RAG dataset menggunakan metrik RAGAS.
        """
        sample_scores = []
        for idx, sample in enumerate(dataset, 1):
            # Simulated RAGAS metrics calculations
            f_score = 0.90 if idx != 2 else 0.40 # sample 2 has lower faithfulness
            ar_score = 0.88
            cp_score = 0.95
            cr_score = 0.85

            harmonic_mean = round(4 / (1/f_score + 1/ar_score + 1/cp_score + 1/cr_score), 4)

            sample_scores.append({
                "id": idx,
                "question": sample["question"],
                "faithfulness": f_score,
                "answer_relevance": ar_score,
                "context_precision": cp_score,
                "context_recall": cr_score,
                "ragas_score": harmonic_mean
            })

        avg_f = sum(s["faithfulness"] for s in sample_scores) / len(sample_scores)
        avg_ar = sum(s["answer_relevance"] for s in sample_scores) / len(sample_scores)
        avg_cp = sum(s["context_precision"] for s in sample_scores) / len(sample_scores)
        avg_cr = sum(s["context_recall"] for s in sample_scores) / len(sample_scores)

        return {
            "summary_metrics": {
                "ragas_faithfulness": round(avg_f, 4),
                "ragas_answer_relevance": round(avg_ar, 4),
                "ragas_context_precision": round(avg_cp, 4),
                "ragas_context_recall": round(avg_cr, 4),
                "overall_ragas_score": round((avg_f + avg_ar + avg_cp + avg_cr) / 4.0, 4)
            },
            "sample_details": sample_scores
        }

if __name__ == "__main__":
    print("=== LAB 13: RAGAS FRAMEWORK BATCH EVALUATION ===")

    rag_eval_dataset = [
        {
            "question": "Berapa lama masa retensi log di LLM Observability?",
            "answer": "Log disimpan selama 30 hari secara default pada tier standar.",
            "contexts": ["Masa retensi log standar untuk paket gratis adalah 30 hari. Paket enterprise mendukung hingga 1 tahun."]
        },
        {
            "question": "Bagaimana cara kerja Langfuse?",
            "answer": "Langfuse adalah platform observability open-source untuk tracing, eval, dan prompt management.",
            "contexts": ["Langfuse menyediakan OpenTelemetry tracer SDK untuk Python dan TypeScript."]
        }
    ]

    ragas = RagasEvaluatorSimulated()
    report = ragas.evaluate_dataset(rag_eval_dataset)

    print("\n--- RAGAS BATCH EVALUATION SUMMARY ---")
    for metric_name, score in report["summary_metrics"].items():
        print(f"  {metric_name:<25}: {score * 100:.1f}%")

    print("\n--- Individual Sample Scores ---")
    for sample in report["sample_details"]:
        print(f"\n Sample #{sample['id']}: '{sample['question']}'")
        print(f"   Faithfulness      : {sample['faithfulness'] * 100:.1f}%")
        print(f"   Answer Relevance  : {sample['answer_relevance'] * 100:.1f}%")
        print(f"   Context Precision : {sample['context_precision'] * 100:.1f}%")
        print(f"   Context Recall    : {sample['context_recall'] * 100:.1f}%")
        print(f"   RAGAS Score       : ⭐ {sample['ragas_score']}")
