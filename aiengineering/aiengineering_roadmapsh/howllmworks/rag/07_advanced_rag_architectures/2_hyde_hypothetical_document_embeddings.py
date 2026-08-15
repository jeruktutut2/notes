import os

def generate_hypothetical_document(query: str) -> str:
    """
    HyDE Step 1: Meminta LLM menghasilkan dokumen / jawaban hipotetis ideal untuk query pengguna.
    Jawaban hipotetis ini tidak harus 100% fakta, tetapi strukturnya mencerminkan dokumen target di Vector DB.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
            prompt = f"Tuliskan paragraf sampel dokumen teknis hipotetis yang menjawab pertanyaan berikut secara ideal: '{query}'."
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.5
            )
            return resp.choices[0].message.content.strip()
        except Exception as e:
            print(f"[WARN] Error API: {e}. Menggunakan fallback HyDE document generator.")

    # Fallback simulation
    return (
        f"Dokumen Hipotetis: Untuk menyelesaikan permasalahan {query}, langkah utama yang harus diambil "
        "adalah mengonfigurasi parameter timeout pada koneksi database dan memeriksa log error server."
    )

def main():
    print("=== 02. Advanced RAG: HyDE (Hypothetical Document Embeddings) ===")

    user_query = "Bagaimana mengatasi error HTTP 504 Gateway Timeout pada API RAG?"

    print(f"User Query: '{user_query}'\n")

    print("[Tahap 1 HyDE] Membikin Dokumen Hipotetis via LLM...")
    hypo_doc = generate_hypothetical_document(user_query)
    print(f"Hasil Dokumen Hipotetis:\n\"{hypo_doc}\"\n")

    print("[Tahap 2 HyDE] Vector Embedding & Retrieval:")
    print("  - Vektor dibuat dari Dokumen Hipotetis di atas (BUKAN dari query pendek asli).")
    print("  - Vektor dokumen hipotetis di-match kan dengan Vector Database nyata.")
    print("  - Keunggulan: Teks dokumen hipotetis jauh lebih kaya makna semantik dibanding query pendek 5 kata!")

if __name__ == "__main__":
    main()
