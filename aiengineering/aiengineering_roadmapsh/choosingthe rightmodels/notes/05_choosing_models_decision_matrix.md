# 05 - Choosing the Right Models: Matriks & Kerangka Keputusan

 Memilih model yang tepat (*Choosing the Right Model*) adalah salah satu keputusan arsitektural paling kritis bagi AI Engineer. Tidak ada satu model tunggal yang sempurna untuk seluruh skenario. Keputusan ideal harus mempertimbangkan **Biaya (Cost)**, **Latensi (Latency)**, **Kualitas Penalaran (Quality/Reasoning)**, **Kedaulatan Data (Data Sovereignty/Privacy)**, dan **Kemampuan Integrasi (Tooling/Context)**.

---

## 🎯 Kerangka Keputusan 5-Pilar (5-Pillar Decision Framework)

```text
                     ┌───────────────────────────────┐
                     │   Choosing the Right Model    │
                     └───────────────┬───────────────┘
                                     │
   ┌─────────────────┬───────────────┼───────────────┬─────────────────┐
   ▼                 ▼               ▼               ▼                 ▼
 💰 Cost          ⚡ Latency       🧠 Quality      🔒 Privacy       🛠️ Tooling
 (Token Budget)   (TTFT & TPS)     (Benchmark)   (On-Prem/Cloud)   (JSON/Context)
```

1. **Cost (Anggaran Biaya per 1M Token)**:
   * Closed Models API: $0.15/1M (Flash/Haiku) hingga $15.00/1M (Opus/GPT-4o/o1).
   * Open Weights Self-Hosted: Biaya fixed server/GPU (misal $1.5/jam untuk A10G), sangat murah jika volume throughput tinggi.
2. **Latency (Time-To-First-Token & Tokens-Per-Second)**:
   * Aplikasi interaktif chat UI butuh TPS tinggi (>50 token/dtk).
   * Autocomplete / Voice Agent butuh TTFT ultra-rendah (<200ms).
3. **Quality & Task Capability**:
   * Coding & Math reasoning tinggi: Claude 3.5 Sonnet, GPT-4o, DeepSeek R1, Qwen 2.5-Coder.
   * Simple Extraction & Sentiment: GPT-4o-mini, Llama 3.2 3B, Gemma 2 9B.
4. **Data Privacy & Sovereignty**:
   * Data sensitif finansial/kesehatan yang dilarang dikirim ke cloud publik: Wajib **Self-Hosted Open Source** (Llama 3.1 70B di server VPC internal / Ollama).
5. **Tooling & Context Length**:
   * Kebutuhan 100K-1M token context: Gemini 1.5 Pro (2M), Claude 3.5 Sonnet (200K).
   * Structured Output JSON Schema presisi 100%: OpenAI GPT-4o / Claude 3.5.

---

## 📊 Matriks Trade-off Komprehensif

| Skenario Penggunaan | Model Teratas Yang Direkomendasikan | Alasan Utama | Alternatif Open Source |
| :--- | :--- | :--- | :--- |
| **Enterprise Code Generation** | Claude 3.5 Sonnet | Performa coding #1, Prompt Caching murah | Qwen 2.5-Coder 32B / DeepSeek R1 |
| **Analisis Dokumentasi & Video Masif** | Gemini 1.5 Pro | 2M token context, native video processing | Llama 3.1 405B (via vLLM) |
| **Voice Agent / Chat Real-time** | Gemini 1.5 Flash / GPT-4o-mini | Latensi TTFT terendah & throughput tinggi | Gemma 2 9B (via Groq/vLLM) |
| **Complex Math & Science Research** | DeepSeek R1 / OpenAI o1 | Inference-time CoT Reasoning | DeepSeek-R1-Distill-Qwen-32B |
| **Aplikasi Banking Offline / HIPAA** | Llama 3.1 70B (Self-Hosted) | 100% Privacy & Data Sovereignty | Qwen 2.5 72B (Self-Hosted) |

---

## 💡 Algoritma Pemilihan Model (Flowchart Decision Tree)

```text
Apakah data boleh dikirim ke Cloud Publik?
   ├── TIDAK ──► Gunakan OPEN SOURCE MODEL (Self-Hosted via Ollama/vLLM)
   │               ├── Butuh di HP/Edge Device? ──► Llama 3.2 (1B/3B) / Gemma 2 (2B)
   │               ├── Butuh Performa Server Tinggi? ──► Llama 3.1 70B / Qwen 2.5 72B
   │               └── Butuh Reasoning Matematika? ──► DeepSeek R1 Distill 32B
   │
   └── YA ──► Gunakan CLOSED MODEL API atau AGGREGATOR (OpenRouter)
                   ├── Butuh Analisis Video/Audio atau Konteks >200K? ──► Gemini 1.5 Pro
                   ├── Butuh High-level Coding & System Architecture? ──► Claude 3.5 Sonnet
                   ├── Butuh JSON Schema Strict & Tool Calling standar? ──► OpenAI GPT-4o
                   └── Butuh Harga Murah & Latensi Kilat? ──► Gemini 1.5 Flash / GPT-4o-mini
```
