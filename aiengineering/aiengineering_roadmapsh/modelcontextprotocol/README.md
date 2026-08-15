# Model Context Protocol (MCP) Learning Module

Selamat datang di modul pembelajaran **Model Context Protocol (MCP)**! Modul ini dirancang berdasarkan roadmap **AI Engineer** (https://roadmap.sh/ai-engineer) dan diagram arsitektur resmi MCP.

---

## 🌟 Apa itu Model Context Protocol (MCP)?

**Model Context Protocol (MCP)** adalah protokol standar terbuka (*open standard protocol*) diciptakan oleh Anthropic yang memungkinkan aplikasi LLM (Host & Client) terhubung secara terstruktur, aman, dan dua arah dengan berbagai sumber data (*Resources*), instruksi konteks (*Prompts*), serta eksekusi alat (*Tools*) yang disediakan oleh MCP Server.

```
+-----------------------------------------------------------------------+
|                         CORE COMPONENTS                               |
|                                                                       |
|  +--------------------+  +--------------------+                       |
|  |      MCP Host      |  |     MCP Client     |                       |
|  +--------------------+  +--------------------+                       |
|                                                                       |
|  +--------------------------------------------+                       |
|  |                 MCP Server                 |                       |
|  +--------------------------------------------+                       |
|                                                                       |
|  +--------------------------------------------+                       |
|  |     Data Layer (Resources, Prompts, Tools) |                       |
|  +--------------------------------------------+                       |
|                                                                       |
|  +--------------------------------------------+                       |
|  |    Transport Layer (stdio, SSE / HTTP)     |                       |
|  +--------------------------------------------+                       |
+-----------------------------------------------------------------------+
|                      DEVELOPING WITH MCP                              |
|                                                                       |
|  +--------------------------------------------+                       |
|  |            Building an MCP Server          |                       |
|  +--------------------------------------------+                       |
|  |            Building an MCP Client          |                       |
|  +--------------------------------------------+                       |
|  |            Connect to Local Server         |                       |
|  +--------------------------------------------+                       |
|  |            Connect to Remote Server        |                       |
|  +--------------------------------------------+                       |
+-----------------------------------------------------------------------+
```

---

## 📁 Struktur Repositori

```
modelcontextprotocol/
├── README.md                           # Panduan Utama & Dokumentasi modul
├── requirements.txt                    # Dependensi Python
├── main.py                             # Interactive CLI Runner
├── notes/                              # Catatan materi lengkap
│   ├── 01_mcp_overview_and_architecture.md
│   ├── 02_core_components.md
│   └── 03_developing_with_mcp.md
├── 01_core_components/                 # Kode demonstrasi komponen inti
│   ├── mcp_host_client.py              # Simulator MCP Host & Client lifecycle
│   ├── mcp_server_primitives.py        # Resources, Prompts, dan Tools primitives
│   └── mcp_transports.py               # Stdio vs SSE/HTTP Transports
├── 02_developing_with_mcp/             # Praktik membangun & menghubungkan MCP
│   ├── building_mcp_server.py          # Implementasi server MCP lengkap
│   ├── building_mcp_client.py          # Implementasi client MCP lengkap
│   ├── connect_local_server.py         # Menghubungkan client ke local stdio server
│   └── connect_remote_server.py        # Menghubungkan client ke remote SSE server
└── web_visualizer/                     # Visualisator & Simulator Web Interaktif
    ├── index.html
    ├── styles.css
    └── app.js
```

---

## 🚀 Cara Menggunakan Modul Ini

### 1. Memjalankan Interactive CLI Runner
Jalankan skrip `main.py` menggunakan Python 3:
```bash
python3 main.py
```
Anda akan disajikan menu interaktif untuk mengeksekusi modul-modul skrip Python secara langsung.

### 2. Menjalankan Web Visualizer
Buka `web_visualizer/index.html` langsung di browser atau gunakan HTTP server lokal:
```bash
python3 -m http.server 8000 --directory web_visualizer
```
Akses `http://localhost:8000` di browser untuk membuka simulator visual interaktif MCP (Inspector JSON-RPC, Sandbox Host-Client-Server, Diagram Transport).

---

## 📚 Ringkasan Topik Utama

### 1. Core Components
- **MCP Host**: Aplikasi pengatur utama (seperti Claude Desktop, VS Code, Cursor, atau custom LLM App) yang menginisialisasi koneksi.
- **MCP Client**: Komponen pembantu yang mengelola 1:1 sesi koneksi stateful dengan server.
- **MCP Server**: Layanan terisolasi yang menyediakan akses ke data (*Resources*), templat instruksi (*Prompts*), dan fungsi yang dapat dipanggil (*Tools*).
- **Data Layer**:
  - `Resources`: Data pasif baca-saja yang diidentifikasi oleh URI (misal `file:///data.json`, `postgres://db/table`).
  - `Prompts`: Templat prompt reusable yang disiapkan server untuk LLM.
  - `Tools`: Fungsi terstruktur (JSON schema parameters) yang dapat dieksekusi LLM untuk beraksi di sistem external.
- **Transport Layer**:
  - `stdio`: Standard input/output subprocess communication (sangat cepat & lokal).
  - `SSE (Server-Sent Events) / HTTP`: Komunikasi streaming berbasis HTTP untuk server terpisah/remote.

### 2. Developing with MCP
- **Building an MCP Server**: Mendaftarkan handler `list_resources`, `read_resource`, `list_prompts`, `get_prompt`, `list_tools`, `call_tool`.
- **Building an MCP Client**: Mengirim `initialize`, menegosiasikan protocol version, menemukan kapabilitas server, dan menginstruksikan LLM.
- **Connect to Local Server**: Mengelola subprocess `spawn`, standard I/O pipes framing JSON-RPC.
- **Connect to Remote Server**: Menghubungkan ke Endpoint HTTP/SSE dengan autentikasi Token/Header & error handling.
