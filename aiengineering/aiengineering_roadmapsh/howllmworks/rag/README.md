# RAG AI ENGINEERING - Belajar dari Roadmap.sh

Proyek pembelajaran **Retrieval-Augmented Generation (RAG) AI Engineering** berdasarkan [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).
Setiap modul berisi skrip Python yang bisa langsung dijalankan beserta penjelasan teori dan konsep praktis dalam Bahasa Indonesia.

## Persiapan Environment & Install

```bash
# Menggunakan venv Python 3.9+
pyenv versions
pyenv local 3.9.18
python --version
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai tiktoken numpy chromadb pypdf
deactivate
python3 main.py
```

## Konfigurasi API Key (Opsional)

Sebagian besar modul dasar (matematika embedding, chunking, vector store in-memory, BM25, HyDE simulation, dsb.) dapat dijalankan **tanpa API Key**.
Untuk modul yang memanggil LLM atau API Embedding eksternal, Anda dapat menset environment variable berikut:

```bash
export OPENAI_API_KEY="sk-xxx-your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # atau Provider OpenAI-Compatible (Groq, Together, OpenRouter, Ollama)
export OPENAI_MODEL="gpt-4o-mini"
```

**Provider yang didukung (OpenAI-compatible):**
- OpenAI: `https://api.openai.com/v1`
- Groq: `https://api.groq.com/openai/v1`
- Together AI: `https://api.together.xyz/v1`
- OpenRouter: `https://openrouter.ai/api/v1`
- Ollama (Lokal): `http://localhost:11434/v1`

## Cara Menjalankan

Jalankan menu interaktif CLI untuk memilih modul:

```bash
source .venv/bin/activate
python3 main.py
```

---

## Daftar Modul Pembelajaran

| No | Modul | Topik & Materi |
|----|-------|----------------|
| **01** | Document Loading & Parsing | Text & Markdown Loader, PDF & HTML Parsing, Multimodal Data Prep |
| **02** | Chunking Strategies | Fixed-size & Overlap Chunking, Recursive Character Splitting, Structural & Semantic Chunking |
| **03** | Embeddings & Vectorization | Text Embeddings API, Similarity Metrics (Cosine, Dot, Euclidean), Vector Normalization & Dimensions |
| **04** | Vector Databases & Indexing | In-Memory Vector Store Custom, ChromaDB Integration, Indexing Algorithms (Flat vs HNSW/ANN) |
| **05** | Retrieval Techniques | Dense Semantic Retrieval, Sparse Keyword Retrieval (BM25), Hybrid Search (Reciprocal Rank Fusion / RRF) |
| **06** | Reranking & Context Refinement | Cross-Encoder Reranking, Maximal Marginal Relevance (MMR), Context Compression & Filtering |
| **07** | Advanced RAG Architectures | Query Transformations (Multi-Query & Sub-Query), HyDE (Hypothetical Document Embeddings), Agentic RAG & Routing |
| **08** | Generation & Grounding | Prompt Engineering RAG & Anti-Hallucination, Citation & Source Attribution, Structured RAG Output (JSON Schema) |
| **09** | Evaluasi & Observability | RAG Triad Evaluation (LLM-as-a-Judge), Logging & Tracing Pipeline Performance |

---

## Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap tahap pipeline RAG dapat dibaca di folder [notes/rag_roadmap_notes.md](notes/rag_roadmap_notes.md).
