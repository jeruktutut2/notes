# CATATAN SKEMA TEORI CONTEXT ENGINEERING AI

Dokumen ini berisi rangkuman konsep, arsitektur, teknik optimasi, dan metrik evaluasi dalam **Context Engineering** untuk Large Language Models (LLM) berdasarkan rekomendasi [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 1. Arsitektur Context Window & Anatomi Context

Context Window adalah jumlah maksimum token yang dapat diproses oleh LLM dalam satu kali inferensi (termasuk input prompt + output generation). Context Engineering berfokus pada optimasi pengisian context window agar LLM dapat memahami instruksi dan fakta secara efisien tanpa mengalami kegagalan akibat limit token atau *attention degradation*.

### 1.1 Anatomi Context Window
Sebuah Context Window yang terstruktur terdiri dari beberapa lapisan komponen:
1. **System Prompt & Persona Framing:** Mengatur perilaku, constraint, gaya bahasa, dan kemampuan agen.
2. **Global Rules & Safety Guardrails:** Batasan keamanan dan instruksi pemformatan output (misal: JSON Schema).
3. **Retrieval Context (RAG / External Data):** Informasi dokumen luar yang relevan dengan kueri pengguna.
4. **Episodic / Conversation History:** Riwayat percakapan sebelumnya antara user dan agen.
5. **Short-Term Memory / Entity Memory:** Ringkasan fakta pengguna (nama, preferensi, variabel aktif).
6. **Working Memory / Scratchpad:** Ruang kerja untuk penalaran bertahap (Chain-of-Thought / ReAct thoughts).
7. **User Query & Immediate Input:** Kueri terbaru dari pengguna.

### 1.2 Masalah "Lost in the Middle" & Attention Sinks
- **Lost in the Middle:** Penelitian oleh Liu et al. (2023) menunjukkan bahwa LLM memiliki kecenderungan mengingat informasi yang berada di *awal* (primacy bias) dan di *akhir* (recency bias) context window dengan sangat baik, namun performa recall turun drastis pada informasi di *tengah-tengah* context.
- **Attention Sinks (StreamingLLM):** Pada model Transformer berbasis autoregressive, token pertama dalam prompt sering bertindak sebagai "Attention Sink" yang memegang nilai attention score sangat tinggi. Jika token awal ini terpotong (truncated), kualitas generasi model akan runtuh.
- **Mitigasi:** Tempatkan fakta terpenting (System Prompt & Relevant Knowledge) di posisi paling atas dan paling bawah, serta gunakan struktur penanda XML (misal `<context>...</context>`) untuk memandu perhatian mekanisme Self-Attention.

---

## 2. Teknik Kompresi & Pemangkasan Context (Context Compression)

Menambah ukuran context window memperbesar latency (Time to First Token / TTFT) dan meningkatkan biaya token (input token cost). Oleh karena itu, kompresi context sangat penting.

### 2.1 Selective Token Compression (Mekanisme LLMLingua)
- **Prinsip:** Mengukur *information density* (kepadatan informasi) dari setiap kata/sentence menggunakan *perplexity* atau model bahasa kecil (small LM).
- **Proses:**
  1. Hitung nilai entropi/perkalian probabilitas tiap token.
  2. Hapus token dengan probabilitas sangat tinggi (seperti kata sambung, token pengisi redundan) yang tidak mengubah makna secara matematis.
  3. Mengurangi token hingga 50%-70% dengan tetap menjaga akurasi jawaban hingga >95%.

### 2.2 Semantic Truncation & Sliding Window
- **Sliding Window with Recency Decay:** Menjaga `N` turn percakapan terakhir dan membuang turn lama.
- **Importance Scoring Truncation:** Memberikan skor relevansi pada tiap paragraf/turn berdasarkan similarity kueri terbaru. Turn yang relevan tetap dipertahankan meskipun dari histori lama.

### 2.3 Benchmark Needle In A Haystack (NIAH)
NIAH adalah pengujian standar untuk mengukur akurasi retrieval in-context LLM. Sebuah "needle" (fakta kunci berukuran kecil, misal: *"Warna rahasia kota Atlantis adalah ungu metallic"*) disisipkan pada kedalaman tertentu (0% hingga 100%) di dalam "haystack" (teks panjang puluhan ribu token).

---

## 3. In-Context Memory & State Management

Memori pada LLM bukan disimpan di bobot neural network (parameter), melainkan disajikan secara dinamis di dalam context window.

### 3.1 Jenis-jenis Memori Agen AI
1. **Episodic Memory:** Catatan interaksi spesifik di masa lalu (misal: "User pernah membatalkan pesanan #1024 kemarin").
2. **Semantic Memory:** Pengetahuan fakta konseptual (misal: "Pengguna alergi terhadap kacang").
3. **Procedural Memory:** Prosedur dan petunjuk langkah-demi-langkah cara menjalankan tugas tertentu.

### 3.2 Strategi Pengelolaan Buffer Percakapan
- **Conversation Summary Buffer:** Secara otomatis menyintesis riwayat lama menjadi paragraf ringkasan eksekutif ketika token percakapan melampaui ambang batas (threshold).
- **Entity Memory:** Mengekstrak entitas kunci (User Name, Device Type, Current Preference) ke dalam format JSON/Key-Value dan memasukkannya ke dalam system prompt.
- **Scratchpad State:** Ruang kerja internal di mana agen menyimpan status sementara (misal: variabel kalkulasi, daftar tugas terverifikasi) selama beberapa siklus tool-use.

---

## 4. Dynamic Context Assembly & Context Caching

### 4.1 Dynamic Context Assembler Pipeline
Perakitan prompt tidak lagi menggunakan string concatenation sederhana (`"Hello " + input`), melainkan melalui pipeline:
$$\text{Final Context} = \mathcal{A}(\text{SystemTemplate}, \text{EntityMemory}, \text{RetrievedChunks}, \text{FilteredHistory}, \text{UserQuery})$$
Pipeline ini mengevaluasi kondisional (misal: hanya masukkan panduan bayar jika user bertanya soal billing) dan menerapkan constraint budget token secara ketat.

### 4.2 Prompt Caching / KV-Cache Reuse
- **Cara Kerja:** LLM modern (Anthropic, OpenAI, vLLM) mengizinkan *prefix caching*. Jika bagian awal prompt (System Prompt + Large Documents) tetap identik antar request, GPU dapat menggunakan kembali hasil perhitungan *Key-Value (KV) Cache* dari memori VRAM.
- **Dampak:**
  - Mengurangi latency TTFT hingga 80%.
  - Mengurangi biaya input token hingga 50-90%.
- **Aturan Prefix Caching:** Karakter pada awal prompt hingga batas cache harus 100% identik (*byte-for-byte exact match*).

### 4.3 Multi-Tenant Context Hygiene & Security
Dalam aplikasi multi-user:
- **Context Contamination:** Terjadinya kebocoran data pengguna A ke pengguna B karena kesalahan penggabungan context buffer.
- **PII Redaction & Sanitization:** Melakukan hashing/masking otomatis terhadap informasi pribadi (email, nomor kartu kredit, alamat) sebelum context dimasukkan ke LLM.

---

## 5. Context Routing & Multi-Context Orchestration

### 5.1 Context Isolation pada Multi-Agent
Pada arsitektur Multi-Agent, mengirimkan seluruh context percakapan ke semua sub-agent membuat token boros dan membingungkan agen.
- **Sub-Agent Context Isolation:** Setiap sub-agent (misal: *Code Generator*, *Security Auditor*, *Documentation Specialist*) hanya menerima slice context yang relevan bagi tugas spesifiknya.

### 5.2 Context Sharding & Map-Reduce Pattern
Untuk menganalisis dokumen raksasa (ratusan halaman):
1. **Shard:** Dokumen dipecah menjadi `N` bagian (shards).
2. **Map Phase:** Setiap shard dikirim secara paralel ke LLM untuk membuat ringkasan/analisis lokal.
3. **Reduce Phase:** Hasil analisis lokal digabungkan ke dalam satu context master untuk sintesis akhir oleh LLM.

---

## 6. Metrik Evaluasi & Benchmarking Kualitas Context

Kualitas context yang dimasukkan ke LLM menentukan 90% keberhasilan jawaban agen (Garbage In, Garbage Out).

### 6.1 Metrik Kualitas Context (RAGAS / TruLens Framework)
1. **Context Precision:** Persentase informasi relevan dibandingkan total informasi yang dimasukkan.
   $$\text{Context Precision} = \frac{|\text{Relevan} \cap \text{Retrieved}|}{|\text{Retrieved}|}$$
2. **Context Recall:** Seberapa banyak informasi yang dibutuhkan untuk menjawab kueri yang berhasil ditangkap oleh context.
   $$\text{Context Recall} = \frac{|\text{Relevan} \cap \text{Retrieved}|}{|\text{Ground Truth Relevan}|}$$
3. **Information Density Score:** Rasio informasi unik bermanfaat per 100 token.
4. **Noise-to-Signal Ratio (NSR):** Rasio kata pengisi/irrelevant terhadap kata kunci esensial.

### 6.2 Degredasi Performa & Analisis Biaya Token
- **Cost & Latency Modeling:** Mengalkulasi ekspansi linier/kuadratik dari Time-To-First-Token (TTFT) dan biaya kuadratik pada panjang context.
- **Hallucination Rate vs Context Size:** Semakin besar context window yang tidak terstruktur, semakin tinggi probabilitas LLM mengalami kebingungan (*hallucination / distraction*).
