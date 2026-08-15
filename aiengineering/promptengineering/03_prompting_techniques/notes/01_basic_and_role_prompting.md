# 01. Basic & Role-Based Prompting Techniques

## Overview
Dokumen ini membahas teknik prompting fundamental yang terdapat pada diagram roadmap.sh: **Zero-Shot Prompting**, **One-Shot / Few-Shot Prompting**, serta **System / Role / Contextual Prompting**.

---

## 1. Zero-Shot Prompting
Teknik memberi instruksi langsung kepada LLM tanpa memberikan contoh pasangan input-output (*exemplars*) sebelumnya.
- **Prinsip**: Mengandalkan pengetahuan dan pemahaman yang sudah diinternalisasi oleh model selama fase pre-training dan instruction-tuning.
- **Contoh**:
  ```markdown
  Klasifikasikan sentimen dari ulasan berikut sebagai Positif, Netral, atau Negatif:
  "Pengiriman barang sangat cepat, tetapi kemasannya sedikit penyok."
  ```

---

## 2. One-Shot & Few-Shot Prompting (In-Context Learning)
Teknik menyertakan satu (*One-Shot*) atau beberapa (*Few-Shot*) contoh pasangan instruksi dan jawaban ideal di dalam prompt sebelum memberikan input sebenarnya.

### Mengapa Few-Shot Sangat Efektif?
- Mengarahkan format output spesifik (misal: JSON, format ID khusus) tanpa perlu membebankan instruksi verbal yang panjang.
- Membantu model menangkap nuansa gaya bahasa, klasifikasi domain khusus, atau taksonomi perusahaan.

### Contoh Few-Shot Prompting:
```markdown
Tugas: Ubah nama kota dan negara menjadi format kode IATA bandara utama.

Input: Jakarta, Indonesia
Output: CGK

Input: Tokyo, Japan
Output: HND

Input: London, United Kingdom
Output: LHR

Input: Surabaya, Indonesia
Output:
```

---

## 3. System / Role / Contextual Prompting

Sub-node pada diagram roadmap.sh membagi kategori ini menjadi 3 komponen utama:

```
┌─────────────────────────────────────────┐
│        System / Role / Contextual       │
│  ┌───────────────────────────────────┐  │
│  │         System Prompting          │  │
│  ├───────────────────────────────────┤  │
│  │           Role Prompting          │  │
│  ├───────────────────────────────────┤  │
│  │        Contextual Prompting       │  │
│  └───────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### A. System Prompting
Instruksi tingkat atas (*top-level instruction*) yang menetapkan aturan baku, kebijakan keamanan, batasan format, dan guardrails yang berlaku di seluruh sesi percakapan.

### B. Role Prompting (Persona Alignment)
Menginstruksikan LLM untuk mengadopsi persona atau kepribadian ahli spesifik.
- **Efek Psikologis LLM**: Ketika diberi instruksi *"Anda adalah seorang Senior Cybersecurity Engineer dengan pengalaman 15 tahun"*, LLM mempersempit distribusi token ke dalam ruang vektor terminologi dan penalaran teknis tingkat lanjut.

### C. Contextual Prompting
Menyediakan latar belakang informasi (*background context*) atau fakta pendukung sebelum instruksi utama dieksekusi, sehingga respons model tetap berpatokan pada batasan bisnis (*grounded in domain context*).
