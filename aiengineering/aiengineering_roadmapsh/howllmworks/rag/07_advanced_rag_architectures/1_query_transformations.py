import os

def generate_multi_queries(original_query: str) -> list:
    """Mengubah 1 query pengguna menjadi beberapa variasi sudut pandang pencarian."""
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key, base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"))
            prompt = f"Hasilkan 3 variasi pertanyaan alternatif dari query ini untuk pencarian dokumen: '{original_query}'. Tulis 1 variasi per baris tanpa nomor."
            resp = client.chat.completions.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            lines = resp.choices[0].message.content.strip().splitlines()
            return [l.strip("- 123456789.") for l in lines if l.strip()]
        except Exception as e:
            print(f"[WARN] Error API: {e}. Menggunakan fallback multi-query simulation.")

    # Fallback simulation
    return [
        f"Bagaimana cara kerja {original_query}?",
        f"Penjelasan lengkap dan contoh penerapan {original_query}.",
        f"Panduan teknis dan keunggulan {original_query}."
    ]

def decompose_sub_queries(complex_query: str) -> list:
    """Memecah query kompleks menjadi sub-query independen."""
    return [
        "Apa perbedaan harga antara Produk A dan Produk B?",
        "Apa perbedaan spesifikasi teknis antara Produk A dan Produk B?"
    ]

def main():
    print("=== 01. Advanced RAG: Query Transformations ===")

    original = "RAG vs Fine-Tuning"

    print(f"Original Query: '{original}'\n")

    print("1. Multi-Query Generation Result:")
    variations = generate_multi_queries(original)
    for i, v in enumerate(variations, 1):
        print(f"  - Variasi #{i}: {v}")

    print("\n2. Sub-Query Decomposition Result:")
    complex_q = "Bandingkan harga dan spesifikasi teknis Produk A vs Produk B"
    print(f"  Complex Query: '{complex_q}'")
    sub_qs = decompose_sub_queries(complex_q)
    for i, sq in enumerate(sub_qs, 1):
        print(f"  - Sub-Query #{i}: {sq}")

if __name__ == "__main__":
    main()
