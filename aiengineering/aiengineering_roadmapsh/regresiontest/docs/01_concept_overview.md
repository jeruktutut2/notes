# 01. Concept Overview: AI Engineering Regression Testing 🧠🧪

## Apa itu Regression Testing pada AI Engineering?

**Regression Testing** (Pengujian Regresi) dalam rekayasa kecerdasan buatan (*AI Engineering*) adalah proses sistematis untuk memastikan bahwa pembaruan pada aplikasi AI—seperti penyuntingan *system prompt*, pembaruan versi model LLM, penyesuaian parameter RAG, atau modifikasi arsitektur agent—**tidak merusak kualitas, keamanan, format, atau performa** pada fungsionalitas yang sebelumnya sudah berjalan dengan baik.

---

## Traditional Software Testing vs AI Regression Testing

Perbandingan mendasar antara pengujian lunak tradisional dengan pengujian aplikasi LLM/AI:

| Dimensi | Software Testing Tradisional | AI Engineering Regression Testing |
| :--- | :--- | :--- |
| **Sifat Output** | Deterministik (`f(2, 3) = 5`) | Probabilistik / Non-deterministik (`f("Jelaskan 2+3") = "5" / "Hasilnya lima"`) |
| **Kriteria Lolos** | Exact Match (`assert result == expected`) | Threshold Similarity, LLM-as-a-Judge, Regex, Metric Bounds |
| **Penyebab Regresi** | Bug pada logika kode, breaking API change | Prompt drift, model update, context truncation, fine-tuning shift |
| **Alat Utama** | JUnit, Pytest, Jest | DeepEval, Promptfoo, Ragas, Pytest + Custom Evaluators |
| **Skala Uji** | Ribuan unit test cepat | Golden datasets (100–1000 sampel acuan ber-label) |

---

## Tantangan Utama Regresi pada LLM

1. **Non-Determinism**: Bahkan pada `temperature=0`, pembaruan infra internal penyedia LLM (seperti OpenAI atau Google Cloud) dapat menyebabkan variasi kecil pada pilihan token.
2. **The "Fix-One-Break-Ten" Dilemma**: Saat developer memperbaiki prompt agar LLM bisa menjawab pertanyaan Edge Case A, perbaikan tersebut sering memicu regresi pada Case B dan Case C yang sebelumnya berhasil.
3. **Model Version Deprecation & Upgrades**: Ketika penyedia beralih dari model versi `v1` ke `v2`, model baru mungkin lebih patuh pada instruksi tertentu namun kehilangan gaya penulisan atau kedalaman sintaksis tertentu.
4. **Latency & Cost Inflation**: Prompt yang makin panjang untuk memperbaiki edge cases dapat menaikkan token cost hingga 3x lipat dan membuat response time (TTFT) menjadi sangat lambat.

---

## Metrik Kunci Pengujian Regresi AI

1. **Pass Rate (%)**: Persentase test case yang memenuhi kriteria ambang batas (*threshold*).
2. **Semantic Similarity Score (0.0 - 1.0)**: Tingkat kemiripan makna antara jawaban кандидат (*Candidate*) dengan jawaban acuan (*Golden Reference*).
3. **JSON Schema Compliance Rate (%)**: Persentase jawaban yang berhasil di-parse sesuai struktur schema JSON target.
4. **Win / Tie / Loss Rate (%)**: Skor perbandingan head-to-head antara Prompt Baru (Candidate) vs Prompt Lama (Baseline) yang dinilai oleh LLM Evaluator (LLM-as-a-Judge).
5. **Cost & Latency Delta**: Selisih konsumsi token dan waktu respon (ms) antar versi.
