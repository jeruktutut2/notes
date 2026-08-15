# DOCUMENTATION: MODEL SELECTION & HOSTING (ROADMAP.SH AI ENGINEER)

Dokumen ini mendokumentasikan topik **Model Selection & Hosting** yang berhubungan erat dengan strategi Prompt & Context Engineering dari [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 📑 Topik Pembahasan

1. **Pre-trained Models**
2. **Closed vs Open Source Models**
3. **Self-Hosted Models**

---

## 1. Pre-trained Foundation Models
- **Skala Parameter**: 7B/8B (Ringan, lokal), 70B (Standar Enterprise), 405B+ (Model Raksasa SOTA).
- **Pengaruh terhadap Prompt/Context Strategy**:
  - Model skala kecil (8B) membutuhkan *Few-Shot Prompting* dan pembatas XML yang lebih ketat agar tidak membuat kesalahan format.
  - Model skala besar (70B+) mampu mengeksekusi penalaran *Zero-Shot CoT* dan *ReAct Agent* dengan akurasi jauh lebih tinggi.

## 2. Closed vs Open Source Models
- **Closed-Source API (Proprietary)**: OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet), Google (Gemini 1.5 Pro).
  - *Keunggulan*: SOTA reasoning, zero infra management, built-in prompt caching.
  - *Pertimbangan*: Privasi data dikirim ke vendor, biaya variabel linier dengan volume transaksi.
- **Open-Source / Open-Weights**: Meta Llama 3.3, Mistral, Qwen 2.5, DeepSeek R1.
  - *Keunggulan*: Privasi 100% (On-premise / Private Cloud), bebas di-fine-tune, biaya infrastruktur tetap (*fixed GPU cost*).

## 3. Self-Hosted Models & Inference Engines
- **High-Performance Engines**: vLLM (PagedAttention KV Cache), Ollama (Local dev), TensorRT-LLM (High-throughput NVIDIA GPU optimization).
- **Quantization (Kuantisasi Bobot)**: AWQ / GGUF / INT4 menekan kebutuhan memori VRAM GPU hingga 70% dengan degradasi akurasi < 1%.
