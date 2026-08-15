# 02 - Vector Similarity

## Apa itu Vector Similarity?

Vector Similarity adalah cara mengukur seberapa **mirip** dua vektor satu sama lain. Dalam konteks AI, ini berarti mengukur seberapa mirip makna dua buah teks, gambar, atau data lainnya yang sudah dikonversi menjadi embedding.

```
Query: "cara memasak nasi goreng"

Hasil similarity search:
1. "resep nasi goreng sederhana"     → similarity: 0.92 ✅
2. "tips memasak nasi yang pulen"    → similarity: 0.75
3. "harga beras di pasar"           → similarity: 0.35
4. "jadwal kereta api hari ini"     → similarity: 0.08 ❌
```

---

## Jenis-Jenis Similarity Metrics

### 1. Cosine Similarity

Mengukur **sudut** antara dua vektor. Nilainya antara -1 sampai 1.

- **1** = identik (arah sama persis)
- **0** = tidak berhubungan (tegak lurus)
- **-1** = berlawanan

```
Cosine Similarity = (A · B) / (||A|| × ||B||)
```

**Kapan digunakan:** Paling umum digunakan. Cocok ketika yang penting adalah "arah" vektor, bukan besarnya.

```python
import numpy as np

def cosine_similarity(a, b):
    """Menghitung cosine similarity antara dua vektor."""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    return dot_product / (norm_a * norm_b)

# Contoh
vec_a = np.array([1, 2, 3])
vec_b = np.array([1, 2, 3.5])
vec_c = np.array([3, 1, -2])

print(f"A vs B: {cosine_similarity(vec_a, vec_b):.4f}")  # ~0.998 (sangat mirip)
print(f"A vs C: {cosine_similarity(vec_a, vec_c):.4f}")  # ~0.014 (tidak mirip)
```

### 2. Euclidean Distance (L2 Distance)

Mengukur **jarak lurus** antara dua titik vektor. Semakin kecil nilainya, semakin mirip.

```
Euclidean Distance = √(Σ(ai - bi)²)
```

**Kapan digunakan:** Ketika magnitude (besaran) vektor juga penting, bukan hanya arah.

```python
def euclidean_distance(a, b):
    """Menghitung Euclidean distance antara dua vektor."""
    return np.sqrt(np.sum((a - b) ** 2))

# Atau menggunakan numpy
distance = np.linalg.norm(vec_a - vec_b)
print(f"A vs B distance: {distance:.4f}")  # kecil = mirip
```

### 3. Dot Product (Inner Product)

Mengukur **proyeksi** satu vektor ke vektor lain. Semakin besar nilainya, semakin mirip.

```
Dot Product = Σ(ai × bi)
```

**Kapan digunakan:** Ketika vektor sudah dinormalisasi. Pada vektor ternormalisasi, dot product = cosine similarity.

```python
def dot_product(a, b):
    """Menghitung dot product antara dua vektor."""
    return np.dot(a, b)

score = dot_product(vec_a, vec_b)
print(f"Dot product: {score:.4f}")
```

### 4. Manhattan Distance (L1 Distance)

Mengukur jarak dengan menjumlahkan **selisih absolut** setiap dimensi. Seperti berjalan di grid kota.

```
Manhattan Distance = Σ|ai - bi|
```

```python
def manhattan_distance(a, b):
    """Menghitung Manhattan distance."""
    return np.sum(np.abs(a - b))
```

---

## Perbandingan Metrics

| Metric | Range | Semakin Mirip | Kecepatan | Use Case |
|--------|-------|---------------|-----------|----------|
| **Cosine Similarity** | [-1, 1] | → 1 | Cepat | Teks, NLP (paling umum) |
| **Euclidean Distance** | [0, ∞) | → 0 | Cepat | Gambar, spatial data |
| **Dot Product** | (-∞, ∞) | → besar | Sangat cepat | Vektor ternormalisasi |
| **Manhattan Distance** | [0, ∞) | → 0 | Cepat | High-dimensional sparse data |

---

## Nearest Neighbor Search

### Apa itu?
Menemukan vektor yang paling dekat (mirip) dengan vektor query dari kumpulan vektor yang ada.

### Jenis-Jenis Search

#### 1. Exact Nearest Neighbor (Brute Force)
Membandingkan query dengan **semua** vektor di database. Akurat 100% tapi lambat.

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Database vektor (misal 1000 dokumen, 384 dimensi)
database = np.random.rand(1000, 384)

# Query vektor
query = np.random.rand(1, 384)

# Hitung similarity dengan semua dokumen
similarities = cosine_similarity(query, database)[0]

# Ambil top-5 paling mirip
top_k = 5
top_indices = np.argsort(similarities)[-top_k:][::-1]

for i, idx in enumerate(top_indices):
    print(f"#{i+1}: Dokumen {idx} (similarity: {similarities[idx]:.4f})")
```

#### 2. Approximate Nearest Neighbor (ANN)
Mengorbankan sedikit akurasi untuk **kecepatan yang jauh lebih tinggi**. Ini yang digunakan oleh vector databases.

Algoritma populer:
- **HNSW** — Paling umum, balance kecepatan & akurasi
- **IVF** — Membagi data ke cluster, cari hanya di cluster terdekat
- **LSH** — Locality-Sensitive Hashing

```python
# Contoh menggunakan FAISS (Facebook AI Similarity Search)
import faiss
import numpy as np

# Data: 10000 vektor, 128 dimensi
d = 128
nb = 10000
data = np.random.rand(nb, d).astype('float32')

# Buat index (Flat = brute force)
index_flat = faiss.IndexFlatL2(d)
index_flat.add(data)

# Buat index (IVF = approximate)
nlist = 100  # jumlah cluster
quantizer = faiss.IndexFlatL2(d)
index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist)
index_ivf.train(data)
index_ivf.add(data)

# Query
query = np.random.rand(1, d).astype('float32')
k = 5  # top-5

# Search
D_flat, I_flat = index_flat.search(query, k)   # exact
D_ivf, I_ivf = index_ivf.search(query, k)      # approximate

print("Exact results:", I_flat[0])
print("Approx results:", I_ivf[0])
```

---

## Praktik: Semantic Search Sederhana

```python
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 1. Load model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Database dokumen
documents = [
    "Python adalah bahasa pemrograman yang populer untuk data science",
    "Machine learning menggunakan data untuk membuat prediksi",
    "Kucing dan anjing adalah hewan peliharaan yang populer",
    "Deep learning adalah subset dari machine learning",
    "Resep nasi goreng kampung yang lezat",
    "Neural network terinspirasi dari otak manusia",
    "Cara merawat tanaman hias di rumah",
    "TensorFlow dan PyTorch adalah framework deep learning",
]

# 3. Buat embedding untuk semua dokumen
doc_embeddings = model.encode(documents)

# 4. Query
query = "bagaimana cara belajar AI?"
query_embedding = model.encode([query])

# 5. Hitung similarity
similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

# 6. Tampilkan hasil terurut
print(f"Query: '{query}'\n")
print("Hasil pencarian:")
print("-" * 60)

ranked = sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)
for rank, (idx, score) in enumerate(ranked, 1):
    emoji = "✅" if score > 0.3 else "❌"
    print(f"  {rank}. [{score:.4f}] {emoji} {documents[idx]}")
```

---

## Visualisasi Vektor (Opsional)

Menampilkan embedding dalam 2D menggunakan t-SNE:

```python
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Reduksi dimensi ke 2D
tsne = TSNE(n_components=2, random_state=42, perplexity=5)
embeddings_2d = tsne.fit_transform(doc_embeddings)

# Plot
plt.figure(figsize=(12, 8))
plt.scatter(embeddings_2d[:, 0], embeddings_2d[:, 1], c='steelblue', s=100)

for i, doc in enumerate(documents):
    label = doc[:40] + "..." if len(doc) > 40 else doc
    plt.annotate(label, (embeddings_2d[i, 0], embeddings_2d[i, 1]),
                fontsize=8, ha='center', va='bottom')

plt.title("Visualisasi Document Embeddings (t-SNE)")
plt.xlabel("Dimensi 1")
plt.ylabel("Dimensi 2")
plt.tight_layout()
plt.savefig("embedding_visualization.png", dpi=150)
plt.show()
```

---

## Hal Penting

1. **Pilih metric yang sesuai** dengan model embedding yang digunakan (cek dokumentasi model)
2. **Cosine similarity** adalah default yang aman untuk kebanyakan kasus NLP
3. **ANN lebih cepat** dari exact search, tapi ada tradeoff akurasi (~95-99%)
4. **Normalisasi vektor** sebelum menggunakan dot product agar setara dengan cosine similarity
5. **Threshold similarity**: Tentukan batas minimum similarity (misal 0.3) untuk memfilter hasil yang tidak relevan

---

## Referensi
- [FAISS Documentation](https://github.com/facebookresearch/faiss/wiki)
- [Understanding Distance Metrics - Pinecone](https://www.pinecone.io/learn/vector-similarity/)
- [Sklearn Pairwise Metrics](https://scikit-learn.org/stable/modules/metrics.html)
- [ANN Benchmarks](http://ann-benchmarks.com/)
