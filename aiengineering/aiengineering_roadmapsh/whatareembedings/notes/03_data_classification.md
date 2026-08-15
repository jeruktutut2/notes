# 03. DATA CLASSIFICATION & SEMANTIC CLUSTERING

## 🏷️ Penggunaan Embeddings untuk Klasifikasi Data

Embeddings mengubah data teks/unstructured menjadi vektor fitur berdimensi tinggi yang kaya akan konteks semantik. Vektor ini dapat langsung digunakan sebagai masukan (feature input) untuk algoritma Machine Learning tradisional maupun teknik Zero-Shot.

---

## 🛠️ Pendekatan Klasifikasi Berbasis Embeddings

### 1. Embedded Linear Classifier (Logistic Regression / SVM)
Langkah-langkah:
1. Konversi teks training menjadi vektor embedding $\mathbf{X}$.
2. Latih classifier ringan (seperti Logistic Regression atau Linear SVM) di atas $\mathbf{X}$ untuk memprediksi label $y$.
3. Sangat cepat dilatih (hitungan detik) dibanding fine-tuning seluruh arsitektur LLM!

```python
# Konsep Ringkas:
X_train_emb = [get_embedding(text) for text in train_texts]
clf = LogisticRegression()
clf.fit(X_train_emb, y_train)
```

### 2. Zero-Shot Semantic Classification
Klasifikasi **tanpa proses training data** sama sekali!
1. Buat vektor embedding untuk label kategori (misal: `"Pertanyaan Tagihan"`, `"Dukungan Teknis"`, `"Pengembalian Barang"`).
2. Buat vektor embedding dari teks query pengguna.
3. Hitung **Cosine Similarity** antara query dengan setiap embedding label.
4. Kategori dengan Cosine Similarity tertinggi dipilihi sebagai prediksi label.

---

## 🧩 Semantic Clustering (Topic Modeling)

Clustering mengelompokkan data yang tidak berlabel berdasarkan kedekatan jarak semantik di ruang vektor.

### K-Means Clustering pada Embeddings
- Mengelompokkan $N$ dokumen ke dalam $K$ kluster.
- **Centroid Kluster**: Merupakan rerata vektor dari seluruh dokumen dalam kluster tersebut, yang mewakili "pusat topik/tema".
- **Guna**: Menemukan topik otomatis dari ribuan review pelanggan, tiket keluhan, atau berita tanpa butuh label manual.
