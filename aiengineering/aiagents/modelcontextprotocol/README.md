# MODEL CONTEXT PROTOCOL (MCP) - AI AGENTS WORKSPACE

Proyek pembelajaran **Model Context Protocol (MCP)** untuk AI Agents berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan spesifikasi standar terbuka MCP (Anthropic / Model Context Protocol).

Proyek ini mencakup simulasi murni (*self-contained*) dari pilar utama arsitektur dan pembuatan server MCP:
- **Core Components**:
  - **MCP Hosts & MCP Client**: Inisialisasi koneksi, handshake, negosiasi kapabilitas, dan penemuan server.
  - **MCP Servers & Primitives**: 3 Pilar utama MCP Primitives (**Tools**, **Resources**, **Prompts**) + **Sampling**.
  - **JSON-RPC 2.0 & Transports**: Format protokol JSON-RPC 2.0, **Stdio Transport** (Local IPC), dan **SSE Transport** (HTTP Event Stream).
- **Creating MCP Servers**:
  - **Building MCP Server (SDK Pattern)**: Pendaftaran handler via dekorator `@mcp.tool`, `@mcp.resource`, `@mcp.prompt`, dan validasi error.
  - **Local Desktop Deployment Mode**: Peluncuran server lokal sebagai *stdio subprocess*, parsing `claude_desktop_config.json`, dan eksekusi terisolasi.
  - **Remote / Cloud Deployment Mode**: Server terpusat via HTTP/SSE, otentikasi Bearer Token/API Key, multi-tenant session management.

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`json`, `sys`, `os`, `io`, `time`, `uuid`, `inspect`, `subprocess`, `typing`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

```bash
# Menggunakan Python 3.9+
python3 -m venv .venv
source .venv/bin/activate
```

---

## 🚀 Cara Menjalankan CLI Interaktif

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul simulasi secara visual:

```bash
python3 main.py
```

---

## 📚 Daftar Modul Pembelajaran

| No | Modul | Topik & Materi Utama | Skrip Python |
|----|-------|----------------------|--------------|
| **01** | **Core Components** | • MCP Hosts & MCP Client Architecture<br>• Handshake, Capability Exchange & Discovery<br>• MCP Primitives: Tools, Resources, Prompts<br>• JSON-RPC 2.0 Specification & Transports (Stdio vs SSE) | [`01_core_components/`](file:///Users/bsa/Documents/por/aiagents/modelcontextprotocol/01_core_components/) |
| **02** | **Creating MCP Servers** | • Pembuatan Server MCP dengan FastMCP SDK Pattern<br>• Dekorator `@mcp.tool`, `@mcp.resource`, `@mcp.prompt`<br>• Deployment Mode 1: Local Desktop (Subprocess Stdio)<br>• Deployment Mode 2: Remote / Cloud (HTTPS SSE + Bearer Auth) | [`02_creating_mcp_servers/`](file:///Users/bsa/Documents/por/aiagents/modelcontextprotocol/02_creating_mcp_servers/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari pemecahan masalah $M \times N$ integration, spesifikasi JSON-RPC 2.0, transport mechanics, hingga keamanan & sandboxing) dapat dibaca di folder:
👉 [notes/model_context_protocol_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/modelcontextprotocol/notes/model_context_protocol_roadmap_notes.md)
