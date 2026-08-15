# 01. LLM Mechanics & Fundamentals of Prompts

## Overview
Selamat datang di modul dasar **Prompt Engineering**. Dokumen ini membahas tiga pertanyaan fundamental yang menjadi fondasi seluruh materi [roadmap.sh/prompt-engineering](https://roadmap.sh/prompt-engineering):
1. **LLMs and how they work?** (Bagaimana Large Language Model bekerja?)
2. **What is a Prompt?** (Apa itu Prompt?)
3. **What is Prompt Engineering?** (Apa itu Prompt Engineering?)

---

## 1. LLMs and How They Work? (Mekanisme Dasar LLM)

Large Language Model (LLM) seperti GPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, Llama 3, dan DeepSeek R1 adalah model kecerdasan buatan berbasis arsitektur **Transformer** (khususnya *Decoder-only* architecture).

### A. Core Operation: Next-Token Prediction
Secara fundamental, LLM **tidak "berpikir" atau "memahami" seperti manusia**. LLM adalah sebuah **mesin prediktor probabilitas token berikutnya** (*auto-regressive token predictor*).

Given a sequence of input tokens $X = (t_1, t_2, \dots, t_n)$, LLM menghitung distribusi probabilitas untuk token berikutnya $t_{n+1}$:

$$P(t_{n+1} \mid t_1, t_2, \dots, t_n) = \text{softmax}(W \cdot h_n)$$

Di mana:
- $h_n$ adalah representasi tersembunyi (hidden representation) yang dihasilkan oleh Self-Attention layers dari Transformer.
- $W$ adalah matrik bobot output (language modeling head).

### B. Tahapan Pelatihan LLM
1. **Pre-Training (Unsupervised Learning)**:
   - Model dilatih pada triliunan token teks internet.
   - Tugas utama: Menebak token berikutnya (*Causal Language Modeling*).
   - Mengahasilkan **Base Model** (contoh: Llama-3-Base). Base model belum bisa diajak berdialog secara natural; base model cenderung meneruskan pola teks (misal: diberi kalimat pertanyaan, base model bisa malah menghasilkan barisan pertanyaan lain).

2. **Post-Training / Instruction Tuning (SFT - Supervised Fine-Tuning)**:
   - Model dilatih menggunakan pasangan dataset instruksi manusia: `(Instruction, Ideal Response)`.
   - Mengubah Base Model menjadi **Instruct/Chat Model**.

3. **Aligning with Preferences (RLHF / DPO)**:
   - *Reinforcement Learning from Human Feedback* (RLHF) atau *Direct Preference Optimization* (DPO).
   - Memastikan respons aman (Safety), bermanfaat (Helpful), dan jujur (Honest/Harmless).

---

## 2. What is a Prompt? (Anatomi & Struktur Prompt)

**Prompt** adalah sekumpulan teks, instruksi, konteks, dan data masukan yang diberikan kepada LLM sebagai panduan untuk menghasilkan respons (*output generation*).

### Anatomi Lengkap Sebuah Prompt Professional
Sebuah prompt yang terstruktur secara optimal terdiri dari 5 komponen utama:

```markdown
[SYSTEM INSTRUCTION / ROLE]
Anda adalah seorang Senior Software Architect ahli Python dan Sistem Terdistribusi.

[CONTEXT / BACKGROUND]
Kami sedang membangun layanan REST API mikroservis untuk sistem pembayaran e-commerce yang menangani 10.000 transaksi per detik.

[INSTRUCTION / TASK]
Tuliskan kode fungsi Python menggunakan `asyncio` dan `httpx` untuk melakukan retry dengan exponential backoff dan jitter ketika terjadi network timeout.

[INPUT DATA / CONSTRAINTS]
- Maksimal retry: 3 kali.
- Initial delay: 100ms, Max delay: 2000ms.
- Gunakan tipe data Pydantic v2 untuk respons.

[OUTPUT INDICATOR / FORMAT]
Kembalikan jawaban HANYA berupa kode Python di dalam block markdown ```python tanpa komentar pengantar.
```

### Peran Role (Roles) dalam LLM API
Dalam API standar (OpenAI/Anthropic/Google), prompt dikategorikan ke dalam 3 role:
- **`system`**: Menentukan persona, aturan keamanan, batasan format, dan perilaku permanen model.
- **`user`**: Input langsung dari pengguna (instruksi spesifik atau data yang ingin diproses).
- **`assistant`**: Respons yang dihasilkan model (atau contoh respons dalam *few-shot prompting*).

---

## 3. What is Prompt Engineering?

**Prompt Engineering** adalah disiplin merancang, menstrukturkan, mengoptimalkan, dan menguji input (*prompts*) secara sistematis untuk mengarahkan LLM agar menghasilkan output yang akurat, konsisten, aman, dan berformat tepat **tanpa mengubah bobot (weights) internal model**.

### Mengapa Prompt Engineering Sangat Krusial?
1. **Determinisme dari Model Stokastik**: LLM pada dasarnya bersifat probabilistik. Prompt engineering mengurangi variabilitas dan ketidakpastian respons.
2. **Penghematan Biaya & Latensi**: Prompt yang efisien menghemat penggunaan token (mengurangi biaya API dan mempercepat response time).
3. **Pencegahan Hallucination & Security Vulnerability**: Menjaga model agar tidak mengarang fakta palsu atau terkena serangan *Prompt Injection*.
4. **Programmatic Interoperability**: Memastikan output LLM dapat diparse langsung oleh sistem software (format JSON, XML, Schema).

---

## Ringkasan Konsep
- **LLM**: Mesin prediktor token berbasis Transformer.
- **Prompt**: Konteks masukan + instruksi yang menentukan ruang pencarian jawaban model.
- **Prompt Engineering**: Teknik mengemudikan LLM agar hasil output relevan, aman, dan terstruktur.
