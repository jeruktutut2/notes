"""
=================================================================
1. INDEXING & OPTIMIZATION
=================================================================
Teknik-teknik optimasi untuk mempercepat dan meningkatkan kualitas
pencarian di vector database.

Topik:
1. Hybrid Search (Vector + Keyword)
2. Reranking (Cross-Encoder)
3. Metadata Filtering lanjutan
4. Caching untuk query berulang

┌──────────────────┬──────────────────────────────────────────┐
│ Teknik           │ Kapan Digunakan                          │
├──────────────────┼──────────────────────────────────────────┤
│ Hybrid Search    │ Saat keyword penting (nama, kode, dll)   │
│ Reranking        │ Meningkatkan akurasi top-K results       │
│ Metadata Filter  │ Multi-tenant, multi-category data        │
│ Caching          │ Query berulang, mengurangi latensi        │
└──────────────────┴──────────────────────────────────────────┘
=================================================================
"""

import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np
import time
import hashlib


# Dataset untuk demo
DOCUMENTS = [
    "Python 3.12 memperkenalkan fitur type parameter syntax baru",
    "JavaScript ES2024 menambahkan Array.groupBy dan Temporal API",
    "Rust memiliki ownership system yang menjamin memory safety",
    "Go atau Golang dikembangkan oleh Google untuk concurrency",
    "TypeScript adalah superset dari JavaScript dengan static typing",
    "Java Spring Boot digunakan untuk membuat microservices",
    "Docker container mengisolasi aplikasi dari environment host",
    "Kubernetes (K8s) mengatur orkestrasi container secara otomatis",
    "PostgreSQL mendukung JSON, full-text search, dan vector search",
    "Redis adalah in-memory database untuk caching dan pub/sub",
    "FastAPI adalah web framework Python yang sangat cepat",
    "React adalah library JavaScript untuk membangun user interface",
    "PyTorch digunakan untuk deep learning dan neural network",
    "scikit-learn menyediakan algoritma machine learning klasik",
    "Pandas digunakan untuk manipulasi dan analisis data tabular",
]

CATEGORIES = [
    "python", "javascript", "rust", "go", "typescript",
    "java", "devops", "devops", "database", "database",
    "python", "javascript", "ai", "ai", "python",
]


def demo_hybrid_search():
    """Demo: Hybrid Search (Vector + Keyword / BM25)."""
    print("=" * 60)
    print("DEMO 1: Hybrid Search (Vector + Keyword)")
    print("=" * 60)

    model = SentenceTransformer("all-MiniLM-L6-v2")
    doc_embeddings = model.encode(DOCUMENTS, show_progress_bar=False)

    def keyword_score(query, document):
        """Skor keyword sederhana: berapa kata query yang ada di dokumen."""
        query_words = set(query.lower().split())
        doc_words = set(document.lower().split())
        if not query_words:
            return 0
        return len(query_words & doc_words) / len(query_words)

    def hybrid_search(query, alpha=0.5, top_k=5):
        """Hybrid search: alpha * vector + (1-alpha) * keyword."""
        # Vector search
        query_emb = model.encode([query], show_progress_bar=False)[0]
        vector_scores = np.array([
            np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
            for doc_emb in doc_embeddings
        ])

        # Keyword search
        kw_scores = np.array([keyword_score(query, doc) for doc in DOCUMENTS])

        # Normalisasi
        if vector_scores.max() > vector_scores.min():
            v_norm = (vector_scores - vector_scores.min()) / (vector_scores.max() - vector_scores.min())
        else:
            v_norm = vector_scores
        
        if kw_scores.max() > kw_scores.min():
            k_norm = (kw_scores - kw_scores.min()) / (kw_scores.max() - kw_scores.min())
        else:
            k_norm = kw_scores

        # Gabungkan
        hybrid = alpha * v_norm + (1 - alpha) * k_norm
        top_idx = np.argsort(hybrid)[-top_k:][::-1]

        return [(i, hybrid[i], v_norm[i], k_norm[i]) for i in top_idx]

    # Test query: kata kunci spesifik (keyword penting)
    query = "Python FastAPI web framework"
    print(f"\n🔍 Query: \"{query}\"")
    print(f"\n📊 Perbandingan alpha (0=keyword only, 1=vector only):")
    print("-" * 75)

    for alpha in [0.0, 0.3, 0.5, 0.7, 1.0]:
        results = hybrid_search(query, alpha=alpha, top_k=3)
        print(f"\n   Alpha={alpha:.1f}:")
        for idx, score, v_score, k_score in results:
            print(f"     [{score:.3f}] (v:{v_score:.3f} k:{k_score:.3f}) {DOCUMENTS[idx][:55]}")

    print(f"\n💡 Kesimpulan:")
    print("   - alpha=0 → hanya keyword match (nama bahasa, framework exact)")
    print("   - alpha=1 → hanya vector/semantic (makna)")
    print("   - alpha=0.5 → balance → biasanya hasil terbaik")
    print("   - Jika query mengandung nama spesifik, turunkan alpha")


def demo_reranking():
    """Demo: Reranking menggunakan cross-encoder."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Reranking (Cross-Encoder)")
    print("=" * 60)

    print("\n📌 Konsep Reranking:")
    print("   1. Bi-encoder: encode query & doc TERPISAH → cepat tapi kurang akurat")
    print("   2. Cross-encoder: encode query + doc BERSAMAAN → lambat tapi lebih akurat")
    print("   3. Strategi: retrieve top-20 dengan bi-encoder, rerank ke top-5 dengan cross-encoder")

    try:
        from sentence_transformers import CrossEncoder

        bi_encoder = SentenceTransformer("all-MiniLM-L6-v2")
        cross_encoder = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

        query = "framework untuk membuat API di Python"
        print(f"\n🔍 Query: \"{query}\"")

        # Step 1: Bi-encoder retrieve top-10
        query_emb = bi_encoder.encode([query], show_progress_bar=False)[0]
        scores = [
            np.dot(query_emb, bi_encoder.encode([doc], show_progress_bar=False)[0])
            / (np.linalg.norm(query_emb) * np.linalg.norm(bi_encoder.encode([doc], show_progress_bar=False)[0]))
            for doc in DOCUMENTS
        ]
        bi_top10 = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:10]

        print(f"\n📊 Step 1: Bi-encoder Top-10")
        print("-" * 60)
        for rank, (idx, score) in enumerate(bi_top10, 1):
            print(f"   {rank:>2}. [{score:.4f}] {DOCUMENTS[idx][:55]}")

        # Step 2: Cross-encoder rerank
        pairs = [[query, DOCUMENTS[idx]] for idx, _ in bi_top10]
        ce_scores = cross_encoder.predict(pairs)
        
        reranked = sorted(
            zip([idx for idx, _ in bi_top10], ce_scores),
            key=lambda x: x[1], reverse=True
        )

        print(f"\n📊 Step 2: Cross-encoder Reranked Top-5")
        print("-" * 60)
        for rank, (idx, score) in enumerate(reranked[:5], 1):
            # Cari rank asli di bi-encoder
            bi_rank = [r for r, (i, _) in enumerate(bi_top10, 1) if i == idx][0]
            change = f"(was #{bi_rank})" if bi_rank != rank else "(same)"
            print(f"   {rank:>2}. [{score:.4f}] {DOCUMENTS[idx][:50]} {change}")

        print(f"\n💡 Kesimpulan:")
        print("   - Cross-encoder bisa mengubah ranking dari bi-encoder")
        print("   - Hasil reranking biasanya lebih relevan")
        print("   - Trade-off: cross-encoder ~100x lebih lambat dari bi-encoder")

    except Exception as e:
        print(f"\n⚠️ Cross-encoder tidak tersedia: {e}")
        print("   Install dengan: pip install sentence-transformers")
        print("\n   Penjelasan konsep:")
        print("   - Bi-encoder: query & doc di-encode terpisah, bandingkan vektor")
        print("   - Cross-encoder: query + doc di-encode bersamaan, lebih akurat")
        print("   - Pipeline: retrieve banyak (bi-encoder) → rerank sedikit (cross-encoder)")


def demo_caching():
    """Demo: Query caching untuk mengurangi latensi."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Query Caching")
    print("=" * 60)

    # Setup ChromaDB
    client = chromadb.Client()
    collection = client.create_collection(name="cache_demo")
    collection.add(
        documents=DOCUMENTS,
        metadatas=[{"kategori": c} for c in CATEGORIES],
        ids=[f"doc_{i}" for i in range(len(DOCUMENTS))]
    )

    # Simple cache
    query_cache = {}

    def search_with_cache(query, n_results=3):
        """Search dengan caching."""
        cache_key = hashlib.md5(query.encode()).hexdigest()

        if cache_key in query_cache:
            return query_cache[cache_key], True  # cache hit

        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "distances"]
        )
        query_cache[cache_key] = results
        return results, False  # cache miss

    # Simulasi query berulang
    queries = [
        "machine learning Python",
        "web framework",
        "machine learning Python",   # duplikat
        "database caching",
        "web framework",              # duplikat
        "machine learning Python",   # duplikat lagi
    ]

    print(f"\n📝 Menjalankan {len(queries)} query (ada duplikat):")
    print("-" * 60)

    total_hits = 0
    for i, query in enumerate(queries, 1):
        start = time.time()
        results, is_cached = search_with_cache(query)
        elapsed = (time.time() - start) * 1000

        status = "🟢 CACHE HIT" if is_cached else "🔴 CACHE MISS"
        if is_cached:
            total_hits += 1
        print(f"   {i}. [{elapsed:>6.2f}ms] {status} \"{query}\"")

    print(f"\n📊 Statistik Cache:")
    print(f"   Total queries : {len(queries)}")
    print(f"   Cache hits    : {total_hits}")
    print(f"   Cache misses  : {len(queries) - total_hits}")
    print(f"   Hit rate      : {total_hits/len(queries):.0%}")
    print(f"   Cache entries : {len(query_cache)}")

    print(f"\n💡 Kesimpulan:")
    print("   - Cache menghindari komputasi ulang untuk query yang sama")
    print("   - Sangat efektif jika banyak user bertanya hal serupa")
    print("   - Di produksi, gunakan Redis atau TTL-based cache")


def demo_metadata_advanced():
    """Demo: Advanced metadata filtering."""
    print("\n\n" + "=" * 60)
    print("DEMO 4: Advanced Metadata Filtering")
    print("=" * 60)

    client = chromadb.Client()
    collection = client.create_collection(name="filter_demo")
    collection.add(
        documents=DOCUMENTS,
        metadatas=[{"kategori": c, "index": i} for i, c in enumerate(CATEGORIES)],
        ids=[f"doc_{i}" for i in range(len(DOCUMENTS))]
    )

    queries_filters = [
        ("teknologi terbaru", None, "Tanpa filter"),
        ("teknologi terbaru", {"kategori": "python"}, "Hanya Python"),
        ("teknologi terbaru", {"kategori": "ai"}, "Hanya AI"),
        ("teknologi terbaru", {"kategori": {"$in": ["python", "ai"]}}, "Python ATAU AI"),
    ]

    for query, where_filter, label in queries_filters:
        print(f"\n🔍 Query: \"{query}\" — Filter: {label}")
        print("-" * 60)

        kwargs = {"query_texts": [query], "n_results": 3}
        if where_filter:
            kwargs["where"] = where_filter

        results = collection.query(**kwargs)
        for i, (doc, meta, dist) in enumerate(
            zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), 1
        ):
            sim = 1 - dist
            print(f"   {i}. [{sim:.4f}] [{meta['kategori']}] {doc[:55]}")

    print(f"\n💡 Operator filter ChromaDB:")
    print("   $eq  → sama dengan           $ne  → tidak sama dengan")
    print("   $gt  → lebih besar dari       $gte → lebih besar atau sama")
    print("   $lt  → lebih kecil dari       $lte → lebih kecil atau sama")
    print("   $in  → salah satu dari list   $nin → bukan salah satu dari list")
    print("   $and → semua kondisi          $or  → salah satu kondisi")


def main():
    demo_hybrid_search()
    demo_reranking()
    demo_caching()
    demo_metadata_advanced()
    print("\n\n" + "=" * 60)
    print("🎉 SELESAI! Semua modul Vector Database telah dipelajari!")
    print("=" * 60)
    print("\nRingkasan yang telah dipelajari:")
    print("   01. Embeddings — mengubah teks menjadi vektor")
    print("   02. Similarity Search — mengukur kemiripan vektor")
    print("   03. Vector Databases — ChromaDB, FAISS, dll")
    print("   04. Chunking — memecah dokumen untuk embedding")
    print("   05. RAG Pipeline — retrieval + generation")
    print("   06. Optimization — hybrid search, reranking, caching")


if __name__ == "__main__":
    main()
