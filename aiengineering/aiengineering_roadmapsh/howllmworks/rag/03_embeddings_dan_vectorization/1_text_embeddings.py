import os
import hashlib
import numpy as np

def get_fallback_embedding(text: str, dim: int = 1536) -> list:
    """
    Generator embedding deterministik lokal untuk pengujian tanpa API key.
    Menghasilkan vektor pseudo-random berukuran dim berdasarkan hash teks.
    """
    seed = int(hashlib.sha256(text.encode('utf-8')).hexdigest(), 16) % (2**32)
    np.random.seed(seed)
    vec = np.random.randn(dim)
    norm = np.linalg.norm(vec)
    return (vec / norm).tolist()

def get_text_embedding(text: str) -> list:
    """
    Mengambil embedding teks dari API OpenAI (jika OPENAI_API_KEY diset),
    atau menggunakan generator fallback jika API Key tidak tersedia.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(
                api_key=api_key,
                base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            )
            model = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
            response = client.embeddings.create(input=[text], model=model)
            return response.data[0].embedding
        except Exception as e:
            print(f"[WARN] Gagal memanggil API Embedding: {e}. Menggunakan fallback generator.")
            return get_fallback_embedding(text)
    else:
        print("[INFO] OPENAI_API_KEY tidak ditemukan. Menggunakan fallback embedding generator.")
        return get_fallback_embedding(text)

def main():
    print("=== 01. Text Embeddings Generation ===")

    text1 = "Kecerdasan Buatan (AI) mengubah cara manusia memproses informasi."
    text2 = "Machine Learning dan Deep Learning adalah bagian dari Artificial Intelligence."
    text3 = "Resep membuat kue bolu yang lembut dan manis."

    print(f"\nTeks 1: '{text1}'")
    emb1 = get_text_embedding(text1)
    print(f"Vektor Dimensi: {len(emb1)}")
    print(f"Sample 5 elemen pertama: {emb1[:5]}\n")

    print(f"Teks 2: '{text2}'")
    emb2 = get_text_embedding(text2)

    print(f"Teks 3: '{text3}'")
    emb3 = get_text_embedding(text3)

    # Perhitungan kemiripan sederhana
    vec1 = np.array(emb1)
    vec2 = np.array(emb2)
    vec3 = np.array(emb3)

    sim_1_2 = np.dot(vec1, vec2)
    sim_1_3 = np.dot(vec1, vec3)

    print(f"Cosine Similarity (Teks 1 & Teks 2 - Topik AI): {sim_1_2:.4f}")
    print(f"Cosine Similarity (Teks 1 & Teks 3 - Topik Kuliner): {sim_1_3:.4f}")

if __name__ == "__main__":
    main()
