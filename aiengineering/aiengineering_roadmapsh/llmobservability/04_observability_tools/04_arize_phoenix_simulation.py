"""
04_arize_phoenix_simulation.py
------------------------------
Simulasi platform Arize AI & Phoenix (OpenTelemetry Spans, Embedding Clustering, & RAG Evals).
"""

import random
from typing import Dict, Any, List

class ArizePhoenixSimulator:
    """Simulasi Arize Phoenix ML & LLM Observability Platform"""

    def __init__(self):
        self.spans: List[Dict[str, Any]] = []
        self.evaluation_benchmarks: List[Dict[str, Any]] = []

    def log_open_inference_span(
        self,
        name: str,
        kind: str, # LLM, RETRIEVER, CHAIN, EMBEDDING
        input_data: Dict[str, Any],
        output_data: Dict[str, Any],
        latency_ms: float
    ) -> str:
        span_id = f"px-span-{len(self.spans) + 1:04d}"
        span = {
            "span_id": span_id,
            "name": name,
            "kind": kind,
            "input": input_data,
            "output": output_data,
            "latency_ms": latency_ms
        }
        self.spans.append(span)
        return span_id

    def run_phoenix_evaluators(self, query: str, context: str, response: str) -> Dict[str, Any]:
        """Runs Arize Phoenix built-in QA & Hallucination evaluators"""
        faithfulness = round(random.uniform(0.85, 0.99), 2)
        qa_correctness = round(random.uniform(0.88, 1.00), 2)

        eval_result = {
            "eval_name": "Phoenix RAG Evaluator",
            "metrics": {
                "faithfulness": faithfulness,
                "qa_correctness": qa_correctness
            },
            "status": "PASSED" if faithfulness >= 0.8 else "FAILED"
        }
        self.evaluation_benchmarks.append(eval_result)
        return eval_result

def main():
    print(f"\n=======================================================")
    print(f"🔥 ARIZE AI & PHOENIX OBSERVABILITY SIMULATION LAB")
    print(f"=======================================================\n")

    phoenix = ArizePhoenixSimulator()

    print("1. Mengirim OpenInference Embedding Span ke Phoenix...")
    s1 = phoenix.log_open_inference_span(
        name="TextEmbeddingGeneration",
        kind="EMBEDDING",
        input_data={"text": "Cara reset password akun fintech"},
        output_data={"embedding_dim": 1536, "norm": 1.0},
        latency_ms=45.2
    )
    print(f"   Logged Span ID: {s1}")

    print("2. Mengirim OpenInference LLM Span ke Phoenix...")
    s2 = phoenix.log_open_inference_span(
        name="OpenAI GPT-4o Call",
        kind="LLM",
        input_data={"prompt": "Rekomendasikan laptop untuk video editing."},
        output_data={"completion": "Rekomendasi laptop: MacBook Pro M3 atau Asus ROG Zephyrus."},
        latency_ms=520.0
    )
    print(f"   Logged Span ID: {s2}")

    print("3. Menjalankan Built-in Phoenix RAG Evaluators...")
    eval_res = phoenix.run_phoenix_evaluators(
        query="Rekomendasikan laptop untuk video editing.",
        context="MacBook Pro M3 dan Asus ROG sangat cocok untuk video editing 4K.",
        response="Rekomendasi laptop: MacBook Pro M3 atau Asus ROG Zephyrus."
    )
    print(f"   Faithfulness Score : {eval_res['metrics']['faithfulness']}")
    print(f"   QA Correctness     : {eval_res['metrics']['qa_correctness']}")
    print(f"   Status Evaluation  : {eval_res['status']}\n")

    print("✅ Arize Phoenix simulation lab completed successfully!")

if __name__ == "__main__":
    main()
