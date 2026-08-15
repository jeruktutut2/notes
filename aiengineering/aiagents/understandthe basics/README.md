# UNDERSTAND THE BASICS - AI AGENTS LEARNING WORKSPACE

Proyek pembelajaran **Understand the Basics** untuk AI Agents berdasarkan roadmap resmi di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents).

Proyek ini mencakup laboratorium simulasi murni (*self-contained*) dari 6 pilar utama **Understand the Basics**:
1. **Streamed vs Unstreamed Responses** (Mekanisme SSE vs Blocking HTTP & Perceived Latency UX)
2. **Reasoning vs Standard Models** (Arsitektur Chain-of-Thought / Thinking Tokens vs Direct Response)
3. **Fine-Tuning vs Prompt Engineering** (Matriks Keputusan, In-Context Learning vs LoRA PEFT)
4. **Embeddings and Vector Search** (Matematika Vektor, Cosine Similarity, Dot Product & Semantic Search)
5. **Understand the Basics of RAG** (Pipeline Document Ingestion, Top-K Retrieval & Synthesis)
6. **Pricing of Common Models** (Kalkulator Biaya LLM Populer, Prompt Caching & Agent Loop Cost)

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`math`, `json`, `time`, `dataclasses`, `typing`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

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
| **01** | **Streamed vs Unstreamed Responses** | • Visualisasi HTTP Streaming (SSE) vs Blocking Batch<br>• Analisis Time-to-First-Token (TTFT) & Perceived Latency<br>• Keuntungan & Kasus Penggunaan pada Agent UI/UX | [`01_streamed_vs_unstreamed/`](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/01_streamed_vs_unstreamed/1_streamed_vs_unstreamed_responses.py) |
| **02** | **Reasoning vs Standard Models** | • Perbandingan DeepSeek R1 / o1 / o3-mini vs GPT-4o / Claude 3.5<br>• Hidden/Visible Reasoning Tokens (Chain-of-Thought)<br>• Tradeoff Akurasi Logika Kompleks vs Waktu & Biaya | [`02_reasoning_vs_standard/`](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/02_reasoning_vs_standard/1_reasoning_vs_standard_models.py) |
| **03** | **Fine-Tuning vs Prompt Engineering** | • Decision Framework & Matriks Keputusan ROI<br>• In-Context Learning (Few-Shot / RAG) vs LoRA Fine-Tuning<br>• Analisis Ambang Jumlah Request & Penghematan Token Input | [`03_finetuning_vs_prompt_engineering/`](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/03_finetuning_vs_prompt_engineering/1_finetuning_vs_prompt_engineering.py) |
| **04** | **Embeddings and Vector Search** | • Perhitungan Cosine Similarity, Dot Product, & Euclidean Distance<br>• Semantik Vector Search vs Lexical Keyword Matching<br>• Konsep Indeks Vektor (Flat KNN vs HNSW Graph) | [`04_embeddings_and_vector_search/`](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/04_embeddings_and_vector_search/1_embeddings_and_vector_search.py) |
| **05** | **Understand the Basics of RAG** | • End-to-End Pipeline RAG (Chunking -> Embedding -> Retrieval)<br>• Injeksi Konteks Top-K ke Prompt LLM<br>• Mitigasi Halusinasi & Pengujian Dokumen Internal | [`05_understand_basics_of_rag/`](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/05_understand_basics_of_rag/1_basics_of_rag.py) |
| **06** | **Pricing of Common Models** | • Tabel Tarif LLM SOTA (OpenAI, Anthropic, Gemini, DeepSeek)<br>• Simulasi Diskon Prompt Caching (Diskon 50%-90%)<br>• Estimasi Biaya Multi-Step Agent Tool Loop | [`06_pricing_of_common_models/`](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/06_pricing_of_common_models/1_pricing_of_common_models.py) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari matematika Cosine Similarity, TTFT, arsitektur RAG, hingga strategi pricing) dapat dibaca di folder:
👉 [notes/understand_the_basics_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/understandthe%20basics/notes/understand_the_basics_roadmap_notes.md)
