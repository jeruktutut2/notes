# 01. Sampling Parameters (Temperature, Top-P, Top-K)

## Overview
Ketika LLM memprediksi token berikutnya, model menghitung distribusi probabilitas logit untuk seluruh kosakata (*vocabulary*). **Sampling Parameters** mengontrol bagaimana model memilih token berdasarkan distribusi tersebut.

---

## 1. Temperature ($T$)

Temperature mengontrol tingkat acak (*randomness*) dan kreativitas respons LLM dengan menskalakan logits sebelum fungsi Softmax diterapkan.

Formula penyesuaian logit $z_i$:

$$P(t_i) = \frac{\exp(z_i / T)}{\sum_j \exp(z_j / T)}$$

### Dampak Nilai Temperature:
- **$T = 0.0$ (Greedy Decoding / Deterministic)**:
  - Model selalu memilih token dengan probabilitas tertinggi ($P_{\max}$).
  - Hasil respons selalu identik jika dikirim berulang kali.
  - **Use Case**: Factual QA, Coding, Ekstraksi Data JSON, Kueri SQL, Matematika.
- **$T = 0.2 - 0.5$ (Focused & Creative Balance)**:
  - Cocok untuk penulisan teknis, dokumentasi, dan ringkasan teks.
- **$T = 0.7 - 1.0$ (High Creativity)**:
  - Distribusi probabilitas menjadi lebih merata (*flattened*). Model berani memilih kata-kata alternatif yang kurang umum.
  - **Use Case**: Brainstorming ide, penulisan cerita fiksi, copywriting pemasaran.
- **$T > 1.2$ (Unstable / Nonsensical)**:
  - Distribusi probabilitas terlalu mendekati seragam. Model menghasilkan teks acak, tidak koheren, dan penuh kata-kata aneh.

---

## 2. Top-P (Nucleus Sampling)

Top-P (*Nucleus Sampling*) membatasi ruang pemilihan token hanya pada kumpulan token teratas yang **jumlah kumulatif probabilitasnya mencapai $P$**.

### Mekanisme Kerja:
1. Urutkan semua token dari probabilitas tertinggi ke terendah.
2. Tambahkan token satu per satu hingga total probabilitas $\sum P(t_i) \ge P$.
3. Potong (*cut-off*) seluruh token sisanya.
4. Lakukan sampling secara acak dari himpunan token yang tersisa.

### Contoh Kasus ($P = 0.90$):
Jika token "kucing" (0.50), "anjing" (0.25), "burung" (0.16) totalnya $= 0.91$, maka hanya 3 token ini yang dipertimbangkan. Token "ikan" (0.04) dan lainnya dibuang.

- **`Top-P = 0.1`**: Sangat konservatif (hanya mempertimbangkan top 10% probabilitas kumulatif).
- **`Top-P = 0.9`**: Sangat fleksibel (mempertimbangkan 90% distribusi).

---

## 3. Top-K Sampling

Top-K membatasi pemilihan token hanya pada **$K$ token teratas** dengan probabilitas tertinggi, tanpa memedulikan probabilitas kumulatifnya.

- **`Top-K = 1`**: Identik dengan Temperature $0.0$ (Greedy Search).
- **`Top-K = 40`**: Model hanya akan memilih dari 40 kata paling mungkin.

---

## Best Practice Kombinasi Parameter
> [!IMPORTANT]
> **Rekomendasi dari OpenAI & Anthropic**: Ubah salah satu antara `Temperature` **ATAU** `Top-P`, namun **JANGAN menaikkan/menurunkan keduanya sekaligus**, untuk menghindari perilaku model yang tak terprediksi.

| Goal / Task | Temperature | Top-P | Top-K |
| :--- | :--- | :--- | :--- |
| **Strict JSON / Code Extraction** | `0.0` | `1.0` | `1` |
| **Data Analysis & RAG Chatbot** | `0.2` | `0.9` | `20` |
| **Creative Writing & Marketing** | `0.8` | `0.95` | `50` |
