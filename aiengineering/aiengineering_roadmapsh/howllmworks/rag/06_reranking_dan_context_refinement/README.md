# Modul 06: Reranking & Context Refinement

Setelah dokumen awal diambil (*initial retrieval*), tahap Reranking dan Refinement bertugas melakukan evaluasi ulang terhadap dokumen Top-K untuk meningkatkan presisi dan menghilangkan noise.

## Materi Pembelajaran

1. **`1_cross_encoder_reranking.py`**
   - Perbedaan Bi-Encoder vs Cross-Encoder.
   - Simulasi scoring ulang dokumen Top-K menggunakan Cross-Encoder Reranker.

2. **`2_maximal_marginal_relevance.py`**
   - Algoritma MMR (Maximal Marginal Relevance) dari nol.
   - Menyeimbangkan antara relevansi terhadap query ($\lambda$) dan keberagaman hasil pencarian ($1-\lambda$).

3. **`3_context_compression_and_filtering.py`**
   - Memangkas kalimat/paragraf non-relevan dari dokumen sebelum disuapkan ke LLM untuk menghemat token dan meningkatkan performa.

## Cara Menjalankan

```bash
python3 06_reranking_dan_context_refinement/1_cross_encoder_reranking.py
python3 06_reranking_dan_context_refinement/2_maximal_marginal_relevance.py
python3 06_reranking_dan_context_refinement/3_context_compression_and_filtering.py
```
