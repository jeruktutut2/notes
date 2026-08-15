# 03. Human Evals & Annotation Workflows

Meskipun evaluasi otomatis dan LLM-as-a-Judge berkembang pesat, **Human Evals** tetap menjadi *Gold Standard* (Standar Acuan Utama) dalam AI Engineering untuk memverifikasi kebenaran dan keselarasan (*alignment*) dengan kebutuhan manusia.

---

## 📌 Komponen Utama Human Evals

### 1. Human-in-the-Loop (HITL) & Feedback Collection
- **Binary Pass/Fail**: Penilaian cepat apakah respons aman/sesuai (1) atau cacat/salah (0).
- **Skala Likert (1-5)**: Penilaian berjenjang (1: Sangat Buruk, 3: Cukup, 5: Sangat Baik) untuk dimensi kualitas seperti *Helpfulness*, *Harmlessness*, *Clarity*.
- **Fine-Grained Text Highlighting**: Manusia menandai bagian teks yang mengalami halusinasi, bias, atau kesalahan tata bahasa.

### 2. Inter-Annotator Agreement (IAA)
Ketika beberapa manusia menilai dataset yang sama, penting untuk mengukur seberapa setuju mereka satu sama lain untuk memastikan kualitas data annotator.

- **Cohen's Kappa ($\kappa$)**: Mengukur kesepakatan antara **2 annotator** dengan mengoreksi faktor kebetulan (*chance agreement*).
  $$\kappa = \frac{P_o - P_e}{1 - P_e}$$
  - $\kappa > 0.8$: Kesepakatan sangat tinggi (*Almost Perfect*).
  - $\kappa < 0.4$: Kesepakatan rendah (Petunjuk annotator perlu diperbaiki).

- **Fleiss' Kappa ($\kappa$)**: Ekstensi dari Cohen's Kappa untuk **>2 annotator** pada variabel kategorikal.

### 3. Chatbot Arena & Elo Rating System
Diinspirasi oleh catur, Chatbot Arena (seperti LMSYS) menyajikan pertandingan *Blind Pairwise Evaluation* di mana pengguna nyata memilih jawaban LLM yang lebih baik.

- **Rumus Pembaruan Rating Elo**:
  $$E_A = \frac{1}{1 + 10^{(R_B - R_A)/400}}$$
  $$R_A' = R_A + K \times (S_A - E_A)$$
  Di mana $S_A$ adalah skor pertandingan (1 jika menang, 0.5 jika seri, 0 jika kalah).
