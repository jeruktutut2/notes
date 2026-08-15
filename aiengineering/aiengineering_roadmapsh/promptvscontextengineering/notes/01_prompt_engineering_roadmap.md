# DOCUMENTATION: PROMPT ENGINEERING (ROADMAP.SH AI ENGINEER)

Dokumen ini mendokumentasikan seluruh **13 Elemen Kunci Prompt Engineering** dari kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 📑 Daftar 13 Topik Utama Prompt Engineering

```
┌──────────────────────────────────────────────────────────────────────────┐
│                         PROMPT ENGINEERING ROADMAP                       │
├───────────────────────┬────────────────────────┬─────────────────────────┤
│ 1. Zero-Shot          │ 2. Few-Shot            │ 3. ReAct Framework      │
│ 4. Chain-of-Thought   │ 5. Input Format        │ 6. Function Calling     │
│ 7. Prompt Caching     │ 8. Streaming Responses │ 9. System Prompting     │
│ 10. Role & Behavior   │ 11. Context            │ 12. Constraints         │
│ 13. Structured Output │                        │                         │
└───────────────────────┴────────────────────────┴─────────────────────────┘
```

---

## 1. Zero-Shot Prompting
- **Penjelasan**: Mengeksekusi instruksi langsung tanpa memberikan contoh keluaran sebelumnya.
- **Kapan Digunakan**: Tugas-tugas standar di mana LLM memiliki pemahaman mendalam bawaan.
- **Formulasi Terbaik**: Gunakan kata kerja aksi yang jelas (`Analisis`, `Ekstrak`, `Klasifikasikan`).

## 2. Few-Shot Prompting (In-Context Examples)
- **Penjelasan**: Menyediakan contoh pasangan input-output di dalam prompt untuk mengarahkan format dan pola berpikir.
- **Praktik Terbaik**: Gunakan 2–5 contoh yang variatif dan representatif. Pastikan pembatas contoh menggunakan XML Tags atau Markdown yang konsisten.

## 3. ReAct (Reasoning + Acting)
- **Penjelasan**: Siklus interaktif LLM: `Thought` (Penalaran) -> `Action` (Eksekusi Alat Eksternal) -> `Observation` (Hasil Alat) -> `Repeat` -> `Final Answer`.
- **Integrasi**: Fondasi utama pembangunan AI Agents yang mandiri.

## 4. Chain-of-Thought (CoT)
- **Penjelasan**: Meminta LLM menghasilkan langkah-langkah penalaran sekuensial sebelum mencetak hasil akhir.
- **Manfaat**: Meningkatkan akurasi matematika, pemrograman, dan logika deduktif hingga 40%+.

## 5. Input Format
- **Penjelasan**: Struktur tata letak teks masukan menggunakan Delimiter (XML `<context>`, Markdown `#`, CSV, atau JSON).
- **Fungsi**: Mengisolasi instruksi utama dari data masukan pengguna agar tidak terjadi kebocoran perbatasan (*boundary drift*).

## 6. Function Calling (Tools API)
- **Penjelasan**: Kemampuan LLM mengembalikan objek JSON berisi `tool_name` dan `arguments` terstruktur untuk dipanggil oleh backend aplikasi.
- **Standard Protocol**: Mengikuti skema JSON OpenAPI / JSON Schema.

## 7. Prompt Caching
- **Penjelasan**: Menyimpan *KV Attention Tensor* dari prefix prompt statis di memori GPU penyedia LLM.
- **Efisiensi**: Menghemat biaya API hingga 80% dan memotong latensi Time-To-First-Token (TTFT).

## 8. Streaming Responses
- **Penjelasan**: Mengirimkan token luaran secara real-time via Server-Sent Events (SSE) begitu token selesai digenerasi.
- **UX Impact**: Menurunkan *perceived latency* dari hitungan detik menjadi milidetik.

## 9. System Prompting
- **Penjelasan**: Instruksi tingkat teratas yang mendefinisikan batas aturan, identitas, dan peran dasar model.
- **Sifat**: Bersifat konstan selama seluruh sesi percakapan berlangsung.

## 10. Role & Behavior Alignment
- **Penjelasan**: Mengatur nada suara, persona kepakaran (misal: *Financial Advisor*), dan aturan kepatuhan perilaku (*behavioral safety*).

## 11. Context Injection (In-Prompt)
- **Penjelasan**: Menyertakan dokumen latar belakang atau data referensi di dalam prompt untuk membatasi jawaban pada fakta yang tersedia (Closed-Domain Q&A).

## 12. Hard & Soft Constraints
- **Hard Constraints**: Batasan mutlak yang dilarang dilanggar (misal: *"Dilarang menyebutkan nama kompetitor"*, *"Jawab maksimal 20 kata"*).
- **Soft Constraints**: Panduan rekomendasi nada atau prioritas gaya penulisan.

## 13. Structured Output (JSON Mode & Grammars)
- **Penjelasan**: Penegakan luaran dalam format terstruktur (JSON / XML) menggunakan *Constrained Decoding* atau *Self-Repair Loop*.
