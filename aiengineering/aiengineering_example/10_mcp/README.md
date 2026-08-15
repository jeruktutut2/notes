# 📘 Modul 10 — Model Context Protocol (MCP)

Modul ini mempelajari **MCP (Model Context Protocol)**, standar terbuka industri buatan Anthropic yang mendefinisikan cara seragam bagi aplikasi AI untuk terhubung ke berbagai Tools dan Resources eksternal.

---

## 🔌 Mengapa MCP Dibutuhkan?

| Sebelum MCP | Setelah Ada MCP |
|---|---|
| Setiap aplikasi AI harus menulis konektor kustom untuk setiap database/API. | Satu **MCP Server** dapat digunakan oleh **banyak MCP Client** (Claude Desktop, Cursor IDE, Custom App). |
| Terikat (*Vendor Lock-in*) pada satu provider AI. | Protokol standar universal berbasis JSON-RPC yang independen. |

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# 1. Jalankan pengujian MCP Server
python 10_mcp/mcp_server.py

# 2. Jalankan interaksi MCP Client
python 10_mcp/mcp_client.py
```
