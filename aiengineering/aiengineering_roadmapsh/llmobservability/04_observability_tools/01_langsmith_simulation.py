"""
01_langsmith_simulation.py
---------------------------
Simulasi pola integrasi SDK LangSmith (Run tracing, Dataset Evaluasi, dan Feedback collection).
"""

import time
import json
from typing import Dict, Any, List

class LangSmithSimulator:
    """Simulasi LangSmith Client & SDK Pattern"""

    def __init__(self, api_key: str = "ls__simulated_key_9981"):
        self.api_key = api_key
        self.runs: List[Dict[str, Any]] = []
        self.datasets: Dict[str, List[Dict[str, Any]]] = {}

    def create_run(
        self,
        name: str,
        run_type: str,
        inputs: Dict[str, Any],
        outputs: Dict[str, Any],
        prompt_tokens: int,
        completion_tokens: int,
        execution_time_ms: float,
        parent_run_id: str = None
    ) -> str:
        run_id = f"run_{len(self.runs) + 1:04d}"
        run_data = {
            "id": run_id,
            "name": name,
            "run_type": run_type, # 'chain', 'llm', 'tool', 'retriever'
            "inputs": inputs,
            "outputs": outputs,
            "parent_run_id": parent_run_id,
            "metrics": {
                "prompt_tokens": prompt_tokens,
                "completion_tokens": completion_tokens,
                "latency_ms": execution_time_ms
            }
        }
        self.runs.append(run_data)
        return run_id

    def log_feedback(self, run_id: str, key: str, score: float, comment: str = None):
        for run in self.runs:
            if run["id"] == run_id:
                if "feedback" not in run:
                    run["feedback"] = []
                run["feedback"].append({"key": key, "score": score, "comment": comment})
                return True
        return False

    def create_dataset_example(self, dataset_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any]):
        if dataset_name not in self.datasets:
            self.datasets[dataset_name] = []
        self.datasets[dataset_name].append({"inputs": inputs, "outputs": outputs})

def main():
    print(f"\n=======================================================")
    print(f"🦜🔗 LANGSMITH SDK SIMULATION LAB")
    print(f"=======================================================\n")

    client = LangSmithSimulator()

    print("1. Mengirim Parent Chain Run ke LangSmith...")
    parent_id = client.create_run(
        name="CustomerSupportAgent",
        run_type="chain",
        inputs={"question": "Apakah barang bisa dikirim via GO-SEND?"},
        outputs={"answer": "Ya, pengiriman via GO-SEND Instant tersedia untuk wilayah Jabodetabek."},
        prompt_tokens=320,
        completion_tokens=45,
        execution_time_ms=620.0
    )
    print(f"   Created Run ID: {parent_id}")

    print("2. Mengirim Child Tool Run (Vector DB Retriever)...")
    child_retriever_id = client.create_run(
        name="ShippingPolicyRetriever",
        run_type="retriever",
        inputs={"query": "GO-SEND instant Jabodetabek"},
        outputs={"documents": ["Dokumen Kebijakan Pengiriman v3.pdf - Halaman 4"]},
        prompt_tokens=0,
        completion_tokens=0,
        execution_time_ms=110.0,
        parent_run_id=parent_id
    )
    print(f"   Created Child Run ID: {child_retriever_id}")

    print("3. Mengirim Feedback Evaluasi ke Run...")
    client.log_feedback(parent_id, key="correctness", score=1.0, comment="Jawaban akurat sesuai kebijakan seller")
    print("   Feedback logged successfully.")

    print("4. Menambahkan sampel ke LangSmith Test Dataset...")
    client.create_dataset_example(
        dataset_name="shipping_faq_eval_v1",
        inputs={"question": "Apakah barang bisa dikirim via GO-SEND?"},
        outputs={"answer": "Ya, pengiriman via GO-SEND Instant tersedia untuk wilayah Jabodetabek."}
    )
    print("   Dataset example registered.")

    print(f"\nTotal Runs Recorded in LangSmith Platform: {len(client.runs)}")
    print("✅ LangSmith simulation lab completed successfully!")

if __name__ == "__main__":
    main()
