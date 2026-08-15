# UNDERSTAND THE BASICS - CATATAN PANDUAN PENGEMBANGAN AI AGENTS

Dokumen ini menyajikan panduan mendalam (*deep-dive reference*) mengenai **Understand the Basics** dari [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents). Catatan ini dirancang khusus bagi pengembang AI Agent yang ingin memahami fondasi teknis operasional LLM, mulai dari mekanisme transmisi data response (*Streaming vs Unstreamed*), klasifikasi arsitektur model (*Reasoning vs Standard*), strategi adaptasi pengetahuan (*Fine-Tuning vs Prompt Engineering*), mekanisme pemrosesan vektor semantik (*Embeddings & Vector Search*), arsitektur pencarian konteks (*Basics of RAG*), hingga kalkulasi dan optimasi ekonomi operasional (*Pricing of Common Models*).

---

## 📋 DAFTAR ISI

1. [Bab 1: Streamed vs Unstreamed Responses](#bab-1-streamed-vs-unstreamed-responses)
2. [Bab 2: Reasoning vs Standard Models](#bab-2-reasoning-vs-standard-models)
3. [Bab 3: Fine-Tuning vs Prompt Engineering](#bab-3-fine-tuning-vs-prompt-engineering)
4. [Bab 4: Embeddings and Vector Search](#bab-4-embeddings-and-vector-search)
5. [Bab 5: Understand the Basics of RAG](#bab-5-understand-basics-of-rag)
6. [Bab 6: Pricing of Common Models](#bab-6-pricing-of-common-models)
7. [Bab 7: Arsitektur Integrasi Fondasi pada AI Agent System](#bab-7-arsitektur-integrasi-fondasi-pada-ai-agent-system)

---

## 🌊 BAB 1: STREAMED VS UNSTREAMED RESPONSES

Dalam sistem AI Agent modern, cara transmisi token dari server LLM ke aplikasi menentukan kualitas **User Experience (UX)**, **Time-to-First-Token (TTFT)**, serta **Perceived Latency**.

```
Unstreamed (Blocking Batch Response):
Client ──[Request Prompt]──> LLM Engine ──(Menunggu Generasi 100% Token: 5.0 detik)──> Client (Terima Semua Teks)
                                                                                      (User Menunggu Layar Kosong!)

Streamed Response (Server-Sent Events / SSE):
Client ──[Request Prompt]──> LLM Engine ──[Token 1: 0.2s]──> Client (Langsung Tampak!)
                                         ──[Token 2: 0.25s]─> Client
                                         ──[Token 3: 0.3s]──> Client ...
```

### 1.1 Unstreamed (Blocking) Responses
- **Mekanisme**: Client mengirimkan HTTP POST request dan menunggu (*blocking*) hingga LLM selesai melakukan penarikan token berturut-turut (*autoregressive generation*) hingga token `[EOS]` (End of Stream) atau `max_tokens` tercapai.
- **Karakteristik**:
  - Respon dikirimkan sekaligus sebagai objek JSON lengkap (`choices[0].message.content`).
  - **TTFT = Total Generation Time**. Jika jawaban membutuhkan 1000 token (~4 detik), pengguna harus menunggu 4 detik tanpa indikasi visual progres teks.
  - Sangat cocok untuk: *Backend-to-Backend agent step*, penanganan pemicu webhook, sintesis JSON terstruktur (*Function Calling/Structured Outputs*), atau background batch jobs di mana UI pengguna tidak secara langsung menunggu keluaran teks.

### 1.2 Streamed Responses (SSE / Chunked Transfer)
- **Mekanisme**: Menggunakan protokol *Server-Sent Events* (SSE) dengan `HTTP 200 OK` header `Content-Type: text/event-stream`.
- **Karakteristik**:
  - Setiap kali LLM menghasilkan token tunggal (atau beberapa sub-words/chunks), server inferensi memancar paket data `data: {"choices": [{"delta": {"content": "Hello"}}]}\n\n`.
  - **TTFT sangat kecil** (biasanya 100ms - 400ms), memberikan kesan bahwa AI merespons seketika (*instantaneous feel*).
  - Sangat cocok untuk: Chatbot UI, live agent writing assistant, terminal CLI visualizer, dan agen interaktif.

### 1.3 Metrik Latensi & Matematika Transmisi
1. **Time to First Token (TTFT)**: Waktu dari saat request dikirim hingga token pertama diterima client.
   $$\text{TTFT} = t_{\text{network\_request}} + t_{\text{prompt\_processing\_(prefill)}} + t_{\text{first\_token\_generation}}$$
2. **Inter-Token Latency (ITL)**: Waktu rata-rata jeda antar token yang dikirim secara bertahap.
   $$\text{ITL} = \frac{\text{Total Generation Time} - \text{TTFT}}{\text{Total Output Tokens} - 1}$$
3. **Total Latency**:
   $$\text{Total Latency} = \text{TTFT} + (\text{Output Tokens} - 1) \times \text{ITL}$$

| Metrik | Unstreamed (Blocking) | Streamed (SSE Chunked) |
| :--- | :--- | :--- |
| **TTFT User View** | Sangat Tinggi (Sama dengan Total Time) | Sangat Rendah (100 - 400 ms) |
| **Parsing Structured Data (JSON)** | Mudah (JSON utuh valid) | Butuh Streaming JSON Parser / Buffering |
| **Penggunaan Memory Client** | Buffer Tunggal | Incremental Memory Append |
| **Kebutuhan HTTP Connection** | Standard HTTP Request | Persistent HTTP Streaming Connection |

---

## 🧠 BAB 2: REASONING VS STANDARD MODELS

Perkembangan terkini memperkenalkan dikotomi arsitektur model: **Standard Models** (e.g., GPT-4o, Claude 3.5 Sonnet, Gemini 2.0 Flash) dan **Reasoning Models** (e.g., DeepSeek R1, OpenAI o1, o3-mini).

```
Standard Model (Direct Generation):
Input Prompt ──> [LLM Direct Inference Layer] ──> Direct Answer / Output

Reasoning Model (Chain-of-Thought Internal Generation):
Input Prompt ──> [Internal Reasoning Loop / Hidden CoT Tokens]
                    ├── Step 1: Analisis Batasan & Asumsi
                    ├── Step 2: Eksplorasi Alternatif & Self-Correction
                    └── Step 3: Verifikasi Jawaban Akhir
                 ──> Final Clean Output
```

### 2.1 Standard Models
- **Mekanisme**: Menghasilkan respon langsung token demi token tanpa fase refleksi internal yang terpisah secara ekplisit. Model dipelajari dengan Instruction Tuning (RLHF/DPO) untuk memberikan respon efisien dan langsung (*direct response*).
- **Keunggulan**: Latensi cepat, biaya per token lebih murah, sangat handal untuk instruksi umum, pemanggilan fungsi (*Tool Calling / Function Calling*), serta ekstraksi data terstruktur.
- **Kelemahan**: Rentan terhadap kegagalan penalaran logika kompleks (*hallucination in deep logic*), matematika tingkat tinggi, atau algoritma kode yang membutuhkan *look-ahead planning*.

### 2.2 Reasoning Models
- **Mekanisme**: Dilatih menggunakan *Large-Scale Reinforcement Learning* (RL) tanpa atau dengan minimal supervised fine-tuning untuk mengeksekusi *Chain-of-Thought* (CoT) internal sebelum menghasilkan jawaban final.
- **Fitur Utama**:
  - **Reasoning Tokens / Thinking Tokens**: Model memicu ratusan hingga ribuan token penalaran internal yang menghitung hipotesis, mendeteksi kesalahan sendiri (*self-correction*), dan memverifikasi langkah logis.
  - **Hidden vs Visible CoT**: Beberapa model (seperti OpenAI o1/o3-mini) menyembunyikan raw reasoning tokens demi keamanan atau kerahasiaan prompt, sedangkan model open (seperti DeepSeek R1) menampilkan reasoning dalam tag `<think>...</think>`.
- **Keunggulan**: Performa mendekati atau melampaui manusia dalam olimpiade matematika, pemecahan masalah algoritma rumit, refactoring arsitektur software, serta penalaran ilmiah.
- **Kelemahan**: Biaya jauh lebih tinggi (karena jumlah total token membengkak akibat token reasoning), TTFT dan latensi total lebih lama.

### 2.3 Matriks Perbandingan & Kapan Menggunakan

| Aspek | Standard Models (GPT-4o, Claude 3.5) | Reasoning Models (DeepSeek R1, o1/o3) |
| :--- | :--- | :--- |
| **Fokus Utama** | Kecepatan, Instukstivitas, Tool Use | Logika Kompleks, Matematika, Kode RUMIT |
| **Jumlah Token Output** | $N$ token jawaban | $N_{\text{reasoning}} + N_{\text{jawaban}}$ |
| **Kecepatan Respons** | Sangat Cepat (Real-time agent) | Lambat (Perlu fase "Thinking") |
| **Biaya per Pertanyaan** | Rendah hingga Sedang | Tinggi (Akibat token reasoning ekstra) |
| **Relevansi Agent** | Routing agent, Fast QA, Function Calling | Complex Planner, Deep Code Refactor |

---

## 🎯 BAB 3: FINE-TUNING VS PROMPT ENGINEERING

Dalam mengembangkan AI Agent spesifik industri/domain, terdapat dua pendekatan utama untuk menyesuaikan pengetahuan dan perilaku model: **Prompt Engineering** (beserta In-Context Learning/RAG) dan **Fine-Tuning** (Full / LoRA PEFT).

```
                        ┌────────────────────────────────────────┐
                        │   Domain Adaptation & Learning Strategy │
                        └───────────────────┬────────────────────┘
                                            │
               ┌────────────────────────────┴────────────────────────────┐
               ▼                                                         ▼
┌─────────────────────────────┐                           ┌─────────────────────────────┐
│     Prompt Engineering      │                           │         Fine-Tuning         │
│  (In-Context Learning / RAG)│                           │ (LoRA / QLoRA / Full FT)    │
└──────────────┬──────────────┘                           └──────────────┬──────────────┘
               │                                                         │
 ├── Mengubah Input Prompt                                ├── Mengubah Bobot Parameter (Weights)
 ├── Dynamic Context Injection                            ├── Mengunci Gaya Bahasa & Format
 ├── Tanpa Biaya Training GPU                             ├── Membutuhkan Dataset Pasangan (Q, A)
 └── Terbatas Panjang Context                             └── Resiko Catastrophic Forgetting
```

### 3.1 Prompt Engineering & In-Context Learning
- **Definisi**: Teknik memandu perilaku LLM dengan cara merancang instruksi sistem (*System Prompt*), memberikan contoh (*Few-Shot Prompting*), atau menyuntikkan dokumen relevan (*RAG*) langsung pada prompt input tanpa mengubah bobot internal model.
- **Keunggulan**:
  - **Zero Training Cost**: Tidak membutuhkan GPU cluster atau proses retraining.
  - **Dinamis & Real-Time**: Informasi dapat diperbarui secara instan melalui sistem pencarian dokumen (RAG).
  - **Iterasi Cepat**: Perubahan instruksi dapat dilakukan dalam hitungan detik.
- **Kekurangan**:
  - Memakan kuota *Context Window*, meningkatkan biaya token input pada setiap request.
  - Kurang konsisten jika dipaksa mengikuti format sintaks yang sangat ketat tanpa panduan ketat.

### 3.2 Fine-Tuning (Parameter-Efficient Fine-Tuning / LoRA)
- **Definisi**: Proses melatih ulang bobot model (*weights*) menggunakan dataset spesifik pasangan (Input Prompt, Desired Output). Modern fine-tuning menggunakan **LoRA (Low-Rank Adaptation)** untuk mengupdate sebagian kecil matriks bobot tambahan ($\Delta W = A \times B$).
- **Keunggulan**:
  - **Gaya & Format Terkunci**: Sangat handal mengunci gaya bahasa, dialek khusus, atau format JSON/XML kompleks tanpa memerlukan contoh few-shot yang panjang.
  - **Token Input Efisien**: Tidak perlu mengulang instruksi panjang di System Prompt, menghemat biaya input token.
  - **Offline Domain Specialization**: Model lokal berukuran kecil (7B-8B) yang di-fine-tune dapat menandingi model 70B untuk tugas spesifik tertentu.
- **Kekurangan**:
  - Pengetahuan bersifat statis (terkunci pada waktu training).
  - Risiko *Catastrophic Forgetting* (kemampuan penalaran umum model mengalami penurunan).
  - Biaya komputasi training awal dan tantangan pemeliharaan versi model.

### 3.3 Pohon Keputusan (*Decision Framework*)

```
Apakah Anda perlu menyuntikkan fakta/informasi baru yang terus berubah?
 ├── YA  ──> Gunakan RAG + Prompt Engineering
 └── TIDAK ──> Apakah Anda ingin mengunci gaya bahasa, jargon, atau format khusus secara permanen?
                ├── YA  ──> Gunakan Fine-Tuning (LoRA / QLoRA)
                └── TIDAK ──> Gunakan Prompt Engineering (Few-Shot / System Prompt)
```

---

## 📐 BAB 4: EMBEDDINGS AND VECTOR SEARCH

**Vector Embeddings** adalah representasi numerik berbentuk array bilangan riil berkondisi tinggi (*high-dimensional dense vectors*) yang menangkap makna semantik dari teks, gambar, atau audio.

```
Teks Input: "Kucing tidur di atas karpet"
     │
[Embedding Model e.g. text-embedding-3-small]
     │
Vektor Dense (1536 Dimensi): [-0.021, 0.045, 0.128, -0.009, ..., 0.082]
```

### 4.1 Metrik Keserupaan Vektor (*Vector Distance Metrics*)
Untuk menghitung seberapa dekat dua vektor semantik $\vec{A}$ dan $\vec{B}$:

1. **Cosine Similarity** ($\cos(\theta)$):
   Mengukur sudut antara dua vektor tanpa mempedulikan magnitudo/panjang vektor. Rentang nilai: $[-1, 1]$ (atau $[0, 1]$ pada vektor yang dinormalisasi).
   $$\text{Cosine Similarity}(\vec{A}, \vec{B}) = \frac{\vec{A} \cdot \vec{B}}{\|\vec{A}\| \|\vec{B}\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}$$

2. **Dot Product (Inner Product)**:
   Mengukur perkalian skalar langsung. Jika kedua vektor telah dinormalisasi (magnitudo = 1), maka **Dot Product sama dengan Cosine Similarity**.
   $$\text{Dot Product}(\vec{A}, \vec{B}) = \vec{A} \cdot \vec{B} = \sum_{i=1}^{n} A_i B_i$$

3. **Euclidean Distance (L2 Distance)**:
   Mengukur jarak garis lurus antartitik dalam ruang $n$-dimensi. Nilai semakin kecil menunjukkan keserupaan semakin tinggi.
   $$d(\vec{A}, \vec{B}) = \sqrt{\sum_{i=1}^{n} (A_i - B_i)^2}$$

### 4.2 Pencarian Semantik vs Pencarian Kata Kunci (*Lexical Search*)
- **Lexical/Keyword Search (BM25 / TF-IDF)**: Mencocokkan kata yang identik secara harfiah. Gagal ketika query menggunakan sinonim (misal: "Dokter" tidak cocok dengan "Medis").
- **Semantic Search (Vector Embeddings)**: Mencocokkan berdasarkan ide/konsep. "Mobil listrik" akan memiliki skor keserupaan tinggi dengan "Kendaraan baterai EV" meskipun kata yang digunakan berbeda.

### 4.3 Struktur Indeks Vektor (*Vector Indexes*)
- **Flat Index (Exact KNN)**: Membandingkan query dengan *setiap* vektor dalam database ($O(N)$). Memiliki akurasi 100% (*100% recall*), namun sangat lambat untuk jutaan dokumen.
- **Approximate Nearest Neighbor (ANN)**:
  - **IVFFlat (Inverted File Index)**: Membagi ruang vektor menjadi klaster-klaster (Voronoi cells) dan hanya mencari pada klaster terdekat.
  - **HNSW (Hierarchical Navigable Small World)**: Membangun struktur graf multi-layer yang memungkinkan pencarian vektor skala jutaan dengan kecepatan $<5\text{ms}$ ($O(\log N)$ complexity).

---

## 🔍 BAB 5: UNDERSTAND THE BASICS OF RAG

**Retrieval-Augmented Generation (RAG)** adalah pola arsitektur yang menggabungkan kekuatan pencarian informasi (*Information Retrieval*) dengan kemampuan generasi LLM (*Generative Synthesis*). RAG memecahkan dua masalah utama LLM: **Hallucination** dan **Knowledge Cutoff**.

```
                           +-------------------------------------+
                           | 1. INGESTION & CHUNKING PIPELINE    |
                           +-------------------------------------+
                                              │
    [Dokumen Mentah] ──> [Text Chunking] ──> [Embedding Model] ──> [Vector Store (DB)]
    (PDF/Docx/HTML)      (e.g., 500 chars)     (Vektor 1536D)       (HNSW Index)

-----------------------------------------------------------------------------------------

                           +-------------------------------------+
                           | 2. QUERY & RETRIEVAL PIPELINE       |
                           +-------------------------------------+
                                              │
 User Query: "Berapa garansi laptop X?" ──> [Query Embedding]
                                                   │
                                    [Vector Cosine Search]
                                                   │
                                Top-K Relevan Chunks ([Chunk #3], [Chunk #12])

-----------------------------------------------------------------------------------------

                           +-------------------------------------+
                           | 3. AUGMENTATION & GENERATION        |
                           +-------------------------------------+
                                              │
 Augmented Prompt = System Instruction + [Retrieved Context] + User Query
                                              │
                                     [LLM Inference]
                                              │
                             Jawaban Tepat Berdasarkan Dokumen!
```

### 5.1 Tahapan Pipeline RAG
1. **Document Chunking**: Memecah dokumen panjang menjadi potongan-potongan (*chunks*) berukuran optimal (misal: 250 - 1000 tokens) dengan persentase overlap (misal: 10-15%) agar konteks di batas potongan tidak hilang.
2. **Indexing**: Mengonversi setiap chunk menjadi vektor embedding dan menyimpannya di Vector Store bersama metadata (nomor halaman, judul dokumen, tanggal).
3. **Retrieval (Top-K)**: Saat query datang, query dikonversi ke vektor, lalu Vector Store mengambil $K$ potongan teks paling serupa secara semantik.
4. **Augmentation**: Menggabungkan $K$ potongan teks yang berhasil ditemukan ke dalam System Prompt/User Prompt sebagai konteks pendukung.
5. **Generation**: LLM diminta menjawab pertanyaan *hanya berdasarkan konteks yang disuntikkan*, meminimalisir halusinasi.

---

## 💰 BAB 6: PRICING OF COMMON MODELS

Ekonomi operasional AI Agent didasarkan pada kuantitas token yang diproses oleh API provider. Pemahaman struktur biaya sangat krusial untuk mencegah pembengkakan anggaran saat agent berjalan dalam siklus otomatis (*agent loop*).

```
Total Biaya Request = (Input Tokens × Rate_Input) + (Cached Input Tokens × Rate_Cached) + (Output Tokens × Rate_Output)
```

### 6.1 Struktur Biaya Token Input vs Output
- **Input Tokens**: Token dari instruksi prompt, riwayat chat, konteks RAG, serta skema tools. Biasanya dihargai **3x hingga 4x lebih murah** dibanding Output Tokens karena pemrosesan input bersifat *parallelizable prefill phase*.
- **Output Tokens**: Token yang dihasilkan oleh LLM. Lebih mahal karena diproses secara *sequential autoregressive generation* yang memakan bandwidth GPU VRAM secara signifikan.
- **Prompt Caching Discount**: Penyedia API modern (OpenAI, Anthropic, DeepSeek, Gemini) memberikan diskon **50% hingga 90%** untuk Input Tokens yang berulang (misal: System Prompt panjang atau skema tools yang sama antar request).

### 6.2 Tabel Perbandingan Harga LLM Populer (Estimasi Standar per 1 Million Tokens)

| Model | Provider | Input Price / 1M | Prompt Cache / 1M | Output Price / 1M |
| :--- | :--- | :--- | :--- | :--- |
| **GPT-4o** | OpenAI | \$2.50 | \$1.25 | \$10.00 |
| **o3-mini** | OpenAI | \$1.10 | \$0.55 | \$4.40 |
| **Claude 3.5 Sonnet** | Anthropic | \$3.00 | \$0.30 | \$15.00 |
| **Gemini 2.0 Flash** | Google | \$0.10 | \$0.025 | \$0.40 |
| **DeepSeek V3** | DeepSeek | \$0.14 | \$0.014 | \$0.28 |
| **DeepSeek R1** | DeepSeek | \$0.55 | \$0.14 | \$2.19 |

### 6.3 Kalkulasi Biaya Siklus AI Agent Multi-Turn
Dalam sebuah agen yang menjalankan siklus *ReAct* (Reasoning + Acting) sebanyak $N$ iterasi turn:
$$\text{Total Cost} = \sum_{i=1}^{N} \left( \text{Input}_i \times \text{Rate}_{\text{in}} + \text{Output}_i \times \text{Rate}_{\text{out}} \right)$$

Karena setiap iterasi membawa kembali seluruh sejarah chat (*chat history accumulation*), jumlah Input Tokens pada turn ke-$i$ membengkak secara kuadratik jika tidak dilakukan *truncation* atau *prompt caching*.

---

## 🏗️ BAB 7: ARSITEKTUR INTEGRASI FONDASI PADA AI AGENT SYSTEM

Sebuah arsitektur AI Agent modern yang efisien menggabungkan seluruh 6 konsep dasar di atas menjadi satu sistem yang harmonis:

```
                                    +-----------------------------------------+
                                    |         USER INTERFACE / CLIENT         |
                                    +--------------------+--------------------+
                                                         │ Streamed SSE Tokens
                                                         ▼
+--------------------------------------------------------------------------------------------------+
|                                    AI AGENT ORCHESTRATOR ENGINE                                  |
|                                                                                                  |
|  1. QUERY ROUTER (Standard vs Reasoning Selection)                                              |
|     ├── Query Logika Sederhana/QA ──> Standard Fast Model (Gemini 2.0 Flash / GPT-4o)             |
|     └── Query Algoritma Kompleks ──> Reasoning Model (DeepSeek R1 / o3-mini)                     |
|                                                                                                  |
|  2. CONTEXT RETRIEVAL (Vector Embeddings & RAG)                                                  |
|     └── Vector DB (HNSW Index + Cosine Similarity) ──> Inject Top-K Context                      |
|                                                                                                  |
|  3. COST & BUDGET GUARDRAILS                                                                     |
|     └── Prompt Caching Optimization + Token Counter (Biaya terpantau real-time)                  |
+--------------------------------------------------------------------------------------------------+
```

Dengan menguasai 6 elemen dasar ini (*Streaming*, *Reasoning*, *Fine-Tuning*, *Embeddings*, *RAG*, dan *Pricing*), pengembang dapat membangun AI Agent yang tidak hanya cerdas dan responsif, tetapi juga hemat biaya dan dapat diandalkan secara arsitektural.
