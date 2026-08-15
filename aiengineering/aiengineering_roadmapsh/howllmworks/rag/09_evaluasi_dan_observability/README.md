# Modul 09: Evaluasi & Observability

Sistem RAG skala produksi membutuhkan pengujian kualitas secara berkelanjutan (Evaluasi) dan pemantauan performa real-time (Observabilitas & Tracing).

## Materi Pembelajaran

1. **`1_rag_triad_evaluation.py`**
   - Evaluasi **RAG Triad** berbasis LLM-as-a-Judge:
     - **Context Relevance**: Seberapa relevan dokumen yang di-retrieve?
     - **Groundedness / Faithfulness**: Seberapa akurat jawaban terhadap konteks (bebas halusinasi)?
     - **Answer Relevance**: Seberapa tepat jawaban menjawab pertanyaan pengguna?

2. **`2_logging_and_tracing.py`**
   - Tracing & logging pipeline RAG dari awal hingga akhir.
   - Merekam latensi tiap tahap (Retrieval Time, LLM Latency, Token Usage) dan skor similarity.

## Cara Menjalankan

```bash
python3 09_evaluasi_dan_observability/1_rag_triad_evaluation.py
python3 09_evaluasi_dan_observability/2_logging_and_tracing.py
```
