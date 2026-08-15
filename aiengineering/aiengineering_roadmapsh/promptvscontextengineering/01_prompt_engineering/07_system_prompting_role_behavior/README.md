# 07. System Prompting, Role & Behavior

Modul ini mempelajari teknik penetapan pesan sistem (*System Prompting*), pembentukan peran persona (*Role Framing*), dan penyelarasan perilaku (*Behavioral Alignment*).

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. System Prompting vs User Prompting
- **System Prompt**: Instruksi tingkat atas (*top-level metadata*) yang mengatur identitas, aturan dasar, batasan privasi, dan instruksi permanen yang melandasi seluruh sesi percakapan.
- **User Prompt**: Kueri masukan spesifik dari pengguna per turn.

### 2. Role & Behavior Framing
- **Persona Alignment**: Menetapkan kepribadian, gaya bahasa, dan tingkat kepakaran model (contoh: *"Anda adalah Pengacara Senior dengan gaya bahasa formal dan analitis"*).
- **Negative Constraints**: Mendefinisikan apa yang **TIDAK BOLEH** dilakukan model (contoh: *"Dilarang memberikan saran medis atau menyebut nama kompetitor"*).
- **Fallback Behavior**: Menentukan tindakan baku jika model tidak mengetahui jawaban (contoh: *"Jika informasi tidak ada dalam dokumen RAG, jawab dengan 'Maaf, data tidak tersedia'"*).

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat perbedaan perilaku LLM ketika diberi System Role & Behavioral Constraints yang berbeda.
