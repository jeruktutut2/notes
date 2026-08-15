# PROMPT ENGINEERING AI ENGINEERING - ROADMAP NOTES

Dokumen ini berisi rangkuman teori komprehensif, formula matematika, arsitektur sistem, dan panduan keamanan **Prompt Engineering** berdasarkan kurikulum **AI Engineer roadmap.sh**.

---

## DAFTAR ISI
1. [Anatomi & Komponen Utama Prompt](#1-anatomi--komponen-utama-prompt)
2. [Teknik Prompting Dasar (Zero-Shot, Few-Shot, CoT, Self-Consistency, ToT)](#2-teknik-prompting-dasar)
3. [Teknik Prompting Lanjutan (ReAct, Directional Stimulus, Least-to-Most, Chaining)](#3-teknik-prompting-lanjutan)
4. [Output Structuring & Constraint Enforcement](#4-output-structuring--constraint-enforcement)
5. [Keamanan Prompt & Red Teaming (Injection, Jailbreaking, Defense)](#5-keamanan-prompt--red-teaming)
6. [Evaluasi Otomatis & Optimasi Prompt (LLM-as-a-Judge, APE, Cost & Token)](#6-evaluasi-otomatis--optimasi-prompt)

---

## 1. Anatomi & Komponen Utama Prompt

Prompt yang dirancang dengan efektif memiliki 4 elemen utama:

| Komponen | Penjelasan & Fungsi | Contoh |
|---|---|---|
| **Instruction (Instruksi)** | Tugas spesifik atau aksi yang harus dieksekusi oleh LLM. | "Ringkaslah teks ulasan berikut." |
| **Context (Konteks)** | Informasi latar belakang, peran system role, atau batasan domain. | "Anda adalah pakar analisis sentimen e-commerce." |
| **Input Data (Data Input)** | Teks, query, atau payload acuan yang perlu diolah. | "Ulasan: 'Barang cepat sampai tapi packing penyok.'" |
| **Output Indicator** | Format balasan yang diinginkan (JSON, Markdown, Bullet points). | "Kembalikan output JSON dengan key: status, sentimen." |

### Formula Kuantitas Prompt Optimal
$$\text{Prompt Quality} \propto \frac{\text{Spesifisitas Instruksi} \times \text{Kejelasan Konteks}}{\text{Ambiguitas Teks} + \text{Noise Token}}$$

---

## 2. Teknik Prompting Dasar

### A. Zero-Shot vs Few-Shot Learning
- **Zero-Shot**: Menanyakan pertanyaan atau instruksi tanpa memberikan contoh sebelumnya. Cocok untuk tugas generik yang sudah tercakup dalam *pre-training* model.
- **Few-Shot (In-Context Learning)**: Memberikan 1 sampai $N$ contoh pasangan $(x_i, y_i)$ sebelum input sebenarnya.
  - *Exemplar Selection*: Pilih contoh yang beragam (diverse) dan relevan secara semantik dengan input pengguna.

### B. Chain-of-Thought (CoT)
Mendorong LLM menghasilkan langkah-langkah penalaran (*reasoning steps*) sebelum memberikan jawaban akhir.
- **Zero-Shot CoT**: Menambahkan frasa pemicu `"Let's think step by step"` atau `"Mari kita berpikir langkah demi langkah"`.
- **Manual Few-Shot CoT**: Menuliskan contoh penalaran secara manual di dalam prompt.

### C. Self-Consistency Sampling & Tree-of-Thought (ToT)
- **Self-Consistency**: Menjalankan $N$ jalur CoT secara paralel dengan temperatur $T > 0$, lalu melakukan *majority voting*:
  $$\hat{y} = \arg\max_{v} \sum_{i=1}^{N} \mathbb{I}(y_i = v)$$
- **Tree-of-Thought (ToT)**: Menggunakan struktur pohon untuk mengeksplorasi beberapa jalur keputusan (*tree search* seperti BFS/DFS) beserta fungsi evaluasi node oleh LLM.

---

## 3. Teknik Prompting Lanjutan

### A. ReAct Framework (Reason + Act)
Menggabungkan penalaran dan eksekusi aksi (Tool Use):
1. **Thought**: "Saya perlu mencari harga tiket pesawat Jakarta-Bali."
2. **Action**: `search_flight_api(origin='CGK', dest='DPS')`
3. **Observation**: "Harga termurah Rp 850.000."
4. **Final Answer**: Mengembalikan hasil akhir ke pengguna.

### B. Least-to-Most Prompting
Memecah masalah kompleks menjadi daftar sub-pertanyaan yang lebih mudah, kemudian memproses sub-pertanyaan secara sekuensial dari yang paling sederhana hingga paling kompleks.

### C. Prompt Chaining (Pipelines)
Menghubungkan beberapa prompt secara berurutan di mana:
$$\text{Output}_k \rightarrow \text{Input}_{k+1}$$
Memungkinkan komposisi tugas besar (seperti Ekstraksi $\rightarrow$ Summarization $\rightarrow$ Translation) menjadi unit prompt modular yang stabil.

---

## 4. Output Structuring & Constraint Enforcement

### A. JSON Schema Enforcement
Memaksa LLM menghasilkan JSON valid dengan:
- Menyertakan contoh skema JSON (JSON Schema Standard).
- Menggunakan regex parser & retry-repair loop saat sintaks JSON rusak.

### B. Negative Constraints & Guardrails
- **Negative Constraints**: Instruksi negatif eksplisit seperti `"JANGAN gunakan kata X"`, `"MAKSIMAL 3 kalimat"`.
- **Algorithmic Guardrails**: Validator eksternal yang memeriksa output LLM menggunakan regex, blacklist, atau classifier sebelum dikembalikan ke client.

---

## 5. Keamanan Prompt & Red Teaming

### A. Jenis Serangan Prompt
1. **Direct Prompt Injection**: Pengguna sengaja mengetik `"Abaikan instruksi sebelumnya..."`.
2. **Indirect Prompt Injection**: Data dari luar (halaman web/PDF) mengandung instruksi tersembunyi.
3. **Jailbreaking**: Eksploitasi peran (DAN, Hypo-roleplay, Cipher Base64) untuk menembus filter etika.

### B. Arsitektur Pertahanan (Defensive Prompting)
- **Sandwich Defense**: Meletakkan instruksi sistem di bagian awal DAN di bagian paling akhir prompt.
- **XML Tag Isolation**: Mengurung input pengguna di dalam `<user_input>` dan memerintahkan LLM menganggapnya HANYA sebagai data pasif.
- **Heuristic Injection Detector**: Memfilter prompt masukan sebelum dikirim ke API LLM.

---

## 6. Evaluasi Otomatis & Optimasi Prompt

### A. Metrik Evaluasi Prompt
- **Jaccard Similarity / Exact Match**:
  $$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$
- **LLM-as-a-Judge**: Menggunakan LLM terpisah (misal GPT-4) dengan rubrik khusus untuk menilai keakuratan dan kepatuhan format respon pada skala 1-5.

### B. Optimasi Token & Biaya
$$\text{Total Cost} = \left(\frac{N_{\text{prompt}}}{1000} \times P_{\text{input}}\right) + \left(\frac{N_{\text{completion}}}{1000} \times P_{\text{output}}\right)$$
Kompresi prompt dengan menghapus kata filler dapat menekan biaya API hingga 20%-40% tanpa menurunkan kualitas output.
