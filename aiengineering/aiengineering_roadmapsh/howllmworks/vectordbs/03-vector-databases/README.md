# 03 - Vector Databases (Hands-On)

## Apa itu Vector Database?

Vector Database adalah database yang didesain khusus untuk menyimpan, mengindeks, dan melakukan query terhadap **data vektor** (embedding) secara efisien. Berbeda dengan database tradisional yang mencari berdasarkan exact match, vector database mencari berdasarkan **kemiripan semantik**.

### Perbedaan dengan Database Tradisional

| Aspek | SQL/NoSQL | Vector Database |
|-------|-----------|-----------------|
| **Data yang disimpan** | Teks, angka, JSON | Vektor (array angka) + metadata |
| **Cara query** | WHERE, LIKE, regex | Similarity search (cosine, L2) |
| **Hasil pencarian** | Exact match | Nearest neighbors (paling mirip) |
| **Indexing** | B-Tree, Hash | HNSW, IVF, PQ |
| **Use case** | CRUD tradisional | Semantic search, RAG, rekomendasi |

---

## Vector Databases Populer

### 1. ChromaDB (Recommended untuk Belajar)

**Tipe:** Open-source, embedded (berjalan lokal)
**Kelebihan:** Paling mudah untuk memulai, tidak perlu server

#### Instalasi
```bash
pip install chromadb
```

#### Penggunaan Dasar
```python
import chromadb
from chromadb.utils import embedding_functions

# 1. Buat client
client = chromadb.Client()  # in-memory
# client = chromadb.PersistentClient(path="./chroma_db")  # persistent

# 2. Pilih embedding function
# Default: menggunakan all-MiniLM-L6-v2
default_ef = embedding_functions.DefaultEmbeddingFunction()

# Atau gunakan OpenAI
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key="YOUR_API_KEY",
#     model_name="text-embedding-3-small"
# )

# 3. Buat collection
collection = client.create_collection(
    name="my_documents",
    embedding_function=default_ef,
    metadata={"hnsw:space": "cosine"}  # similarity metric
)

# 4. Tambahkan dokumen
collection.add(
    documents=[
        "Python adalah bahasa pemrograman populer untuk AI",
        "Machine learning menggunakan data untuk prediksi",
        "Kucing adalah hewan peliharaan yang lucu",
        "Deep learning adalah bagian dari machine learning",
        "Resep nasi goreng kampung yang enak",
    ],
    metadatas=[
        {"category": "programming", "language": "id"},
        {"category": "ai", "language": "id"},
        {"category": "animals", "language": "id"},
        {"category": "ai", "language": "id"},
        {"category": "cooking", "language": "id"},
    ],
    ids=["doc1", "doc2", "doc3", "doc4", "doc5"]
)

# 5. Query (similarity search)
results = collection.query(
    query_texts=["bagaimana belajar artificial intelligence?"],
    n_results=3
)

print("Hasil pencarian:")
for i, (doc, score) in enumerate(
    zip(results["documents"][0], results["distances"][0])
):
    print(f"  {i+1}. [{score:.4f}] {doc}")

# 6. Query dengan filter metadata
results_filtered = collection.query(
    query_texts=["teknologi terbaru"],
    n_results=3,
    where={"category": "ai"}  # filter hanya kategori AI
)
```

#### Operasi CRUD
```python
# UPDATE
collection.update(
    ids=["doc1"],
    documents=["Python 3.12 adalah versi terbaru"],
    metadatas=[{"category": "programming", "language": "id", "updated": True}]
)

# DELETE
collection.delete(ids=["doc5"])

# GET (ambil tanpa search)
doc = collection.get(ids=["doc1"])
print(doc)

# COUNT
print(f"Total dokumen: {collection.count()}")
```

---

### 2. Pinecone (Managed Cloud)

**Tipe:** Fully managed cloud service
**Kelebihan:** Scalable, tidak perlu kelola infrastruktur

#### Instalasi
```bash
pip install pinecone-client
```

#### Penggunaan Dasar
```python
from pinecone import Pinecone, ServerlessSpec

# 1. Inisialisasi
pc = Pinecone(api_key="YOUR_API_KEY")

# 2. Buat index
pc.create_index(
    name="my-index",
    dimension=384,  # sesuaikan dengan model embedding
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
    )
)

# 3. Connect ke index
index = pc.Index("my-index")

# 4. Upsert (insert/update) vektor
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    "Python untuk data science",
    "Machine learning basics",
    "Deep learning dengan PyTorch",
]

embeddings = model.encode(documents).tolist()

vectors = [
    {
        "id": f"doc_{i}",
        "values": emb,
        "metadata": {"text": doc, "category": "tech"}
    }
    for i, (doc, emb) in enumerate(zip(documents, embeddings))
]

index.upsert(vectors=vectors)

# 5. Query
query_embedding = model.encode("belajar AI").tolist()

results = index.query(
    vector=query_embedding,
    top_k=3,
    include_metadata=True
)

for match in results["matches"]:
    print(f"  [{match['score']:.4f}] {match['metadata']['text']}")
```

---

### 3. FAISS (Facebook AI Similarity Search)

**Tipe:** Library (bukan database, tidak ada server)
**Kelebihan:** Sangat cepat, cocok untuk riset dan dataset besar

#### Instalasi
```bash
pip install faiss-cpu  # atau faiss-gpu untuk GPU
```

#### Penggunaan Dasar
```python
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

# 1. Buat embedding
documents = [
    "Python untuk data science",
    "Machine learning basics",
    "Kucing lucu di internet",
    "Deep learning dengan PyTorch",
    "Resep masakan padang",
]

embeddings = model.encode(documents).astype('float32')
dimension = embeddings.shape[1]  # 384

# 2. Buat index
# Flat (brute force, paling akurat)
index = faiss.IndexFlatIP(dimension)  # Inner Product (cosine jika dinormalisasi)

# Normalisasi vektor agar Inner Product = Cosine Similarity
faiss.normalize_L2(embeddings)
index.add(embeddings)

print(f"Total vektor: {index.ntotal}")

# 3. Search
query = model.encode(["belajar artificial intelligence"]).astype('float32')
faiss.normalize_L2(query)

k = 3  # top-3
distances, indices = index.search(query, k)

print("\nHasil pencarian:")
for i, (idx, dist) in enumerate(zip(indices[0], distances[0])):
    print(f"  {i+1}. [{dist:.4f}] {documents[idx]}")

# 4. Simpan dan load index
faiss.write_index(index, "my_index.faiss")
loaded_index = faiss.read_index("my_index.faiss")
```

#### FAISS dengan IVF (Approximate, Lebih Cepat)
```python
# Untuk dataset besar (>100K vektor)
nlist = 50  # jumlah cluster
quantizer = faiss.IndexFlatIP(dimension)
index_ivf = faiss.IndexIVFFlat(quantizer, dimension, nlist)

# Train dulu (wajib untuk IVF)
index_ivf.train(embeddings)
index_ivf.add(embeddings)

# Set nprobe (jumlah cluster yang dicek saat search)
index_ivf.nprobe = 10  # semakin besar = lebih akurat tapi lebih lambat

distances, indices = index_ivf.search(query, k)
```

---

### 4. Qdrant

**Tipe:** Open-source, bisa self-hosted atau cloud
**Kelebihan:** Filtering canggih, performa tinggi

#### Instalasi
```bash
pip install qdrant-client
```

#### Penggunaan Dasar
```python
from qdrant_client import QdrantClient
from qdrant_client.models import (
    VectorParams, Distance, PointStruct, Filter,
    FieldCondition, MatchValue
)

# 1. Client (lokal/in-memory)
client = QdrantClient(":memory:")  # atau QdrantClient(url="http://localhost:6333")

# 2. Buat collection
client.create_collection(
    collection_name="my_docs",
    vectors_config=VectorParams(
        size=384,
        distance=Distance.COSINE
    )
)

# 3. Insert data
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

documents = [
    {"text": "Python untuk data science", "category": "tech"},
    {"text": "Machine learning basics", "category": "tech"},
    {"text": "Kucing lucu di internet", "category": "animals"},
]

points = []
for i, doc in enumerate(documents):
    embedding = model.encode(doc["text"]).tolist()
    points.append(PointStruct(
        id=i,
        vector=embedding,
        payload=doc
    ))

client.upsert(collection_name="my_docs", points=points)

# 4. Search
query_vector = model.encode("belajar AI").tolist()

results = client.query_points(
    collection_name="my_docs",
    query=query_vector,
    limit=3
)

for point in results.points:
    print(f"  [{point.score:.4f}] {point.payload['text']}")

# 5. Search dengan filter
results_filtered = client.query_points(
    collection_name="my_docs",
    query=query_vector,
    query_filter=Filter(
        must=[FieldCondition(key="category", match=MatchValue(value="tech"))]
    ),
    limit=3
)
```

---

### 5. Supabase (pgvector)

**Tipe:** PostgreSQL extension
**Kelebihan:** Cocok jika sudah menggunakan PostgreSQL/Supabase

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Buat tabel
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    category TEXT,
    embedding vector(384)  -- dimensi sesuai model
);

-- Insert dengan embedding
INSERT INTO documents (content, category, embedding)
VALUES (
    'Python untuk data science',
    'tech',
    '[0.1, 0.2, ...]'  -- vektor 384 dimensi
);

-- Similarity search (cosine distance)
SELECT content, category,
       1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM documents
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;

-- Dengan filter
SELECT content, category,
       1 - (embedding <=> '[0.1, 0.2, ...]') AS similarity
FROM documents
WHERE category = 'tech'
ORDER BY embedding <=> '[0.1, 0.2, ...]'
LIMIT 5;
```

---

## Perbandingan Vector Databases

| Fitur | ChromaDB | Pinecone | FAISS | Qdrant | pgvector |
|-------|----------|----------|-------|--------|----------|
| **Setup** | Sangat mudah | Mudah (cloud) | Menengah | Menengah | Mudah (jika sudah pakai PG) |
| **Hosting** | Lokal/embedded | Cloud only | Lokal (library) | Lokal/Cloud | Lokal/Cloud |
| **Scalability** | Kecil-menengah | Sangat besar | Sangat besar | Besar | Menengah |
| **Filtering** | Ya | Ya | Tidak native | Ya (canggih) | Ya (SQL) |
| **Persistence** | Ya | Ya (cloud) | File-based | Ya | Ya (PostgreSQL) |
| **Harga** | Gratis | Freemium | Gratis | Gratis/Cloud | Gratis |
| **Cocok untuk** | Belajar, prototipe | Produksi skala besar | Riset, batch processing | Produksi | Integrasi dengan SQL |

---

## Tips Memilih Vector Database

1. **Baru belajar?** → Mulai dengan **ChromaDB** (paling mudah)
2. **Produksi, tidak mau kelola server?** → **Pinecone** atau **Qdrant Cloud**
3. **Butuh kecepatan maksimal?** → **FAISS** (library level)
4. **Sudah pakai PostgreSQL?** → **pgvector/Supabase**
5. **Butuh filtering & query kompleks?** → **Qdrant** atau **Weaviate**

---

## Referensi
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [Pinecone Documentation](https://docs.pinecone.io/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
