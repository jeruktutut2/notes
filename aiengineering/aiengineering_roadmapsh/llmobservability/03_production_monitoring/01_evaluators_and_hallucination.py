"""
01_evaluators_and_hallucination.py
----------------------------------
Lab runnable untuk mengevaluasi kualitas output LLM secara otomatis menggunakan LLM-as-a-Judge
dan metrik evaluasi RAGAS (Faithfulness, Answer Relevance, Hallucination Risk).
"""

import random
from typing import Dict, Any

class ProductionEvaluator:
    """Simulasi Evaluator Kualitas & Halusinasi LLM"""

    def evaluate_rag_output(
        self,
        query: str,
        retrieved_context: str,
        llm_response: str
    ) -> Dict[str, Any]:
        """
        Menghitung skor evaluasi:
        1. Faithfulness: Apakah jawaban hanya bersumber dari konteks?
        2. Answer Relevance: Apakah jawaban menjawab query pengguna?
        3. Hallucination Risk: Probabilitas adanya klaim tanpa dasar.
        """
        
        # Heuristic scoring simulation for demonstration
        # 1. Faithfulness score based on key overlap or hallucination markers
        words_in_context = set(retrieved_context.lower().split())
        response_words = set(llm_response.lower().split())

        # Check for ungrounded hallucination keywords in simulation
        hallucination_triggers = ["quantum", "teleportation", "alien", "1000%", "terbukti secara gaib"]
        has_hallucination = any(trigger in llm_response.lower() for trigger in hallucination_triggers)

        if has_hallucination:
            faithfulness_score = round(random.uniform(0.1, 0.35), 2)
            hallucination_risk = round(random.uniform(0.80, 0.95), 2)
        else:
            faithfulness_score = round(random.uniform(0.85, 0.99), 2)
            hallucination_risk = round(random.uniform(0.01, 0.10), 2)

        relevance_score = round(random.uniform(0.88, 0.98), 2)

        pass_evaluation = (faithfulness_score >= 0.70) and (hallucination_risk < 0.30)

        return {
            "query": query,
            "faithfulness_score": faithfulness_score,
            "answer_relevance_score": relevance_score,
            "hallucination_risk": hallucination_risk,
            "passed_quality_gate": pass_evaluation,
            "evaluation_verdict": "PASSED" if pass_evaluation else "FAILED (HALUCINATION DETECTED)"
        }

def main():
    print(f"\n=======================================================")
    print(f"🔬 LLM-AS-A-JUDGE & HALLUCINATION EVALUATOR LAB")
    print(f"=======================================================\n")

    evaluator = ProductionEvaluator()

    # Case 1: Valid RAG Output
    print("--- EVALUASI SAMPLING 1: Valid Grounded Answer ---")
    query_1 = "Berapa jam garansi resmi laptop X200?"
    context_1 = "Garansi resmi laptop X200 berlaku selama 24 bulan sejak tanggal pembelian."
    response_1 = "Laptop X200 memiliki masa garansi resmi selama 24 bulan (2 tahun)."

    res1 = evaluator.evaluate_rag_output(query_1, context_1, response_1)
    print(f"Query           : {res1['query']}")
    print(f"Faithfulness    : {res1['faithfulness_score']} / 1.00")
    print(f"Relevance       : {res1['answer_relevance_score']} / 1.00")
    print(f"Hallucination   : {res1['hallucination_risk']}")
    print(f"Verdict         : {res1['evaluation_verdict']}\n")

    # Case 2: Hallucinated Output
    print("--- EVALUASI SAMPLING 2: Hallucinated Answer ---")
    query_2 = "Apakah garansi meng-cover kerusakan akibat air?"
    context_2 = "Garansi hanya mencakup kerusakan pabrik dan sparepart internal. Garansi tidak mencakup cairan."
    response_2 = "Ya, garansi mencakup air karena laptop dilengkapi teknologi quantum waterproofing 1000%."

    res2 = evaluator.evaluate_rag_output(query_2, context_2, response_2)
    print(f"Query           : {res2['query']}")
    print(f"Faithfulness    : {res2['faithfulness_score']} / 1.00")
    print(f"Relevance       : {res2['answer_relevance_score']} / 1.00")
    print(f"Hallucination   : {res2['hallucination_risk']}")
    print(f"Verdict         : {res2['evaluation_verdict']}\n")

    print("✅ Evaluasi kualitas produksi selesai!")

if __name__ == "__main__":
    main()
