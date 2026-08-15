# 02. Advanced Reasoning Prompting Techniques

## Overview
Dokumen ini mengupas 6 teknik penalaran lanjut (*advanced reasoning*) pada roadmap.sh yang terbukti secara akademis mampu meningkatkan skor akurasi LLM dari 30% hingga di atas 90% pada masalah logika, matematika, dan pemrograman.

---

## 1. Chain of Thought (CoT) Prompting
Teknik mendorong LLM untuk menguraikan tahapan berpikir (*intermediate reasoning steps*) sebelum menghasilkan jawaban akhir.
- **Zero-Shot CoT**: Cukup tambahkan frasa ajaib `"Mari kita berpikir langkah demi langkah (Let's think step by step)"` di akhir prompt.
- **Few-Shot CoT**: Berikan contoh problem lengkap dengan alur penalaran langkah-demi-langkahnya.

---

## 2. Tree of Thoughts (ToT) Prompting
Pengembangan dari CoT di mana LLM mengeksplorasi beberapa cabang pemikiran (*multiple reasoning branches*) secara bersamaan dalam bentuk struktur pohon (tree graph).
- **Proses**:
  1. **Thought Generation**: Menghasilkan 3 alternatif solusi awal.
  2. **State Evaluation**: Mengevaluasi peluang keberhasilan setiap cabang (skor 1-10).
  3. **Search Algorithm**: Menggunakan Breadth-First Search (BFS) atau Depth-First Search (DFS) untuk memilih cabang terbaik dan melanjutkan eksplorasi hingga menemukan jawaban optimal.

---

## 3. Self-Consistency Prompting
Teknik melakukan sampling beberapa jalur CoT (*sampling multiple reasoning paths*) dengan Temperature $> 0$, lalu mengambil jawaban yang paling dominan melalui suara terbanyak (*majority voting*).

---

## 4. ReAct Prompting (Reasoning + Acting)
Teknik yang memadukan penalaran spasial (*Reasoning*) dan eksekusi tindakan (*Acting*) secara iteratif dengan alat eksternal (*Tools/APIs*).
- **Pola Iteratif ReAct**:
  - `Thought`: Analisis apa yang perlu dilakukan.
  - `Action`: Eksekusi tool (misal: `Search[Cuaca Jakarta]`).
  - `Observation`: Baca hasil dari tool.
  - `Thought` -> `Action` -> `Observation` -> `Final Answer`.

---

## 5. Step-Back Prompting
Teknik meminta LLM untuk "mundur satu langkah" dan mengajukan pertanyaan umum/abstrak mengenai prinsip dasar hukum fisika/matematika/bisnis dari masalah tersebut sebelum menjawab pertanyaan detail.

---

## 6. Prompt Tuning (Soft Prompting)
Berbeda dengan *Hard Prompting* (menulis kata-kata manusia), **Prompt Tuning** adalah teknik pemodelan di mana vektor embening virtual (*continuous prompt vectors*) dilatih menggunakan gradient descent bersamaan dengan pelapisan masukan LLM tanpa mengubah bobot utama model.
