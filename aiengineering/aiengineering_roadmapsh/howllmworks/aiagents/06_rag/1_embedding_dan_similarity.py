import numpy as np

def main():
    print("=== 6.1 Embedding dan Cosine Similarity ===\n")
    print("Script ini TIDAK membutuhkan API key.\n")

    # ---------------------------------------------------------------
    # APA ITU EMBEDDING?
    # Embedding = representasi teks sebagai vektor angka (array).
    # Teks yang mirip maknanya → vektor yang berdekatan.
    # Teks yang berbeda maknanya → vektor yang berjauhan.
    #
    # Digunakan untuk: pencarian semantik, RAG, clustering, dll.
    # ---------------------------------------------------------------

    # 1. KONSEP EMBEDDING (Visualisasi Sederhana)
    print("=" * 60)
    print("1. KONSEP EMBEDDING - Teks Menjadi Angka")
    print("=" * 60)

    # Contoh embedding manual (dimensi 3 untuk visualisasi)
    # Di dunia nyata, embedding punya 768-3072 dimensi
    embeddings_manual = {
        "kucing":    np.array([0.9, 0.1, 0.2]),
        "anjing":    np.array([0.8, 0.15, 0.25]),
        "mobil":     np.array([0.1, 0.9, 0.3]),
        "motor":     np.array([0.15, 0.85, 0.35]),
        "python":    np.array([0.2, 0.3, 0.9]),
        "javascript":np.array([0.25, 0.28, 0.88]),
    }

    print("\nContoh embedding (3 dimensi):")
    for kata, vec in embeddings_manual.items():
        print(f"  '{kata}' → {vec}")

    # 2. COSINE SIMILARITY
    print(f"\n{'='*60}")
    print("2. COSINE SIMILARITY - Mengukur Kemiripan")
    print(f"{'='*60}")

    def cosine_similarity(a, b):
        """Menghitung cosine similarity antara dua vektor."""
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    print("\nPerbandingan kemiripan:")
    pasangan = [
        ("kucing", "anjing"),     # Mirip (sama-sama hewan)
        ("kucing", "mobil"),      # Beda (hewan vs kendaraan)
        ("mobil", "motor"),       # Mirip (sama-sama kendaraan)
        ("python", "javascript"), # Mirip (sama-sama bahasa pemrograman)
        ("kucing", "python"),     # Beda
    ]

    for kata1, kata2 in pasangan:
        sim = cosine_similarity(embeddings_manual[kata1], embeddings_manual[kata2])
        bar = "█" * int(sim * 30)
        print(f"  {kata1:12} ↔ {kata2:12} : {sim:.4f} {bar}")

    # 3. SEMANTIC SEARCH (Pencarian Berdasarkan Makna)
    print(f"\n{'='*60}")
    print("3. SEMANTIC SEARCH - Pencarian Berdasarkan Makna")
    print(f"{'='*60}")

    # Simulasi dokumen dan embedding-nya
    # Menggunakan hash-based pseudo-embedding untuk demo
    def pseudo_embedding(text, dim=64):
        """Pseudo-embedding berdasarkan hash (untuk demo saja)."""
        np.random.seed(hash(text.lower().strip()) % (2**31))
        vec = np.random.randn(dim).astype(np.float32)
        return vec / (np.linalg.norm(vec) + 1e-8)

    dokumen = [
        "Python adalah bahasa pemrograman yang populer untuk AI dan machine learning",
        "Nasi goreng adalah makanan khas Indonesia yang dibuat dari nasi yang digoreng",
        "Machine learning adalah subset dari artificial intelligence",
        "Rendang adalah masakan daging yang kaya rempah dari Minangkabau",
        "TensorFlow dan PyTorch adalah framework deep learning populer",
        "Sate ayam biasanya disajikan dengan bumbu kacang dan lontong",
        "Neural network terinspirasi dari cara kerja otak manusia",
        "Gado-gado adalah salad sayuran Indonesia dengan saus kacang",
    ]

    # Buat embedding untuk semua dokumen
    doc_embeddings = [pseudo_embedding(doc) for doc in dokumen]

    # Fungsi search
    def search(query, top_k=3):
        query_emb = pseudo_embedding(query)
        similarities = []
        for i, doc_emb in enumerate(doc_embeddings):
            sim = cosine_similarity(query_emb, doc_emb)
            similarities.append((i, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]

    queries = [
        "framework untuk deep learning",
        "makanan tradisional Indonesia",
        "belajar artificial intelligence",
    ]

    for query in queries:
        print(f"\n  🔍 Query: '{query}'")
        results = search(query, top_k=3)
        for rank, (idx, sim) in enumerate(results, 1):
            print(f"     [{rank}] (sim={sim:.4f}) {dokumen[idx]}")

    # 4. PERBANDINGAN: Keyword vs Semantic Search
    print(f"\n{'='*60}")
    print("4. KEYWORD vs SEMANTIC SEARCH")
    print(f"{'='*60}")

    print("""
    Keyword Search (Tradisional):
    - Mencari kecocokan kata persis
    - "deep learning" → hanya match dokumen yang mengandung "deep learning"
    - Cepat tapi tidak paham sinonim/konteks

    Semantic Search (Embedding):
    - Mencari kecocokan MAKNA
    - "belajar AI" → match "machine learning", "neural network", dll.
    - Paham sinonim dan konteks
    - Membutuhkan model embedding

    Di Produksi, gunakan model embedding seperti:
    - OpenAI: text-embedding-3-small (1536 dim) / text-embedding-3-large (3072 dim)
    - Open Source: sentence-transformers/all-MiniLM-L6-v2 (384 dim)
    - Google: text-embedding-004
    """)

    print("✅ Selesai! Memahami embedding dan similarity search.")
    print("\nRingkasan:")
    print("- Embedding mengubah teks menjadi vektor angka")
    print("- Cosine similarity mengukur kemiripan antara dua vektor (0-1)")
    print("- Semantic search menemukan dokumen berdasarkan MAKNA, bukan keyword")
    print("- Ini adalah fondasi untuk RAG (Retrieval-Augmented Generation)")

if __name__ == "__main__":
    main()
