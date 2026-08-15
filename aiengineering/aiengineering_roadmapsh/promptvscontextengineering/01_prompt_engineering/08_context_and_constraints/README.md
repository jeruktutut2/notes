# 08. Context & Constraints

Modul ini mempelajari teknik injeksi data referensi (*In-Prompt Context*) dan pembatasan eksplisit (*Hard Constraints*) dalam Prompt Engineering.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. In-Prompt Context
- **Definisi**: Memasukkan dokumen latar belakang, kebijakan, atau cuplikan teks pendukung langsung di dalam prompt agar LLM menjawab berdasarkan data tersebut (Closed-Domain Q&A).
- **Teknik Framing**: Mengurung konteks dalam XML tags `<context>...</context>` atau triple quotes `"""..."""`.

### 2. Hard & Soft Constraints
- **Hard Constraints**: Batasan yang tidak boleh dilanggar (misal: *"Maksimal 3 kalimat"*, *"Jawab HANYA menggunakan informasi dari teks di atas"*, *"Dilarang menggunakan kata 'tidak'"*).
- **Soft Constraints**: Petunjuk prioritas gaya bahasa atau nada.
- **Constraint Validation**: Menggunakan skrip pengecek pasca-generasi untuk memastikan LLM mematuhi batasan.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi penegakan Hard Constraints dan Closed-Domain Q&A.
