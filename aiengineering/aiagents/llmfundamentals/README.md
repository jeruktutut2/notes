# LLM FUNDAMENTALS & MODEL MECHANISMS - AI AGENTS LEARNING WORKSPACE

Proyek pembelajaran **LLM Fundamentals & Model Mechanisms** untuk AI Agents berdasarkan roadmap resmi di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents).

Proyek ini mencakup simulasi murni (*self-contained*) dari pilar utama **Transformer Models and LLMs - Model Mechanisms** (*Tokenization*, *Context Windows*, dan *Token Based Pricing*) beserta topik fondasi pendukung (*Transformer Architecture*, *Model Selection & Quantization*, dan *Evaluasi & Benchmarks*).

---

## 🛠️ Persiapan Environment & Instalasi

 Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`math`, `json`, `re`, `dataclasses`, `time`, `typing`, `unicodedata`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

```bash
# Menggunakan Python 3.9+
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

---

## 🚀 Cara Menjalankan CLI Interaktif

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul simulasi secara visual:

```bash
python3 main.py
```

---

## 📚 Daftar Modul Pembelajaran

| No | Modul | Topik & Materi Utama | Skrip Python |
|----|-------|----------------------|--------------|
| **01** | **Tokenization Mechanics** | • BPE, WordPiece, & SentencePiece Visual Merging<br>• Tiktoken Byte-Level BPE & Efisiensi Token Bahasa<br>• Token-Split Security Attack & Special Token Smuggling | [`01_tokenization/`](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/01_tokenization/) |
| **02** | **Context Windows & Attention** | • Anatomi Context Window & Kalkulator VRAM KV-Cache<br>• Positional Embeddings (RoPE, ALiBi, YaRN Scaling)<br>• Lost in the Middle & Streaming Attention Sinks (NIAH) | [`02_context_windows/`](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/02_context_windows/) |
| **03** | **Token-Based Pricing & Cost** | • Kalkulator Biaya Single Call & Multi-Turn Agent Loop<br>• Prompt Caching Simulator (Diskon 50%-90% & TTFT Latency)<br>• Token Bucket Rate Limiter & Budget Guardrails | [`03_token_based_pricing/`](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/03_token_based_pricing/) |
| **04** | **Transformer Architecture** | • Scaled Dot-Product Attention & MHA vs MQA vs GQA<br>• Autoregressive Sampling (Temp, Top-P, Top-K) & Speculative Decoding | [`04_transformer_architecture/`](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/04_transformer_architecture/) |
| **05** | **Model Selection & Kuantisasi** | • Closed API vs Local Open Weight Selection Matrix<br>• Matematika Kuantisasi (FP16, INT8, GGUF INT4) & Engine (Ollama/vLLM) | [`05_model_selection_and_quantization/`](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/05_model_selection_and_quantization/) |
| **06** | **Evaluasi & Benchmarks** | • Benchmark Standar (MMLU, HumanEval) & Metrik Pass@k<br>• LLM-as-a-Judge Pattern & Mitigasi Bias (Position/Verbosity) | [`06_evaluasi_dan_benchmarks/`](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/06_evaluasi_dan_benchmarks/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari matematika Attention Sinks hingga arsitektur Prompt Caching, Rumus KV-Cache VRAM, dan Kuantisasi) dapat dibaca di folder:
👉 [notes/llm_fundamentals_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/llmfundamentals/notes/llm_fundamentals_roadmap_notes.md)
