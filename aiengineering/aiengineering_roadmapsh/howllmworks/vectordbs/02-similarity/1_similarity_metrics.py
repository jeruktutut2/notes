"""
=================================================================
1. SIMILARITY METRICS
=================================================================
Vector Similarity adalah cara mengukur seberapa mirip dua vektor.
Dalam konteks AI, ini berarti mengukur kemiripan makna antara
dua teks yang sudah dikonversi menjadi embedding.

Jenis-Jenis Similarity Metrics:
┌──────────────────────┬───────────┬──────────────────────────┐
│ Metric               │ Range     │ Semakin Mirip →          │
├──────────────────────┼───────────┼──────────────────────────┤
│ Cosine Similarity    │ [-1, 1]   │ Mendekati 1              │
│ Euclidean Distance   │ [0, ∞)    │ Mendekati 0              │
│ Dot Product          │ (-∞, ∞)   │ Semakin besar            │
│ Manhattan Distance   │ [0, ∞)    │ Mendekati 0              │
└──────────────────────┴───────────┴──────────────────────────┘
=================================================================
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import time


def cosine_similarity(a, b):
    """Menghitung cosine similarity antara dua vektor."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def euclidean_distance(a, b):
    """Menghitung Euclidean distance (L2) antara dua vektor."""
    return np.sqrt(np.sum((a - b) ** 2))


def dot_product(a, b):
    """Menghitung dot product antara dua vektor."""
    return np.dot(a, b)


def manhattan_distance(a, b):
    """Menghitung Manhattan distance (L1) antara dua vektor."""
    return np.sum(np.abs(a - b))


def demo_similarity_metrics():
    """Demo: membandingkan berbagai similarity metrics."""
    print("=" * 60)
    print("DEMO 1: Perbandingan Similarity Metrics")
    print("=" * 60)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    kalimat = [
        "Kucing adalah hewan peliharaan yang lucu",       # [0]
        "Anjing juga merupakan hewan peliharaan populer",  # [1] mirip [0]
        "Python digunakan untuk machine learning",         # [2] berbeda
    ]

    print(f"\n📝 Kalimat:")
    for i, k in enumerate(kalimat):
        print(f"   [{i}] {k}")

    embeddings = model.encode(kalimat, show_progress_bar=False)

    # Bandingkan setiap pasangan dengan semua metrics
    print(f"\n📊 Hasil Semua Metrics:")
    print("-" * 75)
    print(f"   {'Pasangan':<12} {'Cosine':>10} {'Euclidean':>12} {'Dot Product':>13} {'Manhattan':>12}")
    print("-" * 75)

    for i in range(len(kalimat)):
        for j in range(i + 1, len(kalimat)):
            cos = cosine_similarity(embeddings[i], embeddings[j])
            euc = euclidean_distance(embeddings[i], embeddings[j])
            dot = dot_product(embeddings[i], embeddings[j])
            man = manhattan_distance(embeddings[i], embeddings[j])

            print(f"   [{i}] vs [{j}]   {cos:>10.4f} {euc:>12.4f} {dot:>13.4f} {man:>12.4f}")

    print("\n💡 Kesimpulan:")
    print("   - Cosine: paling populer untuk NLP, mengukur arah vektor")
    print("   - Euclidean: mengukur jarak absolut, dipengaruhi magnitude")
    print("   - Dot Product: cepat, setara cosine jika vektor dinormalisasi")
    print("   - Manhattan: alternatif Euclidean, kurang umum untuk embedding")


def demo_semantic_search():
    """Demo: semantic search sederhana menggunakan cosine similarity."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Semantic Search Sederhana")
    print("=" * 60)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Database dokumen
    dokumen = [
        "Python adalah bahasa pemrograman populer untuk data science",
        "Machine learning menggunakan data untuk membuat prediksi",
        "Kucing dan anjing adalah hewan peliharaan yang populer",
        "Deep learning adalah subset dari machine learning",
        "Resep nasi goreng kampung yang lezat dan mudah",
        "Neural network terinspirasi dari cara kerja otak manusia",
        "Cara merawat tanaman hias di dalam rumah",
        "TensorFlow dan PyTorch adalah framework deep learning",
    ]

    print(f"\n📚 Database: {len(dokumen)} dokumen")
    for i, d in enumerate(dokumen):
        print(f"   [{i}] {d}")

    # Buat embedding untuk semua dokumen
    doc_embeddings = model.encode(dokumen, show_progress_bar=False)

    # Query
    queries = [
        "bagaimana cara belajar AI?",
        "hewan peliharaan apa yang bagus?",
        "framework apa untuk deep learning?",
    ]

    for query in queries:
        print(f"\n🔍 Query: \"{query}\"")
        print("-" * 60)

        query_embedding = model.encode([query], show_progress_bar=False)[0]

        # Hitung similarity dengan semua dokumen
        scores = []
        for i, doc_emb in enumerate(doc_embeddings):
            sim = cosine_similarity(query_embedding, doc_emb)
            scores.append((i, sim))

        # Urutkan berdasarkan similarity (tertinggi dulu)
        scores.sort(key=lambda x: x[1], reverse=True)

        # Tampilkan top-3
        print("   Top-3 hasil:")
        for rank, (idx, sim) in enumerate(scores[:3], 1):
            emoji = "✅" if sim > 0.3 else "⚠️"
            print(f"   {rank}. {emoji} [{sim:.4f}] {dokumen[idx]}")

    print("\n💡 Kesimpulan:")
    print("   - Semantic search menemukan dokumen berdasarkan MAKNA, bukan kata kunci")
    print("   - 'belajar AI' cocok dengan 'machine learning', 'neural network', dll.")
    print("   - Ini jauh lebih powerful daripada pencarian keyword biasa!")


def demo_threshold_filtering():
    """Demo: menggunakan threshold untuk memfilter hasil yang tidak relevan."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Threshold Filtering")
    print("=" * 60)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    dokumen = [
        "Python untuk data science dan machine learning",
        "JavaScript untuk web development",
        "Resep masakan padang yang enak",
        "Cara bermain gitar untuk pemula",
        "Deep learning dengan PyTorch",
    ]

    doc_embeddings = model.encode(dokumen, show_progress_bar=False)

    query = "belajar programming"
    query_embedding = model.encode([query], show_progress_bar=False)[0]

    THRESHOLD = 0.3
    print(f"\n🔍 Query: \"{query}\"")
    print(f"📏 Threshold: {THRESHOLD}")
    print("-" * 60)

    for i, doc_emb in enumerate(doc_embeddings):
        sim = cosine_similarity(query_embedding, doc_emb)
        if sim >= THRESHOLD:
            print(f"   ✅ [{sim:.4f}] {dokumen[i]}")
        else:
            print(f"   ❌ [{sim:.4f}] {dokumen[i]}  ← di bawah threshold")

    print(f"\n💡 Kesimpulan:")
    print(f"   - Threshold {THRESHOLD} memfilter hasil yang tidak relevan")
    print("   - Terlalu tinggi → banyak hasil terlewat (false negative)")
    print("   - Terlalu rendah → banyak hasil tidak relevan (false positive)")
    print("   - Nilai 0.3-0.5 biasanya cocok untuk kebanyakan kasus")


def main():
    demo_similarity_metrics()
    demo_semantic_search()
    demo_threshold_filtering()
    print("\n\n✅ Selesai! Lanjut ke: 2_nearest_neighbor_search.py")


if __name__ == "__main__":
    main()
