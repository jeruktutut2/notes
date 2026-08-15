# 04. Evaluation Metrics & RAG Triad

Evaluasi LLM memerlukan metrik yang terukur secara kuantitatif. Metrik ini terbagi dua: **Metrik Klasik (NLP/Klasifikasi)** dan **Metrik Spesifik RAG (RAG Triad)**.

---

## 📊 Metrik Klasik NLP & Klasifikasi

1. **Accuracy**: Persentase prediksi yang persis benar terhadap total sampel.
2. **Precision**: Rasio prediksi positif yang benar dibanding seluruh prediksi positif ($\frac{TP}{TP + FP}$).
3. **Recall (Sensitivity)**: Rasio prediksi positif yang benar dibanding seluruh fakta positif ($\frac{TP}{TP + FN}$).
4. **F1-Score**: Harmonic mean dari Precision dan Recall ($2 \times \frac{Precision \times Recall}{Precision + Recall}$).
5. **Perplexity (PPL)**: Mengukur seberapa "terkejut" model terhadap urutan teks ($PPL = \exp(-\frac{1}{N} \sum \log P(x_i | x_{<i}))$. Semakin rendah nilai PPL, semakin baik kemampuan prediktif bahasa model tersebut.

---

## 🔺 Metrik RAG Triad (Retrieval-Augmented Generation)

RAG Triad adalah kerangka kerja evaluasi standar industri yang dipopulerkan oleh TruLens dan RAGAS untuk mengevaluasi sistem RAG tanpa memerlukan *ground truth* jawaban ideal.

```
       [User Query]
          /     \
         /       \
  Context         Answer
 Precision        Relevance
       /           \
      /             \
[Retrieved Contexts] --- Faithfulness --- [LLM Response]
```

### 1. Faithfulness (Kejujuran / Anti-Halusinasi)
- **Definisi**: Mengukur apakah seluruh klaim dalam *LLM Response* didukung secara faktual oleh *Retrieved Contexts*.
- **Skor**: 0.0 - 1.0 (1.0 = Tidak ada halusinasi sama sekali).
- **Formula Logic**:
  $$\text{Faithfulness} = \frac{\text{Jumlah Klaim Respons yang Terbukti di Context}}{\text{Total Klaim dalam Respons}}$$

### 2. Answer Relevance (Relevansi Jawaban)
- **Definisi**: Mengukur seberapa tepat respons menjawab pertanyaan pengguna (*User Query*), tanpa memasukkan informasi yang irelevan.
- **Skor**: 0.0 - 1.0 (1.0 = Sangat relevan dan fokus pada pertanyaan).
- **Formula Logic**: Menghitung *cosine similarity* antara embedding query asli dan embedding query buatan yang direkayasa kembali dari respons.

### 3. Context Precision (Presisi Konteks)
- **Definisi**: Mengukur apakah dokumen/chunk relevan berada di urutan atas (*top ranks*) hasil pencarian vektor retriever.
- **Skor**: 0.0 - 1.0. High precision berarti *noise* minim di peringkat teratas.

### 4. Context Recall (Kelengkapan Konteks)
- **Definisi**: Mengukur apakah semua informasi faktual yang dibutuhkan untuk menjawab *Ground Truth* telah berhasil diambil oleh *Retriever*.
- **Skor**: 0.0 - 1.0.
