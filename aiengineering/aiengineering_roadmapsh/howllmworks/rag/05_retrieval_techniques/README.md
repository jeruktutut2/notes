# Modul 05: Retrieval Techniques

Teknik pengambilan dokumen (*Retrieval*) menentukan bagaimana sistem RAG menemukan potongan dokumen paling relevan untuk menjawab pertanyaan pengguna.

## Materi Pembelajaran

1. **`1_dense_semantic_retrieval.py`**
   - Dense Retrieval berbasis vektor embedding semantik.
   - Keunggulan: Menangkap konteks, sinonim, dan makna tersirat.

2. **`2_sparse_keyword_retrieval.py`**
   - Sparse Retrieval berbasis kata kunci pencarian menggunakan BM25 & TF-IDF.
   - Keunggulan: Presisi sangat tinggi untuk istilah khusus, kode produk, dan nama spesifik.

3. **`3_hybrid_search_rrf.py`**
   - Hybrid Search yang memadukan keunggulan Dense + Sparse Search.
   - Menggabungkan peringkat hasil menggunakan algoritma **Reciprocal Rank Fusion (RRF)**.

## Cara Menjalankan

```bash
python3 05_retrieval_techniques/1_dense_semantic_retrieval.py
python3 05_retrieval_techniques/2_sparse_keyword_retrieval.py
python3 05_retrieval_techniques/3_hybrid_search_rrf.py
```
