# 03. Context Compaction

Modul ini mempelajari teknik *Context Compaction* (Kompresi Konteks) untuk memadat informasi dokumen/riwayat percakapan panjang tanpa kehilangan makna esensial.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Mengapa Context Compaction Dibutuhkan?
- **Context Overflow Avoidance**: Mencegah kegagalan aplikasi saat data riwayat / RAG melebihi batas *Context Window* LLM (misal: 128K tokens).
- **Latency & Cost Reduction**: Menghapus token yang redundan/tidak berinformasi menekan biaya input API dan mempercepat waktu inferensi.

### 2. Metode Context Compaction
1. **Selective Token Pruning (LLMLingua)**: Menggunakan model bahasa kecil (Small Language Model seperti GPT-2/Llama-3B) untuk mengukur *surprisal score* tiap kata, lalu menghapus kata-kata berinformasi rendah (misal: stop-words, klausa berulang).
2. **Summarization Buffer (Hierarchical Summarization)**: Merangkum $N$ turn percakapan terakhir menjadi kalimat ringkas, mempertahankan entitas penting saja.
3. **Semantic Truncation & Recency Decay**: Membuang dokumen/pesan paling tua yang kemiripan semantiknya paling rendah dengan kueri pengguna terkini.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi LLMLingua-style Token Compaction dan Summarization Buffer.
