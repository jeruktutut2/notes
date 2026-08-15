# VECTOR DATABASES - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **Vector Databases** berdasarkan peta kurikulum resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)** dan diagram struktur referensi.

---

## 🎯 Peta Kurikulum & Diagram Topik

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                          Purpose and Functionality                      │
├─────────────────────────────────────────────────────────────────────────┤
│  • Mengapa Database Tradisional Tidak Cukup (B-Tree vs High-Dim Vector) │
│  • Direct Distance Metrics: Cosine Similarity, Dot Product, Euclidean L2│
│  • Exact Nearest Neighbor (k-NN) vs Approximate Nearest Neighbor (ANN)  │
│  • Payload & Metadata Filtering Strategies                              │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Popular Vector DBs (pick one)                       │
├─────────────────────────────────────────────────────────────────────────┤
│  • Pinecone ⭐ (Cloud-Native Serverless, Namespaces, Single-stage Hybrid)│
│  • Chroma DB (Open Source Embedded DB untuk Python / JS Prototyping)    │
│  • FAISS (In-Memory GPU-Accelerated Vector Library oleh Meta AI)        │
│  • Weaviate, LanceDB, Qdrant, Supabase (pgvector), & MongoDB Atlas      │
└─────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                       Implementing Vector Search                        │
├─────────────────────────────────────────────────────────────────────────┤
│  • Indexing Embeddings: HNSW (Multi-layer Graph), IVF (Voronoi), PQ     │
│  • Performing Similarity Search: k-NN, Pre/Post Filtering, Hybrid Search│
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Struktur Direktori Workspace

```text
vectordatabases/
├── README.md                                    # Panduan utama workspace & kurikulum
├── main.py                                      # Master Interactive CLI Runner & Test Suite
├── requirements.txt                             # Dependencies Python (pinecone, chromadb, faiss-cpu, numpy)
│
├── notes/                                       # Catatan Teori Komprehensif (Bahasa Indonesia)
│   ├── 01_purpose_and_functionality.md          # Konsep dasar, metrik jarak, ANN vs k-NN
│   ├── 02_popular_vector_dbs.md                 # Komparasi Pinecone, Chroma, FAISS, Qdrant, Weaviate, dll.
│   └── 03_implementing_vector_search.md         # Indexing algorithms (HNSW, IVF, PQ) & Hybrid Search
│
├── 01_purpose_and_functionality/                # Modul Purpose & Functionality
│   ├── 01_vector_db_vs_traditional_db.py        # Demo komparatif SQL vs Vector DB
│   ├── 02_distance_metrics_and_payloads.py      # Cosine, Dot, L2 & Payload filtering engine
│   └── README.md                                # Submodul README
│
├── 02_popular_vector_dbs/                       # Modul Popular Vector DBs
│   ├── 01_pinecone_hands_on.py                  # Pinecone Client, Serverless, upsert, metadata filter
│   ├── 02_chroma_db_hands_on.py                 # ChromaDB Persistent Client & Collections
│   ├── 03_faiss_hands_on.py                     # FAISS IndexFlatL2, IndexIVFFlat, IndexHNSW
│   ├── 04_ecosystem_comparison.py               # Ecosystem Comparison Matrix & Benchmark
│   └── README.md                                # Submodul README
│
├── 03_implementing_vector_search/               # Modul Implementing Vector Search
│   ├── 01_indexing_embeddings_hnsw_ivf.py       # Algoritma pengindeksan HNSW vs IVF vs Flat
│   ├── 02_performing_similarity_search.py      # Similarity search, Pre/Post Filter & Hybrid Search
│   └── README.md                                # Submodul README
│
└── web_visualizer/                              # Interactive Web Dashboard Visualizer
    ├── index.html                               # Dashboard UI Modern (Dark Mode Glassmorphism)
    ├── styles.css                               # Design System & Styling
    └── app.js                                   # Interactive Vector Space & HNSW Simulator
```

---

## 🚀 Cara Menjalankan Workspace

### 1. Menjalankan Master Interactive CLI Runner
Jalankan file `main.py` untuk menguji seluruh modul interaktif secara langsung dari terminal:

```bash
python3 main.py
```

Untuk menjalankan seluruh test suite otomatis:
```bash
python3 main.py --all
```

### 2. Menjalankan Standalone Python Modules
Masing-masing modul Python dapat dijalankan secara terpisah tanpa ketergantungan API key (dilengkapi mode simulasi fallback):

```bash
# 1. Vector DB vs Traditional DB
python3 01_purpose_and_functionality/01_vector_db_vs_traditional_db.py

# 2. Distance Metrics & Metadata Filtering
python3 01_purpose_and_functionality/02_distance_metrics_and_payloads.py

# 3. Pinecone Hands-On (Featured Highlighted DB)
python3 02_popular_vector_dbs/01_pinecone_hands_on.py

# 4. Chroma DB Embedded Hands-On
python3 02_popular_vector_dbs/02_chroma_db_hands_on.py

# 5. FAISS In-Memory High Performance Search
python3 02_popular_vector_dbs/03_faiss_hands_on.py

# 6. Ecosystem Comparison Matrix
python3 02_popular_vector_dbs/04_ecosystem_comparison.py

# 7. Indexing Algorithms (HNSW vs IVF vs Flat)
python3 03_implementing_vector_search/01_indexing_embeddings_hnsw_ivf.py

# 8. Similarity Search & Hybrid Dense-Sparse Search
python3 03_implementing_vector_search/02_performing_similarity_search.py
```

### 3. Membuka Interactive Web Visualizer Dashboard
Buka visualizer interaktif beresolusi tinggi di browser pilihan Anda:

```bash
python3 -m http.server 8080 --directory web_visualizer
# Buka http://localhost:8080 di browser!
```
