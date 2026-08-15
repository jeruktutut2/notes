# ⚡ WHAT ARE RAGS (Retrieval-Augmented Generation) - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **What Are RAGs** berdasarkan peta kurikulum resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)** dan diagram arsitektur RAG.

---

## 🎯 Peta Kurikulum & Diagram Topik

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                                RAG Usecases                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Enterprise Knowledge Base (Q&A Dokumen SOP HR)                           │
│  • Customer Support Chatbots (Data Transaksi & Retur Real-Time)             │
│  • Codebase QA & Developer Assistant (Monorepo Search)                      │
│  • Legal & Compliance Analysis (Analisis Dokumen & Regulasi)                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            RAG vs Fine-tuning                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Sumber Pengetahuan: Memori Eksternal vs Memori Parametrik Internal       │
│  • Kemutakhiran Data: Instant Update di Vector DB vs Retrain Mahal          │
│  • Pengurangan Halusinasi & Transparansi Sitasi Sumber                      │
│  • Matriks Evaluasi & Decision Tree Arsitektur                              │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│...                           Implementing RAG                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ ┌────────────┐  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌────────────┐ │
│ │  Chunking  │─►│ Embedding │─►│ Vector DB │─►│ Retrieval │─►│ Generation │ │
│ └────────────┘  └───────────┘  └───────────┘  └───────────┘  └────────────┘ │
│                                                                             │
│                        Ways of Implementing RAG                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │                          Using SDKs Directly                            │ │
│ ├────────────────────────────────────┬────────────────────────────────────┤ │
│ │ LangChain                          │ LlamaIndex                         │ │
│ ├────────────────────────────────────┼────────────────────────────────────┤ │
│ │ Haystack                           │ RAGFlow                            │ │
│ └────────────────────────────────────┴────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Struktur Direktori Workspace

```text
whatarerags/
├── README.md                                    # Panduan utama workspace & kurikulum
├── main.py                                      # Master Interactive CLI Runner & Test Suite
├── requirements.txt                             # Dependencies Python (numpy, faiss-cpu, chromadb, langchain, llama-index)
│
├── notes/                                       # Catatan Teori Komprehensif (Bahasa Indonesia)
│   ├── 01_rag_usecases.md                       # Enterprise QA, Support, Codebase, Legal
│   ├── 02_rag_vs_finetuning.md                  # Matriks perbandingan RAG vs Fine-Tuning & Decision Tree
│   ├── 03_implementing_rag.md                   # Breakdown 5 tahapan RAG (Chunking ➔ Embedding ➔ VectorDB ➔ Retrieval ➔ Generation)
│   └── 04_ways_of_implementing.md               # Analisis komparatif SDKs, LangChain, LlamaIndex, Haystack, RAGFlow
│
├── 01_rag_usecases/                             # Modul 01: RAG Usecases
│   ├── 01_rag_usecases_demo.py                  # Simulasi skenario RAG multi-domain
│   └── README.md                                # Submodul README
│
├── 02_rag_vs_finetuning/                        # Modul 02: RAG vs Fine-Tuning
│   ├── 01_rag_vs_finetuning_matrix.py           # Benchmark perbandingan & evaluator keputusan arsitektur
│   └── README.md                                # Submodul README
│
├── 03_implementing_rag/                         # Modul 03: Implementing RAG Pipeline
│   ├── 01_chunking_strategies.py                # Fixed-size, Sentence, & Recursive Character Chunking
│   ├── 02_embedding_generation.py               # Generasi Dense Vector Embedding
│   ├── 03_vector_database_storage.py            # Penyimpanan Vector & Payload Metadata Indexing
│   ├── 04_retrieval_process.py                  # Similarity Search, Hybrid Search (Dense + BM25) & Filter
│   ├── 05_generation_synthesis.py               # Augmented Prompt System, Grounded Generation & Sitasi
│   └── README.md                                # Submodul README
│
├── 04_ways_of_implementing/                     # Modul 04: Ways of Implementing RAG
│   ├── 01_using_sdks_directly.py                # Custom RAG Pipeline tanpa framework pihak ketiga (Pure Python)
│   ├── 02_langchain_rag.py                      # Implementasi RAG dengan LangChain Framework
│   ├── 03_llamaindex_rag.py                     # Implementasi RAG dengan LlamaIndex Framework
│   ├── 04_haystack_and_ragflow.py               # Overview Haystack (Nodes/Pipelines) & RAGFlow (Agentic Parsing)
│   └── README.md                                # Submodul README
│
└── web_visualizer/                              # Interactive Web Dashboard Visualizer
    ├── index.html                               # Modern UI Dashboard (Dark Mode Glassmorphism)
    ├── styles.css                               # Design System & Styling (Amber Gold Palette)
    └── app.js                                   # Interactive Chunking Lab, Pipeline Simulator, & Code Playground
```

---

## 🚀 Cara Menjalankan Workspace

### 1. Menjalankan Master Interactive CLI Runner
Jalankan file `main.py` untuk memilih dan menguji modul secara interaktif dari terminal:

```bash
python3 main.py
```

Untuk menjalankan seluruh modul test suite secara otomatis:
```bash
python3 main.py --all
```

### 2. Menjalankan Standalone Python Script
Masing-masing modul Python dapat dijalankan secara terpisah:

```bash
# 1. RAG Usecases
python3 01_rag_usecases/01_rag_usecases_demo.py

# 2. RAG vs Fine-tuning Matrix
python3 02_rag_vs_finetuning/01_rag_vs_finetuning_matrix.py

# 3. Chunking Strategies
python3 03_implementing_rag/01_chunking_strategies.py

# 4. Vector DB Storage & Indexing
python3 03_implementing_rag/03_vector_database_storage.py

# 5. RAG Pipeline: Pure Python / Direct SDKs
python3 04_ways_of_implementing/01_using_sdks_directly.py
```

### 3. Membuka Interactive Web Visualizer
Buka file `web_visualizer/index.html` di browser favorit Anda atau jalankan HTTP server lokal:

```bash
python3 -m http.server 8080 --directory web_visualizer
```
Akses di browser: `http://localhost:8080`
