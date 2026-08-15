# 02. Common Terminology in AI & Prompt Engineering

## Overview
Dokumen ini menjelaskan **10 Istilah Utama (Common Terminology)** yang terdapat pada diagram roadmap.sh/prompt-engineering. Memahami istilah-istilah ini sangat penting untuk berkomunikasi dan membangun aplikasi AI modern.

---

## 1. LLM (Large Language Model)
Model kecerdasan buatan berbasis jaringan saraf tiruan (neural network) dengan miliaran hingga triliunan parameter yang dilatih pada corpus teks skala masif untuk memahami, menghasilkan, dan merangkum bahasa alami.

---

## 2. Tokens (Tokenisasi)
Unit terkecil dari teks yang diproses oleh LLM. Token bisa berupa kata utuh, sub-kata (subword), karakter, atau bagian dari kode.
- **Aturan umum**: 1 token $\approx$ 4 karakter teks bahasa Inggris, atau $\approx 0.75$ kata. Dalam Bahasa Indonesia, 1 kata sering kali dipecah menjadi 2-3 token.
- Contoh: Kata `"Prompting"` dipecah oleh Byte-Pair Encoding (BPE) menjadi token `["Prompt", "ing"]`.

---

## 3. Context Window (Jendela Konteks)
Batas maksimum jumlah total token (input prompt + output generation) yang dapat diproses oleh LLM dalam satu kali panggilan (request).
- **GPT-4o**: 128k token.
- **Claude 3.5 Sonnet**: 200k token.
- **Gemini 1.5 Pro**: 2.000.000 (2M) token.
*Catatan*: Meskipun context window besar, terjadi fenomena **"Lost in the Middle"** di mana LLM cenderung lupa informasi yang diletakkan di tengah-tengah context window yang sangat panjang.

---

## 4. Hallucination (Halusinasi AI)
Kondisi di mana LLM menghasilkan informasi yang terdengar sangat meyakinkan, runtut, dan tata bahasanya benar, namun secara faktual salah, tidak ada, atau bertentangan dengan kenyataan.
- **Penyebab**: LLM memprediksi token berdasarkan pola probabilitas statistik, bukan berdasarkan tabel fakta database mutlak.
- **Mitigasi**: Menggunakan RAG (Retrieval-Augmented Generation), grounded prompting, dan temperature rendah ($0.0$).

---

## 5. Agents (AI Agents)
Sistem kecerdasan buatan yang memadukan LLM dengan kemampuan:
1. **Planning** (Perencanaan & Pembagian tugas / CoT / ToT).
2. **Memory** (Ingatan jangka pendek & panjang).
3. **Tool Use / Function Calling** (Kemampuan mengeksekusi fungsi Python, pencarian web, kalkulator, kueri database SQL).

---

## 6. Prompt Injection
Vulnerabilitas keamanan pada LLM di mana input yang tidak terpercaya (user input atau untrusted data) berhasil "mengambil alih" instruksi sistem (*system prompt*) dan memaksa LLM melakukan tindakan yang melanggar aturan keamanan (misal: membocorkan API key, menjalankan script jahat).
- **Direct Injection**: User langsung menulis instruksi jahat di kolom input.
- **Indirect Injection**: Teks jahat disisipkan di dalam dokumen web/PDF yang dibaca oleh RAG.

---

## 7. Model Weights / Parameters (Parameter Model)
Nilai-nilai numerik (bobot dan bias) dalam neural network yang dipelajari selama proses training. Parameter inilah yang menyimpan pengetahuan dan kemampuan penalaran model.
- Contoh: Llama-3-8B memiliki 8 Miliar parameter; GPT-4 diperkirakan memiliki $\sim 1.8$ Triliun parameter (MoE - Mixture of Experts).

---

## 8. Fine-Tuning vs Prompt Engineering

| Kriteria | Prompt Engineering | Fine-Tuning |
| :--- | :--- | :--- |
| **Definisi** | Mengatur input teks tanpa mengubah bobot model | Mengupdate bobot (weights) model pada dataset spesifik |
| **Waktu & Biaya** | Instan (hitungan detik), biaya modal $0 | Membutuhkan GPU/TPU & dataset berlabel (biaya tinggi) |
| **Keahlian** | Kemampuan merancang instruksi & konteks | Machine Learning & Data Engineering |
| **Pengetahuan Baru** | Menginput informasi via Context / RAG | Menginternalisasi gaya/format permanen ke dalam model |

---

## 9. AI vs AGI

- **AI (Artificial Intelligence / Narrow AI)**: Sistem AI khusus yang sangat cerdas pada tugas spesifik (contoh: pemrosesan bahasa, pengenalan gambar, catur). Seluruh LLM saat ini adalah Narrow AI.
- **AGI (Artificial General Intelligence)**: AI hipotetis yang memiliki kemampuan intelektual setara atau melebihi manusia dalam hampir semua tugas ekonomi dan kognitif secara mandiri.

---

## 10. RAG (Retrieval-Augmented Generation)
Arsitektur yang menggabungkan sistem pencarian dokumen (*Information Retrieval* / Vector Database) dengan LLM. 
1. Pertanyaan user diubah menjadi embedding vector.
2. Database mencari dokumen relevan.
3. Dokumen relevan disisipkan ke dalam prompt sebagai konteks nyata.
4. LLM menjawab berdasarkan konteks dokumen tersebut, sehingga menghilangkan halusinasi dan memberikan pengetahuan up-to-date.
