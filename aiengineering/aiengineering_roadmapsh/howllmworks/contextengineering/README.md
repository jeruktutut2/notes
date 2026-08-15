# CONTEXT ENGINEERING AI ENGINEERING - Belajar dari Roadmap.sh

Proyek pembelajaran **Context Engineering & AI Engineering** berdasarkan [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

Setiap modul berisi skrip Python runnable yang dapat langsung dijalankan beserta simulasi mekanisme context window, token compression (LLMLingua), in-context memory, prefix caching, multi-tenant isolation, context sharding, dan metrik evaluasi lengkap dalam Bahasa Indonesia.

## Persiapan Environment & Install

```bash
# Menggunakan Python 3.9+
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

> **Catatan Dependensi:** Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`math`, `json`, `re`, `dataclasses`, `time`, `typing`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

## Cara Menjalankan CLI Interaktif

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul:

```bash
python3 main.py
```

---

## Daftar Modul Pembelajaran

| No | Modul | Topik & Materi | Skrip Python |
|----|-------|----------------|--------------|
| **01** | Context Window & Anatomi Context | Context Window Allocation Matrix, Boundary Sanitization (XML Tags), Lost in the Middle (U-Shape) & Attention Sinks | `01_context_window_dan_anatomi/` |
| **02** | Context Compression & Pruning | Selective Token Information Density Compression (LLMLingua), Semantic Truncation & Recency Decay, Needle In A Haystack (NIAH) | `02_context_compression_dan_pruning/` |
| **03** | In-Context Memory & State Management | Conversation Summary Buffer & Entity Memory, Tripartite Memory (Episodic, Semantic, Procedural), Working Memory Scratchpad | `03_memory_management_dan_state/` |
| **04** | Dynamic Context Assembly & Caching | Dynamic Context Assembler Pipeline, Prefix/Prompt Caching & KV Cache Simulator, Multi-Tenant Context Isolation & PII Sanitizer | `04_dynamic_context_assembly_dan_caching/` |
| **05** | Context Routing & Multi-Context Orchestration | Hierarchical Context & Sub-Agent Context Isolation, Context Sharding & Map-Reduce Pattern | `05_context_routing_dan_orchestration/` |
| **06** | Evaluasi, Metrik & Biaya Context | Context Precision, Recall, Relevancy, NSR & Information Density, Context Cost Scaling & Latency TTFT Benchmark | `06_evaluasi_metrik_dan_biaya_context/` |

---

## Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik context engineering (mulai dari matematika Attention Sinks hingga arsitektur Prefix Caching dan Metrik Precision/Recall) dapat dibaca di folder [notes/context_engineering_roadmap_notes.md](notes/context_engineering_roadmap_notes.md).
