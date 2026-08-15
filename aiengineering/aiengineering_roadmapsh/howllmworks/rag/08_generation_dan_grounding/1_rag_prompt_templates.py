import os

RAG_SYSTEM_PROMPT = """Anda adalah asisten AI teknis yang jujur dan akurat.
Tugas Anda adalah menjawab pertanyaan pengguna HANYA berdasarkan konteks dokumen yang diberikan di bawah ini.

ATURAN KETAT:
1. Jika informasi untuk menjawab pertanyaan TIDAK ADA di dalam konteks, Anda HARUS menjawab secara eksplisit: "Maaf, informasi tidak ditemukan dalam dokumen referensi."
2. JANGAN MEMBUAT-BUAT FAKTA atau menggunakan pengetahuan di luar konteks (Anti-Hallucination).
3. Buat jawaban singkat, padat, dan langsung pada inti pertanyaan.
"""

def generate_rag_response(query: str, contexts: list) -> str:
    formatted_context = "\n\n".join([f"[Dokumen {i+1}]: {ctx}" for i, ctx in enumerate(contexts)])
    user_message = f"KONTEKS DOKUMEN:\n{formatted_context}\n\nPERTANYAAN PENGGUNA:\n{query}"

    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": RAG_SYSTEM_PROMPT},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.0 # Deterministic grounding
            )
            return resp.choices[0].message.content
        except Exception as e:
            print(f"[WARN] Error API: {e}. Menggunakan fallback simulator.")

    # Fallback simulation
    if "kuota" in query.lower() or "garansi" in query.lower():
        return "[Simulasi LLM] Berdasarkan Dokumen 1, garansi produk berlaku selama 12 bulan sejak tanggal pembelian."
    else:
        return "[Simulasi LLM] Maaf, informasi tidak ditemukan dalam dokumen referensi."

def main():
    print("=== 01. Anti-Hallucination RAG Prompting ===")

    contexts = [
        "Garansi produk Laptop AI Pro berlaku selama 12 bulan untuk perbaikan perangkat keras.",
        "Pusat layanan purna jual resmi berlokasi di Jakarta dan Surabaya."
    ]

    # Kasus 1: Pertanyaan didukung konteks
    query1 = "Berapa lama masa garansi Laptop AI Pro?"
    print(f"\nPertanyaan 1: '{query1}'")
    answer1 = generate_rag_response(query1, contexts)
    print(f"Jawaban LLM:\n{answer1}")

    # Kasus 2: Pertanyaan TIDAK didukung konteks (Menguji anti-halusinasi)
    query2 = "Berapa harga tiket pesawat ke Bali saat ini?"
    print(f"\nPertanyaan 2 (Diluar konteks): '{query2}'")
    answer2 = generate_rag_response(query2, contexts)
    print(f"Jawaban LLM:\n{answer2}")

if __name__ == "__main__":
    main()
