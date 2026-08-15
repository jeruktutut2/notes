# Vector Databases

> Bagian dari roadmap [AI Engineer - roadmap.sh](https://roadmap.sh/ai-engineer)

Vector Database adalah jenis database yang dioptimalkan untuk menyimpan, mengindeks, dan melakukan query terhadap **high-dimensional vectors** (embedding). Berbeda dengan database tradisional (SQL/NoSQL) yang bekerja dengan data terstruktur, vector database memungkinkan **pencarian berdasarkan kemiripan semantik** — sangat penting untuk aplikasi AI modern seperti RAG, recommendation system, dan semantic search.

---

## 📚 Apa yang Dipelajari

### 1. Konsep Dasar (Core Concepts)

| Topik | Deskripsi |
|-------|-----------|
| **Apa itu Vector Database** | Memahami mengapa database tradisional (SQL/NoSQL) tidak cukup untuk AI dan bagaimana vector database memungkinkan pencarian semantik |
| **Apa itu Embeddings** | Cara data (teks, gambar, audio) dikonversi menjadi vektor numerik yang menangkap makna semantik |
| **Embedding Models** | Cara menghasilkan vektor menggunakan API (OpenAI, Cohere, Gemini) atau model open-source (Sentence Transformers, HuggingFace) |
| **Vector Similarity** | Mekanisme mengukur seberapa dekat dua vektor satu sama lain (Cosine Similarity, Euclidean Distance, Dot Product) |

### 2. Implementasi Teknis (Technical Implementation)

| Topik | Deskripsi |
|-------|-----------|
| **Indexing** | Cara data diorganisir dalam vector database untuk pencarian cepat dan efisien (HNSW, IVF, dll.) |
| **Chunking** | Strategi memecah dokumen besar menjadi potongan-potongan kecil sebelum di-embed dan disimpan |
| **Performing Similarity Search** | Proses query database untuk menemukan "nearest neighbors" atau item yang paling mirip secara semantik |
| **Implementing Vector Search** | Mengintegrasikan proses pencarian ke dalam alur aplikasi |

### 3. Popular Vector Databases

Pilih salah satu atau beberapa untuk dipelajari secara hands-on:

| Database | Tipe | Catatan |
|----------|------|---------|
| **Chroma** | Open-source, embedded | Ringan, cocok untuk prototyping dan development lokal |
| **Pinecone** | Managed cloud service | Fully managed, mudah digunakan, scalable |
| **Weaviate** | Open-source | Mendukung hybrid search (vector + keyword) |
| **FAISS** | Library (Facebook AI) | Sangat cepat, cocok untuk riset dan large-scale search |
| **LanceDB** | Open-source, embedded | Serverless, berbasis columnar format |
| **Qdrant** | Open-source | Performa tinggi, filtering canggih |
| **Supabase (pgvector)** | PostgreSQL extension | Cocok jika sudah menggunakan PostgreSQL |
| **MongoDB Atlas** | Cloud service | Vector search terintegrasi dengan MongoDB |

### 4. RAG (Retrieval-Augmented Generation)

Vector database sangat erat kaitannya dengan arsitektur RAG:

| Topik | Deskripsi |
|-------|-----------|
| **Apa itu RAG** | Arsitektur yang menggabungkan LLM dengan sistem retrieval untuk menjawab pertanyaan berdasarkan data privat |
| **RAG Use Cases** | Kapan dan mengapa menggunakan RAG vs fine-tuning |
| **Retrieval Process** | Bagaimana sistem mengidentifikasi dan mengambil konteks relevan untuk meningkatkan respons AI |
| **RAG Pipeline** | End-to-end pipeline: load → chunk → embed → store → retrieve → generate |

---

## 🗺️ Alur Belajar

```
1. Pahami Konsep Embedding
   ↓
2. Pelajari Vector Similarity (Cosine, Euclidean, Dot Product)
   ↓
3. Pilih & Setup Vector Database (misal: Chroma atau Pinecone)
   ↓
4. Praktik: Buat Embedding dari Teks (OpenAI / Sentence Transformers)
   ↓
5. Simpan Embedding ke Vector DB
   ↓
6. Lakukan Similarity Search
   ↓
7. Pelajari Chunking Strategies
   ↓
8. Bangun RAG Pipeline Sederhana
   ↓
9. Optimasi: Indexing, Filtering, Hybrid Search
```

---

## 🔑 Konsep Penting

### Embeddings
- Representasi numerik dari data (teks, gambar, audio) dalam ruang berdimensi tinggi
- Teks yang mirip secara makna akan memiliki vektor yang berdekatan
- Dihasilkan oleh model seperti `text-embedding-ada-002` (OpenAI), `all-MiniLM-L6-v2` (Sentence Transformers)

### Similarity Metrics
- **Cosine Similarity**: Mengukur sudut antara dua vektor (paling umum digunakan)
- **Euclidean Distance (L2)**: Mengukur jarak lurus antara dua titik vektor
- **Dot Product**: Mengukur proyeksi satu vektor ke vektor lain

### Chunking Strategies
- **Fixed-size chunks**: Potong teks setiap N karakter/token
- **Semantic chunking**: Potong berdasarkan paragraf atau section
- **Overlapping chunks**: Chunks yang saling tumpang tindih untuk menjaga konteks
- **Recursive character splitting**: Strategi splitting bertingkat (paragraf → kalimat → kata)

### Indexing Algorithms
- **HNSW (Hierarchical Navigable Small World)**: Cepat, akurat, banyak digunakan
- **IVF (Inverted File Index)**: Membagi vektor ke dalam cluster
- **PQ (Product Quantization)**: Kompresi vektor untuk menghemat memori
- **Flat/Brute Force**: Pencarian eksak, lambat untuk data besar

---

## 🚀 Quick Start

### 1. Buat Virtual Environment

```bash
pyenv versions
pyenv local 3.9.18
python --version
python -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
pip install --upgrade pip
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Jalankan Modul

Jalankan menu interaktif CLI:

```bash
python main.py
```

Atau jalankan skrip secara individual:

```bash
# Modul 1: Embeddings
python 01-embeddings/1_apa_itu_embedding.py
python 01-embeddings/2_embedding_models.py

# Modul 2: Similarity Search
python 02-similarity/1_similarity_metrics.py
python 02-similarity/2_nearest_neighbor_search.py

# Modul 3: Vector Databases (ChromaDB)
python 03-vector-databases/1_chromadb_dasar.py
python 03-vector-databases/2_chromadb_persistent.py

# Modul 4: Chunking Strategies
python 04-chunking/1_chunking_strategies.py

# Modul 5: RAG Pipeline
python 05-rag-pipeline/1_rag_pipeline.py

# Modul 6: Optimization
python 06-optimization/1_optimization_techniques.py
```

> **Note:** Setiap file Python bisa dijalankan secara independen atau melalui `main.py`. Baca README.md di setiap folder untuk teori lengkap sebelum menjalankan kode.

---

## 📂 Struktur Folder

Setiap modul berisi **README.md** (teori) dan **file Python** (praktik hands-on):

```
vectordbs/
├── README.md                       # File ini
├── requirements.txt                # Dependencies
├── main.py                         # Menu CLI utama untuk memilih modul
│
├── 01-embeddings/                  # Belajar tentang embeddings
│   ├── README.md                   #   Teori: apa itu embedding, model, dimensi
│   ├── 1_apa_itu_embedding.py      #   Praktik: membuat & membandingkan embedding
│   └── 2_embedding_models.py       #   Praktik: sentence transformers, batch, multilingual
│
├── 02-similarity/                  # Similarity metrics & search
│   ├── README.md                   #   Teori: cosine, euclidean, dot product
│   ├── 1_similarity_metrics.py     #   Praktik: membandingkan metrics, semantic search
│   └── 2_nearest_neighbor_search.py#   Praktik: brute force, IVF, FAISS indexes
│
├── 03-vector-databases/            # Hands-on dengan vector DB
│   ├── README.md                   #   Teori: ChromaDB, Pinecone, FAISS, dll
│   ├── 1_chromadb_dasar.py         #   Praktik: CRUD, query, metadata filtering
│   └── 2_chromadb_persistent.py    #   Praktik: persistent storage, load ulang data
│
├── 04-chunking/                    # Chunking strategies
│   ├── README.md                   #   Teori: fixed-size, sentence, paragraph, recursive
│   └── 1_chunking_strategies.py    #   Praktik: semua strategi chunking + perbandingan
│
├── 05-rag-pipeline/                # Membangun RAG pipeline
│   ├── README.md                   #   Teori: ingestion, retrieval, generation
│   └── 1_rag_pipeline.py           #   Praktik: end-to-end RAG dengan ChromaDB
│
└── 06-optimization/                # Indexing & optimization
    ├── README.md                   #   Teori: hybrid search, reranking, caching
    └── 1_optimization_techniques.py#   Praktik: hybrid search, cross-encoder, caching
```

---

## 🔗 Referensi

- [AI Engineer Roadmap - roadmap.sh](https://roadmap.sh/ai-engineer)
- [Pinecone Learning Center](https://www.pinecone.io/learn/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FAISS Wiki](https://github.com/facebookresearch/faiss/wiki)
- [Weaviate Documentation](https://weaviate.io/developers/weaviate)
- [LangChain - Vector Stores](https://python.langchain.com/docs/modules/data_connection/vectorstores/)
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
