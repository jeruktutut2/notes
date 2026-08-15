# CATATAN TEORI LENGKAP: AGENT MEMORY UNTUK AI AGENTS

Dokumen ini memuat panduan komprehensif mengenai **Agent Memory** pada sistem AI Agents berdasarkan alur arsitektur [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan visualisasi diagram komponen memory.

---

## 1. APA ITU AGENT MEMORY? (WHAT IS AGENT MEMORY?)

### 1.1 Kebutuhan Memori pada AI Agents
LLM (Large Language Models) secara native bersifat *stateless* — setiap kali sebuah API call dikirimkan ke model, LLM tidak mengingat interaksi sebelumnya kecuali riwayat percakapan dimasukkan kembali ke dalam prompt. Bagi sebuah **AI Agent** yang mandiri dan beroperasi dalam durasi panjang (*long-running agent*), keterbatasan *stateless* ini menjadi hambatan utama.

**Agent Memory** adalah mekanisme yang memungkinkan AI Agent untuk:
1. Menyimpan konteks tugas saat ini (*working memory / scratchpad*).
2. Mengingat interaksi sebelumnya dengan pengguna atau lingkungan (*history / experience*).
3. Mengakses pengetahuan eksternal yang relevan secara dinamis (*retrieval-augmented knowledge*).
4. Mempertahankan identitas, preferensi pengguna, dan fakta jangka panjang (*long-term persistence*).

---

### 1.2 Taksonomi Memori: Short-Term vs Long-Term Memory

| Karakteristik | Short-Term Memory (STM) | Long-Term Memory (LTM) |
| :--- | :--- | :--- |
| **Lokasi Storage** | In-Prompt / Context Window (RAM LLM) | External Storage (Vector DB, SQL, NoSQL, File System) |
| **Kapasitas** | Terbatas oleh *Context Window* model (e.g. 8k - 1M tokens) | Tidak terbatas (Terbatas pada disk storage DB) |
| **Kecepatan Akses** | Sangat Cepat (langsung diproses oleh mekanisme Attention) | Memerlukan Latensi Query & Retrieval (RAG / DB lookup) |
| **Persistensi** | *Transient* (Hilang setelah sesi percakapan selesai) | *Persistent* (Bertahan antar-sesi & restart sistem) |
| **Biaya Token** | Meningkat seiring panjangnya konteks (*Context Cost*) | Efisien (Hanya memuat potongan informasi relevan) |
| **Komponen Visual Diagram** | **Within Prompt** | **Vector DB / SQL / Custom** |

```
+-------------------------------------------------------------------------+
|                           AGENT MEMORY ARCHITECTURE                      |
+-------------------------------------------------------------------------+
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   |                       WHAT IS AGENT MEMORY?                     |   |
|   +-----------------------------------------------------------------+   |
|                                    |                                    |
|              +---------------------+---------------------+              |
|              |                                           |              |
|   +-----------------------+                   +---------------------+   |
|   |   SHORT TERM MEMORY   |                   |  LONG TERM MEMORY   |   |
|   +-----------------------+                   +---------------------+   |
|   |    (Within Prompt)    |                   | (Vector DB / SQL /  |   |
|   |                       |                   |      Custom)        |   |
|   +-----------------------+                   +---------------------+   |
|                                                                         |
+-------------------------------------------------------------------------+
```

#### A. Short-Term Memory (Within Prompt)
- **Working Memory / Scratchpad**: Tempat agent menyimpan hasil pemikiran sementara (*CoT - Chain of Thought*), status *plan*, dan *observation* dari *tool invocation*.
- **Conversation Window**: Riwayat *chat messages* (System, User, Assistant, Tool Output) yang berada dalam konteks prompt aktif.
- **Attention Mechanism**: Model memanfaatkan *Self-Attention* untuk menghubungkan informasi yang ada di dalam prompt secara langsung.

#### B. Long-Term Memory (Vector DB / SQL / Custom Store)
- **Vector Database**: Menyimpan representasi *vector embedding* dari teks untuk pencarian kemiripan semantik (*semantic similarity search*). Contoh: Pinecone, Qdrant, ChromaDB, Milvus, PGVector.
- **SQL / Relational DB**: Menyimpan informasi terstruktur seperti tabel pengguna, transaksi, *logs*, dan metrik performa. Contoh: PostgreSQL, SQLite.
- **Custom / Key-Value Stores**: Menyimpan status agen, konfigurasi, dan dokumen JSON. Contoh: Redis, MongoDB.

---

## 2. EPISODIC VS SEMANTIC MEMORY

Arsitektur memori AI Agents mengadaptasi teori kognitif psikologi tentang memori manusia, yang membagi **Explicit/Declarative Memory** menjadi dua kategori utama:

```
                  +-----------------------------------+
                  |   EPISODIC VS SEMANTIC MEMORY     |
                  +-----------------------------------+
                                    |
            +-----------------------+-----------------------+
            |                                               |
  +-------------------+                           +-------------------+
  |  EPISODIC MEMORY  |                           |  SEMANTIC MEMORY  |
  +-------------------+                           +-------------------+
  | • Event Sequence  |                           | • Facts & Knowledge|
  | • Timestamps      |                           | • User Profiles   |
  | • "What Happened" |                           | • "What is Known" |
  +-------------------+                           +-------------------+
```

### 2.1 Episodic Memory (Memori Episodis / Pengalaman)
- **Definisi**: Memori yang merekam urutan kejadian, pengalaman spesifik, serta jejak tindakan (*trajectories*) yang dialami oleh agent di masa lalu beserta stempel waktu (*timestamp*).
- **Pertanyaan Utama**: *"Apa yang telah terjadi sebelumnya?"*, *"Langkah apa yang berhasil menyelesaikan masalah serupa kemarin?"*
- **Karakteristik**:
  - Kontekstual dan terikat waktu (*time-bound*).
  - Menyimpan *Agent Action Loop*: `(State, Action, Observation, Outcome)`.
  - Berguna untuk *few-shot learning from past execution*, introspeksi kesalahan, dan menghindari pengulangan blunder.

### 2.2 Semantic Memory (Memori Semantik / Pengetahuan Faktual)
- **Definisi**: Memori yang menyimpan pengetahuan umum, fakta, preferensi, aturan bisnis, dan konsep yang telah disarikan (*abstracted*) dari pengalaman atau dokumen eksternal.
- **Pertanyaan Utama**: *"Apa fakta mengenai topik ini?"*, *"Apa preferensi bahasa pengguna ini?"*
- **Karakteristik**:
  - Terbebas dari konteks waktu spesifik (*time-independent*).
  - Berbentuk *User Profiles*, *Domain Knowledge*, *Rules & Guidelines*, atau *Knowledge Graph (Entity-Relation-Attribute)*.
  - Diperbarui melalui ekstraksi fakta (*Fact Extraction*) saat percakapan berlangsung.

### 2.3 Tabel Perbandingan Episodic vs Semantic Memory

| Fitur | Episodic Memory | Semantic Memory |
| :--- | :--- | :--- |
| **Fokus Informasi** | Pengalaman, peristiwa, langkah kerja (*trajectories*) | Fakta, konsep, definisi, profil pengguna |
| **Format Data** | Log kronologis `(t, input, reasoning, action, result)` | Key-Value, Knowledge Graph, JSON Profile, Document Vector |
| **Metode Retrieval** | Semantic Similarity + Temporal Recency + Success Metric | Semantic Similarity / Exact Key Lookup |
| **Contoh Penggunaan** | *"Minggu lalu agent gagal menjalankan query SQL karena port 5432 closed"* | *"Database server beralih ke port 5433 menurut konfigurasi prod"* |

---

## 3. MAINTAINING MEMORY (PEMELIHARAAN MEMORI)

Seiring bertambahnya waktu dan interaksi, kapasitas memori agent akan membengkak. Jika tidak dipelihara, sistem akan mengalami hambatan: *Context Window Overflow*, biaya token melonjak, latensi meningkat, dan masalah *Memory Pollution* (informasi usang/bertentangan).

Oleh karena itu, arsitektur Agent Memory membutuhkan modul **Maintaining Memory** yang terdiri dari 4 komponen pilar:

```
+-------------------------------------------------------------------------+
|                            MAINTAINING MEMORY                           |
+-------------------------------------------------------------------------+
|                                                                         |
|   +-----------------------------------------------------------------+   |
|   |                  RAG and Vector Databases                       |   |
|   +-----------------------------------------------------------------+   |
|   |                  User Profile Storage                           |   |
|   +-----------------------------------------------------------------+   |
|   |                  Summarization / Compression                    |   |
|   +-----------------------------------------------------------------+   |
|   |                  Forgetting / Aging Strategies                  |   |
|   +-----------------------------------------------------------------+   |
|                                                                         |
+-------------------------------------------------------------------------+
```

---

### 3.1 RAG and Vector Databases (Retrieval-Augmented Generation)

**RAG** adalah teknik untuk menyuntikkan dokumen/pengetahuan relevan dari *Vector Database* ke dalam prompt short-term memory agen secara dinamis.

#### Algoritma Utama:
1. **Chunking**: Teks dipecah menjadi potongan (*chunks*) berukuran 250 - 1000 karakter dengan *overlap*.
2. **Embedding Generation**: Mengubah potongan teks menjadi vektor numerik berdimensi tinggi \(d \in \mathbb{R}^n\).
3. **Similarity Search**: Mencari k-tetangga terdekat (*Top-K Nearest Neighbors*) menggunakan pengukuran jarak:
   - **Cosine Similarity**:
     \[
     \text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|} = \frac{\sum_{i=1}^{n} A_i B_i}{\sqrt{\sum_{i=1}^{n} A_i^2} \sqrt{\sum_{i=1}^{n} B_i^2}}
     \]
   - **Dot Product** atau **Euclidean Distance (\(L_2\))**.
4. **Context Injection**: Hasil retrieval Top-K disuntikkan ke dalam bagian `<context>` pada system prompt.

---

### 3.2 User Profile Storage

**User Profile Storage** bertugas mencatat dan memperbarui informasi spesifik pengguna secara berkelanjutan agar percakapan terasa personal dan efisien.

#### Struktur Data Profile:
```json
{
  "user_id": "usr_99812",
  "name": "Budi Santoso",
  "preferences": {
    "language": "Indonesian",
    "coding_style": "PEP8 Python with explicit typing",
    "communication_tone": "Concise & Professional"
  },
  "extracted_facts": [
    {"fact": "Bekerja sebagai Data Engineer", "confidence": 0.95, "updated_at": "2026-07-20"},
    {"fact": "Menggunakan macOS dengan Apple Silicon", "confidence": 0.99, "updated_at": "2026-07-26"}
  ]
}
```

#### Mekanisme Pembaruan Profile:
1. **Fact Extraction Pipeline**: Menjalankan instruksi latar belakang (*background extraction prompt*) untuk mengekstrak entitas & preferensi dari input pengguna.
2. **Conflict Resolution**: Jika pengguna menyebutkan fakta baru yang bertentangan (misal: *"Saya pindah ke Bandung"* vs fakta lama *"Saya tinggal di Jakarta"*), sistem memperbarui nilai terbaru dan mengarsipkan riwayat lama.

---

### 3.3 Summarization / Compression (Kompresi & Ringkasan Memori)

Untuk mencegah pesan dalam short-term memory melampaui batas *context window*, teknik **Summarization / Compression** digunakan untuk merangkum percakapan tanpa menghilangkan konteks krusial.

#### Strategi Kompresi Utama:
1. **Summary Buffer Memory (Sliding Window + Condensation)**:
   - Menyimpan \(N\) pesan terbaru secara utuh (*raw messages*).
   - Pesan yang lebih lama dari \(N\) dirangkum secara konsisten menjadi satu paragraph ringkasan (*condensed summary*) yang terus diperbarui secara iteratif.
2. **Recursive / Progressive Summarization**:
   \[
   \text{Summary}_{t} = \text{LLM\_Summarize}(\text{Summary}_{t-1} + \text{Message}_{t})
   \]
3. **Token Pruning / Selective Trimming**:
   - Menghapus pesan-pesan instruksi sementara (seperti output log yang sangat panjang atau pesan kesalahan sementara) setelah tugas selesai, dan hanya menyisakan jawaban akhir.

---

### 3.4 Forgetting / Aging Strategies (Strategi Retensi & Peluruhan Memori)

Sama seperti otak manusia, AI Agent membutuhkan mekanisme untuk **melupakan** (*forgetting*) memori yang usang, tidak relevan, atau memiliki tingkat penting (*importance*) yang rendah.

#### 1. Formula Peluruhan Memori (Memory Decay Rate):
Skor retensi memori \(S(t)\) dihitung berdasarkan kurva peluruhan eksponensial (*Ebbinghaus Forgetting Curve*) dipadukan dengan frekuensi akses dan skor pentingnya informasi (*importance score*):

\[
S(t) = S_0 \cdot e^{-\lambda \cdot \Delta t} + \alpha \cdot \text{AccessCount}
\]

Dimana:
- \(S_0\): Skor kepentingan awal (*Initial Importance Score* dari scale 1-10).
- \(\lambda\): *Decay Factor* (Tingkat peluruhan per satuan waktu).
- \(\Delta t\): Durasi waktu sejak memori terakhir kali diakses.
- \(\alpha\): Bobot penguat akses (*Access Amplification Weight*).

#### 2. Eviction Policies (Kebijakan Penghapusan Memori):
- **LRU (Least Recently Used)**: Menghapus memori yang paling lama tidak diakses saat kapasitas penuh.
- **Importance Threshold Eviction**: Menghapus memori yang memiliki skor retensi \(S(t) < S_{\text{min}}\).
- **TTL (Time-To-Live)**: Memori dengan stempel expired yang diset otomatis dibersihkan.

---

## 4. RINGKASAN INTEGRASI AGENT MEMORY PIPELINE

```
+------------------------------------------------------------------------+
|                      FULL AGENT MEMORY FLOW                            |
+------------------------------------------------------------------------+
|                                                                        |
|  [ User Input ]                                                        |
|        |                                                               |
|        v                                                               |
|  [ Memory Retrieval ]  <--->  [ Long-Term Memory / RAG Vector DB ]     |
|        |                      [ User Profile Storage ]                 |
|        v                                                               |
|  [ Context Assembly ]  ---->  Injects (System Prompt + Profile + RAG   |
|        |                              + Short Term History)            |
|        v                                                               |
|  [ LLM Inference & Action ]                                            |
|        |                                                               |
|        v                                                               |
|  [ Memory Update Pipeline ]                                            |
|        |---> Append to Short-Term Memory                              |
|        |---> Extract & Update Semantic Memory (Facts/Profiles)        |
|        |---> Save Episodic Event Log                                   |
|        |---> Compress / Summarize if Context Window Limit Reached      |
|        |---> Apply Forgetting / Aging Policy to Old Memories           |
|                                                                        |
+------------------------------------------------------------------------+
```

Dokumen ini menjadi acuan teori utama bagi seluruh simulasi di folder `01_what_is_agent_memory`, `02_episodic_vs_semantic_memory`, dan `03_maintaining_memory`.
