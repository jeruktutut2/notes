"""
01_llm_judge_single_and_pairwise.py
-----------------------------------
Demonstrasi LLM-as-a-Judge:
1. Single Grading Evaluation (Nilai Absolut 1-5 dengan Alasan CoT)
2. Pairwise Ranking Evaluation (Model A vs Model B)
3. Prompt Engineering untuk Evaluator Judge
"""

import json
import os

# Simulated LLM Judge Response for offline testing fallback
def mock_llm_judge_call(prompt: str) -> str:
    """Simulasi panggilan ke LLM Judge (seperti GPT-4o)."""
    prompt_lower = prompt.lower()
    if "single grading" in prompt_lower:
        return json.dumps({
            "score": 4.5,
            "reasoning": "Jawaban sangat akurat dan terstruktur dengan baik. Menjelaskan konsep RAG dengan tepat, namun contoh alur bisa sedikit lebih mendalam."
        })
    elif "pairwise evaluation" in prompt_lower:
        return json.dumps({
            "winner": "Model A",
            "reasoning": "Model A memberikan langkah teknis yang konkret dan contoh kode singkat, sedangkan Model B hanya memberikan gambaran konseptual umum."
        })
    return json.dumps({"score": 3.0, "reasoning": "Evaluasi umum."})

def single_grading_eval(user_query: str, llm_response: str, rubrics: str) -> dict:
    """Single grading evaluation prompt & parsing."""
    prompt = f"""
System: Anda adalah Evaluator Ahli (LLM Judge). Tugas Anda adalah menilai respons berikut berdasarkan rubrik yang diberikan.

[USER QUERY]: {user_query}
[LLM RESPONSE]: {llm_response}

[EVALUATION RUBRICS]:
{rubrics}

Berikan penilaian dalam format JSON valid:
{{
  "score": <float 1.0 - 5.0>,
  "reasoning": "<penjelasan CoT secara singkat>"
}}

Single Grading Task
"""
    raw_res = mock_llm_judge_call(prompt)
    try:
        return json.loads(raw_res)
    except Exception:
        return {"score": 0.0, "reasoning": raw_res}

def pairwise_grading_eval(user_query: str, response_a: str, response_b: str) -> dict:
    """Pairwise ranking evaluation prompt & parsing."""
    prompt = f"""
System: Anda adalah Evaluator Netral. Bandingkan dua respons LLM berikut untuk menentukan mana yang lebih baik.

[USER QUERY]: {user_query}

[RESPONSE MODEL A]:
{response_a}

[RESPONSE MODEL B]:
{response_b}

Kriteria Penilaian: Keakuratan, kejelasan, kelengkapan, dan kepraktisan.
Tentukan pemenang: "Model A", "Model B", atau "Tie".

Berikan luaran JSON valid:
{{
  "winner": "<Model A / Model B / Tie>",
  "reasoning": "<penjelasan perbandingan>"
}}

Pairwise Evaluation Task
"""
    raw_res = mock_llm_judge_call(prompt)
    try:
        return json.loads(raw_res)
    except Exception:
        return {"winner": "Unknown", "reasoning": raw_res}


if __name__ == "__main__":
    print("=== LAB 04: LLM-AS-A-JUDGE (SINGLE & PAIRWISE) ===")

    query = "Bagaimana cara kerja RAG dalam LLM?"
    resp_a = "RAG (Retrieval-Augmented Generation) menggabungkan pencarian dokumen dari Vector Database dengan prompt LLM untuk mengurangi halusinasi."
    resp_b = "RAG adalah cara agar AI menjadi lebih pintar dengan membaca buku."

    rubric_text = """
- Skor 5: Penjelasan teknis sangat akurat, menyebutkan komponen kunci (Retriever/Vector DB & Generator).
- Skor 3: Penjelasan cukup akurat namun terlalu umum.
- Skor 1: Informasi salah atau membingungkan.
"""

    print("\n[1] Single Grading Evaluation:")
    print(f"    Query: '{query}'")
    eval_single = single_grading_eval(query, resp_a, rubric_text)
    print(f"    Assigned Score: {eval_single['score']} / 5.0")
    print(f"    Judge CoT Reasoning: {eval_single['reasoning']}")

    print("\n[2] Pairwise Comparison Evaluation:")
    print(f"    Model A: {resp_a}")
    print(f"    Model B: {resp_b}")
    eval_pairwise = pairwise_grading_eval(query, resp_a, resp_b)
    print(f"    Winner: 🏆 {eval_pairwise['winner']}")
    print(f"    Judge CoT Comparison: {eval_pairwise['reasoning']}")
