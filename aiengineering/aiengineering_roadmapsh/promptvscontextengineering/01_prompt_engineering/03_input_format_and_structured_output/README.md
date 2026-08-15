# 03. Input Format & Structured Output

Modul ini mempelajari teknik pembentukan format masukan (*Input Formatting*) dan penjaminan keluaran terstruktur (*Structured Output / JSON Schema Enforcement*).

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Input Formatting Patterns
- **XML Tag Delimiters**: Menggunakan tag `<instruction>`, `<context>`, `<user_input>` untuk memisahkan instruksi dari data eksternal.
- **Markdown & Bullet Points**: Mengatur hierarki informasi menggunakan struktur Markdown (`#`, `##`, `*`).
- **CSV & Key-Value Pair**: Memuat dataset terstruktur dalam bentuk tabel CSV/TSV untuk efisiensi token.

### 2. Structured Output Enforcement
- **JSON Mode & JSON Schema**: Memaksa LLM mengembalikan JSON valid yang dapat langsung di-parse oleh aplikasi tanpa *syntax error*.
- **Constrained Decoding / Grammars**: Teknik pembatasan kosa kata token (logits processor / BNF grammar) di tingkat inferensi LLM server.
- **Self-Repair Loop**: Algoritma otomatis yang mendeteksi kesalahan JSON dan mengirimkan error traceback kembali ke LLM untuk diperbaiki secara otomatis.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat penerapan XML Input Format dan simulasi Self-Repair Loop JSON Output.
