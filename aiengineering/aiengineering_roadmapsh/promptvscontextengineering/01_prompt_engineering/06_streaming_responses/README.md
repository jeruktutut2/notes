# 06. Streaming Responses

Modul ini mempelajari teknik *Streaming Responses* (Server-Sent Events / Chunked Transfer) untuk menyajikan respons LLM secara real-time token demi token.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Mengapa Streaming Sangat Penting?
- **Perceived Latency vs Absolute Latency**: LLM membutuhkan waktu beberapa detik untuk menyelesaikan paragraf panjang. Dengan streaming, token pertama tampil dalam hitungan milidetik (*Low Time-To-First-Token / TTFT*), memberikan UX yang responsif.
- **Protokol Streaming**:
  - **Server-Sent Events (SSE)**: HTTP-based streaming standar yang dipakai OpenAI / Anthropic (`stream=True`).
  - **WebSockets**: Dipakai untuk komunikasi dua arah real-time (misal: voice-to-voice agents).

### 2. Tantangan & Implementation Patterns
- **JSON Parsing pada Streaming**: Jika menggunakan Structured Output / JSON mode, token yang dikirim secara bertahap belum berupa JSON valid sampai token terakhir tiba.
  - *Solusi*: Menggunakan *Partial JSON Parser* (seperti `partialjson` atau buffer parser) untuk me-render UI komponen secara bertahap.
- **Handling Interruption**: Mengizinkan pengguna menghentikan generasi pertengahan jalan (*Aborting stream*) untuk menghemat biaya token output.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi efek streaming token demi token di terminal.
