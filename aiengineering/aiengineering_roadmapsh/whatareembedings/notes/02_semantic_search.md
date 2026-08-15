# 02. SEMANTIC SEARCH (PENCARIAN SEMANTIK)

## 🔍 Apa Itu Semantic Search?
**Semantic Search** adalah teknik pencarian dokumen berbasis **makna dan niat (intent)** dari query pengguna, bukan sekadar pencocokan persis string kata kunci (keyword matching).

| Fitur | Keyword Search (Lexical) | Semantic Search (Vector) |
| :--- | :--- | :--- |
| **Metode** | Pencocokan token / TF-IDF / BM25 | Jarak Vektor Embedding (Cosine/L2) |
| **Sinonim** | Gagal jika tidak ada alias eksplisit | Berhasil (misal "smartphone" ~ "HP") |
| **Konteks & Niat** | Mengabaikan tata bahasa & konteks | Memahami nuansa & arti kalimat |
| **Pencarian Lintas Bahasa** | Perlu penerjemahan eksplisit | Bekerja native dengan Multilingual Embeddings |
| **Typo & Variasi** | Membutuhkan Fuzzy Match | Toleran secara alami dalam ruang vektor |

---

## 🏗️ Komponen Utama Pipeline Semantic Search

```
[ Dokumen ] ──► [ Chunking ] ──► [ Embedding Generator ] ──► [ Vector Store / Index ]
                                                                      │
[ Query User ] ─────────────────► [ Embedding Generator ] ────────────┤
                                                                      ▼
[ Ranked Results ] ◄─── [ Re-ranker (Cross-Encoder) ] ◄─── [ Cosine / KNN Search ]
```

### 1. Chunking Strategy
Dokumen panjang harus dipecah menjadi potongan teks (chunks) berukuran optimal (misal 256–512 token) sebelum di-embed.
- **Fixed-size Chunking**: Memotong berdasarkan jumlah karakter/token tertentu dengan overlap.
- **Paragraph / Sentence Chunking**: Memotong berdasarkan batas paragraf atau struktur batas kalimat alami.
- **Semantic Chunking**: Memotong teks di titik di mana jarak semantik antar kalimat bertetangga mengalami lonjakan (perubahan topik).

### 2. Bi-Encoder vs Cross-Encoder
- **Bi-Encoder**: Memproses Query dan Dokumen secara terpisah menjadi vektor tunggal. Sangat cepat ($O(1)$ pencarian via Vector DB), cocok untuk Retrieval tahap pertama.
- **Cross-Encoder**: Memproses pasangan `(Query, Dokumen)` secara bersamaan dalam model Transformer. Sangat akurat tetapi lambat, cocok untuk tahap **Re-ranking**.

---

## ⚡ Hybrid Search (Pencarian Hibrida)

Pencarian produksi terbaik menggabungkan keunggulan **BM25 (Pencocokan Kata Kunci Spesifik/Kode Produk)** dan **Vector Embeddings (Makna Semantik)**.

### RRF (Reciprocal Rank Fusion)
Metode populer untuk menggabungkan skor dari dua sistem pencarian tanpa perlu melakukan kalkulasi korelasi skala skor:

$$\text{RRF Score}(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$$

Di mana:
- $r_m(d)$ adalah urutan rank dokumen $d$ dalam sistem $m$ (misal BM25 atau Vector Search).
- $k$ adalah konstanta perhalus (biasanya $k=60$).
