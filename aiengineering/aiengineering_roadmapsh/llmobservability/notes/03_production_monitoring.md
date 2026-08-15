# 03 - Production Monitoring & Evaluations dalam LLM Observability

## Overview
Pemantauan aplikasi LLM di lingkungan produksi (Production Monitoring) berfokus pada **Kualitas Output**, **Halusinasi**, **Pergeseran Data (Drift)**, dan **Umpan Balik Pengguna (User Feedback)**. Karena output LLM tidak memiliki assert sederhana (seperti `assert status_code == 200`), teknik pemantauan khusus seperti **LLM-as-a-Judge** dan **Metrik RAGAS** diterapkan.

---

## 1. LLM-as-a-Judge & Metrik Evaluasi Produksi

Metode evaluasi otomatis menggunakan LLM lain yang lebih kuat (misal: GPT-4o) untuk menilai kualitas respons secara kontinu:

```
[Query User] + [Context Retrieved] + [LLM Output]
                   │
                   ▼
     [LLM-as-a-Judge Evaluator]
                   │
  ┌────────────────┼────────────────┐
  ▼                ▼                ▼
Faithfulness   Answer Relevance  Context Precision
(0.0 - 1.0)      (0.0 - 1.0)       (0.0 - 1.0)
```

### Metrik-Metrik Utama:
1. **Faithfulness (Kejujuran/Kebenaran terhadap Konteks)**:
   - Mengukur apakah klaim dalam jawaban LLM didukung penuh oleh dokumen konteks yang diambil (RAG).
   - Menghindari **Halusinasi** di mana LLM mengarang fakta yang tidak ada di dokumen.
2. **Answer Relevance (Relevansi Jawaban)**:
   - Mengukur seberapa tepat jawaban terhadap pertanyaan awal user, tanpa menyimpang ke topik lain.
3. **Hallucination Score**:
   - Persentase atau skor probabilitas klaim yang berlawanan atau tidak ada dalam grounding data.
4. **Toxicity & Policy Safety Score**:
   - Menilai apakah output mengandung ujaran kebencian, kata-kata kasar, atau melanggar aturan keamanan.

---

## 2. Monitoring Drift (Pergeseran Embeddings & Prompt)

Sistem AI dapat mengalami penurunan performa seiring waktu karena beberapa bentuk **Drift**:

- **Embedding / Data Drift**: Pertanyaan pengguna berubah polanya (misal: muncul produk baru atau tren baru yang belum ada di Vector DB).
- **Prompt Drift**: Perubahan minor pada System Prompt atau Few-shot Examples dapat memberikan dampak tak terduga pada distribusi jawaban.
- **Model Version Drift**: Provider (seperti OpenAI) memperbarui model di belakang layar yang dapat mengubah karakteristik output.

### Cara Mendeteksi Drift:
1. Menghitung rata-rata Cosine Similarity antar embedding query pengguna dari waktu ke waktu.
2. Melacak penurunan rata-rata skor evaluasi harian.

---

## 3. User Feedback & Telemetri Interaksi

Umpan balik langsung dari user merupakan sinyal kualitas berharga di produksi:

- **Explicit Feedback**: Thumbs up (+1) / Thumbs down (-1), rating bintang, atau laporan teks kesalahan.
- **Implicit Feedback**: User melakukan copy-to-clipboard, user meminta regenerate jawaban, atau user langsung menutup percakapan (churn).

### Menghubungkan Feedback ke Trace:
Setiap kali pengguna memberikan feedback, skor tersebut harus ditautkan kembali ke `trace_id` yang bersangkutan dalam platform observability:

```python
# Tautkan feedback thumbs down ke trace spesifik
log_feedback(
    trace_id="tr-9842a",
    score=-1.0,
    comment="Jawaban salah, informasi tidak sesuai manual produk."
)
```
