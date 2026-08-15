# 01. External Memory in Context Engineering

Modul ini mempelajari teknik arsitektur *External Memory* (Penyimpanan Memori Eksternal) untuk mengatasi keterbatasan *Context Window* bawaan LLM.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Jenis-Jenis External Memory
- **Episodic Memory Store**: Menyimpan riwayat transaksional percakapan per sesi di Redis / DynamoDB.
- **Semantic Memory Store**: Menyimpan profil, entitas, dan preferensi pengguna jangka panjang di Vector Database / Relational DB.
- **Graph Memory (Knowledge Graph)**: Menyimpan hubungan entitas (seperti Neo4j) untuk kueri yang membutuhkan hubungan antar konsep (*entity-relationship retrieval*).

### 2. Synchronization & Retrieval Mechanism
- **Memory Read/Write Loop**: Saat pengguna mengirim pesan, sistem membaca profil dari External Memory, di-inject ke prompt, lalu meng-update memori pasca jawaban LLM.
- **TTL & Expiration Policies**: Mengatur retensi memori agar data usang tidak membebani context window.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat alur kerja pembacaan dan penulisan External Memory secara dinamis.
