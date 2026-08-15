# PURPOSE AND FUNCTIONALITY OF VECTOR DATABASES

Panduan teori mendalam mengenai **Tujuan Utama & Fungsionalitas Vector Databases** dalam ekosistem AI Engineering dan aplikasi berbasis Large Language Models (LLM).

---

## 💡 1. Mengapa Database Tradisional Tidak Cukup?

Database tradisional (Relational SQL seperti PostgreSQL/MySQL, atau NoSQL Document Store seperti MongoDB) didesain untuk pencarian berdasar **pencocokan persis (exact match)** atau query terstruktur ber-indeks B-Tree / Hash.

| Fitur / Karakteristik | Database Tradisional (SQL / NoSQL) | Vector Databases |
| :--- | :--- | :--- |
| **Tipe Data Utama** | Teks, Angka, Boolean, JSON, Datetime | Dense Float Vectors (Embeddings 1536D, 768D, 384D) + Metadata Payload |
| **Metode Pencarian** | Exact Matching (`WHERE status = 'active'`), Range Queries, Full-text Search (BM25) | Semantic Similarity Search (Nearest Neighbor / ANN) |
| **Struktur Indeks** | B-Tree, B+Tree, Hash Index, LSM Tree | HNSW, IVF (Inverted File), PQ (Product Quantization) |
| **Query Input** | SQL syntax, JSON filter (`{"age": {"$gt": 25}}`) | Embedding Query Vector `[0.012, -0.043, ..., 0.891]` |
| **Skalabilitas Vektor** | Lambat (Skalar O(N) linear scan untuk vektor dimensi tinggi) | Cepat (Sub-linear O(log N) ANN Retrieval untuk miliaran vektor) |

---

## 🎯 2. Fungsionalitas Utama Vector Database

Vector Database tidak hanya menyimpan susunan angka (vektor embedding), melainkan menyediakan ekosistem terpadu untuk data tak terstruktur (*unstructured data*):

### A. High-Dimensional Vector Storage & CRUD Operations
- **Store**: Menyimpan vektor hasil konversi LLM/Embedding model bersama ID unik dan payload metadata (misal: dokumen mentah, author, timestamp, tags).
- **Upsert**: Meng-update atau menyisipkan pasangan vektor-metadata secara atomic.
- **Delete & Soft Delete**: Menghapus data vektor beserta indeks tanpa perlu membangun ulang seluruh indeks (*indexing cost reduction*).

### B. Similarity Search Metrics
Perhitungan kemiripan vektor dilakukan menggunakan kalkulasi jarak dalam ruang linier serba-banyak dimensi:

1. **Cosine Similarity**:
   $$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|}$$
   *Mengukur sudut antar vektor. Rentang: -1 hingga 1. Ideal untuk teks embedding di mana orientasi kata lebih penting dibanding panjang dokumen.*

2. **Dot Product (Inner Product)**:
   $$\text{Dot Product}(\vec{A}, \vec{B}) = \sum_{i=1}^n A_i B_i$$
   *Sangat cepat dihitung. Apabila vektor sudah di-normalisasi (L2 norm = 1), Dot Product identik dengan Cosine Similarity.*

3. **Euclidean Distance (L2 Distance)**:
   $$\text{L2}(\vec{A}, \vec{B}) = \sqrt{\sum_{i=1}^n (A_i - B_i)^2}$$
   *Mengukur jarak fisik garis lurus antar dua titik. Nilai semakin kecil mengindikasikan kemiripan semakin tinggi.*

### C. Payload & Metadata Filtering
Vector Database memungkinkan pencarian gabungan (*hybrid query*): mencari vektor yang paling mirip secara kontekstual, namun membatasi hasil pencarian berdasarkan kriteria metadata terstruktur.

```json
{
  "vector": [0.012, -0.043, 0.512, "..."],
  "top_k": 5,
  "filter": {
    "category": "ai_engineering",
    "year": { "$gte": 2024 }
  }
}
```

---

## 🧠 3. Exact Nearest Neighbor (k-NN) vs Approximate Nearest Neighbor (ANN)

- **k-NN (Exact)**: Membandingkan vektor query terhadap **seluruh** vektor yang ada di database satu per satu (Brute-force / Linear Scan $O(N \cdot D)$). Akurasi 100%, tetapi sangat lambat dan boros memori jika jumlah data mencapai jutaan.
- **ANN (Approximate)**: Menggunakan struktur grafik atau klusterisasi cerdas untuk menyempitkan ruang pencarian ke wilayah yang paling relevan ($O(\log N)$). Pengorbanan kecil pada akurasi ( recall ~95%-99%) memberikan peningkatan kecepatan hingga **100x - 1000x**.
