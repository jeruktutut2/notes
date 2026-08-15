# 02. Types of AI Regression 📊🚨

Dalam AI Engineering, regresi dapat terjadi dalam berbagai dimensi. Memahami kategori regresi membantu engineer mengisolasi akar masalah dan menentukan metode evaluasi yang tepat.

---

## 1. Quality & Correctness Regression (Regresi Kualitas & Keakuratan)
Terjadi ketika akurasi, kedalaman, atau kebenaran faktual dari jawaban model menurun setelah ada perubahan prompt atau versi model.
- **Contoh**: Prompt v1 menjawab ringkasan medis dengan akurat. Prompt v2 melupakan rincian dosis obat krusial.
- **Deteksi**: Semantic Cosine Similarity, Factuality Evaluator, Exact/Fuzzy Matching pada kata kunci penting.

---

## 2. Format & Schema Regression (Regresi Format Data)
Terjadi ketika LLM gagal mematuhi format output terstruktur seperti JSON, XML, atau Markdown yang dibutuhkan oleh backend/sistem downstream.
- **Contoh**: Prompt v1 mengembalikan `{"status": "success", "code": 200}`. Prompt v2 tiba-tiba menambahkan teks pembuka: *"Tentu, ini JSON Anda: ```json {"status": "success"}```"*, yang merusak parser JSON backend.
- **Deteksi**: Automated Pydantic / JSON Schema Validation assertions.

---

## 3. Safety & Guardrail Regression (Regresi Keamanan)
Terjadi ketika perubahan prompt atau model membuat sistem kembali rentan terhadap *Prompt Injection*, *Jailbreaking*, pembocoran data pribadi (PII), atau pencetakan konten beracun/harmful.
- **Contoh**: System prompt disingkat agar hemat token, namun menyebabkannya tidak lagi memblokir permintaan pengubah kata sandi pengguna lain.
- **Deteksi**: Adversarial test suite, Jailbreak Prompt Regression Datasets, Moderation API checks.

---

## 4. RAG Retrieval & Faithfulness Regression (Regresi RAG)
Pada arsitektur Retrieval-Augmented Generation (RAG), regresi dapat terjadi pada dua tahap:
- **Retrieval Regression**: Perubahan chunking (dari 500 token ke 200 token) membuat chunk acuan terpotong sehingga document rank turun di luar Top-K.
- **Generation Faithfulness Regression**: Model mulai memuat *hallucination* (informasi yang tidak bersumber dari konteks dokumen yang di-retrieve).
- **Deteksi**: Ragas Metrics (Faithfulness, Answer Relevance, Context Recall).

---

## 5. Latency, Throughput & Cost Regression (Regresi Performa & Biaya)
Terjadi ketika perubahan prompt (misalnya menambahkan few-shot examples yang panjang) atau pergantian model (misalnya dari Haiku ke Sonnet) meningkatkan biaya operasional dan latency di luar batas SLA.
- **Contoh**: Average latency naik dari 800ms menjadi 3500ms, atau biaya per 1,000 request melonjak dari $0.10 ke $1.50.
- **Deteksi**: Latency & Token Budget assertions pada pipeline CI/CD.
