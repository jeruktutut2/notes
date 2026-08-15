# 📘 AI Engineering — Kategori & Contoh Program

> Belajar AI Engineering dari contoh program nyata, dikelompokkan per kategori.
> Setiap contoh bisa langsung dijalankan. Semua gratis (Ollama / Gemini API).

---

## 🗂️ Kategori AI Engineering

```
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│   KATEGORI 1          KATEGORI 2          KATEGORI 3                     │
│   ┌──────────┐        ┌──────────┐        ┌──────────┐                   │
│   │ Chatbot  │        │ Dokumen  │        │ Ekstraksi│                   │
│   │ & Prompt │        │ & RAG    │        │ Data     │                   │
│   └──────────┘        └──────────┘        └──────────┘                   │
│                                                                           │
│   KATEGORI 4          KATEGORI 5          KATEGORI 6                     │
│   ┌──────────┐        ┌──────────┐        ┌──────────┐                   │
│   │ AI Agent │        │ Keamanan │        │ Produksi │                   │
│   │ & Otomasi│        │ & Kualitas│       │ & Deploy │                   │
│   └──────────┘        └──────────┘        └──────────┘                   │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

---

## Kategori 1: Chatbot & Prompt Engineering

**Inti:** Berkomunikasi dengan LLM dan mengontrol jawabannya.

| # | Contoh Program | Belajar Apa | Tingkat |
|---|---|---|---|
| 1.1 | **Chatbot Terminal** — Chat dengan AI di terminal | Panggil LLM via API, kelola percakapan | ⭐ Pemula |
| 1.2 | **Penerjemah Otomatis** — Terjemahkan teks ke bahasa apapun | Prompt engineering dasar, system prompt | ⭐ Pemula |
| 1.3 | **Asisten Penulis** — AI bantu tulis email/artikel profesional | Few-shot prompting, role prompting | ⭐ Pemula |
| 1.4 | **Analisis Sentimen** — Klasifikasi sentimen review produk | Zero-shot & few-shot classification | ⭐ Pemula |
| 1.5 | **Chatbot Multi-Persona** — Chatbot yang bisa ganti karakter | System prompt dinamis, temperature | ⭐⭐ Menengah |

### Konsep yang dipelajari:
- Cara panggil LLM (Ollama lokal / Gemini API)
- System prompt vs user prompt
- Teknik prompt: zero-shot, few-shot, chain-of-thought
- Manajemen history percakapan
- Temperature & parameter LLM

---

## Kategori 2: Dokumen & RAG (Retrieval-Augmented Generation)

**Inti:** Membuat AI bisa menjawab berdasarkan dokumen/data kita sendiri.

| # | Contoh Program | Belajar Apa | Tingkat |
|---|---|---|---|
| 2.1 | **Tanya Jawab Dokumen** — Upload dokumen, tanya apa saja | Embedding, vector DB, RAG dasar | ⭐⭐ Menengah |
| 2.2 | **Pencarian Semantik** — Cari data berdasarkan makna, bukan kata kunci | Cosine similarity, embedding | ⭐⭐ Menengah |
| 2.3 | **Chatbot FAQ Perusahaan** — Bot yang jawab dari knowledge base | Chunking, retrieval strategy | ⭐⭐ Menengah |
| 2.4 | **Ringkasan Dokumen Panjang** — Rangkum PDF/artikel panjang | Document loading, map-reduce | ⭐⭐ Menengah |

### Konsep yang dipelajari:
- Embedding (teks → vektor angka)
- Vector database (ChromaDB)
- Chunking (memotong dokumen jadi bagian kecil)
- Retrieval + generation pipeline
- Cosine similarity

---

## Kategori 3: Ekstraksi Data & Structured Output

**Inti:** Memaksa AI mengeluarkan data terstruktur (JSON) yang bisa dipakai di kode.

| # | Contoh Program | Belajar Apa | Tingkat |
|---|---|---|---|
| 3.1 | **Ekstraksi Info dari Teks** — Ambil nama, tanggal, alamat dari teks bebas | Pydantic, JSON output | ⭐⭐ Menengah |
| 3.2 | **Klasifikasi Otomatis** — Kategorikan email/tiket support otomatis | Enum output, classification | ⭐⭐ Menengah |
| 3.3 | **Parser Nota/Invoice** — Baca foto nota, keluarkan data terstruktur | Multi-modal (gambar + teks) | ⭐⭐⭐ Lanjutan |

### Konsep yang dipelajari:
- Pydantic untuk validasi data
- JSON schema sebagai output format
- Retry logic kalau output tidak sesuai
- Multi-modal AI (teks + gambar)

---

## Kategori 4: AI Agent & Otomasi

**Inti:** AI yang bisa merencanakan, bertindak, dan menyelesaikan tugas secara mandiri.

| # | Contoh Program | Belajar Apa | Tingkat |
|---|---|---|---|
| 4.1 | **AI + Kalkulator** — AI yang bisa menghitung dengan akurat | Function/tool calling dasar | ⭐⭐ Menengah |
| 4.2 | **AI + Web Search** — AI yang bisa cari info terbaru di internet | Tool calling + API eksternal | ⭐⭐ Menengah |
| 4.3 | **Agent Riset** — Beri topik, AI riset dan buat laporan sendiri | ReAct loop, planning, LangGraph | ⭐⭐⭐ Lanjutan |
| 4.4 | **Agent Coding** — AI yang bisa tulis dan jalankan kode Python | Code execution, reflection | ⭐⭐⭐ Lanjutan |
| 4.5 | **Multi-Agent** — Tim AI: satu riset, satu tulis, satu review | Multi-agent, supervisor pattern | ⭐⭐⭐ Lanjutan |

### Konsep yang dipelajari:
- Function/tool calling
- ReAct pattern (Reasoning + Acting)
- Agent loop: Think → Act → Observe → Repeat
- LangGraph untuk agent kompleks
- Multi-agent collaboration
- MCP (Model Context Protocol)

---

## Kategori 5: Keamanan & Kualitas AI

**Inti:** Memastikan AI aman, akurat, dan bisa dipercaya.

| # | Contoh Program | Belajar Apa | Tingkat |
|---|---|---|---|
| 5.1 | **Guardrails Sederhana** — Blokir jailbreak & output berbahaya | Input/output filtering | ⭐⭐ Menengah |
| 5.2 | **AI Test Suite** — Automated testing untuk cek kualitas AI | pytest, evaluasi otomatis | ⭐⭐ Menengah |
| 5.3 | **Deteksi Hallucination** — Cek apakah AI mengarang fakta | Grounding, fact-checking | ⭐⭐⭐ Lanjutan |

### Konsep yang dipelajari:
- Guardrails (input & output validation)
- AI Evals (evaluasi sistematis)
- Deteksi hallucination
- Prompt injection defense
- LLM-as-Judge

---

## Kategori 6: Produksi & Deployment

**Inti:** Menjadikan aplikasi AI siap dipakai pengguna nyata.

| # | Contoh Program | Belajar Apa | Tingkat |
|---|---|---|---|
| 6.1 | **API Server AI** — REST API untuk aplikasi AI dengan FastAPI | API design, server deployment | ⭐⭐ Menengah |
| 6.2 | **Caching AI** — Cache jawaban AI agar cepat & hemat biaya | Semantic caching | ⭐⭐ Menengah |
| 6.3 | **AI dengan Logging** — Tracing setiap request AI | Observability, Langfuse | ⭐⭐⭐ Lanjutan |
| 6.4 | **MCP Server** — Buat tool AI standar yang bisa dipakai di mana saja | MCP protocol | ⭐⭐⭐ Lanjutan |
| 6.5 | **Fine-Tune Model** — Latih ulang model kecil dengan data sendiri | LoRA, QLoRA, Unsloth | ⭐⭐⭐ Lanjutan |

### Konsep yang dipelajari:
- FastAPI untuk AI endpoints
- Caching (exact match & semantic)
- Tracing & monitoring
- MCP server & client
- Fine-tuning dengan LoRA/QLoRA
- Docker containerization

---

## 🗺️ Urutan Belajar yang Disarankan

```
                        ┌──────────────────┐
                        │ Mulai dari sini!  │
                        └────────┬─────────┘
                                 ▼
                    ┌─── Kategori 1 ───┐
                    │  1.1 Chatbot     │
                    │  1.2 Penerjemah  │
                    └────────┬─────────┘
                             ▼
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌─ Kategori 2 ─┐ ┌─ Kategori 3 ─┐ ┌─ Kategori 4 ─┐
     │ 2.1 Tanya     │ │ 3.1 Ekstraksi│ │ 4.1 AI +     │
     │     Dokumen   │ │     Data     │ │     Kalkulator│
     └───────┬───────┘ └──────┬───────┘ └──────┬───────┘
             │                │                │
             └────────────────┼────────────────┘
                              ▼
                    ┌─── Kategori 5 ───┐
                    │  5.1 Guardrails  │
                    │  5.2 Testing     │
                    └────────┬─────────┘
                             ▼
                    ┌─── Kategori 6 ───┐
                    │  6.1 API Server  │
                    │  6.4 MCP Server  │
                    └────────┬─────────┘
                             ▼
                         DONE! 🎉
```

> **Catatan:** Kategori 2, 3, 4 bisa dipelajari **paralel** (urutan bebas) setelah paham Kategori 1.

---

## 🛠️ Tool yang Dipakai (Semua Gratis)

| Tool | Fungsi | Kategori |
|---|---|---|
| **Ollama** | Jalankan AI di laptop sendiri (gratis, offline) | Semua |
| **Gemini API** | AI cloud dari Google (free tier) | Semua |
| **Pydantic** | Validasi data & structured output | 3 |
| **ChromaDB** | Vector database untuk RAG | 2 |
| **LangGraph** | Framework untuk AI agent | 4 |
| **FastAPI** | API server Python | 6 |
| **pytest** | Testing otomatis | 5 |
| **MCP SDK** | Buat MCP server/client | 6 |

---

## 📁 Struktur Folder

```
aiengineering_example/
│
├── KATEGORI.md                    ← 📘 File ini
├── CATATAN_BELAJAR.md             ← 📖 Catatan teori lengkap
├── requirements.txt
├── .env.example
│
├── 1_chatbot_prompt/              ← Kategori 1
│   ├── 1_chatbot_terminal.py
│   ├── 2_penerjemah.py
│   ├── 3_asisten_penulis.py
│   ├── 4_analisis_sentimen.py
│   └── 5_chatbot_multi_persona.py
│
├── 2_dokumen_rag/                 ← Kategori 2
│   ├── 1_tanya_jawab_dokumen.py
│   ├── 2_pencarian_semantik.py
│   ├── 3_chatbot_faq.py
│   ├── 4_ringkasan_dokumen.py
│   └── documents/
│
├── 3_ekstraksi_data/              ← Kategori 3
│   ├── 1_ekstraksi_info.py
│   ├── 2_klasifikasi_otomatis.py
│   └── 3_parser_invoice.py
│
├── 4_agent_otomasi/               ← Kategori 4
│   ├── 1_ai_kalkulator.py
│   ├── 2_ai_web_search.py
│   ├── 3_agent_riset.py
│   ├── 4_agent_coding.py
│   └── 5_multi_agent.py
│
├── 5_keamanan_kualitas/           ← Kategori 5
│   ├── 1_guardrails.py
│   ├── 2_test_suite.py
│   └── 3_deteksi_hallucination.py
│
└── 6_produksi_deploy/             ← Kategori 6
    ├── 1_api_server.py
    ├── 2_caching_ai.py
    ├── 3_ai_logging.py
    ├── 4_mcp_server.py
    └── 5_fine_tune.py
```

---

## ▶️ Cara Mulai

```bash
# 1. Install Ollama (satu kali)
brew install ollama              # Mac
# atau download dari https://ollama.com

# 2. Download model AI (satu kali, ~2.3 GB)
ollama pull gemma3:4b

# 3. Setup Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Jalankan contoh pertama!
python 1_chatbot_prompt/1_chatbot_terminal.py
```

---

> **Selanjutnya:** Bilang kategori mana yang mau dibuat contohnya duluan, atau kita mulai dari **1.1 Chatbot Terminal** 🚀
