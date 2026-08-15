# ⚖️ MODUL 02: RAG VS FINE-TUNING

Dalam pengembangan aplikasi AI berbasis LLM, salah satu keputusan arsitektural terbesar adalah memilih antara **Retrieval-Augmented Generation (RAG)** atau **Fine-Tuning**.

---

## 🔍 Perbandingan Konseptual

| Dimensi Evaluasi | Retrieval-Augmented Generation (RAG) | Fine-Tuning |
| :--- | :--- | :--- |
| **Sumber Pengetahuan (*Knowledge Source*)** | Memori Eksternal (Vector DB, Search Engine, SQL DB) | Memori Internal Parametrik (Bobot/Weights Model) |
| **Kemutakhiran Data (*Freshness*)** | Real-time / Instant (Tinggal update data di Vector DB) | Statis (Harus retrain / fine-tune ulang saat data berubah) |
| **Pengurangan Halusinasi** | Sangat Tinggi (Model dipaksa menjawab berdasarkan konteks) | Sedang - Rendah (Model masih dapat mengalami halusinasi) |
| **Transparansi & Sitasi** | Tinggi (Dapat menyertakan sumber dokumen & nomor halaman) | Buruk (Model merespons dari memori tersembunyi/implisit) |
| **Fokus Utama** | Menambah **Pengetahuan Fakta / Konteks Spesifik** | Mengubah **Gaya, Format, Nada, atau Tugas Khusus** |
| **Biaya Komputasi & Waktu** | Murah & Cepat (Indexing dokumen dalam hitungan detik) | Mahal & Membutuhkan GPU High-End (Waktu jam - hari) |

---

## 🧠 Kapan Menggunakan RAG vs Fine-Tuning?

```text
               PERTANYAAN KUNCI ARSITEKTUR:
┌─────────────────────────────────────────────────────────────┐
│ Apakah Anda perlu menambahkan data fakta baru/privat?       │
└──────────────────────────────┬──────────────────────────────┘
                               │
               ┌───────────────┴───────────────┐
               ▼                               ▼
            [ YA ]                           [ TIDAK ]
               │                               │
 ┌─────────────┴─────────────┐   ┌─────────────┴─────────────┐
 │ Apakah datanya sering     │   │ Apakah Anda perlu         │
 │ berubah / butuh sitasi?   │   │ mengubah gaya/format/tugas│
 └─────────────┬─────────────┘   │ khusus (misal: JSON mode)?│
               │                 └─────────────┬─────────────┘
        ┌──────┴──────┐                         │
        ▼             ▼                  ┌──────┴──────┐
     [ YA ]        [ TIDAK ]             ▼             ▼
        │             │               [ YA ]        [ TIDAK ]
        ▼             ▼                  ▼             ▼
    ★ RAG ★    ★ Hybrid RAG ★   ★ Fine-Tuning ★  ★ Prompt Eng ★
```

---

## 🤝 Pendekatan Hibrida: RAG + Fine-Tuning
Untuk kasus penggunaan tingkat lanjut, keduanya dapat digabungkan:
1. **Fine-Tuning** digunakan untuk mengajari model memahami format khusus, jargon domain medis/hukum, atau mengeluarkan output JSON yang ketat.
2. **RAG** digunakan untuk menyuplai fakta-fakta spesifik dokumen terbaru saat *runtime*.
