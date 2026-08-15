import os

def evaluate_rag_triad(query: str, retrieved_context: str, generated_answer: str) -> dict:
    """
    Evaluasi RAG Triad menggunakan metode LLM-as-a-Judge:
    1. Context Relevance (0 - 10)
    2. Groundedness / Faithfulness (0 - 10)
    3. Answer Relevance (0 - 10)
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
            judge_prompt = f"""Bertindaklah sebagai Evaluator Kualitas RAG. Berikan skor (0-10) untuk 3 kriteria berikut:
1. Context Relevance: Seberapa relevan dokumen konteks dengan query pengguna?
2. Groundedness: Seberapa bebas jawaban dari halusinasi (didasarkan pada konteks)?
3. Answer Relevance: Seberapa tepat jawaban menjawab query?

INPUT:
Query: {query}
Konteks: {retrieved_context}
Jawaban: {generated_answer}

FORMAT BALASAN (Tulis angka skor saja):
Context Relevance: <skor>
Groundedness: <skor>
Answer Relevance: <skor>
"""
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": judge_prompt}],
                temperature=0.0
            )
            print("Hasil Evaluasi LLM-as-a-Judge (API Real):")
            print(resp.choices[0].message.content)
            return {}
        except Exception as e:
            print(f"[WARN] Error API: {e}. Menggunakan simulator evaluasi.")

    # Fallback simulation
    return {
        "Context Relevance": "9.5/10 (Dokumen memuat informasi persis yang dibutuhkan)",
        "Groundedness": "10/10 (Jawaban murni mengekstrak kalimat dari dokumen tanpa asumsi)",
        "Answer Relevance": "9.0/10 (Jawaban menjawab pertanyaan secara komprehensif)"
    }

def main():
    print("=== 01. Evaluasi RAG Triad (LLM-as-a-Judge) ===")

    query = "Berapa lama masa berlaku garansi Laptop AI Pro?"
    context = "Garansi resmi Laptop AI Pro berlaku selama 12 bulan sejak tanggal pembelian tercantum di faktur."
    answer = "Masa berlaku garansi Laptop AI Pro adalah 12 bulan terhitung sejak tanggal pembelian."

    print(f"Query    : '{query}'")
    print(f"Konteks  : '{context}'")
    print(f"Jawaban  : '{answer}'\n")

    scores = evaluate_rag_triad(query, context, answer)

    if scores:
        print("[Hasil Evaluasi RAG Triad Simulator]")
        for kriteria, skor in scores.items():
            print(f"  - {kriteria:<20}: {skor}")

if __name__ == "__main__":
    main()
