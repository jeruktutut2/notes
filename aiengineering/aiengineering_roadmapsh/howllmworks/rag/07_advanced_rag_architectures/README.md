# Modul 07: Advanced RAG Architectures

Arsitektur RAG tingkat lanjut meningkatkan akurasi retrieval dengan memanipulasi query pengguna, menghasilkan dokumen hipotetis, dan membuat keputusan routing dinamis.

## Materi Pembelajaran

1. **`1_query_transformations.py`**
   - Query Rewriting: Memperjelas pertanyaan yang ambigu.
   - Multi-Query Generation: Menghasilkan 3 variasi pertanyaan untuk memperluas jangkauan retrieval.
   - Sub-Query Decomposition: Memecah pertanyaan kompleks menjadi beberapa pertanyaan kecil.

2. **`2_hyde_hypothetical_document_embeddings.py`**
   - HyDE Architecture: Menggunakan LLM untuk membuat *hypothetical document* (jawaban contoh), lalu meng-embed dokumen tersebut untuk mencari dokumen nyata di DB.

3. **`3_agentic_rag_and_routing.py`**
   - Router RAG & Agentic decision: Memilih sumber retrieval secara otomatis (seperti Vector DB Produk vs DB Regulasi vs Web Search).

## Cara Menjalankan

```bash
python3 07_advanced_rag_architectures/1_query_transformations.py
python3 07_advanced_rag_architectures/2_hyde_hypothetical_document_embeddings.py
python3 07_advanced_rag_architectures/3_agentic_rag_and_routing.py
```
