# DOCUMENTATION: CONTEXT ENGINEERING (ROADMAP.SH AI ENGINEER)

Dokumen ini mendokumentasikan seluruh **4 Elemen Kunci Context Engineering** dari kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 📑 Daftar 4 Topik Utama Context Engineering

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         CONTEXT ENGINEERING ROADMAP                      │
├───────────────────────┬────────────────────────┬─────────────────────────┤
│ 1. External Memory    │ 2. RAG & Dynamic Filter│ 3. Context Compaction   │
│ 4. Context Isolation  │                        │                         │
└───────────────────────┴────────────────────────┴─────────────────────────┘
```

---

## 1. External Memory
- **Penjelasan**: Arsitektur penyimpanan memori eksternal (Redis, Vector Database, Relational DB) untuk mengelola *state* jangka panjang di luar batas *Context Window* LLM.
- **Tipe Memori**:
  - **Episodic Memory**: Riwayat percakapan transaksional per sesi.
  - **Semantic Memory**: Profil pengguna, fakta, dan preferensi permanen.
  - **Procedural Memory**: Aturan alur kerja dan sistem bisnis bawaan.

## 2. RAG and Dynamic Filters
- **Penjelasan**: Penggabungan *Retrieval-Augmented Generation* (RAG) dengan *Dynamic Metadata Filtering* untuk mengambil dokumen yang presisi secara kontekstual.
- **Hybrid Search**: Kombinasi pencarian vektor (*Dense Retrieval*) + pencarian kata kunci (*BM25 Sparse Retrieval*) + *Cross-Encoder Re-Ranking*.
- **Dynamic Metadata Filtering**: Memfilter pencarian berdasarkan metadata (`tenant_id`, `date`, `category`) sebelum kalkulasi vektor dilakukan.

## 3. Context Compaction (Tokens & History)
- **Penjelasan**: Teknik pengompresan konteks untuk menghemat token dan menghindari *Context Window Overflow*.
- **Metode utama**:
  - **LLMLingua Token Pruning**: Membuang kata-kata berinformasi rendah berdasarkan nilai surprisal.
  - **Summarization Buffer**: Merangkum riwayat lama menjadi ringkasan faktual.
  - **Recency Decay**: Membuang bagian konteks tertua yang tidak relevan dengan query terbaru.

## 4. Context Isolation (Privacy & Multi-Tenant Boundaries)
- **Penjelasan**: Isolasi ketat untuk menjamin data antar penyewa (*multi-tenant*) tidak saling membocorkan informasi dan mengamankan data sensitif pengguna.
- **Komponen Utama**:
  - **PII Masking / Redaction**: Mengganti No HP, Email, NIK dengan token placeholder sebelum masuk ke LLM.
  - **Boundary Isolation Tags**: Penggunaan XML tags terisolasi `<tenant_boundary>` untuk mencegah kebocoran antar tenant.
  - **Sub-Agent Isolation**: Membatasi konteks yang diberikan ke sub-agent hanya pada data relevan untuk tugas spesifiknya.
