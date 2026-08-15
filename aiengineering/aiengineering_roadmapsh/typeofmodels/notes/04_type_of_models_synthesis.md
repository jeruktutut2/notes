# Catatan Pembelajaran: Syntesis & Matrix Keputusan Pemilihan Model

## 1. Kerangka Strategis Pemilihan Model (Model Selection Framework)

Memilih model AI yang tepat untuk sistem produksi bukan hanya tentang mencari model dengan skor benchmark tertinggi (seperti LMSYS Chatbot Arena), melainkan mencari keseimbangan optimum antara **Kualitas (Capability)**, **Kecepatan (Latency/TPS)**, **Biaya (Cost)**, dan **Keamanan (Privacy/Compliance)**.

```text
               +----------------------------------+
               |   THE AI TRILEMMA & TRADEOFF     |
               +----------------------------------+
                 /                |               \
                /                 |                \
    +-------------------+ +---------------+ +--------------------+
    |   PERFORMANCE     | |     COST      | | PRIVACY & SPEED    |
    | (GPT-4o, Claude)  | | (SLM / INT4)  | | (Self-Hosted vLLM) |
    +-------------------+ +---------------+ +--------------------+
```

---

## 2. Tabel Sintesis & Rekomendasi Kasus Penggunaan

| Skenario Penggunaan | Model Yang Direkomendasikan | Arsitektur & Deployment | Rationale / Alasan |
| :--- | :--- | :--- | :--- |
| **Startup MVP / Prototipe Cepat** | OpenAI GPT-4o-mini / Claude 3.5 Haiku | Closed Proprietary API | Zero infra setup, bayar murah per request, fokus validasi produk |
| **Penalaran Kompleks & Agentic Workflow** | OpenAI GPT-4o / Claude 3.5 Sonnet | Closed Proprietary API | Kemampuan Tool Use, Structured JSON, dan Reasoning terbaik |
| **Aplikasi Finansial / Kesehatan / Regulasi Strict** | Llama 3.1 70B / Qwen 2.5 72B | Self-Hosted Open Weights (vLLM di On-Prem GPU) | 100% Data Sovereignty, memenuhi GDPR/HIPAA, tanpa data leak |
| **Edge / Mobile / Offline App** | Phi-3 Mini / Gemma 2B / Llama 3.2 3B | Local Ollama / GGUF 4-bit di Perangkat | Memori kecil (~2-4 GB RAM), latensi lokal instantaneous |
| **High Throughput RAG System (> 100M tokens/month)** | DeepSeek V2.5 / Llama 3.1 8B AWQ | Self-Hosted vLLM dengan GPU Auto-scaling | Menghemat biaya hingga 80% dibanding API per-token pada skala massal |

---

## 3. Checklist Kesiapan Produksi (Production Readiness Checklist)

Sebelum meluncurkan model AI ke produksi, pastikan telah melakukan verifikasi:

- [ ] **SLA Latency**: Apakah Time-To-First-Token (TTFT) < 800ms dan Tokens-Per-Second (TPS) > 30 tps?
- [ ] **Kalkulasi Biaya TCO**: Apakah biaya bulanan API vs Self-Hosted GPU sudah disimulasikan hingga 12 bulan ke depan?
- [ ] **Fallback Strategy**: Jika API vendor mengalami downtime, apakah ada fallback ke model open weights atau API sekunder?
- [ ] **Evaluasi Guardrails**: Apakah output model telah divalidasi terhadap Prompt Injection & Hallucination?
- [ ] **Monitoring & Observability**: Apakah latensi, token count, dan biaya dicatat per user/request?
