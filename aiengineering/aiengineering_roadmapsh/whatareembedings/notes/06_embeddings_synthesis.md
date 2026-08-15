# 06. EMBEDDINGS SYNTHESIS & STRATEGIC GUIDE

## 🧠 Sintesis Panduan Strategis Embeddings bagi AI Engineer

Modul ini merangkum seluruh fondasi dan kasus penggunaan utama dari **Embeddings** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 🗺️ Matriks Kasus Penggunaan Embeddings

| Kasus Penggunaan | Metrik Jarak Direkomendasikan | Algoritma / Metode Utama | Tantangan Utama |
| :--- | :--- | :--- | :--- |
| **Semantic Search** | Cosine Similarity / Inner Product | Bi-Encoder + Vector DB + Cross-Encoder Re-ranker | Granularitas chunking & hybrid search |
| **Data Classification** | Cosine / Euclidean | Logistic Regression pada Vektor / Zero-Shot | Pemilihan threshold & representasi label |
| **Recommendation Systems** | Cosine Similarity | User Profile Aggregation / Item-to-Item KNN | Handling Cold-start & bias preferensi lama |
| **Anomaly Detection** | Cosine Distance / KNN Score | Centroid Distance Thresholding / Isolation Forest | Menentukan threshold presisi vs recall |

---

## 🚀 Check-list Produksi AI Engineering

1. **Normalisasi Vektor**: Selalu pastikan apakah model embedding Anda menghasilkan vektor ter-normalisasi L2.
2. **Dimension Reduction (Matryoshka Embeddings)**: Gunakan fitur pemotongan dimensi jika ingin menghemat memory Vector DB tanpa mengorbankan kualitas secara drastis.
3. **Chunking Quality**: Kualitas pencarian semantik sangat ditentukan oleh strategi pemotongan teks (chunking) daripada sekadar pilihan model.
4. **Hybrid Search**: Jangan tinggalkan pencarian lexical (BM25) ketika menangani pencarian istilah teknis, serial number, atau nama persis!
