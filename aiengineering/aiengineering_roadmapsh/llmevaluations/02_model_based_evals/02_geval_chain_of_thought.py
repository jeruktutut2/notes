"""
02_geval_chain_of_thought.py
----------------------------
Demonstrasi Framework G-Eval (Zheng et al.):
1. Evaluasi berbasis Formulated Evaluation Steps & Rubrik Tertulis
2. Multi-criteria Evaluation (Coherence, Relevance, Correctness)
3. Weighted Score Aggregation
"""

import json

class GEvalEvaluator:
    """Implementasi Simulator G-Eval Framework."""

    def __init__(self, criteria_weights: dict = None):
        self.criteria_weights = criteria_weights or {
            "relevance": 0.4,
            "correctness": 0.4,
            "coherence": 0.2
        }

    def generate_evaluation_steps(self, criterion: str) -> list[str]:
        """Minta LLM mendefinisikan langkah evaluasi spesifik untuk satu kriteria."""
        steps_map = {
            "relevance": [
                "1. Baca pertanyaan pengguna secara cermat.",
                "2. Periksa apakah respons menjawab pertanyaan utama.",
                "3. Identifikasi apakah ada informasi yang menyimpang dari topik."
            ],
            "correctness": [
                "1. Bandingkan fakta dalam respons dengan fakta di Ground Truth.",
                "2. Cari klaim yang salah, kontra-indikatif, atau berhalusinasi.",
                "3. Tentukan tingkat kebenaran secara keseluruhan."
            ],
            "coherence": [
                "1. Periksa alur logika antar paragraf dan kalimat.",
                "2. Pastikan tata bahasa dan keterbacaan yang runtut.",
                "3. Nilai kerapihan struktur penulisan."
            ]
        }
        return steps_map.get(criterion, ["1. Evaluasi respons umum."])

    def evaluate_criterion(self, criterion: str, input_text: str, actual_output: str, ground_truth: str = None) -> dict:
        """Menilai satu kriteria menggunakan langkah-langkah G-Eval CoT."""
        steps = self.generate_evaluation_steps(criterion)
        
        # Simulated LLM response containing score and step-by-step reasoning
        mock_scores = {
            "relevance": {"score": 5.0, "reason": "Respons 100% fokus pada pertanyaan RAG."},
            "correctness": {"score": 4.0, "reason": "Fakta akurat, hanya saja tidak menyebutkan reranking."},
            "coherence": {"score": 5.0, "reason": "Struktur narasi sangat runtut dan jelas."}
        }
        
        res = mock_scores.get(criterion, {"score": 3.0, "reason": "Cukup baik."})
        return {
            "criterion": criterion,
            "evaluation_steps": steps,
            "score": res["score"],
            "reason": res["reason"]
        }

    def run_geval_pipeline(self, input_text: str, actual_output: str, ground_truth: str = None) -> dict:
        """Menjalankan pipeline G-Eval menyeluruh dan menghitung weighted score akhir."""
        results = {}
        total_weighted_score = 0.0
        
        for criterion, weight in self.criteria_weights.items():
            eval_res = self.evaluate_criterion(criterion, input_text, actual_output, ground_truth)
            results[criterion] = eval_res
            total_weighted_score += eval_res["score"] * weight

        return {
            "final_geval_score": round(total_weighted_score, 2),
            "max_score": 5.0,
            "normalised_score_percentage": round((total_weighted_score / 5.0) * 100, 1),
            "breakdown": results
        }

if __name__ == "__main__":
    print("=== LAB 05: G-EVAL CHAIN-OF-THOUGHT EVALUATION ===")

    query = "Jelaskan perbedaan antara Prompt Engineering dan Fine-tuning."
    output = "Prompt Engineering adalah cara mengarahkan LLM dengan teks tanpa mengubah bobot model. Fine-tuning adalah melatih ulang bobot model pada dataset spesifik."
    ground_truth = "Prompt Engineering mengubah konteks input. Fine-tuning mengubah bobot internal model."

    geval = GEvalEvaluator()
    geval_res = geval.run_geval_pipeline(query, output, ground_truth)

    print(f"\n[G-Eval Target Query]: '{query}'")
    print(f"[Actual Output]      : '{output}'")
    print(f"\n[Final G-Eval Score] : {geval_res['final_geval_score']} / 5.0 ({geval_res['normalised_score_percentage']}%)")

    print("\n--- Detailed Breakdown per Criterion ---")
    for crit, data in geval_res['breakdown'].items():
        print(f"\nKriteria: {crit.upper()} (Skor: {data['score']} / 5.0)")
        print("Steps CoT:")
        for step in data['evaluation_steps']:
            print(f"  {step}")
        print(f"Reasoning: {data['reason']}")
