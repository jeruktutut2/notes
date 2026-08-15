"""
02_langfuse_simulation.py
-------------------------
Simulasi pola integrasi Langfuse SDK (Traces, Generations, Scores, & Prompt Management).
"""

import time
import json
from typing import Dict, Any, List

class LangfuseSimulator:
    """Simulasi Open-Source LLM Observability Langfuse"""

    def __init__(self, public_key: str = "pk-lf-9821", secret_key: str = "sk-lf-7712"):
        self.public_key = public_key
        self.secret_key = secret_key
        self.traces: List[Dict[str, Any]] = []
        self.prompts: Dict[str, Dict[str, Any]] = {
            "qa_prompt": {
                "version": 2,
                "template": "System: Jawablah berdasarkan context berikut.\nContext: {{context}}\nUser: {{question}}"
            }
        }

    def trace(self, name: str, user_id: str, tags: List[str] = None) -> str:
        trace_id = f"lf-tr-{len(self.traces) + 1:03d}"
        trace_obj = {
            "id": trace_id,
            "name": name,
            "user_id": user_id,
            "tags": tags or [],
            "generations": [],
            "scores": []
        }
        self.traces.append(trace_obj)
        return trace_id

    def generation(
        self,
        trace_id: str,
        name: str,
        model: str,
        input_prompt: str,
        output_text: str,
        prompt_tokens: int,
        completion_tokens: int,
        total_cost_usd: float
    ):
        for tr in self.traces:
            if tr["id"] == trace_id:
                gen_data = {
                    "name": name,
                    "model": model,
                    "input": input_prompt,
                    "output": output_text,
                    "usage": {
                        "prompt_tokens": prompt_tokens,
                        "completion_tokens": completion_tokens,
                        "total_tokens": prompt_tokens + completion_tokens
                    },
                    "calculated_cost_usd": total_cost_usd
                }
                tr["generations"].append(gen_data)
                return True
        return False

    def score(self, trace_id: str, name: str, value: float, comment: str = None):
        for tr in self.traces:
            if tr["id"] == trace_id:
                tr["scores"].append({"name": name, "value": value, "comment": comment})
                return True
        return False

    def get_prompt(self, name: str, version: int = None) -> str:
        if name in self.prompts:
            return self.prompts[name]["template"]
        return ""

def main():
    print(f"\n=======================================================")
    print(f"🪢 LANGFUSE OBSERVABILITY SDK SIMULATION LAB")
    print(f"=======================================================\n")

    langfuse = LangfuseSimulator()

    print("1. Mengambil Prompt Ter-manage dari Langfuse UI...")
    template = langfuse.get_prompt("qa_prompt")
    print(f"   Template Versi Terbaru: \"{template}\"\n")

    print("2. Membuat Trace Baru di Langfuse...")
    trace_id = langfuse.trace(
        name="fintech_faq_query",
        user_id="user_8832",
        tags=["production", "v2.1", "mobile_app"]
    )
    print(f"   Trace ID Dibuat: {trace_id}")

    print("3. Mencatat LLM Generation di dalam Trace...")
    langfuse.generation(
        trace_id=trace_id,
        name="gpt4o_generation",
        model="gpt-4o",
        input_prompt=template.replace("{{context}}", "Batas harian transfer adalah Rp 50.000.000.").replace("{{question}}", "Berapa limit transfer per hari?"),
        output_text="Batas maksimal transfer per hari adalah Rp 50.000.000.",
        prompt_tokens=450,
        completion_tokens=22,
        total_cost_usd=0.001345
    )
    print("   Generation metrics (Tokens & Cost) logged.")

    print("4. Mengirimkan Evaluasi Score (LLM-as-a-Judge)...")
    langfuse.score(trace_id, name="faithfulness", value=1.0, comment="100% grounded on context")
    print("   Score registered.")

    print("\n✅ Langfuse simulation lab completed successfully!")

if __name__ == "__main__":
    main()
