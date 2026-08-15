#!/usr/bin/env python3
"""
Modul 03: Decision Matrix & Architectural Routing Engine
Membahas Matriks Keputusan kapan menggunakan Prompt Eng vs Context Eng vs RAG vs Fine-Tuning.
"""

import json
from typing import Dict, Any, List

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class ArchitecturalDecisionEngine:
    """Mesin Pengambil Keputusan Arsitektur AI Engineering"""

    @staticmethod
    def evaluate_use_case(
        data_volume: str,        # "NONE", "SMALL_DOCS", "LARGE_ENTERPRISE_KB"
        data_volatility: str,    # "STATIC", "DYNAMIC_REALTIME"
        reasoning_complexity: str,# "FORMATTING_ONLY", "LOGICAL_STEP_BY_STEP", "DOMAIN_STRICT_BEHAVIOR"
        latency_budget_ms: int,  # Max latency allowed
        token_budget_per_call: int
    ) -> Dict[str, Any]:
        """Menentukan strategi arsitektural yang paling optimal"""

        recommendations = []
        primary_architecture = ""
        rationale = []

        # Decision Tree logic
        if data_volume == "NONE" and reasoning_complexity in ["FORMATTING_ONLY", "LOGICAL_STEP_BY_STEP"]:
            primary_architecture = "PROMPT_ENGINEERING_ONLY"
            rationale.append("Tidak ada dokumen eksternal yang perlu di-inject ke context. Cukup gunakan CoT / Few-Shot prompt.")
        
        elif data_volume == "SMALL_DOCS" and data_volatility == "STATIC" and token_budget_per_call > 16000:
            primary_architecture = "CONTEXT_ENGINEERING_IN_CONTEXT"
            rationale.append("Dokumen kecil dan dapat muat langsung dalam Context Window menggunakan In-Context Prompting + Prefix Caching.")

        elif data_volume == "LARGE_ENTERPRISE_KB" or data_volatility == "DYNAMIC_REALTIME":
            primary_architecture = "CONTEXT_ENGINEERING_PLUS_RAG"
            rationale.append("Basis data besar / real-time tidak muat dalam prompt statis. Wajib menggunakan Context Assembler + RAG Vector DB.")

        elif reasoning_complexity == "DOMAIN_STRICT_BEHAVIOR" and data_volatility == "STATIC":
            primary_architecture = "FINE_TUNING_PLUS_PROMPT_ENGINEERING"
            rationale.append("Membutuhkan penyesuaian bobot internal model untuk tone/gaya domain khusus, ditambah Prompt Framing untuk guardrails.")

        else:
            primary_architecture = "HYBRID_PROMPT_AND_CONTEXT_ENGINEERING"
            rationale.append("Kombinasi optimal: Prompt Framing untuk format & persona + Context Engineering untuk memory & document assembly.")

        return {
            "input_metrics": {
                "data_volume": data_volume,
                "data_volatility": data_volatility,
                "reasoning_complexity": reasoning_complexity,
                "latency_budget_ms": latency_budget_ms,
                "token_budget": token_budget_per_call
            },
            "recommended_architecture": primary_architecture,
            "rationale": rationale,
            "architecture_blueprint": ArchitecturalDecisionEngine._get_blueprint(primary_architecture)
        }

    @staticmethod
    def _get_blueprint(arch_type: str) -> Dict[str, str]:
        blueprints = {
            "PROMPT_ENGINEERING_ONLY": {
                "System Prompt": "XML Persona + CoT Step-by-Step",
                "Context Assembly": "Disabled (0 extra tokens)",
                "Storage Needed": "None",
                "Optimization Focus": "Few-Shot examples & Output JSON Schema"
            },
            "CONTEXT_ENGINEERING_IN_CONTEXT": {
                "System Prompt": "Static Persona Prefix",
                "Context Assembly": "Document Ingestion + Token Density Pruning",
                "Storage Needed": "In-Memory Prefix Cache (vLLM / Anthropic)",
                "Optimization Focus": "Prefix Caching & Lost-in-the-middle positioning"
            },
            "CONTEXT_ENGINEERING_PLUS_RAG": {
                "System Prompt": "Strict Guardrail Framing",
                "Context Assembly": "Semantic Search -> Re-ranking -> Summary Buffer -> Assembler",
                "Storage Needed": "Vector Database (Chroma / Qdrant)",
                "Optimization Focus": "Chunking Strategy, Context Precision & Recall"
            },
            "HYBRID_PROMPT_AND_CONTEXT_ENGINEERING": {
                "System Prompt": "Structured XML Delimiters + Self-Repair Loop",
                "Context Assembly": "Tripartite Memory + Sanitized PII + Dynamic RAG",
                "Storage Needed": "Redis Memory Store + Vector DB",
                "Optimization Focus": "Balanced Latency, Cost, and Accuracy"
            }
        }
        return blueprints.get(arch_type, blueprints["HYBRID_PROMPT_AND_CONTEXT_ENGINEERING"])

def main():
    print_header("MODUL 03: ARCHITECTURAL DECISION MATRIX ENGINE")

    test_scenarios = [
        {
            "name": "Skenario 1: Parsing PDF Invoice ke JSON",
            "params": ("NONE", "STATIC", "FORMATTING_ONLY", 500, 2000)
        },
        {
            "name": "Skenario 2: Customer Care Bot 10.000 FAQ Produk",
            "params": ("LARGE_ENTERPRISE_KB", "DYNAMIC_REALTIME", "LOGICAL_STEP_BY_STEP", 2000, 32000)
        },
        {
            "name": "Skenario 3: Analis Dokumen Kontrak Hukum (50 Halaman)",
            "params": ("SMALL_DOCS", "STATIC", "LOGICAL_STEP_BY_STEP", 1500, 64000)
        }
    ]

    for sc in test_scenarios:
        print(color(f"\n{sc['name']}:", "1;33"))
        res = ArchitecturalDecisionEngine.evaluate_use_case(*sc["params"])
        print(color(f"  ► Rekomendasi Utama : {res['recommended_architecture']}", "1;32"))
        print(f"  ► Rationale         : {res['rationale'][0]}")
        print(color("  ► Architecture Blueprint:", "36"))
        for k, v in res['architecture_blueprint'].items():
            print(f"      • {k:<18}: {v}")

    print_header("MATRIKS KEPUTUSAN RINGKAS")
    print("┌───────────────────────────┬───────────────────────┬────────────────────────────┐")
    print("│ Kebutuhan Sistem          │ Pilihan Terbaik       │ Komponen Kunci             │")
    print("├───────────────────────────┼───────────────────────┼────────────────────────────┤")
    print("│ Reasoning & Format Cepat  │ Prompt Engineering    │ CoT, XML Tags, Few-Shot    │")
    print("│ Percakapan Long-Memory    │ Context Engineering   │ Summary Buffer, State Mem  │")
    print("│ Enterprise Knowledge Base │ Context Eng + RAG     │ Dynamic Assembler, VectorDB│")
    print("│ Model Tone Khusus Domain  │ Fine-Tuning + Prompt  │ Weight Tuning + Guardrail  │")
    print("└───────────────────────────┴───────────────────────┴────────────────────────────┘")

if __name__ == "__main__":
    main()
