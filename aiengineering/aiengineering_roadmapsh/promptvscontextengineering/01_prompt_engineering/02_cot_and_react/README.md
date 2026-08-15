# 02. Chain-of-Thought (CoT) & ReAct Framework

Modul ini mempelajari teknik penalaran sekuensial (*Chain-of-Thought*) dan framework interaksi agen dengan eksternal tools (*ReAct: Reasoning + Acting*).

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Chain-of-Thought (CoT) Prompting
- **Definisi**: Meminta LLM untuk menghasilkan langkah-langkah pemikiran (*intermediate reasoning steps*) sebelum mengembalikan jawaban akhir.
- **Frasa Kunci**: `"Mari kita selesaikan langkah demi langkah (Think step-by-step)."`
- **Mengapa CoT Bekerja?**:
  - LLM bekerja secara *autoregressive* (token demi token). Memaksa model mencetak token pemikiran memberikan alokasi komputasi ekstra untuk memproses masalah sebelum menentukan angka/keputusan akhir.
- **Variasi CoT**:
  - **Zero-Shot CoT**: Menambahkan instruksi *"Let's think step by step"*.
  - **Few-Shot CoT**: Memberikan contoh soal lengkap dengan penjelasan penalaran tiap langkah.
  - **Self-Consistency Voting**: Menjalankan CoT $N$ kali dengan suhu $T > 0$ lalu mengambil jawaban mayoritas.

### 2. ReAct Framework (Reasoning + Acting)
- **Definisi**: Menggabungkan kemampuan penalaran (*Thought*) dengan aksi nyata (*Action*) memanggil alat eksternal (APIs, Search Engine, Database) dan membaca hasilnya (*Observation*).
- **Siklus Loop ReAct**:
  1. **Thought**: LLM memikirkan langkah berikutnya berdasarkan tujuan pengguna.
  2. **Action**: LLM memilih alat yang akan dipanggil, misal `search(query)` atau `calculator(expr)`.
  3. **Observation**: Sistem mengeksekusi alat dan mengembalikan hasilnya ke LLM.
  4. **Repeat**: Ulangi sampai LLM menghasilkan `Final Answer`.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi eksekusi CoT dan siklus loop ReAct Agent secara langsung.
