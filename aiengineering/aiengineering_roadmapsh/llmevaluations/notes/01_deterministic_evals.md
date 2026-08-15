# 01. Deterministic Evals

**Deterministic Evals** adalah teknik evaluasi luaran LLM menggunakan aturan matematis, komparasi string, pemindaian pola (regex), skema data tertutup, atau metrik n-gram statistik tanpa melibatkan panggilan ke LLM lain.

---

## 💡 Mengapa Menggunakan Deterministic Evals?

1. **Kecepatan Tinggi (Sub-millisecond)**: Berjalan secara lokal di CPU tanpa *network latency*.
2. **Biaya $0**: Tidak memerlukan token API.
3. **100% Reprodusibilitas**: Input yang sama akan selalu menghasilkan skor yang persis sama.
4. **Ideal untuk CI/CD Gate**: Sangat cocok dijadikan regresi awal sebelum evaluasi berat berbasis LLM.

---

## 📐 Komponen Utamanya

### 1. String Match & Exact Comparison
- **Exact Match (EM)**: Memeriksa apakah output persis sama dengan jawaban target (`output.strip() == target.strip()`).
- **Levenshtein Distance**: Menghitung jumlah minimum penyuntingan (insert, delete, substitute) untuk mengubah satu string menjadi string lain.
- **Substring / Contains Check**: Memastikan keyword penting muncul dalam luaran.

### 2. Regex Pattern Matching & Extraction
- Memastikan luaran memenuhi format spesifik (misalnya format Email, UUID, ISO Date, atau URL).
- Mengekstrak blok data XML/Markdown tag (`<think>...</think>`, ````json...````).

### 3. Schema & Structural Validation (Pydantic / JSON Schema)
- Menguji apakah LLM mampu mematuhi aturan JSON terstruktur (*Structured Output*).
- Menvalidasi tipe data (*integer*, *boolean*, *nested objects*), field wajib, dan batasan rentang (*range constraints*).

### 4. Code AST & Execution Asserts
- **AST Parsing**: Memeriksa apakah kode Python yang dihasilkan oleh LLM bebas dari *syntax error* tanpa mengeksekusinya.
- **Sandboxed Execution**: Menjalankan fungsi kode dalam lingkungan terbatas dan menguji dengan *unit test assertions*.

### 5. N-Gram & Statistical Metrics (BLEU, ROUGE, METEOR)
- **BLEU (Bilingual Evaluation Understudy)**: Mengukur presisi n-gram dari output terhadap teks referensi (umum untuk translate & summarization).
- **ROUGE (Recall-Oriented Understudy for Gisting Evaluation)**:
  - `ROUGE-1`: Precision, Recall, F1 untuk unigram.
  - `ROUGE-2`: Precision, Recall, F1 untuk bigram.
  - `ROUGE-L`: Based on Longest Common Subsequence (LCS).
- **METEOR**: Memperhitungkan *stemming* dan sinonim kata (WordNet) selain n-gram match.
