# Implementasi Point 6: RAG (Retrieval-Augmented Generation)

Modul ini berisi implementasi RAG — teknik menghubungkan LLM dengan sumber pengetahuan
eksternal agar jawaban lebih akurat dan up-to-date.

## Daftar File
1. `1_embedding_dan_similarity.py`: Membuat embedding dan menghitung cosine similarity (tanpa API key).
2. `2_simple_rag_pipeline.py`: RAG pipeline sederhana dari nol (retrieve → augment → generate).
3. `3_rag_with_chunking.py`: Chunking dokumen panjang + RAG pipeline lengkap.

## Urutan Eksekusi

```bash
python 1_embedding_dan_similarity.py   # Tidak butuh API key
python 2_simple_rag_pipeline.py
python 3_rag_with_chunking.py
```

### Cara Instalasi Library
```bash
pip install openai numpy
```
