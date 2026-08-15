# Submodul 02: Open Source Embedding Models

Submodul ini mencakup implementasi praktis penggunaan model-model open-source secara lokal:

1. **`01_sentence_transformers.py`**:
   - Penggunaan framework `sentence-transformers`.
   - Loading model lokal (`all-MiniLM-L6-v2`, `bge-small-en-v1.5`), batch encoding, & cosine similarity.
2. **`02_models_on_huggingface.py`**:
   - Ekstraksi manual embeddings dari Hugging Face Hub menggunakan `AutoTokenizer` dan `AutoModel`.
   - Implementasi PyTorch `mean_pooling` dan `cls_pooling`.
3. **`03_jina_embeddings.py`**:
   - Penggunaan Jina AI Embeddings v2/v3 secara lokal/API.
   - Penanganan dokumen panjang dengan 8,192 context window & konsep late chunking.

> Note: Semua script dilengkapi fallback/simulasi PyTorch & NumPy sehingga dapat berjalan di CPU lingkungan manapun secara instan.
