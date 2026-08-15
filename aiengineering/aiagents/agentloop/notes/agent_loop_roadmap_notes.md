# PANDUAN LENGKAP & TEORI AGENT LOOP - AI AGENTS ROADMAP

Dokumen ini berisi catatan komprehensif mengenai **Agent Loop** berdasarkan [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan arsitektur visual sistem AI Agent modern.

---

## 💡 Apa Itu Agent Loop?

Dalam paradigma AI tradisional, interaksi dengan Large Language Model (LLM) bersifat **Single Turn** atau **Stateless Chat** (*Prompt -> Response*). 

Namun, **AI Agent** dirancang untuk menyelesaikan tugas kompleks secara otonom (*autonomous goal achievement*). Untuk mencapai tujuan tersebut, agent membutuhkan mekanisme berulang yang memungkinkannya mengamati lingkungan, merencanakan langkah, mengeksekusi tindakan (menggunakan tool), melihat hasil observasi, dan melakukan refleksi/koreksi mandiri sampai tujuan tercapai. Siklus berulang ini disebut **Agent Loop**.

```
               ┌────────────────────────┐
               │ 1. Perception / Input  │
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │   2. Reason and Plan   │
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │ 3. Acting / Tool Call  │
               └───────────┬────────────┘
                           │
                           ▼
               ┌────────────────────────┐
               │ 4. Observe & Reflect   │
               └───────────┬────────────┘
                           │
             ┌─────────────┴─────────────┐
             │ Goal Reached?             │
             │  ├── Ya  ──► [ Selesai ]  │
             │  └── Tidak ─► [ Repeat ]  │
             └───────────────────────────┘
```

---

## 🔄 4 Pilar Utama Siklus Agent Loop

 Sesuai dengan diagram pertama pada roadmap, siklus Agent Loop terdiri dari 4 tahap berurutan:

### 1. Perception / User Input (Persepsi & Input Pengguna)
- **Definisi**: Tahap awal di mana agent menerima sinyal dari dunia luar. Sinyal ini dapat berupa teks query dari manusia, gambar/audio (multimodal), webhook, file log, atau event dari sistem internal.
- **Komponen Kunci**:
  - **Input Parsing & Intent Extraction**: Mengubah input mentah menjadi variabel terstruktur (Intent, Entities, Target Goal).
  - **Context Ingestion**: Menggabungkan input pengguna dengan konteks memori (riwayat percakapan, preferensi pengguna, aturan sistem).
  - **Input Sanitization & Guardrails**: Memeriksa keamanan input dari ancaman *Prompt Injection*, *Jailbreak*, atau payload berbahaya sebelum masuk ke tahap reasoning.

### 2. Reason and Plan (Penalaran & Perencanaan)
- **Definisi**: Otak dari AI Agent di mana LLM menganalisis persepsi saat ini dan menentukan langkah-langkah selanjutnya yang harus diambil.
- **Metode & Pola Popular**:
  - **ReAct (Reasoning + Acting)**: Mendorong agent menulis *Thought* (pemikiran) sebelum menentukan *Action* (tindakan).
  - **Chain-of-Thought (CoT)**: Menguraikan penalaran langkah demi langkah secara sistematis.
  - **Task Decomposition (DAG Planning)**: Memecah goal besar menjadi sub-tugas terurut dalam bentuk Directed Acyclic Graph.
  - **Tree-of-Thoughts (ToT)**: Mengeksplorasi beberapa cabang perencanaan sekaligus dan memilih jalur paling optimal.

### 3. Acting / Tool Invocation (Tindakan & Eksekusi Tool)
- **Definisi**: Tahap eksekusi di mana agent berinteraksi dengan dunia luar menggunakan pemanggilan fungsi (Tool/Function Calling).
- **Jenis Tools Umum**:
  - **Web Browsing & Search Engine**: Mengambil informasi terkini dari internet.
  - **Code Interpreter / Sandbox**: Menjalankan kode Python/Bash untuk komputasi atau manipulasi file.
  - **API Interoperabilitas**: Memanggil layanan REST/GraphQL (Gmail, Slack, Database SQL, Jira).
- **Mekanisme Eksekusi**:
  - **Schema Validation**: Memastikan argumen JSON sesuai dengan spesifikasi parameter tool.
  - **Error Handling & Retry**: Menangani kegagalan eksekusi (timeout, 404, rate limit) dengan graceful recovery.

### 4. Observation & Reflection (Observasi & Refleksi)
- **Definisi**: Tahap di mana agent membaca hasil dari eksekusi tool (*Observation*), mengevaluasi apakah hasil sesuai harapan, dan memperbarui memori internalnya (*Reflection*).
- **Mekanisme Kunci**:
  - **Result Processing**: Mengompresi atau memformat hasil tool agar muat dalam context window.
  - **Self-Correction (Self-Reflect)**: Jika eksekusi tool menghasilkan eror atau jawaban yang salah, agent merefleksikan kegagalan tersebut dan merencanakan pendekatan alternatif di loop berikutnya.
  - **State & Memory Management**: Menyimpan riwayat *Thought-Action-Observation* ke dalam Working Memory.
  - **Termination Evaluation**: Menilai kriteria penghentian (*Stop Condition*) — apakah tugas selesai atau batas maksimum iterasi telah tercapai.

---

## 🎯 5 Contoh Usecase Agent Loop (Example Usecases)

Sesuai dengan diagram kedua, Agent Loop diterapkan pada berbagai domain industri modern:

| Usecase | Deskripsi Agent Loop | Contoh Tools Utama |
|---------|----------------------|-------------------|
| **1. Personal Assistant** | Mengelola agenda harian, menyaring email, menjadwalkan rapat, dan mengirim pengingat secara otomatis. | Calendar API, Email Client, Task Manager, Weather API |
| **2. Code Generation** | Membaca syarat fitur, menulis kode program, menjalankannya di unit test/sandbox, mengevaluasi stack trace jika eror, dan memperbaiki kode secara otomatis hingga pas. | File System, Code Runner / Sandbox, Linter, Git |
| **3. Data Analysis** | Menerima file CSV/JSON, merencanakan agregasi data, mengeksekusi perhitungan statistik, dan menyusun laporan ringkasan visual. | Pandas, SQL Engine, Chart Generator, File Reader |
| **4. Web Scraping / Crawling** | Menerima kata kunci target, mencari URL, mengekstrak DOM/HTML, mengekstrak tautan terkait, dan mengumpulkan data spesifik secara rinci. | HTTP Client, HTML Parser, Headless Browser, Vector Store |
| **5. NPC / Game AI** | Karakter non-pemain dalam game yang mengamati kondisi dunia (kesehatan, posisi musuh), merencanakan strategi pertarungan/dialog, dan bertindak secara real-time. | Game Engine State API, Pathfinding, Dialogue Tree, Inventory Manager |

---

## ⚙️ Tantangan & Solusi Teknikal dalam Agent Loop

1. **Infinite Loop Protection**:
   - *Masalah*: Agent terjebak memanggil tool yang sama berulang kali karena jawaban eror.
   - *Solusi*: Tetapkan `max_iterations` (misal 10-15 turn), lacak hash dari tool call yang identik.
2. **Context Window Management**:
   - *Masalah*: Riwayat *Thought-Action-Observation* yang panjang dapat memenuhi batas token LLM.
   - *Solusi*: Gunakan **Context Truncation** atau **Summarization Loop** untuk mengompresi observasi lama.
3. **Safety & Tool Sandboxing**:
   - *Masalah*: Agent mengeksekusi perintah berbahaya (misal `rm -rf /` atau penghapusan DB).
   - *Solusi*: Terapkan **Human-in-the-Loop (HITL)** untuk tindakan bermutasi tinggi (Write/Delete) dan sandbox terisolasi.

---

## 📌 Kesimpulan
Agent Loop adalah fondasi utama yang mengubah Large Language Model statis menjadi **AI Agent otonom yang cerdas**. Dengan memahami siklus *Perception -> Reason -> Act -> Reflect*, pengembang dapat membangun agent yang tangguh, adaptif, dan mampu menyelesaikan permasalahan kompleks secara mandiri.
