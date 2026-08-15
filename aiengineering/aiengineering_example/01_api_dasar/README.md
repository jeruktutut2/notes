# 📘 Modul 1 — Memanggil LLM via API (Dasar)

Modul ini membahas fondasi paling mendasar dalam **AI Engineering**: bagaimana cara program Python kita "berbicara" dengan Large Language Model (LLM) melalui HTTP REST API secara langsung tanpa perlu bergantung pada framework kompleks.

---

## 🎯 Tujuan Pembelajaran
1. Memahami cara membaca API key & konfigurasi dari file `.env`.
2. Mengetahui struktur payload data HTTP POST ke Ollama API & Google Gemini API.
3. Memahami perbedaan antara **System Prompt** (aturan/persona AI) dan **User Prompt** (input pengguna).
4. Memahami mode penerimaan jawaban: **Non-Streaming** vs **Streaming (Server-Sent Events)**.

---

## 💻 Struktur Berkas
- `main.py`: Script Python utama yang berisi contoh fungsi pemanggilan API secara murni.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

### Prasyarat:
Pastikan **Ollama** sudah terpasang dan service-nya aktif:
```bash
# 1. Jalankan server Ollama lokal
ollama serve

# 2. Pastikan model pilihan sudah di-download
ollama pull gemma3:4b
```

### Eksekusi Program:
```bash
# Jalankan script dari terminal
python 01_api_dasar/main.py
```

---

## 🔍 Penjelasan Konsep Kunci

### 1. System Prompt vs User Prompt
```json
{
  "messages": [
    {"role": "system", "content": "Kamu adalah asisten customer service yang sopan."},
    {"role": "user", "content": "Bagaimana cara pengembalian barang?"}
  ]
}
```
- **System Prompt**: Mengatur konteks latar belakang, gaya bahasa, batasan topik, dan instruksi keselamatan yang selalu dipatuhi LLM selama interaksi.
- **User Prompt**: Pertanyaan atau perintah dinamis yang dimasukkan oleh pengguna akhir.

### 2. Streaming Output
Dengan menetapkan `"stream": true`, response dikirim dari Ollama dalam bentuk deretan chunk JSON terpisah. Ini memungkinkan antarmuka aplikasi menampilkan teks kata demi kata secara real-time seperti pada ChatGPT.
