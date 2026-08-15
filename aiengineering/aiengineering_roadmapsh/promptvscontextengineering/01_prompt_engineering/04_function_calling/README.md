# 04. Function Calling (Tools API)

Modul ini mempelajari teknik *Function Calling* di mana LLM memutus fungsi/alat (*tool*) mana yang harus dipanggil berserta argumen terstrukturnya.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Dasar Function Calling
- **Definisi**: Menyuplai daftar fungsi (beserta nama, deskripsi, dan JSON Schema argumen) ke LLM agar model dapat merespons dengan JSON pemanggilan alat ketimbang teks biasa.
- **Komponen Utama**:
  - `tools`: Daftar fungsi yang tersedia (OpenAI / Anthropic standard tool spec).
  - `tool_choice`: Mengontrol apakah LLM wajib memanggil fungsi tertentu (`required`), memilih otomatis (`auto`), atau tidak memanggil (`none`).
  - `tool_calls`: Objek berisi `id`, `function.name`, dan `function.arguments`.

### 2. Workflow & Security Function Calling
- **Alur Eksekusi**:
  1. User mengirim kueri ke LLM + daftar `tools`.
  2. LLM memilih tool & membuat `arguments` JSON.
  3. Aplikasi lokal/backend mengeksekusi fungsi fisik.
  4. Hasil eksekusi dikirim kembali sebagai `tool` message ke LLM.
  5. LLM menyusun jawaban akhir bagi pengguna.
- **Toleransi Kesalahan & Sandboxing**:
  - Selalu memvalidasi argumen yang dibuat LLM sebelum dieksekusi di database/server fisik untuk mencegah SQL Injection atau Arbitrary Code Execution.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi alokasi Tool Call dan Tool Result Execution Loop.
