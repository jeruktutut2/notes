# 04 - Observability Tools (LangSmith, Langfuse, Helicone, Arize AI)

## Overview
Ekosistem LLM Observability memiliki berbagai alat platform profesional. Berdasarkan roadmap.sh AI Engineer, 4 alat utama yang paling luas digunakan di industri adalah **LangSmith**, **Langfuse**, **Helicone**, dan **Arize AI / Phoenix**.

---

## 1. Perbandingan Platform Observability

| Tool | Lisensi / Deploy | Pendekatan Observability | Fitur Unggulan | Target Pengguna Utama |
|------|------------------|-------------------------|----------------|----------------------|
| **LangSmith** | Cloud SaaS (Proprietary by LangChain) | SDK / Callback Tracing | Integrasi erat dengan LangChain/LangGraph, Dataset Evals, Prompt Playground | Pengembang yang menggunakan ekosistem LangChain |
| **Langfuse** | Open-Source / Self-Hosted & SaaS | SDK Tracing & API | Open-source, Trace visualizer modular, Prompt Management, Analytics Biaya | Tim yang menginginkan kontrol penuh & self-hosting |
| **Helicone** | Proxy Gateway / Open-Source | HTTP Proxy (Smart Gateway) | Tanpa perlu ubah kode SDK (cukup ubah `base_url`), Caching, Rate limiting | Tim yang ingin observability instan tanpa refactoring kode |
| **Arize AI / Phoenix** | Open-Source & Enterprise SaaS | OpenTelemetry / ML Monitoring | Embedding Visualization, Drift Analysis, Automated RAG Evals, Cluster Analysis | ML Engineers & Data Scientists |

---

## 2. LangSmith (LangChain Ecosystem)

Developed by LangChain, LangSmith terintegrasi secara seamless melalui tracer callbacks:

### Karakteristik Utama:
- Automatic tracing hanya dengan menyetel environment variables:
  ```bash
  export LANGCHAIN_TRACING_V2="true"
  export LANGCHAIN_API_KEY="ls__..."
  ```
- **Runs & Chains Viewer**: Visualisasi pohon eksekusi Agent, Tool, dan Chain.
- **Dataset & Testing**: Mengubah log produksi yang bermasalah menjadi test suite otomatis dengan 1 klik.

---

## 3. Langfuse (Open-Source LLM Engineering Platform)

Langfuse menawarkan platform open-source yang sangat populer dengan arsitektur SDK modern:

### Karakteristik Utama:
- Mendukung Python, TypeScript, dan OpenAI SDK wrapper.
- **Prompt Management**: Melakukan versioning prompt di UI Langfuse dan mengambilnya via SDK secara dinamis tanpa perlu deploy ulang aplikasi.
- **Score & Evaluation**: Menyimpan skor dari LLM-as-a-Judge atau feedback user secara terstruktur.

---

## 4. Helicone (Proxy-Based Gateway)

Helicone bekerja di layer jaringan sebagai reverse proxy untuk OpenAI, Anthropic, dan provider lainnya:

### Karakteristik Utama:
- Konfigurasi berbasis URL:
  ```python
  import openai
  # Cukup ubah base_url ke proxy Helicone
  client = openai.OpenAI(
      base_url="https://oai.helicone.ai/v1",
      default_headers={"Helicone-Auth": "Bearer HELICONE_API_KEY"}
  )
  ```
- **Automatic Caching**: Menyimpan respons prompt yang sama persis untuk menghemat biaya & mengurangi latensi menjadi ~10ms.
- **Custom Headers**: Mengirimkan metadata seperti `Helicone-User-Id` dan `Helicone-Property-Session`.

---

## 5. Arize AI & Phoenix (ML & Embedding Observability)

Arize Phoenix menyediakan alat analisis visual untuk embedding dan evaluasi RAG:

### Karakteristik Utama:
- **Embedding Clustering & UMAP**: Melihat visualisasi ruang 2D/3D dari prompt user untuk mendeteksi klaster pertanyaan yang sering gagal.
- **OpenTelemetry Standard**: Sepenuhnya kompatibel dengan standar OpenInference.
- **Evals Framework**: Built-in evaluators untuk Hallucination, Q&A Correctness, dan Summarization.
