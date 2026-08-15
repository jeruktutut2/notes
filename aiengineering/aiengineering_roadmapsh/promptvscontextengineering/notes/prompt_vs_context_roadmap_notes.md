# PROMPT VS CONTEXT ENGINEERING - MATERI LENGKAP & ROADMAP AI ENGINEER

Dokumen ini menyajikan panduan teoritis dan praktis komprehensif mengenai **Prompt Engineering vs Context Engineering** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 1. Peta Kurikulum Pembelajaran (Roadmap AI Engineer)

```
                       ┌──────────────────────────────────────────────┐
                       │   AI ENGINEER ROADMAP: PROMPT VS CONTEXT     │
                       └──────────────────────┬───────────────────────┘
                                              │
         ┌────────────────────────────────────┴────────────────────────────────────┐
         ▼                                                                         ▼
┌─────────────────────────────────┐                               ┌─────────────────────────────────┐
│   PROMPT ENGINEERING FOLDER     │                               │  CONTEXT ENGINEERING FOLDER     │
├─────────────────────────────────┤                               ├─────────────────────────────────┤
│ 1. Anatomi & Delimiter XML      │                               │ 1. Context Window Budgeting     │
│ 2. Few-Shot & Reasoning (CoT)   │                               │ 2. Lost-in-the-Middle (U-Shape) │
│ 3. ReAct & Tool Augmentation    │                               │ 3. Token Compression (LLMLingua)│
│ 4. JSON Schema Self-Repair Loop │                               │ 4. Tripartite Memory (State)    │
│ 5. Prompt Injection & Defense   │                               │ 5. Prefix/KV Caching & PII Mask │
└────────────────┬────────────────┘                               └────────────────┬────────────────┘
                 │                                                                 │
                 └────────────────────────────────────┬────────────────────────────┘
                                                      │
                                                      ▼
                       ┌──────────────────────────────────────────────┐
                       │  PROMPT VS CONTEXT COMPARISON & HYBRID LABS  │
                       ├──────────────────────────────────────────────┤
                       │ 1. Benchmark Performa, Latensi & Biaya       │
                       │ 2. Architectural Decision Engine & Routing   │
                       │ 3. End-to-End Production Hybrid Pipeline     │
                       └──────────────────────────────────────────────┘
```

---

## 2. Tabel Perbandingan Paradigma: Prompt vs Context Engineering

| Dimensi Evaluasi | Prompt Engineering | Context Engineering |
|------------------|--------------------|---------------------|
| **Fokus Utama** | Memformulasi instruksi, contoh in-context (Few-shot), penalaran (CoT/ToT), dan batasan luaran. | Mengelola state lingkungan, alokasi token budget, kompresi teks, memori multi-turn, dan retrival RAG. |
| **Input Utama** | Teks instruksi statis / template prompt. | Gabungan data dinamis: Profil user, riwayat percakapan, dokumen RAG, PII masked data. |
| **Skala Token** | Ringkas: $100 - 4,000$ tokens. | Masif: $8,000 - 128,000+$ tokens. |
| **Dampak Latensi (TTFT)**| Latensi sangat rendah (Time-to-first-token cepat). | Berpotensi lambat tanpa *Prefix/Prompt Caching*. |
| **Dampak Biaya API** | Biaya sangat murah per panggilan. | Biaya tinggi jika tidak dikompresi / di-prune. |
| **Penanganan Keamanan** | Fokus pada *Prompt Injection, Jailbreak, Sandwich Defense*. | Fokus pada *Multi-Tenant Isolation, Sanitasi PII, Lost-in-the-Middle*. |
| **Metrik Kunci** | Precision format output, akurasi penalaran CoT. | Context Precision, Context Recall, Latensi TTFT, Token Efficiency Score. |

---

## 3. Kapan Menggunakan Prompt Engineering vs Context Engineering?

### Gunakan **Prompt Engineering** ketika:
1. Tugas berfokus pada **penalaran logika, transformasi format, atau instruksi spesifik** (misal: merangkum teks, mengonversi paragraf ke JSON, analisis sentimen).
2. Data yang diproses bersifat **self-contained** (seluruh informasi sudah ada di dalam input teks pengguna).
3. Anda ingin meminimalkan penggunaan token dan tidak membutuhkan ingatan percakapan masa lalu.

### Gunakan **Context Engineering** ketika:
1. Aplikasi berupa **Chatbot Multi-Turn / AI Agent** yang membutuhkan ingatan percakapan (stateful).
2. Sistem membutuhkan pengetahuan bisnis eksternal dari **Enterprise Knowledge Base (RAG)** atau basis data real-time.
3. Anda mengelola dokumen berukuran besar dan perlu melakukan **token compression** serta **prefix caching** untuk menghemat biaya operasional produksi.

---

## 4. Arsitektur Hybrid Produksi (Best Practice AI Engineering)

Dalam aplikasi tingkat produksi (*enterprise-grade*), Prompt Engineering dan Context Engineering **TIDAK berdiri sendiri**, melainkan digabungkan secara harmonis:

```
[User Request] ──► [PII Masker / Security Guardrail] 
                       │
                       ▼
          [Context Assembler Engine]
          ├── Embeddings & RAG Vector DB
          ├── Summary Buffer (Episodic Memory)
          └── User Profile (Semantic Memory)
                       │
                       ▼
          [Prompt Formatting Engine]
          ├── Persona Framing & System Prefix (KV Cached)
          ├── XML Delimiters Isolation (<context>, <instruction>)
          └── Chain-of-Thought & JSON Schema Constraints
                       │
                       ▼
                 [LLM Execution]
                       │
                       ▼
          [JSON Schema Validation & Repair Loop] ──► [Final Response]
```

---

## 5. Ringkasan Checklist Yang Harus Dipelajari

- [x] **Prompt Engineering**:
  - [x] Anatomi 4 elemen (Persona, Instruction, Context, Output Constraint).
  - [x] Pemanfaatan Tag XML untuk pembatas terisolasi.
  - [x] Zero-Shot, Few-Shot, CoT, Self-Consistency, dan ReAct.
  - [x] Red Teaming: Prompt Injection, Jailbreak, Sandwich Defense.
  - [x] Output Structuring: Parsing JSON Schema & Repair Loop.

- [x] **Context Engineering**:
  - [x] Context Window Allocation & Budgeting (128K Limits).
  - [x] Lost-in-the-Middle Effect (U-Shape Attention Curve).
  - [x] Selective Token Information Density Pruning (LLMLingua style).
  - [x] Tripartite Memory (Procedural, Semantic, Episodic).
  - [x] Prefix / Prompt Caching (vLLM / KV Cache Optimization).
  - [x] Multi-Tenant Isolation & PII Sanitization.

- [x] **Prompt vs Context Synthesis**:
  - [x] Matrix Tradeoff Biaya, Latensi, dan Skalabilitas.
  - [x] Architectural Decision Engine.
  - [x] Production Hybrid Pipeline Implementation.
