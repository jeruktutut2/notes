# Modul 08: Generation & Grounding

Tahap akhir dalam RAG adalah menggabungkan konteks dokumen yang berhasil di-retrieve ke dalam prompt LLM secara ketat (*grounding*), mencegah halusinasi, serta memicu output terstruktur beserta sitasi sumber.

## Materi Pembelajaran

1. **`1_rag_prompt_templates.py`**
   - Perancangan System Prompt anti-halusinasi.
   - Menginjeksi konteks ke LLM dengan batasan instruksi yang tegas.

2. **`2_citation_and_source_attribution.py`**
   - Memaksa LLM memberikan sitasi `[Dokumen X]` dan kutipan kata per kata (*verbatim quote*) dari sumber referensi.

3. **`3_structured_rag_output.py`**
   - Menghasilkan output terstruktur (JSON Schema) memuat respon jawaban, ringkasan, tingkat kepercayaan (*confidence score*), dan daftar dokumen sumber.

## Cara Menjalankan

```bash
python3 08_generation_dan_grounding/1_rag_prompt_templates.py
python3 08_generation_dan_grounding/2_citation_and_source_attribution.py
python3 08_generation_dan_grounding/3_structured_rag_output.py
```
