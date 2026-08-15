# Catatan 02: Core Components Model Context Protocol (MCP)

Sesuai dengan diagram komponen inti MCP, modul ini terbagi ke dalam komponen-komponen arsitektural utama:

---

## 1. MCP Host
**MCP Host** adalah aplikasi tingkat paling atas (*outer container*) yang berinteraksi langsung dengan pengguna manusia atau sistem LLM.

- **Contoh MCP Host**: Claude Desktop, VS Code with Copilot Extension, Cursor IDE, Custom Python LLM Agent application.
- **Tanggung Jawab Host**:
  - Mengelola siklus hidup (*lifecycle*) aplikasi dan antarmuka pengguna (UI/Chat window).
  - Membaca konfigurasi koneksi server (misalnya file `claude_desktop_config.json`).
  - Menginisialisasi dan mengontrol satu atau beberapa instance **MCP Client**.
  - Menggabungkan konteks yang diterima dari MCP Client ke dalam skema prompt LLM.
  - Meminta konfirmasi keamanan dari pengguna sebelum mengeksekusi *Tools* berisiko tinggi.

---

## 2. MCP Client
**MCP Client** adalah komponen pembantu teknis di dalam MCP Host yang menjaga hubungan 1-ke-1 (*1:1 stateful connection*) dengan satu **MCP Server**.

- **Tanggung Jawab Client**:
  - Membuka koneksi saluran transpor (*stdio* atau *SSE*).
  - Melakukan jabat tangan (*handshake*) JSON-RPC `initialize`.
  - Mengarahkan request dari LLM ke Server dan menerjemahkan response kembali ke LLM.
  - Mengelola abonemen (*subscription*) pembaruan data real-time dari Server.

---

## 3. MCP Server
**MCP Server** adalah program terisolasi (dapat berjalan di mesin lokal atau server remote) yang menyediakan data dan fungsionalitas spesifik melalui protokol MCP.

- **Karakteristik Server**:
  - Ringan, dapat ditulis dalam Python, TypeScript/Node.js, Go, Rust, atau C#.
  - Terisolasi (*sandboxed*): Server hanya memiliki akses ke direktori/API yang diberikan izin.
  - Exposes 3 data primitives utama: **Resources**, **Prompts**, dan **Tools**.

---

## 4. Data Layer Primitives
Data Layer pada MCP menyediakan 3 jenis primitif standar:

| Data Primitive | Sifat Akses | Penggunaan Utama | Contoh URI / Identifikasi |
| :--- | :--- | :--- | :--- |
| **Resources** | Read-only (Pasif) | Menyediakan dokumen, file, log, atau status database sebagai teks/binary. | `file:///project/README.md`, `db://users/102` |
| **Prompts** | Reusable Template | Reusable user/system message templates dengan parameter input. | `git_commit_summarizer`, `code_review_prompt` |
| **Tools** | Executable (Aktif) | Fungsi aktif dengan efek samping (*side-effects*) yang dapat dipanggil LLM. | `query_database`, `create_github_issue`, `execute_bash` |

### Detail Masing-Masing Primitif:

#### A. Resources
Resources direpresentasikan dengan URL unik (`URI`). Server menyediakan metode:
- `resources/list`: Mengembalikan daftar resource yang tersedia.
- `resources/read`: Mengembalikan isi teks atau data base64 binary dari URI tertentu.
- `resources/subscribe`: Mendaftarkan notifikasi perubahan data jika file/sumber data diperbarui.

#### B. Prompts
Prompts membantu pengguna mengaktifkan workflow kompleks dengan cepat melalui templat yang terstruktur. Server menyediakan:
- `prompts/list`: Mengembalikan templat prompt beserta argumen yang dibutuhkan.
- `prompts/get`: Menghasilkan susunan pesan (*messages*) siap pakai berdasarkan argumen input pengguna.

#### C. Tools
Tools memungkinkan LLM melakukan tindakan aktif pada dunia nyata melalui fungsi terstruktur. Server menyediakan:
- `tools/list`: Mengembalikan daftar fungsi beserta skema JSON Schema dari argumennya.
- `tools/call`: Mengeksekusi fungsi dengan argumen yang diberikan dan mengembalikan hasil teks/gambar/error.

---

## 5. Transport Layer
Transport Layer bertanggung jawab membungkus dan mentransmisikan paket pesan JSON-RPC 2.0 antara Client dan Server. MCP menetapkan 2 jenis transport standar:

### A. Stdio Transport (Standard Input / Standard Output)
- **Cara Kerja**: MCP Host meluncurkan MCP Server sebagai subprocess lokal (`spawn process`). Komunikasi terjadi melalui pipe `stdin` dan `stdout` proses tersebut.
- **Kelebihan**: Sangat cepat, latensi ultra-rendah, tidak memerlukan port jaringan atau konfigurasi firewall, sangat aman karena terisolasi di mesin lokal.
- **Format Pesan**: Setiap pesan JSON-RPC diakhiri dengan baris baru (`\n`).

### B. SSE / HTTP Transport (Server-Sent Events)
- **Cara Kerja**: Menggunakan protokol web HTTP standar. 
  - Client melakukan HTTP GET request ke endpoint `/sse` untuk membuka saluran aliran peristiwa dari Server ke Client.
  - Client mengirim pesan/request ke Server melalui HTTP POST request terpisah ke endpoint `/messages?sessionId=...`.
- **Kelebihan**: Mendukung arsitektur remote / cloud, dapat diakses dari mana saja via jaringan web.
