# EMBEDDING MODELS - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **Embedding Models** berdasarkan peta kurikulum resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)**.

Workspace ini disusun khusus sesuai dengan arsitektur model embedding (Proprietary Models vs Open Source Models) yang mencakup vendor utama dunia AI Engineering.

---

## 🎯 Peta Arsitektur Pembelajaran

```text
               ┌─────────────────────────────────────────────────┐
               │                Proprietary Models               │
               ├─────────────────────────────────────────────────┤
               │  • Open AI Embeddings API (v3 Matryoshka)       │
               │  • Gemini Embedding (Google Task-Aware 004)     │
               │  • Cohere (Embed v3 Int8/Binary Compression)    │
               └─────────────────────────────────────────────────┘
                                       │
                                       │
               ┌─────────────────────────────────────────────────┐
               │                Open Source Models               │
               ├─────────────────────────────────────────────────┤
               │  • Sentence Transformers (all-MiniLM-L6-v2)     │
               │  • Models on Hugging Face (BAAI bge-small-en)   │
               │  • Jina (jina-embeddings 8k & Late Chunking)    │
               └─────────────────────────────────────────────────┘
```

---

## 📂 Struktur Direktori Workspace

```text
embedingmodels/
├── README.md                                 # Panduan utama workspace & kurikulum
├── main.py                                   # Master CLI Interactive Runner & Test Suite
├── requirements.txt                           # Dependencies Python (NumPy, PyTorch, APIs)
│
├── notes/                                    # Catatan Teori Komprehensif (Bahasa Indonesia)
│   ├── 01_proprietary_models.md              # OpenAI, Gemini, Cohere API & Architecture
│   ├── 02_open_source_models.md              # Sentence Transformers, HF Hub, Jina AI
│   └── 03_embedding_comparison_matrix.md     # Benchmarks MTEB, Latency, Cost, Context Length
│
├── 01_proprietary_models/                    # Modul Standalone Proprietary Models
│   ├── 01_openai_embeddings_api.py           # OpenAI API & Dimension Truncation
│   ├── 02_gemini_embedding_api.py            # Gemini Embedding API & Task Types
│   ├── 03_cohere_embed_api.py                # Cohere Embed API & Compression Modes
│   └── README.md                             # Submodul README
│
├── 02_open_source_models/                    # Modul Standalone Open Source Models
│   ├── 01_sentence_transformers.py           # Sentence-Transformers Python SDK & Batching
│   ├── 02_models_on_huggingface.py           # HuggingFace Transformers, AutoModel & Pooling
│   ├── 03_jina_embeddings.py                 # Jina Embeddings 8k Context & Late Chunking
│   └── README.md                             # Submodul README
│
├── 03_comparison_and_benchmarks/             # Modul Benchmark & Pemilihan Model
│   ├── 01_model_comparison_benchmark.py     # Side-by-side benchmark (Speed, Memory, Similarity)
│   └── README.md                             # Submodul README
│
└── web_visualizer/                           # Interactive Web Playground & Visualizer
    ├── index.html                            # Dashboard UI Modern (Dark Glassmorphism)
    ├── styles.css                            # Design System & Animation
    └── app.js                                # Interactive Simulators, Vector Math, Comparison Matrix
```

---

## 🚀 Cara Menggunakan Workspace

### 1. Menjalankan Master CLI Interactive Runner
Jalankan file `main.py` untuk menguji seluruh modul interaktif secara langsung dari terminal:

```bash
python3 main.py
```

### 2. Menjalankan Standalone Python Modules
Masing-masing modul Python dapat dijalankan secara terpisah tanpa ketergantungan API key (dilengkapi mode simulasi fallback):

```bash
# 1. OpenAI Embeddings API & Matryoshka Truncation
python3 01_proprietary_models/01_openai_embeddings_api.py

# 2. Google Gemini Task-Aware Embedding
python3 01_proprietary_models/02_gemini_embedding_api.py

# 3. Cohere Int8 / Binary Compression Embed
python3 01_proprietary_models/03_cohere_embed_api.py

# 4. Sentence-Transformers Local Fast Inference
python3 02_open_source_models/01_sentence_transformers.py

# 5. Hugging Face Models & Manual Mean Pooling
python3 02_open_source_models/02_models_on_huggingface.py

# 6. Jina AI 8k Context Window & Late Chunking
python3 02_open_source_models/03_jina_embeddings.py

# 7. Model Comparison Benchmark
python3 03_comparison_and_benchmarks/01_model_comparison_benchmark.py
```

### 3. Membuka Interactive Web Visualizer Dashboard
Untuk mengeplorasi visualizer interaktif beresolusi tinggi di browser:

```bash
python3 -m http.server 8080 --directory web_visualizer
# Buka http://localhost:8080 di browser pilihan Anda!
```
