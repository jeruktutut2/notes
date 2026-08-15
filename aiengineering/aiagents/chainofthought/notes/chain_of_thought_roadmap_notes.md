# CATATAN PEMBELAJARAN: CHAIN OF THOUGHT (CoT), TREE OF THOUGHT (ToT) & TOOL DEFINITION

Dokumen ini berisi rangkuman teori komprehensif mengenai **Chain of Thought (CoT)**, **Tree of Thought (ToT)**, **Tool Definition & Schemas**, serta **Examples of Tools** untuk AI Agents berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan arsitektur visual sistem penalaran agen modern.

---

## 📋 DAFTAR ISI
1. [Pengantar & Mengapa Agent Membutuhkan Reasoning](#1-pengantar--mengapa-agent-membutuhkan-reasoning)
2. [Chain of Thought (CoT) Deep-Dive](#2-chain-of-thought-cot-deep-dive)
   - Zero-Shot CoT ("Let's think step by step")
   - Few-Shot CoT & Manual Reasoning Traces
   - Self-Consistency & Majority Voting
   - Thought Execution & Parsing (`<thought>` & `<action>`)
3. [Tree of Thought (ToT) & Multi-Path Reasoning](#3-tree-of-thought-tot--multi-path-reasoning)
   - Konsep Pohon Pemikiran (Branching & States)
   - Algoritma Pencarian (BFS, DFS, A*)
   - Evaluation Metrics, Heuristic Scorer & Backtracking
4. [Hubungan Penalaran ke Tindakan (Tools / Actions)](#4-hubungan-penalaran-ke-tindakan-tools--actions)
   - Siklus ReAct (Reason -> Act -> Observe -> Reason)
5. [Tool Definition & Standard Schema](#5-tool-definition--standard-schema)
   - Name and Description Semantics
   - Input / Output Schema (JSON Schema & Validation)
   - Error Handling & Recovery Strategies
   - Usage Examples & Alignment
6. [Examples of Tools (6 Pilar Contoh Tool AI Agent)](#6-examples-of-tools-6-pilar-contoh-tool-ai-agent)
   - Web Search
   - Code Execution / REPL
   - Database Queries
   - API Requests
   - Email / Slack / SMS
   - File System Access

---

## 1. PENGANTAR & MENGAPA AGENT MEMBUTUHKAN REASONING

Besar dari LLM dasar (Large Language Models) dilatih secara autoregresif untuk memprediksi token berikutnya berdasarkan bobot statistik. Ketika dihadapkan pada masalah komplek (seperti logika matematika, eksplorasi multi-langkah, atau navigasi API), LLM sering kali mengalami *hallucination* atau kegagalan jika dipaksa memberikan jawaban akhir secara langsung (*direct generation*).

```
Direct Prompting:  [Input] ──────────────────────────────────────────► [Jawaban Langsung (Rentan Salah)]

Chain of Thought:  [Input] ──► [Langkah 1] ──► [Langkah 2] ──► [Langkah 3] ──► [Jawaban Akurat]
```

Penalaran terstruktur (*Structured Reasoning*) memungkinkan agen:
1. **Memecah Masalah Kompleks**: Menguraikan tujuan besar menjadi sub-tugas (*task decomposition*).
2. **Memverifikasi Langkah Intermediet**: Memastikan logika pada langkah awal benar sebelum melangkah ke tahap berikutnya.
3. **Memicu Pemanggilan Tool (Tool Invocation)**: Menentukan *kapan* butuh informasi eksternal dan *tool apa* yang harus dipanggil.

---

## 2. CHAIN OF THOUGHT (CoT) DEEP-DIVE

### Zero-Shot CoT
Ditemukan oleh Kojima et al. (2022). Hanya dengan menambahkan frasa pengarah sederhana seperti:
> *"Let's think step by step."* atau *"Mari kita pikirkan langkah demi langkah."*

LLM secara eksplisit akan mengalokasikan token untuk melakukan penalaran urut (*step-by-step reasoning trace*) sebelum membuat kesimpulan.

### Few-Shot CoT
Didesain oleh Wei et al. (2022). Kita memberikan beberapa pasang contoh (demotration exemplars) yang memuat masalah, penalaran bertahap, dan jawaban akhir:
```
Q: Roger punya 5 bola tenis. Dia membeli 2 kaleng bola tenis. Setiap kaleng berisi 3 bola. Berapa bola yang dia punya sekarang?
A: Roger mulai dengan 5 bola. 2 kaleng berisi 3 bola adalah 2 * 3 = 6 bola. 5 + 6 = 11. Jawabannya adalah 11.
```

### Self-Consistency (Wang et al., 2022)
Daripada hanya mengambil satu jalur penalaran (*greedy decoding*), Self-Consistency melakukan hal berikut:
1. Melakukan sampling beberapa jalur penalaran CoT secara acak ($T > 0$).
2. Mengumpulkan jawaban akhir dari setiap jalur.
3. Menggunakan *Majority Voting* (pilihan terbanyak) sebagai konsensus akhir.

### Thought Execution & Action Parsing
Dalam agen otonom, penalaran dipisah dari aksi eksekusi menggunakan format terstruktur seperti Tag XML atau JSON:
```xml
<thought>
User meminta daftar total penjualan bulan ini. Saya perlu menjalankan query SQL pada tabel Sales.
</thought>
<action>
{"tool": "database_query", "parameters": {"sql": "SELECT SUM(amount) FROM sales WHERE month='current'"}}
</action>
```

---

## 3. TREE OF THOUGHT (ToT) & MULTI-PATH REASONING

Ketika masalah membutuhkan strategi trial-and-error, eksplorasi combinatorial, atau perencanaan strategis (misalnya permainan catur, pemecahan teka-teki, penulisan kode kompleks), Chain of Thought (jalur linier) tidak cukup.

Tree of Thought (Yao et al., 2023) memperluas CoT dengan memungkinkan **percabangan pemikiran (branching thoughts)** dan **penilaian status (state evaluation)**.

```
                  [Root Problem]
                   /    |    \
             [Thought A] [Thought B] [Thought C]
               (Score: 0.8) (Score: 0.2) (Score: 0.9)  <-- Evaluasi & Pruning
                              (Pruned)      /    \
                                    [Thought C1] [Thought C2]
                                    (Score: 0.95) -> SOLUSI
```

### Komponen Utama ToT:
1. **Thought Decomposer**: Memecah masalah menjadi langkah-langkah pemikiran intermediet.
2. **Thought Generator**: Menghasilkan $k$ kandidat pemikiran untuk langkah selanjutnya.
3. **State Evaluator**: Menilai prospek keberhasilan setiap state (menggunakan penilaian LLM, statistik, atau skor heuristik 0.0 - 1.0).
4. **Search Algorithm**:
   - **BFS (Breadth-First Search)**: Menyelidiki semua cabang pada kedalaman tertentu sebelum maju.
   - **DFS (Depth-First Search)**: Memilih jalur terbaik hingga ujung; jika jalan buntu, melakukan **Backtracking**.

---

## 4. HUBUNGAN PENALARAN KE TINDAKAN (TOOLS / ACTIONS)

Reasoning (CoT/ToT) bertindak sebagai "Otak", sedangkan Tools/Actions bertindak sebagai "Tangan dan Mata" bagi AI Agent.

### Siklus ReAct (Reason + Act)
```
  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │   1. USER INPUT                                        │
  │      │                                                 │
  │   2. REASON (CoT / Thought Trace)                      │
  │      │                                                 │
  │   3. ACT (Tool Call Invocation)                        │
  │      │                                                 │
  │   4. OBSERVE (Tool Execution Result / Response)        │
  │      │                                                 │
  └──────┴──► (Kembali ke REASON hingga tugas selesai)     │
```

---

## 5. TOOL DEFINITION & STANDARD SCHEMA

Agar LLM dapat memanggil tool secara tepat tanpa kesalahan sintaks, definisi tool harus memenuhi standar skema yang jelas (*Tool Definition*):

### 1. Name and Description
- **Name**: Nama fungsi yang unik dan deskriptif (`search_database`, `read_workspace_file`).
- **Description**: Penjelasan mendalam tentang *fungsi*, *kapan harus digunakan*, dan *kapan TIDAK boleh digunakan*.

### 2. Input / Output Schema
- Menggunakan skema JSON Schema / Pydantic.
- Mendefinisikan tipe data (`string`, `integer`, `boolean`, `array`, `object`), sifat variabel (`required` vs `optional`), serta batasan (*constraints*).

### 3. Error Handling
- Jika LLM memberikan argumen yang salah tipe atau kurang, skema validator harus menghasilkan *Error Feedback Prompt* yang jelas agar LLM dapat memperbaiki pemanggilannya pada perulangan berikutnya.

### 4. Usage Examples
- Menyediakan pasang contoh pemanggilan tool (*few-shot tool examples*) untuk memperjelas format yang diharapkan.

---

## 6. EXAMPLES OF TOOLS (6 PILAR CONTOH TOOL AI AGENT)

Berdasarkan arsitektur AI Agent roadmap, terdapat 6 kategori tool dasar yang paling sering digunakan:

| Kategori Tool | Kegunaan Utama | Contoh Fungsi / Library |
|---------------|────────────────|-------------------------|
| **1. Web Search** | Mencari informasi real-time dan fakta terkini di internet | Google Search API, Tavily, SerpAPI, Web Scraper |
| **2. Code Execution / REPL** | Menjalankan perhitungan matematika kompleks, analisis data, atau visualisasi | Python AST REPL, E2B Sandbox, Jupyter Kernel |
| **3. Database Queries** | Membaca dan menulis data terstruktur/unstructured | SQLite Engine, PostgreSQL Client, Vector DB (RAG) |
| **4. API Requests** | Berinteraksi dengan service pihak ketiga (microservices) | REST Client, GraphQL API, Webhook Invoker |
| **5. Email / Slack / SMS** | Mengirim notifikasi dan komunikasi interaktif manusia | Slack Webhook, Twilio SMS API, SMTP Email Sender |
| **6. File System Access** | Membaca, merubah, dan membuat file di workspace | File Reader/Writer, Directory Searcher |

---
*Catatan ini dirancang sebagai acuan teori lengkap untuk mendampingi skrip simulasi di folder `01_chain_of_thought`, `02_tree_of_thought`, `03_tool_definition`, dan `04_examples_of_tools`.*
