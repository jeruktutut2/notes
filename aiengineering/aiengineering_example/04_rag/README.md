# 📘 Modul 4 — RAG (Retrieval-Augmented Generation)

Modul ini mempelajari arsitektur **RAG (Retrieval-Augmented Generation)** untuk membuat AI mampu menjawab pertanyaan tentang dokumen internal perusahaan yang tidak pernah ada di data pelatihan publik LLM.

---

## 🏗️ Arsitektur RAG End-to-End

```
Fase Indexing:
[Dokumen .txt] -> [Chunking] -> [Embedding Engine (nomic-embed-text)] -> [Vector Database (ChromaDB)]

Fase Query:
[User Query] -> [Embedding Query] -> [Vector Search (Similarity)] -> [Inject Context to System Prompt] -> [LLM Response]
```

---

## 🛠️ Tooling & Perpustakaan
- **Embedding Model**: `nomic-embed-text` via Ollama API
- **Vector Database**: `ChromaDB` (Local Vector Database)
- **Chat Model**: `gemma3:4b`

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

### 1. Unduh Model Embedding & Chat
```bash
ollama pull nomic-embed-text
ollama pull gemma3:4b
```

### 2. Eksekusi Program
```bash
python 04_rag/main.py
```
