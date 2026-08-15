#!/usr/bin/env python3
"""
Modul: Pre-trained Models
Simulasi Perbandingan Karakteristik Model Fondasi (7B, 70B, 405B) dan Pengaruhnya terhadap Prompt/Context Strategy.
"""

import json

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

MODELS_DATABASE = {
    "Llama-3.1-8B-Instruct": {
        "params": "8 Billion",
        "context_window": "128,000 tokens",
        "cot_reasoning_capability": "MEDIUM",
        "ideal_prompt_strategy": "Few-Shot + Explicit XML Delimiters",
        "ideal_context_strategy": "Aggressive Token Compaction (Small memory footprint)"
    },
    "Llama-3.1-70B-Instruct": {
        "params": "70 Billion",
        "context_window": "128,000 tokens",
        "cot_reasoning_capability": "HIGH",
        "ideal_prompt_strategy": "Zero-Shot CoT / ReAct Framework",
        "ideal_context_strategy": "RAG + Prefix Caching"
    },
    "GPT-4o / Claude 3.5 Sonnet": {
        "params": "Proprietary Enterprise Scale",
        "context_window": "128K - 200K tokens",
        "cot_reasoning_capability": "VERY_HIGH",
        "ideal_prompt_strategy": "Structured Output (JSON Schema) + Complex Function Calling",
        "ideal_context_strategy": "Dynamic Context Assembler + Multi-Tenant Isolation"
    }
}

def main():
    print("=" * 70)
    print(color("  MODUL: PRE-TRAINED FOUNDATION MODELS COMPARISON", "1;34"))
    print("=" * 70)

    for model_name, info in MODELS_DATABASE.items():
        print(color(f"\n=== {model_name} ===", "1;33"))
        print(f"  • Parameter Size  : {info['params']}")
        print(f"  • Context Limit   : {info['context_window']}")
        print(f"  • CoT Reasoning   : {info['cot_reasoning_capability']}")
        print(color(f"  • Prompt Strategy : {info['ideal_prompt_strategy']}", "32"))
        print(color(f"  • Context Strategy: {info['ideal_context_strategy']}", "36"))

    print("\n" + "=" * 70)
    print("✓ Memilih skala pre-trained model menentukan kompleksitas prompt & strategi context compaction yang dibutuhkan.")

if __name__ == "__main__":
    main()
