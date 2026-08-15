# 02. RAG and Dynamic Filters

Modul ini mempelajari integrasi *Retrieval-Augmented Generation (RAG)* dan *Dynamic Metadata Filtering* dalam penyusunan konteks dinamis.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. RAG Pipeline Architecture
- **Indexing Phase**: Chunking dokumen (Sentence/Semantic Splitter), Embedding generation, dan Penyimpanan di Vector Database.
- **Retrieval Phase**: Dense Retrieval (Vector Similarity Cosine/Dot Product) + Sparse Retrieval (BM25 Keyword Search) = **Hybrid Search**.
- **Re-Ranking Phase**: Menggunakan model Cross-Encoder (seperti Cohere Re-rank atau BGE-Reranker) untuk menyaring top-K dokumen terbaik sebelum di-inject ke prompt.

### 2. Dynamic Metadata Filtering
- **Definisi**: Memfilter ruang pencarian dokumen berdasarkan atribut metadata (misal: `tenant_id`, `created_year`, `access_level`, `category`) sebelum melakukan vektor pencarian.
- **Mengapa Penting?**:
  - Mencegah percampuran data antar perusahaan (*Multi-Tenant Isolation*).
  - Meningkatkan akurasi pencarian (*Context Precision*) dengan membuang 90% dokumen yang tidak relevan secara kontekstual.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi Hybrid Search + Dynamic Metadata Filter dalam menyusun dokumen RAG ke Context Window.
