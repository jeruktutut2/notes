# 01. Zero-Shot & Few-Shot Prompting

Modul ini mempelajari teknik pengarahan LLM tanpa contoh (*Zero-Shot*) dan dengan contoh *in-context learning* (*Few-Shot*).

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Zero-Shot Prompting
- **Definisi**: Memberikan instruksi langsung ke LLM tanpa contoh pasangan input-output sebelumnya.
- **Kapan Digunakan**:
  - Tugas umum/standar (klasifikasi sentimen, penerjemahan, pemeringkatan).
  - Menghemat token input ketika LLM (seperti GPT-4o / Claude 3.5) sudah memiliki *prior knowledge* yang kuat.
- **Tantangan**: Model rentan membuat kesalahan format jika instruksi ambigu.

### 2. Few-Shot Prompting (In-Context Learning)
- **Definisi**: Menyertakan $N$ contoh pasangan $(x_i, y_i)$ di dalam prompt untuk mengarahkan gaya, pola, atau format keluaran model.
- **Komponen Penting**:
  - **Exemplar Selection**: Memilih contoh yang paling relevan dengan kueri pengguna.
  - **Ordering Sensitivity**: Urutan contoh dapat memengaruhi bias jawaban LLM (efek *recency bias*).
  - **Format Consistency**: Format contoh harus identik dengan format luaran yang diinginkan.
- **Keuntungan**: Meningkatkan akurasi format hingga 95%+ dan mengurangi kebingungan model pada domain khusus.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi perbedaan akurasi, penggunaan token, dan konsistensi format antara Zero-Shot dan Few-Shot Prompting.
