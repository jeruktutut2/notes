# Modul 03: Embeddings & Vectorization

Vector Embedding adalah representasi numerik (vektor kontinu berdimensi tinggi) dari suatu teks yang mengkapsulasi makna semantik dari teks tersebut.

## Materi Pembelajaran

1. **`1_text_embeddings.py`**
   - Generasi dense vector embeddings menggunakan OpenAI API (`text-embedding-3-small` / `text-embedding-ada-002`).
   - Menyediakan fallback generator embedding deterministik berbasis NumPy jika API Key tidak diset.

2. **`2_vector_similarity_metrics.py`**
   - Perhitungan metrik keserupaan vektor secara matematis dari nol menggunakan NumPy:
     - Cosine Similarity
     - Dot Product
     - Euclidean Distance ($L_2$)

3. **`3_embedding_normalization_and_dimensions.py`**
   - Mengapa normalisasi vektor ($L_2$ norm = 1) sangat penting.
   - Pengaruh kuantisasi & reduksi dimensi pada performa pencarian.

## Cara Menjalankan

```bash
python3 03_embeddings_dan_vectorization/1_text_embeddings.py
python3 03_embeddings_dan_vectorization/2_vector_similarity_metrics.py
python3 03_embeddings_dan_vectorization/3_embedding_normalization_and_dimensions.py
```
