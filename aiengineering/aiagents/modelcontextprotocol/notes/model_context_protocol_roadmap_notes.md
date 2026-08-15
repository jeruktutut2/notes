# MODEL CONTEXT PROTOCOL (MCP) - CATATAN PANDUAN LENGKAP

Catatan panduan dan dokumentasi teori komprehensif mengenai **Model Context Protocol (MCP)** berdasarkan roadmap [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan arsitektur standar terbuka Anthropic MCP.

---

## 📌 1. Pendahuluan & Mengapa MCP Dibutuhkan?

### Problem Statement: Masalah Konektivitas M × N
Sebelum adanya Model Context Protocol (MCP), menghubungkan model kecerdasan buatan (LLM) dengan data eksternal, database, API, atau alat bantu (tools) memerlukan integrasi kustom (*custom integration*) untuk setiap kombinasi **Model/Host** dan **Sumber Data/Tool**.
- Jika terdapat $M$ aplikasi AI (e.g. Claude Desktop, VS Code, Custom Web App, Cursor) dan $N$ sumber data/tool (e.g. Postgres DB, GitHub API, Slack, Google Drive, Local File System), maka industri memerlukan $M \times N$ integrasi khusus.
- Format skema tool, otentikasi, dan protokol pertukaran data tidak terstandardisasi.

```
[ TANPA MCP: M × N Integrasi Kustom ]
  Claude Desktop ----+----> Postgres Custom API
  VS Code Copilot ---+----> GitHub Custom REST API
  Custom AI Agent ---+----> Local File System API

[ DENGAN MCP: Standardisasi Protokol Terbuka ]
  MCP Hosts (M) <---> [ MCP Protocol (JSON-RPC 2.0) ] <---> MCP Servers (N)
```

### Solusi Model Context Protocol (MCP)
**Model Context Protocol (MCP)** adalah standar protokol terbuka (*open standard*) universal yang memfasilitasi komunikasi aman dan terstandardisasi antara aplikasi AI (**MCP Hosts**) dengan penyedia konteks/alat bantu (**MCP Servers**).

- Analog seperti **USB-C untuk AI**: Satu jenis colokan standar untuk menghubungkan AI ke semua sumber data dan alat.
- Berbasis **JSON-RPC 2.0** yang fleksibel dan independen terhadap bahasa pemrograman (Python, TypeScript/JavaScript, Go, Kotlin, C++).

---

## 🏗️ 2. Core Components (Komponen Utama MCP)

Berdasarkan arsitektur resmi MCP, sistem terdiri dari tiga komponen utama yang saling berinteraksi:

```
+-----------------------------------------------------------------------+
|                              MCP HOST                                 |
|  (Aplikasi AI Utama, e.g. Claude Desktop, IDE Plugin, AI Workplace)    |
|                                                                       |
|   +---------------------------------------------------------------+   |
|   |                        MCP CLIENT                             |   |
|   |  - Mengelola siklus hidup koneksi 1:1 dengan Server          |   |
|   |  - Negosiasi kapabilitas & pertukaran pesan JSON-RPC 2.0      |   |
|   +---------------------------------------------------------------+   |
+-----------------------------------|-----------------------------------+
                                    | Transport (Stdio / SSE)
                                    v
+-----------------------------------------------------------------------+
|                             MCP SERVERS                               |
|  (Server penyedia konteks, data read-only, atau fungsi eksekusi)      |
|                                                                       |
|  [ 🛠️ Tools ]         [ 📄 Resources ]          [ 💬 Prompts ]       |
+-----------------------------------------------------------------------+
```

### 1. MCP Hosts (Aplikasi AI)
**MCP Host** adalah aplikasi utama yang dijalankan oleh pengguna yang mengkoordinasikan interaksi AI dan antarmuka pengguna.
- **Tanggung Jawab Host**:
  - Mengelola UI/UX dan interaksi prompt dengan pengguna.
  - Memanggil LLM (Large Language Model) untuk memproses teks/perintah.
  - Membaca konfigurasi server MCP (e.g. `claude_desktop_config.json` atau workspace settings).
  - Meluncurkan atau mengkoneksikan proses **MCP Client**.

### 2. MCP Client (Protokol Client)
**MCP Client** adalah komponen internal di dalam Host yang mengimplementasikan spesifikasi protokol MCP.
- **Tanggung Jawab Client**:
  - Membuka koneksi 1-ke-1 (*1:1 connection*) dengan satu MCP Server.
  - Melakukan proses **Handshake** dan **Capability Negotiation** saat pertama kali terhubung.
  - Menerjemahkan permintaan Host menjadi format **JSON-RPC 2.0**.
  - Mengirim pesan via Transport Layer (stdio atau HTTP/SSE) dan menerima respon/event dari Server.

### 3. MCP Servers (Penyedia Konteks & Tool)
**MCP Server** adalah program/layanan eksternal yang mengekspos kapabilitas khusus kepada MCP Client melalui standar MCP.
- Server dapat berjalan secara **lokal** (sebagai *subprocess*) atau secara **remote** (via cloud API).
- Server menyediakan tiga primitif utama (*MCP Primitives*): **Tools**, **Resources**, dan **Prompts**.

---

## 🧩 3. MCP Primitives (Primitif Utama MCP)

MCP Server mengekspos kapabilitasnya dalam 3 kategori primitif utama (ditambah kapabilitas Sampling):

| Primitif MCP | Jenis Interaksi | Deskripsi & Kegunaan | Contoh Penggunaan |
|--------------|-----------------|----------------------|-------------------|
| **Tools** | Executable (Action) | Fungsi komputasi atau aksi yang dapat dipanggil oleh LLM untuk mengubah status atau mengambil data dinamis. | Eksekusi query SQL, kirim email, jalankan skrip Python, panggil API REST. |
| **Resources** | Read-Only (Context Data) | Data konteks pasif yang dapat dibaca oleh Client berbasis URI (`file://`, `postgres://`, `api://`). | Membaca log file, isi tabel database, skema file project, dokumentasi. |
| **Prompts** | Dynamic Template | Template prompt atau instruksi sistem reusable yang disediakan server untuk memandu LLM. | Template `code-review-prompt`, template `bug-fixing-guide`, prompt analisa data. |
| **Sampling** | Reverse Request | Fitur di mana MCP Server meminta kelengkapan jawaban LLM balik melalui MCP Client / Host. | Server meminta LLM meringkas teks sebelum menyimpannya ke database. |

---

## 📡 4. JSON-RPC 2.0 & Transport Layer

### Spesifikasi JSON-RPC 2.0
Seluruh pertukaran pesan dalam MCP menggunakan standar format **JSON-RPC 2.0**.

#### 1. Request (Client -> Server)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "calculate_tax",
    "arguments": {
      "income": 10000000,
      "rate": 0.11
    }
  }
}
```

#### 2. Response Success (Server -> Client)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Pajak penghasilan yang dihitung adalah Rp 1.100.000"
      }
    ],
    "isError": false
  }
}
```

#### 3. Error Response (Server -> Client)
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params: argument 'income' must be positive number."
  }
}
```

### Transport Layer: Stdio vs SSE

| Karakteristik | Stdio Transport (Standard Input/Output) | SSE Transport (Server-Sent Events over HTTP) |
|---------------|------------------------------------------|---------------------------------------------|
| **Target Deployment** | Local Desktop | Remote / Cloud Deployment |
| **Mekanisme IPC** | `stdin` dan `stdout` antar proses dalam satu OS | HTTP POST (request) + SSE HTTP (streaming responses) |
| **Kecepatan / Latensi** | Sangat tinggi, zero network latency | Tergantung koneksi jaringan / internet |
| **Otentikasi** | Diatur oleh akses OS lokal (Sandbox/Permissions) | Memerlukan OAuth2, Bearer Token, API Key header |
| **Skalabilitas** | 1 proses Server untuk 1 Host lokal | Multi-tenant cloud service (banyak client sekaligus) |

---

## 🔨 5. Creating MCP Servers (Membuat Server MCP)

Membuat MCP Server dapat dilakukan menggunakan SDK resmi (Python FastMCP / TypeScript SDK).

### Siklus Hidup Server (Server Lifecycle)
1. **Initialization**: Client mengirim `initialize` request dengan daftar kapabilitas client (`capabilities: { tools: {}, resources: {}, prompts: {} }`).
2. **Handshake & Negotiation**: Server merespon dengan kapabilitas server dan versi protokol (e.g., `2024-11-05`).
3. **Initialized Notification**: Client mengirim notifikasi `notifications/initialized` untuk mengonfirmasi koneksi siap digunakan.
4. **Operation Loop**: Server siap menerima request `tools/list`, `tools/call`, `resources/read`, `prompts/get`.
5. **Shutdown**: Diskoneksi rapi saat Host ditutup.

---

## 🚀 6. Deployment Modes (Mode Penggelaran)

Berdasarkan diagram visual roadmap, terdapat dua **Deployment Modes** utama untuk MCP Server:

```
                   +------------------------+
                   |  Creating MCP Servers  |
                   +-----------+------------+
                               |
                   +-----------+------------+
                   |    Deployment Modes    |
                   +-----+------------+-----+
                         |            |
            +------------+            +------------+
            v                                      v
  +------------------+                    +------------------+
  |  Local Desktop   |                    |  Remote / Cloud  |
  +------------------+                    +------------------+
```

### A. Local Desktop Deployment Mode
Mode penggelaran di mana Server MCP berjalan di komputer lokal pengguna sebagai **subprocess** yang dipanggil langsung oleh MCP Host.

- **Karakteristik & Keunggulan**:
  - Menggunakan **Stdio Transport**.
  - Didefinisikan dalam file konfigurasi JSON Host (e.g. `claude_desktop_config.json`):
    ```json
    {
      "mcpServers": {
        "sqlite-db": {
          "command": "python3",
          "args": ["/path/to/server.py"],
          "env": { "DB_PATH": "./local.db" }
        }
      }
    }
    ```
  - **Akses Langsung**: Memiliki akses langsung ke file lokal, port lokal, CLI tools (git, sqlite, docker).
  - **Keamanan**: Terisolasi pada komputer lokal pengguna tanpa risiko mengekspos port ke internet.

### B. Remote / Cloud Deployment Mode
Mode penggelaran di mana Server MCP berjalan di server terpusat (Cloud, Kubernetes, Serverless, Docker Container) dan diakses melalui jaringan HTTP/HTTPS.

- **Karakteristik & Keunggulan**:
  - Menggunakan **SSE Transport** (Server-Sent Events) over HTTP/HTTPS.
  - **Otentikasi Wajib**: Memerlukan validasi `Authorization: Bearer <token>` atau API Key untuk mengamankan endpoint.
  - **Multi-Tenant**: Satu Server Cloud dapat melayani ribuan Client dari berbagai pengguna secara simultan.
  - **Integrasi Sistem Enterprise**: Sangat ideal untuk menghubungkan AI Host dengan Database Perusahaan (Postgres Cloud, Snowflake), CRM (Salesforce), atau SaaS API (Slack, Jira, GitHub Cloud).

---

## 🛡️ 7. Keamanan & Best Practices (Security & Guidance)

1. **Human-in-the-Loop (Approval User)**:
   - Host HARUS meminta persetujuan pengguna sebelum mengeksekusi Tool yang berisiko tinggi (e.g. menghapus file, mengirim uang, membuat commit git).
2. **Input Validation & Sanitization**:
   - Seluruh argumen pada `tools/call` harus divalidasi dengan JSON Schema yang ketat untuk mencegah serangan *Command Injection* atau *SQL Injection*.
3. **Least Privilege Principle**:
   - Berikan izin akses seminimal mungkin pada Server lokal maupun remote (hanya folder atau database tertentu yang boleh diakses).
4. **Error Isolation**:
   - Kegagalan satu MCP Server tidak boleh merusak proses MCP Host atau menghentikan respon LLM secara keseluruhan.
