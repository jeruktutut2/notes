# Submodul 01: Proprietary Embedding Models

Submodul ini mencakup implementasi praktis penggunaan API embedding komersial dari vendor-vendor utama AI:

1. **`01_openai_embeddings_api.py`**:
   - Penggunaan OpenAI SDK v1.x (`text-embedding-3-small`, `text-embedding-3-large`).
   - Fitur Matryoshka dimension truncation (memotong dimensi vektor).
2. **`02_gemini_embedding_api.py`**:
   - Penggunaan Google GenAI SDK (`text-embedding-004`).
   - Penerapan parameter `task_type` (`RETRIEVAL_DOCUMENT`, `RETRIEVAL_QUERY`, `SEMANTIC_SIMILARITY`).
3. **`03_cohere_embed_api.py`**:
   - Penggunaan Cohere SDK v2 (`embed-multilingual-v3.0`).
   - Penerapan tipe kompresi (`float`, `int8`, `ubyte`) dan `input_type`.

> Note: Semua script dilengkapi dengan mode simulasi fallback (mocking) sehingga dapat dijalankan secara instan tanpa perlu API key nyata!
