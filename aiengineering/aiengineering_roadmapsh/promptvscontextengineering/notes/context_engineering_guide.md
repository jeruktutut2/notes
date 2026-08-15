# Panduan Lengkap Context Engineering (AI Engineering Roadmap)

Panduan ini mendokumentasikan konsep dasar hingga lanjutan **Context Engineering** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 1. Konsep Dasar & Anatomy Context Window

**Context Engineering** adalah disiplin merancang, mengompresi, mengisolasi, dan merutekan seluruh *environment state*, memori percakapan, serta dokumen pengetahuan yang diberikan ke LLM dalam batas *Context Window*.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        LLM CONTEXT WINDOW (128K)                        │
├───────────────┬─────────────────┬───────────────────┬──────────────────┤
│ System Prefix │ Summary Buffer  │  Dynamic RAG Docs │ Output Reserve   │
│ (Prefix Cache)│ (Episodic Mem)  │ (Density Pruned)  │ (Generation Limit│
│  ~2,000 Tok   │  ~10,000 Tok    │   ~108,000 Tok    │  ~8,000 Tok      │
└───────────────┴─────────────────┴───────────────────┴──────────────────┘
```

### Fenomena Lost-in-the-Middle (U-Shape Curve)
Penelitian (*Liu et al.*) menunjukkan bahwa LLM mengingat informasi dengan akurasi tertinggi di **Awal (Beginning)** dan **Akhir (End)** prompt context. Informasi yang diletakkan di **Tengah (Middle)** mengalami penurunan akurasi recall hingga 50%.

> **Solusi Context Eng:** Letakkan *system policy* & dokumen yang paling kritis di awal atau akhir context window.

---

## 2. Token Information Density & Compression

Untuk menekan latensi *Time-To-First-Token (TTFT)* dan biaya API:

1. **Selective Token Pruning (LLMLingua Approach)**:
   - Menghitung nilai *surprisal* / informasi entropy dari setiap kata.
   - Kata-kata *low-information filler* (seperti kata sambung yang berlebihan) dibuang tanpa mengganggu pemahaman LLM.
2. **Semantic Truncation & Summarization**:
   - Merangkum percakapan lampau menggunakan *Summarization Buffer* saat percakapan melebihi ambang batas (*sliding window threshold*).

---

## 3. Tripartite Memory & State Architecture

| Komponen Memori | Definisi | Implementasi Context |
|-----------------|----------|----------------------|
| **Procedural Memory** | Aturan bisnis, persona, dan instruksi alur kerja tetap. | System Prompt Prefix (dapat di-cache). |
| **Semantic Memory** | Fakta panjang tentang pengguna (profil, preferensi, akun). | JSON Profile Store yang di-inject dinamis. |
| **Episodic Memory** | Riwayat interaksi percakapan per sesi. | Sliding Chat Buffer + Summary Window. |

---

## 4. Prefix Caching & Optimization

1. **KV Caching / Prompt Caching**:
   - Menyimpan *Key-Value (KV) Attention State* dari blok teks statis di memori server GPU (misal: vLLM, Anthropic Prompt Caching).
   - Menghasilkan potongan harga hingga 80% untuk *cache read* dan memotong latensi TTFT hingga mendeteksi 0ms overhead untuk bagian prefix statis.
2. **Multi-Tenant Isolation & PII Masking**:
   - Menyamarkan data pribadi (Email, HP, NIK, No Kartu Kredit) menggunakan token placeholder (`[PII_EMAIL_1]`) sebelum dimasukkan ke context window.
   - Memastikan tidak ada percampuran context antar penyewa (*tenant isolation*).
