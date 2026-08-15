# 06 - Indexing & Optimization

## Apa itu Indexing?

Indexing adalah cara **mengorganisir vektor** dalam database agar pencarian (similarity search) bisa dilakukan dengan **cepat dan efisien**. Tanpa indexing, setiap query harus membandingkan dengan semua vektor satu per satu (brute force) — sangat lambat untuk jutaan vektor.

```
Tanpa Index (Brute Force):
  Query → bandingkan dengan SEMUA 1.000.000 vektor → lambat ⏳

Dengan Index (HNSW):
  Query → navigasi graph → cek ~1.000 vektor → cepat ⚡
```

---

## Algoritma Indexing

### 1. Flat (Brute Force)

Membandingkan query dengan **semua vektor**. Akurasi 100% tapi paling lambat.

| Aspek | Detail |
|-------|--------|
| **Akurasi** | 100% (exact) |
| **Kecepatan** | O(n) — lambat |
| **Memori** | Tinggi |
| **Cocok untuk** | Dataset kecil (<10K vektor) |

```python
import faiss
import numpy as np

d = 384  # dimensi
data = np.random.rand(10000, d).astype('float32')

# Flat index (L2 distance)
index = faiss.IndexFlatL2(d)
index.add(data)

# Search
query = np.random.rand(1, d).astype('float32')
D, I = index.search(query, k=5)  # top-5
```

### 2. IVF (Inverted File Index)

Membagi vektor ke dalam **cluster** (voronoi cells). Saat search, hanya cluster terdekat yang dicek.

| Aspek | Detail |
|-------|--------|
| **Akurasi** | ~95-99% (approximate) |
| **Kecepatan** | O(n/nlist × nprobe) — jauh lebih cepat |
| **Memori** | Sedang |
| **Cocok untuk** | Dataset menengah (10K-1M vektor) |

```python
nlist = 100  # jumlah cluster
quantizer = faiss.IndexFlatL2(d)
index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist)

# HARUS di-train dulu
index_ivf.train(data)
index_ivf.add(data)

# nprobe = jumlah cluster yang dicek (trade-off kecepatan vs akurasi)
index_ivf.nprobe = 10  # default 1
D, I = index_ivf.search(query, k=5)
```

**Tuning nprobe:**
| nprobe | Kecepatan | Akurasi |
|--------|-----------|---------|
| 1 | Sangat cepat | Rendah |
| 10 | Cepat | Baik |
| 50 | Sedang | Sangat baik |
| nlist | Lambat (=brute force) | 100% |

### 3. HNSW (Hierarchical Navigable Small World)

Membangun **graph berlapis** dimana setiap vektor terhubung dengan tetangga terdekatnya. Navigasi dimulai dari layer atas (sparse) ke bawah (dense).

| Aspek | Detail |
|-------|--------|
| **Akurasi** | ~98-99.9% |
| **Kecepatan** | O(log n) — sangat cepat |
| **Memori** | Tinggi (menyimpan graph) |
| **Cocok untuk** | Produksi, real-time search |

```python
# HNSW di FAISS
M = 32       # jumlah koneksi per node
ef = 200     # ukuran candidate list saat konstruksi

index_hnsw = faiss.IndexHNSWFlat(d, M)
index_hnsw.hnsw.efConstruction = ef  # saat build
index_hnsw.hnsw.efSearch = 64        # saat search (trade-off)

index_hnsw.add(data)
D, I = index_hnsw.search(query, k=5)
```

**Tuning HNSW:**
| Parameter | Efek naik | Trade-off |
|-----------|-----------|-----------|
| **M** | Akurasi naik | Memori naik |
| **efConstruction** | Akurasi naik | Build time naik |
| **efSearch** | Akurasi naik | Search time naik |

### 4. PQ (Product Quantization)

**Kompresi vektor** menjadi kode yang lebih kecil. Mengurangi penggunaan memori secara drastis.

| Aspek | Detail |
|-------|--------|
| **Akurasi** | ~90-95% |
| **Kecepatan** | Cepat |
| **Memori** | Sangat rendah |
| **Cocok untuk** | Dataset sangat besar (>10M vektor), memori terbatas |

```python
m = 8         # jumlah sub-quantizer
nbits = 8     # bits per sub-quantizer

index_pq = faiss.IndexPQ(d, m, nbits)
index_pq.train(data)
index_pq.add(data)

D, I = index_pq.search(query, k=5)
```

### 5. IVF + PQ (Kombinasi)

Menggabungkan clustering (IVF) dan kompresi (PQ) untuk dataset sangat besar.

```python
nlist = 100
m = 8
nbits = 8

quantizer = faiss.IndexFlatL2(d)
index_ivfpq = faiss.IndexIVFPQ(quantizer, d, nlist, m, nbits)
index_ivfpq.train(data)
index_ivfpq.add(data)
index_ivfpq.nprobe = 10

D, I = index_ivfpq.search(query, k=5)
```

---

## Perbandingan Algoritma

| Algoritma | Akurasi | Kecepatan Search | Memori | Build Time |
|-----------|---------|-----------------|--------|------------|
| **Flat** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **IVF** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **HNSW** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| **PQ** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **IVF+PQ** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐ |

---

## Teknik Optimasi

### 1. Hybrid Search (Vector + Keyword)

Menggabungkan **semantic search** (vector) dengan **keyword search** (BM25/full-text) untuk hasil yang lebih baik.

```python
# Contoh: Weaviate hybrid search
# Alpha = 0 → keyword only, Alpha = 1 → vector only
# Alpha = 0.5 → balanced

# Konsep hybrid search sederhana
from rank_bm25 import BM25Okapi
import numpy as np

def hybrid_search(query, documents, doc_embeddings, model, alpha=0.5, k=5):
    """Gabungkan vector search dan keyword search."""
    
    # --- Vector Search ---
    query_embedding = model.encode([query])
    from sklearn.metrics.pairwise import cosine_similarity
    vector_scores = cosine_similarity(query_embedding, doc_embeddings)[0]
    
    # Normalisasi ke [0, 1]
    vector_scores = (vector_scores - vector_scores.min()) / (
        vector_scores.max() - vector_scores.min() + 1e-8
    )
    
    # --- Keyword Search (BM25) ---
    tokenized_docs = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    keyword_scores = bm25.get_scores(query.lower().split())
    
    # Normalisasi ke [0, 1]
    keyword_scores = (keyword_scores - keyword_scores.min()) / (
        keyword_scores.max() - keyword_scores.min() + 1e-8
    )
    
    # --- Kombinasi ---
    hybrid_scores = alpha * vector_scores + (1 - alpha) * keyword_scores
    
    # Top-k
    top_indices = np.argsort(hybrid_scores)[-k:][::-1]
    
    results = []
    for idx in top_indices:
        results.append({
            "document": documents[idx],
            "hybrid_score": hybrid_scores[idx],
            "vector_score": vector_scores[idx],
            "keyword_score": keyword_scores[idx]
        })
    
    return results
```

### 2. Reranking

Setelah retrieval awal, gunakan **cross-encoder** untuk mereranking hasil agar lebih akurat.

```python
from sentence_transformers import CrossEncoder

# Cross-encoder (lebih akurat dari bi-encoder, tapi lebih lambat)
reranker = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def rerank(query, documents, top_k=5):
    """Rerank dokumen menggunakan cross-encoder."""
    # Buat pasangan [query, document]
    pairs = [[query, doc] for doc in documents]
    
    # Score setiap pasangan
    scores = reranker.predict(pairs)
    
    # Sort berdasarkan score
    ranked = sorted(
        zip(documents, scores), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    return ranked[:top_k]

# Contoh penggunaan dalam pipeline RAG:
# 1. Retrieve top-20 dari vector DB
# 2. Rerank menjadi top-5 dengan cross-encoder
# 3. Kirim top-5 ke LLM
```

### 3. Metadata Filtering

Filter hasil berdasarkan metadata **sebelum** atau **bersamaan** dengan vector search.

```python
# ChromaDB filtering
results = collection.query(
    query_texts=["machine learning"],
    n_results=5,
    where={
        "$and": [
            {"category": {"$eq": "tech"}},
            {"year": {"$gte": 2023}}
        ]
    }
)

# Qdrant filtering
from qdrant_client.models import Filter, FieldCondition, MatchValue, Range

results = client.query_points(
    collection_name="docs",
    query=query_vector,
    query_filter=Filter(
        must=[
            FieldCondition(key="category", match=MatchValue(value="tech")),
            FieldCondition(key="year", range=Range(gte=2023))
        ]
    ),
    limit=5
)
```

### 4. Dimensionality Reduction

Mengurangi dimensi embedding untuk menghemat memori dan mempercepat search.

```python
# Menggunakan PCA
from sklearn.decomposition import PCA

# Kurangi dari 768 dimensi ke 256
pca = PCA(n_components=256)
reduced_embeddings = pca.fit_transform(embeddings)

# Atau gunakan Matryoshka embeddings (OpenAI text-embedding-3)
# yang memungkinkan shortening dimensi tanpa retrain
```

### 5. Caching

Cache hasil query yang sering diulang.

```python
from functools import lru_cache
import hashlib
import json

# Simple cache
query_cache = {}

def cached_search(query, collection, n_results=5):
    """Search dengan caching."""
    cache_key = hashlib.md5(query.encode()).hexdigest()
    
    if cache_key in query_cache:
        print("Cache hit!")
        return query_cache[cache_key]
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    query_cache[cache_key] = results
    return results
```

---

## Benchmark & Monitoring

### Ukur Performa
```python
import time

def benchmark_search(collection, queries, n_results=5):
    """Benchmark kecepatan dan kualitas search."""
    latencies = []
    
    for query in queries:
        start = time.perf_counter()
        results = collection.query(query_texts=[query], n_results=n_results)
        elapsed = time.perf_counter() - start
        latencies.append(elapsed)
    
    avg_latency = sum(latencies) / len(latencies)
    p95_latency = sorted(latencies)[int(0.95 * len(latencies))]
    
    print(f"Queries: {len(queries)}")
    print(f"Avg latency: {avg_latency*1000:.2f}ms")
    print(f"P95 latency: {p95_latency*1000:.2f}ms")
    print(f"QPS: {1/avg_latency:.1f}")
```

---

## Rekomendasi berdasarkan Skala

| Skala Dataset | Algoritma | Database | Catatan |
|---------------|-----------|----------|---------|
| <10K vektor | Flat | ChromaDB | Brute force cukup |
| 10K-100K | HNSW | ChromaDB/Qdrant | Default yang aman |
| 100K-1M | HNSW / IVF | Qdrant/Pinecone | Perlu tuning |
| 1M-10M | IVF+PQ / HNSW | Pinecone/FAISS | Kompresi penting |
| >10M | IVF+PQ, Sharding | Distributed setup | Butuh infrastruktur |

---

## Referensi
- [FAISS Indexing Guidelines](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index)
- [ANN Benchmarks](http://ann-benchmarks.com/)
- [HNSW Paper](https://arxiv.org/abs/1603.09320)
- [Hybrid Search - Weaviate](https://weaviate.io/developers/weaviate/search/hybrid)
- [Reranking - Cohere](https://docs.cohere.com/docs/reranking)
