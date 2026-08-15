import os
import json

def get_structured_rag_output(query: str, context: str) -> dict:
    """Mengembalikan JSON terstruktur berisi jawaban, ringkasan, confidence score, dan sumber."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
            system_instruction = (
                "Kembalikan jawaban HANYA dalam format JSON valid dengan schema berikut:\n"
                "{\n"
                '  "answer": "string",\n'
                '  "summary": "string",\n'
                '  "confidence_score": 0.0 - 1.0,\n'
                '  "referenced_sources": ["string"]\n'
                "}"
            )
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"Konteks:\n{context}\n\nPertanyaan: {query}"}
                ],
                temperature=0.0
            )
            raw_text = resp.choices[0].message.content.strip()
            # Pembersihan markdown codeblock ```json jika ada
            if raw_text.startswith("```"):
                raw_text = raw_text.split("\n", 1)[1].rsplit("\n", 1)[0]
            return json.loads(raw_text)
        except Exception as e:
            print(f"[WARN] Error API: {e}. Menggunakan JSON fallback.")

    # Fallback simulation
    return {
        "answer": "ChromaDB mendukung penyimpanan vektor, metadata filtering, dan similarity search berbasis distance HNSW.",
        "summary": "Fitur utama ChromaDB untuk sistem RAG.",
        "confidence_score": 0.96,
        "referenced_sources": ["Doc_ChromaDB_Overview.md"]
    }

def main():
    print("=== 03. Structured RAG Output (JSON Schema) ===")

    context = "ChromaDB adalah open-source vector database yang mendukung HNSW index dan metadata filtering."
    query = "Apa fitur utama dari ChromaDB?"

    print(f"Query: '{query}'\n")

    json_result = get_structured_rag_output(query, context)

    print("[Hasil JSON Terstruktur Ter-Parse]")
    print(json.dumps(json_result, indent=2, ensure_ascii=False))

    print(f"\nAkses Properti dalam Kode Python:")
    print(f"  - Jawaban: {json_result.get('answer')}")
    print(f"  - Skor Keyakinan: {json_result.get('confidence_score') * 100}%")

if __name__ == "__main__":
    main()
