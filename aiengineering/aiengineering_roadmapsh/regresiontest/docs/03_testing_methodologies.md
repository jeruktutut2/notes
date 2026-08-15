# 03. Testing Methodologies in AI Engineering 🛠️🔬

Untuk membangun saluran regresi (*regression pipeline*) yang andal, AI Engineer memadukan beberapa metodologi pengujian dari yang bersifat deterministik hingga evaluasi berbasis kecerdasan buatan (*model-based evals*).

---

## 1. Golden Datasets (Test Suites Acuan)
Dataset Emas (*Golden Dataset*) adalah koleksi pasangan input, acuan jawaban ideal (*Ground Truth*), dan aturan pengujian (*Assertions*) yang mewakili berbagai skenario nyata:
- **Happy Path Cases**: Kasus penggunaan umum sehari-hari.
- **Edge Cases**: Input panjang, simbol khusus, input ambigu, bahasa asing.
- **Adversarial / Safety Cases**: Percobaan jailbreak dan prompt injection.

> **Prinsip Utama**: Golden dataset harus versi-terkontrol (*version-controlled*) di repository (misalnya `golden_dataset_v1.json`).

---

## 2. Deterministic Assertions & Regex Checks
Pengujian cepat dan tanpa biaya API yang memvalidasi kondisi keras:
- **String Containment**: Memastikan kata kunci atau klausa wajib muncul/tidak muncul.
- **Regex Pattern Matching**: Memastikan format tanggal, email, kode angka terformat dengan benar.
- **JSON Schema Validation**: Memastikan struktur key-value sesuai tipe data yang diharapkan.

---

## 3. Semantic Embedding Similarity (Cosine Similarity)
Mengubah jawaban model dan jawaban acuan menjadi vektor embedding (menggunakan model embedding seperti `text-embedding-3-small` atau TF-IDF/SentenceTransformer), kemudian menghitung sudut kemiripan kosinus (*Cosine Similarity*):

$$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$

- Jika skor $> 0.85$, jawaban dianggap mempertahankan makna yang sama (Lolos Regresi).
- Jika skor $< 0.70$, jawaban dianggap telah mengalami penyimpangan makna (*Semantic Drift*).

---

## 4. Pairwise LLM-as-a-Judge (Evaluasi Head-to-Head)
Metode di mana LLM yang lebih bertenaga (seperti GPT-4o atau Gemini 1.5 Pro) menerima dua jawaban sekaligus:
- **Output A**: Dihasilkan oleh System Prompt Lama / Model Lama (Baseline)
- **Output B**: Dihasilkan oleh System Prompt Baru / Model Baru (Candidate)

Evaluator mengevaluasi kedua output berdasarkank kriteria: Akurasi, Kejujuran, Kejelasan, dan Kegunaan tanpa mengetahui mana Prompt A atau B (untuk mengeliminasi *positional bias*, posisi A/B dibalik secara bergantian).

---

## 5. Continuous Integration (CI/CD) Regression Pipelines
Mengintegrasikan regression test ke dalam workflow Git (seperti GitHub Actions):
1. Perubahan prompt diajukan via Pull Request (PR).
2. GitHub Actions menjalankan `pytest test_ai_regression.py`.
3. Jika Pass Rate $< 95\%$ atau terjadi kerentanan keamanan, PR diblokir secara otomatis dari penggabungan (*merge*) ke `main`.
