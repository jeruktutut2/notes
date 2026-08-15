# 01. Techniques for Improving LLM Reliability

## Overview
Dokumen ini mengulas 4 metode utama untuk meningkatkan keandalan (*reliability*), akurasi, dan netralitas LLM sesuai dengan kotak **"Improving Reliability"** pada roadmap.sh/prompt-engineering.

---

## 1. Prompt Debiasing
LLM berisiko mewarisi bias gender, budaya, ras, atau bias geografis yang ada dalam data pre-training.
- **Teknik Counterfactual Prompting**: Menyajikan konteks yang secara eksplisit menetralisir asumsi implisit model.
- **Explicit Invariant Instruction**: `"Analisis profil kandidat berikut berdasarkan kualifikasi teknis SAJA. Abaikan nama, gender, usia, dan lokasi."`

---

## 2. Prompt Ensembling
Teknik menggabungkan output dari beberapa variasi prompt yang berbeda (atau beberapa model LLM berbeda) untuk menghasilkan keputusan akhir yang jauh lebih stabil dan akurat.
- **Majority Voting**: Mengambil jawaban yang paling sering dihasilkan oleh beberapa prompt.
- **Weighted Averaging**: Memberi bobot lebih tinggi pada respons dari model/prompt yang memiliki skor historis lebih baik.

---

## 3. LLM Self Evaluation (LLM-as-a-Judge)
Menggunakan LLM sebagai "Hakim" untuk mengevaluasi, mengkritik, dan memeriksa kebenaran hasil enerasi model itu sendiri sebelum disajikan ke pengguna.
- **Workflow Critique-and-Refine**:
  1. `Generator Prompt` menghasilkan draft jawaban.
  2. `Evaluator Prompt` memeriksa apakah ada kesalahan faktual atau pelanggaran format.
  3. Jika ada kesalahan, `Evaluator` mengembalikan kritik untuk diperbaiki oleh `Generator`.

---

## 4. Calibrating LLMs (Kalibrasi Keyakinan)
Model yang terkalibrasi dengan baik memiliki tingkat keyakinan (*confidence score*) yang selaras dengan akurasi sebenarnya (jika model 90% yakin, akurasi faktualnya memang 90%).
- **Verbalized Confidence**: Meminta model memberikan skor keyakinan $0-100\%$ beserta alasan rasionalnya.
