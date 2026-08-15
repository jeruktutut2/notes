#!/usr/bin/env python3
"""
Modul 01: Dasar & Anatomi Prompt Engineering
Membahas 4 Komponen Utama Prompt, Persona Framing, dan Delimiter XML Tags.
"""

import json
from typing import Dict, Any

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_header(title: str):
    print("\n" + "=" * 70)
    print(color(f"  {title}", "1;34"))
    print("=" * 70)

class PromptAnatomyDemo:
    """Simulasi Anatomi Prompt dan Perbandingan Formatting"""
    
    @staticmethod
    def construct_unstructured_prompt(task: str, context: str, user_input: str) -> str:
        """Prompt tidak terstruktur (raw text)"""
        return f"{task} {context} Input: {user_input} Tolong jawab dalam JSON."

    @staticmethod
    def construct_structured_prompt(
        instruction: str,
        persona: str,
        context: str,
        user_input: str,
        output_format: str
    ) -> str:
        """Prompt terstruktur menggunakan 4 komponen utama + XML tags"""
        return f"""<system_persona>
{persona}
</system_persona>

<instruction>
{instruction}
</instruction>

<context>
{context}
</context>

<user_input>
{user_input}
</user_input>

<output_constraint>
{output_format}
</output_constraint>"""

    @staticmethod
    def simulate_llm_execution(prompt: str) -> Dict[str, Any]:
        """Simulasi pengolahan LLM terhadap prompt yang diberikan"""
        has_xml = "<instruction>" in prompt and "<system_persona>" in prompt
        
        if has_xml:
            return {
                "status": "SUCCESS",
                "extracted_components": {
                    "persona": "Expert Financial Analyst",
                    "instruction": "Analisis tingkat risiko kredit berdasarkan rasio keuangan",
                    "context_present": True,
                    "input_data": "Debt-to-Equity: 2.5, Current Ratio: 0.8",
                    "output_format": "JSON Structured"
                },
                "simulated_output": {
                    "risk_level": "HIGH",
                    "confidence_score": 0.92,
                    "key_factors": ["High Debt-to-Equity ratio (2.5)", "Low Liquidity / Current Ratio (0.8)"],
                    "recommendation": "Reject loan or require collateral"
                },
                "boundary_isolation_score": "100% (No Instruction Drift)"
            }
        else:
            return {
                "status": "AMBIGUOUS / DRIFT RISK",
                "extracted_components": "Unstructured text block",
                "simulated_output": "Risiko kredit perusahaan ini cukup tinggi karena utangnya besar dan likuiditas rendah.",
                "boundary_isolation_score": "45% (Risk of prompt injection / confusion)"
            }

def main():
    print_header("MODUL 01: DASAR & ANATOMI PROMPT ENGINEERING")
    
    print(color("\n1. 4 Komponen Utama Anatomi Prompt:", "1;33"))
    print("   [1] Persona / System Instruction : Menentukan identitas, nada, dan batas peran LLM.")
    print("   [2] Instruction / Task           : Instruksi spesifik mengenai apa yang harus dikerjakan.")
    print("   [3] Context / Reference Data     : Informasi latar belakang, dokumen pendukung, atau aturan bisnis.")
    print("   [4] Input Data & Output Constraint: Data riil yang diproses & format luaran (misal: JSON/XML).")
    
    instruction = "Analisis tingkat risiko kredit berdasarkan rasio keuangan berikut."
    persona = "Anda adalah Analis Risiko Keuangan Senior di Bank Internasional."
    context = "Aturan Bank: Debt-to-Equity > 2.0 dikategorikan Risiko Tinggi. Current Ratio < 1.0 dikategorikan Likuiditas Buruk."
    user_input = "Perusahaan PT ABC: Debt-to-Equity = 2.5, Current Ratio = 0.8."
    output_format = "Berikan luaran berupa JSON valid dengan field: risk_level, confidence_score, key_factors, recommendation."
    
    print(color("\n2. Perbandingan Prompt Tidak Terstruktur vs Terstruktur (XML Tagging):", "1;33"))
    
    unstructured = PromptAnatomyDemo.construct_unstructured_prompt(instruction, context, user_input)
    structured = PromptAnatomyDemo.construct_structured_prompt(instruction, persona, context, user_input, output_format)
    
    print(color("\n--- Prompt Tidak Terstruktur ---", "1;31"))
    print(unstructured)
    res_unstructured = PromptAnatomyDemo.simulate_llm_execution(unstructured)
    print(color("\nHasil Eksekusi LLM (Unstructured):", "36"))
    print(json.dumps(res_unstructured, indent=2, ensure_ascii=False))
    
    print(color("\n--- Prompt Terstruktur (XML Delimiters) ---", "1;32"))
    print(structured)
    res_structured = PromptAnatomyDemo.simulate_llm_execution(structured)
    print(color("\nHasil Eksekusi LLM (Structured):", "36"))
    print(json.dumps(res_structured, indent=2, ensure_ascii=False))
    
    print_header("RANGKUMAN DASAR ANATOMI PROMPT")
    print("✓ Delimiter XML (`<instruction>`, `<context>`) mencegah percampuran instruksi & data input.")
    print("✓ Persona Framing menetapkan kerangka berpikir LLM dan meningkatkan konsistensi hasil.")
    print("✓ Output Constraints menjamin luaran dapat di-parse secara otomatis oleh sistem downstream.")

if __name__ == "__main__":
    main()
