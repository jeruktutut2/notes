# WHAT ARE EMBEDDINGS - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **What are Embeddings** berdasarkan peta kurikulum resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)**.

Workspace ini merangkum seluruh fondasi matematis vektor, metrik jarak, serta 4 kasus penggunaan utama dari embeddings dalam dunia AI Engineering.

---

## 🎯 Peta Materi Pembelajaran

```text
whatareembedings/
├── README.md                            # Dokumentasi utama workspace
├── main.py                              # Master CLI Interactive Runner & Test Suite
├── requirements.txt                      # Dependencies Python (NumPy, Scikit-Learn)
│
├── notes/                               # Catatan Pembelajaran Komprehensif (Bahasa Indonesia)
│   ├── 01_embedding_fundamentals.md     # Ruang Vektor, Dense vs Sparse, Normalisasi & Metrik Jarak
│   ├── 02_semantic_search.md            # Semantic vs Keyword, Chunking, Bi/Cross-Encoder, Hybrid RRF
│   ├── 03_data_classification.md        # Feature Embeddings, Logistic Regression, Zero-Shot, K-Means
│   ├── 04_recommendation_systems.md     # Content-Based Filtering, User Profile Vector, Top-N Ranking
│   ├── 05_anomaly_detection.md          # Centroid Distance, OOD Guardrails LLM, KNN Log Outlier
│   └── 06_embeddings_synthesis.md       # Matriks Sintesis Panduan Strategis AI Engineer
│
├── 01_embedding_fundamentals/           # Subtopik 1: Embedding Fundamentals
│   ├── 01_vector_space_and_math.py       # Teks ke Vektor, Vektor Math (Raja - Pria + Wanita = Ratu)
│   ├── 02_distance_metrics.py           # Metrik Cosine, Dot Product, Euclidean (L2), Manhattan (L1)
│   ├── 03_normalization_and_dimensions.py# L2 Normalization & Matryoshka Dimension Truncation
│   └── README.md
│
├── 02_semantic_search/                  # Subtopik 2: Semantic Search
│   ├── 01_keyword_vs_semantic_search.py # Lexical Search vs Vector Semantic Search
│   ├── 02_chunking_and_embedding_pipeline.py # Fixed Chunking & Semantic Vector Index Pipeline
│   ├── 03_hybrid_search_bm25_dense.py   # Hybrid Search (BM25 + Vector) via Reciprocal Rank Fusion
│   └── README.md
│
├── 03_data_classification/              # Subtopik 3: Data Classification
│   ├── 01_embedding_intent_classifier.py# Customer Intent Classifier (Embedding + Logistic Regression)
│   ├── 02_zero_shot_classification.py   # Zero-Shot Classification tanpa training data
│   ├── 03_semantic_clustering_kmeans.py # Topic Modeling & Clustering Otomatis dengan K-Means
│   └── README.md
│
├── 04_recommendation_systems/           # Subtopik 4: Recommendation Systems
│   ├── 01_content_based_recommender.py  # Item-to-Item Content Filtering produk
│   ├── 02_user_profile_vector_aggregation.py # User Vector Aggregation berbasis weighted history
│   ├── 03_top_n_item_ranking.py         # Top-N Ranking (Similarity + Popularity Boost)
│   └── README.md
│
├── 05_anomaly_detection/                # Subtopik 5: Anomaly Detection
│   ├── 01_centroid_distance_detector.py # Deteksi Transaksi Anomali via Jarak ke Centroid
│   ├── 02_ood_query_guardrail.py        # LLM Guardrail memblokir Query OOD & Prompt Injection
│   ├── 03_log_event_outlier_scorer.py   # Outlier Scorer Log Event Real-Time dengan KNN
│   └── README.md
│
└── web_visualizer/                      # Interactive Web Visualizer Dashboard
    ├── index.html                       # Modern Dark-Mode Glassmorphism UI
    ├── styles.css                       # Design System & Styling
    └── app.js                           # Interactive Vector Math & Visual Simulators
```

---

## 🚀 Cara Menggunakan Workspace

### 1. Menjalankan Master CLI Runner
Jalankan file master CLI untuk mengakses seluruh modul pembelajaran secara interaktif:

```bash
python3 main.py
```

### 2. Menjalankan Modul Standalone
Setiap script Python bersifat standalone dan dapat dijalankan langsung:

```bash
# Contoh 1: Kalkulator Metrik Jarak
python3 01_embedding_fundamentals/02_distance_metrics.py

# Contoh 2: Hybrid Search RRF
python3 02_semantic_search/03_hybrid_search_bm25_dense.py

# Contoh 3: Zero-Shot Text Classifier
python3 03_data_classification/02_zero_shot_classification.py

# Contoh 4: System Rekomendasi
python3 04_recommendation_systems/01_content_based_recommender.py

# Contoh 5: LLM Guardrail Out-of-Distribution
python3 05_anomaly_detection/02_ood_query_guardrail.py
```

### 3. Membuka Interactive Web Visualizer
Buka file `web_visualizer/index.html` langsung di browser Anda atau jalankan HTTP server:

```bash
python3 -m http.server 8080 --directory web_visualizer
# Buka http://localhost:8080 di browser
```
