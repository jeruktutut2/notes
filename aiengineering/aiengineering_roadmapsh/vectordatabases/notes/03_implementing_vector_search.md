# IMPLEMENTING VECTOR SEARCH: INDEXING & SIMILARITY SEARCH

Panduan mendalam mengenai **Implementasi Pencarian Vektor**, Algoritma Pengindeksan (**Indexing Embeddings**), dan Teknik Eksekusi Kemiripan (**Performing Similarity Search**).

---

## ⚡ 1. Indexing Embeddings (Algoritma Pengindeksan Vektor)

Mengindeks vektor adalah proses menyusun titik-titik embedding berdimensi tinggi ke dalam struktur data yang dapat diquery secara cepat. Berikut adalah 4 algoritma indeks utama:

```text
1. Flat Index (Exact Scan) ───► Recall 100% | Latency Lambat (O(N)) | Tanpa Kompresi
2. IVF (Inverted File)     ───► Voronoi Cells Clustering | Trade-off Speed & Memory
3. HNSW (Hierarchical Graph)───► Multi-layer Small World Graph | Latency Ultra Cepat
4. PQ (Product Quantization)───► Kompresi Vektor Float32 ke Byte Codebook | Memory Efisien
```

### A. Flat / Exact Index
- **Cara Kerja**: Menghitung jarak vektor query ke seluruh titik vektor tanpa kompresi atau pintasan grafik.
- **Kelebihan**: Recall 100% (pencarian persis).
- **Kelemahan**: Tidak berskala untuk juta/miliar vektor.

### B. HNSW (Hierarchical Navigable Small World)
- **Cara Kerja**: Membangun struktur grafik berlapis (*multi-layer graph*). Lapisan atas berisi loncatan jarak jauh (*highway nodes*), dan semakin ke bawah grafik semakin rapat untuk penyempurnaan pencarian lokal.
- **Kelebihan**: Kecepatan pencarian ANN paling stabil dan populer di industri (digunakan oleh Pinecone, Chroma, Qdrant, FAISS).
- **Parameter Utama**:
  - `M`: Jumlah koneksi maksimum per simpul grafik (misal: 16 - 64).
  - `efConstruction`: Ukuran daftar pencarian saat membangun grafik.
  - `efSearch`: Ukuran kandidat pencarian saat eksekusi query.

### C. IVF (Inverted File Index)
- **Cara Kerja**: Membagi ruang vektor ke dalam $K$ buah kluster Voronoi (*Voronoi Cells*) menggunakan K-Means. Saat query masuk, sistem hanya mencari di dalam $N$ kluster terdekat (`nprobe`).
- **Parameter Utama**:
  - `nlist`: Jumlah centroids/kluster Voronoi.
  - `nprobe`: Jumlah kluster terdekat yang diperiksa saat pencarian.

### D. PQ (Product Quantization)
- **Cara Kerja**: Memotong vektor berdimensi tinggi (misal 1536D) menjadi sub-vektor kecil, lalu memetakan sub-vektor tersebut ke *centroid codebook* byte (8-bit).
- **Kelebihan**: Memangkas penggunaan RAM hingga **95%** (misal dari 100GB menjadi 5GB).

---

## 🔍 2. Performing Similarity Search

### A. k-NN Search vs Radius / Threshold Search
- **k-Nearest Neighbors (Top-K)**: Mengembalikan tepat $K$ vektor terdekat berdasarkan skor kemiripan.
- **Threshold Search**: Mengembalikan seluruh vektor yang memiliki skor kemiripan di atas ambang batas (misal: Cosine Similarity $> 0.82$).

### B. Metadata Filtering Strategies
1. **Pre-Filtering**: Memfilter payload metadata terlebih dahulu sebelum melakukan pencarian vektor.
   - *Kelebihan*: Akurasi metadata 100%.
   - *Kekurangan*: Bisa mengurangi efisiensi indeks HNSW jika filter menghapus sebagian besar node grafik.
2. **Post-Filtering**: Mengambil Top-K vektor terlebih dahulu, kemudian menghapus data yang tidak cocok dengan metadata filter.
   - *Kelebihan*: Kecepatan grafik HNSW tetap optimal.
   - *Kekurangan*: Bisa mengembalikan hasil kurang dari $K$ jika banyak kandidat tereliminasi oleh filter metadata.
3. **Single-Stage Hybrid Filtering (Pinecone/Qdrant Way)**: Indeks grafik terintegrasi langsung dengan bitmap metadata, sehingga pemfilteran dilakukan secara simultan saat penelusuran grafik HNSW.

### C. Hybrid Search (Dense + Sparse Search)
Menggabungkan keunggulan dua metode pencarian:
- **Dense Vector Search**: Menangkap arti kontekstual & sinonim (*Semantic Meaning*).
- **Sparse Vector Search (BM25 / SPLADE)**: Menangkap kata kunci spesifik, istilah teknis, serial number, atau nama produk (*Exact Keyword Match*).

$$ \text{Score} = \alpha \cdot \text{DenseScore} + (1 - \alpha) \cdot \text{SparseScore} $$
