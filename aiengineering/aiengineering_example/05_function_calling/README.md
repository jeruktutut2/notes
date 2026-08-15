# 📘 Modul 5 — Function / Tool Calling

Modul ini mendemonstrasikan bagaimana menjembatani Model AI dengan **Aksi Dunia Nyata** (seperti akses database, API pihak ketiga, dan kalkulasi tepat) menggunakan skema **Function / Tool Calling**.

---

## 💡 Konsep Penting
1. **LLM Tidak Mengeksekusi Kode**: LLM tidak secara langsung menjalankan fungsi Python di komputer kita.
2. **Peran LLM**: LLM bertindak sebagai *Routing/Parser* cerdas yang memahami maksud user, memilih fungsi mana yang sesuai, dan memformat argumen JSON-nya.
3. **Peran Aplikasi Kita**: Kode Python kita menerima nama fungsi dari LLM, mengeksekusinya di lingkungan lokal yang aman, lalu mengembalikan hasilnya ke LLM.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# Pastikan Ollama sudah berjalan
ollama serve

# Jalankan skrip tool calling
python 05_function_calling/main.py
```
