# 01. EMBEDDING FUNDAMENTALS & VECTOR SPACE

## 💡 Apa Itu Embeddings?
**Embeddings** adalah teknik pengubahan data non-struktural (teks, gambar, audio, atau item) menjadi himpunan angka kontinu berupa **vektor dalam ruang dimensi tinggi** (high-dimensional vector space).

Tujuan utama embeddings adalah merepresentasikan **makna semantik (semantic meaning)** sehingga komputer dapat mengolah data berdasarkan kemiripan arti, bukan sekadar penamaan literal atau pencocokan kata kunci.

```
       "Raja" ───────► [ 0.82, -0.15,  0.64, ... ]
       "Ratu" ───────► [ 0.80, -0.12,  0.59, ... ]  ──► Jarak sangat dekat!
       "Mobil" ──────► [-0.45,  0.78, -0.11, ... ]  ──► Jarak jauh!
```

---

## 📐 Konsep Utama Ruang Vektor (Vector Space)

### 1. Vector Dimensions (Dimensi Vektor)
Setiap nilai float dalam vektor mewakili suatu "fitur abstrak" atau koordinat dalam ruang $D$-dimensi.
- **Model Kecil**: 384 dimensi (misal `all-MiniLM-L6-v2`)
- **Model Sedang**: 768 / 1536 dimensi (misal `text-embedding-3-small`, `bge-base-en`)
- **Model Besar**: 3072 / 4096 dimensi (misal `text-embedding-3-large`)

### 2. Dense vs Sparse Vectors
- **Sparse Vector (Misal BM25, TF-IDF)**: Memiliki dimensi sangat tinggi (seukuran jumlah kata unik di kamus, misal 50.000+), di mana mayoritas nilainya adalah $0$.
- **Dense Vector (Embeddings Neural)**: Memiliki dimensi tetap (misal 1536) di mana sebagian besar nilainya berupa float kontinu non-nol.

---

## 📊 Metrik Jarak & Kemiripan (Distance Metrics)

Untuk mengukur seberapa mirip dua vektor $\mathbf{A}$ dan $\mathbf{B}$, kita menggunakan fungsi jarak matematis:

### 1. Cosine Similarity (Kemiripan Kosinus)
Mengukur sudut antara dua vektor tanpa mempedulikan magnitudo/panjang vektor. Nilainya berkisar antara $[-1, 1]$ (atau $[0, 1]$ jika vektor bernilai positif).

$$\text{Cosine Similarity}(\mathbf{A}, \mathbf{B}) = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|} = \frac{\sum_{i=1}^n A_i B_i}{\sqrt{\sum_{i=1}^n A_i^2} \sqrt{\sum_{i=1}^n B_i^2}}$$

### 2. Dot Product (Perkalian Titik / Inner Product)
Sama dengan Cosine Similarity jika kedua vektor sudah di-**normalisasi L2** ($\|\mathbf{A}\| = 1, \|\mathbf{B}\| = 1$).

$$\text{Dot Product}(\mathbf{A}, \mathbf{B}) = \mathbf{A} \cdot \mathbf{B} = \sum_{i=1}^n A_i B_i$$

### 3. Euclidean Distance (Jarak L2)
Mengukur jarak garis lurus terpendek antara dua titik dalam ruang vektor.

$$d_{\text{Euclidean}}(\mathbf{A}, \mathbf{B}) = \sqrt{\sum_{i=1}^n (A_i - B_i)^2}$$

### 4. Manhattan Distance (Jarak L1 / Cityblock)
Mengukur total jarak mutlak sepanjang sumbu koordinat.

$$d_{\text{Manhattan}}(\mathbf{A}, \mathbf{B}) = \sum_{i=1}^n |A_i - B_i|$$

---

## 🎯 Normalisasi Vektor (L2 Normalization)

Normalisasi L2 mengubah panjang vektor menjadi $1$ ($\|\mathbf{V}\| = 1$).

$$\mathbf{V}_{\text{norm}} = \frac{\mathbf{V}}{\|\mathbf{V}\|_2} = \frac{\mathbf{V}}{\sqrt{\sum V_i^2}}$$

**Keuntungan Normalisasi L2:**
- Menghitung Cosine Similarity menjadi secepat **Dot Product** biasa ($\mathbf{A} \cdot \mathbf{B}$).
- Menghubungkan Jarak Euclidean dengan Cosine Similarity:

$$d_{\text{Euclidean}}^2(\mathbf{A}_{\text{norm}}, \mathbf{B}_{\text{norm}}) = 2 - 2 \cdot \text{CosineSimilarity}(\mathbf{A}_{\text{norm}}, \mathbf{B}_{\text{norm}})$$

---

## 🛠️ Implementasi Praktis & Best Practices
1. **Model Selection**: Gunakan `text-embedding-3-small` atau `bge-m3` untuk standar efisiensi & akurasi tinggi.
2. **Dimension Truncation**: Model baru seperti `text-embedding-3` mendukung Matryoshka Embeddings (pemotongan dimensi misal dari 1536 ke 512 tanpa kehilangan banyak akurasi).
3. **Normalisasi**: Selalu pastikan apakah vektor sudah tersimpan secara L2-normalized sebelum indeks pencarian.
