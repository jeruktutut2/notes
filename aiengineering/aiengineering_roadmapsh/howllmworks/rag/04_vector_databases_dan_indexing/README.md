# Modul 04: Vector Databases & Indexing

Vector Database adalah infrastruktur penyimpanan yang dirancang khusus untuk mengindeks dan mengkueri vektor berdimensi tinggi secara efisien.

## Materi Pembelajaran

1. **`1_in_memory_vector_store.py`**
   - Membangun Vector Store custom in-memory dari nol menggunakan Python & NumPy.
   - Mendukung penambahan dokumen, kalkulasi vektor, metadata filtering, dan pencarian Top-K similarity.

2. **`2_chromadb_integration.py`**
   - Integrasi dengan ChromaDB (salah satu open-source vector DB terpopuler).
   - Membuat collection, memasukkan dokumen + metadata, melakukan query similarity, dan persistence.

3. **`3_indexing_algorithms.py`**
   - Memahami perbedaan antara **Flat Indexing** (Brute force $O(N)$) vs **HNSW / ANN** (Approximate Nearest Neighbors $O(\log N)$).

## Cara Menjalankan

```bash
python3 04_vector_databases_dan_indexing/1_in_memory_vector_store.py
python3 04_vector_databases_dan_indexing/2_chromadb_integration.py
python3 04_vector_databases_dan_indexing/3_indexing_algorithms.py
```
