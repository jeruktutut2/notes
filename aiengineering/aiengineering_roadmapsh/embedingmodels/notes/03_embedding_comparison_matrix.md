# Matriks Perbandingan & Panduan Keputusan: Embedding Models

Dokumen ini menyajikan matriks perbandingan komprehensif antara **Proprietary Embedding Models** dan **Open Source Embedding Models** sebagai panduan pengambilan keputusan teknis bagi AI Engineer.

---

## 📊 Comprehensive Model Decision Matrix

| Model Name | Kategori | Vendor / Source | Dimensi Vektor | Max Context (Tokens) | Biaya per 1M Tokens | MTEB Score (Avg) | Tipe Deploy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **OpenAI `text-embedding-3-small`** | Proprietary | OpenAI | 1,536 (atau 512) | 8,191 | $0.02 | ~62.3 | Cloud API |
| **OpenAI `text-embedding-3-large`** | Proprietary | OpenAI | 3,072 (atau 1024) | 8,191 | $0.13 | ~64.6 | Cloud API |
| **Gemini `text-embedding-004`** | Proprietary | Google | 768 (atau 256) | 2,048 | $0.025 | ~63.8 | Cloud API |
| **Cohere `embed-multilingual-v3.0`** | Proprietary | Cohere | 1,024 | 512 | $0.10 | ~64.1 | Cloud API / VPC |
| **Sentence-Transformers `all-MiniLM-L6-v2`** | Open Source | UKPLab | 384 | 256 | $0.00 (Self-Host) | ~56.3 | Local / Edge / CPU |
| **BAAI `bge-small-en-v1.5`** | Open Source | Hugging Face | 384 | 512 | $0.00 (Self-Host) | ~62.1 | Local / Server GPU |
| **Jina `jina-embeddings-v2-base-en`** | Open Source | Jina AI | 768 | 8,192 | $0.00 (Self-Host) | ~60.4 | Local / Docker / Cloud |

---

## ⚖️ Trade-off Analysis: Proprietary vs Open Source

```text
               PROPRIETARY MODELS                  OPEN SOURCE MODELS
           (OpenAI, Gemini, Cohere)            (Sentence-Transformers, HF, Jina)
     ┌──────────────────────────────────┐  ┌──────────────────────────────────┐
     │ + No GPU Hardware Costs          │  │ + Total Data Privacy & On-Prem   │
     │ + Ultra High Dimension & Accuracy│  │ + Zero Per-Token API Costs       │
     │ + Managed SLA & Elasticity       │  │ + Fine-Tuning Capability         │
     │ - Dependency on Vendor (Lock-in) │  │ - Requires GPU Memory (VRAM)     │
     │ - Data Privacy Concerns (Cloud)  │  │ - Engineering Overhead & Maint   │
     └──────────────────────────────────┘  └──────────────────────────────────┘
```

---

## 🎯 Strategic Recommendation Framework

### Kapan Memilih Proprietary Models?
1. **Startup / Prototype Cepat**: Menginginkan time-to-market paling cepat tanpa mengurus server.
2. **Kebutuhan Multilingual Ekstrem**: Cohere `embed-multilingual-v3.0` unggul dalam menangani pencarian lintas bahasa.
3. **Fleksibilitas Penyimpanan DB**: Memanfaatkan Matryoshka dimension truncation OpenAI `text-embedding-3-small` untuk memotong dimensi ke 512 demi menghemat indeks memori Vector DB.

### Kapan Memilih Open Source Models?
1. **Regulasi Ketat (Kesehatan, Keuangan, Militer)**: Teks berisi PII (Personally Identifiable Information) yang dilarang dikirim ke Cloud API.
2. **Volume Teks Raksasa (Terabytes)**: Pemprosesan batch jutaan dokumen di mana biaya API per-token akan menjadi sangat mahal.
3. **Offline / Low-Latency Edge Computing**: Aplikasi mobile atau desktop yang butuh ekstraksi embedding tanpa koneksi internet (`all-MiniLM-L6-v2`).
4. **Dokumen PDF Panjang (Long Context)**: Menggunakan `jina-embeddings-v2` yang mendukung 8k context window tanpa terpotong (*truncated*).
