# Catatan 03: Developing with Model Context Protocol (MCP)

Sesuai dengan sub-bagian **Developing with MCP** dari diagram target, catatan ini membahas panduan praktis dalam membangun MCP Server, MCP Client, serta membuat koneksi lokal maupun remote.

---

## 1. Building an MCP Server

Membangun MCP Server melibatkan langkah-langkah berikut:

### Langkah 1: Inisialisasi Server & Pendaftaran Kapabilitas
Menggunakan MCP SDK (misal Python SDK `mcp.server.fastmcp`), kita mendefinisikan server dan kapabilitasnya:

```python
from mcp.server.fastmcp import FastMCP

# Inisialisasi MCP Server
mcp = FastMCP("My Custom MCP Server")
```

### Langkah 2: Menambahkan Resources
```python
@mcp.resource("config://app-settings")
def get_config() -> str:
    """Mengembalikan konfigurasi aplikasi saat ini."""
    return '{"environment": "production", "debug": false}'
```

### Langkah 3: Menambahkan Prompts
```python
@mcp.prompt()
def summarize_code(code: str) -> str:
    """Templat instruksi untuk merangkum kode."""
    return f"Tolong buat ringkasan arsitektur dari kode berikut:\n\n```python\n{code}\n```"
```

### Langkah 4: Menambahkan Tools
```python
@mcp.tool()
def query_user(user_id: int) -> dict:
    """Mencari data pengguna berdasarkan User ID."""
    # Logika query database
    return {"id": user_id, "name": "Budi Santoso", "role": "AI Engineer"}
```

---

## 2. Building an MCP Client

Membangun MCP Client membutuhkan pengolahan koneksi transpor dan pengiriman pesan JSON-RPC:

### Langkah Utama Client:
1. **Pilih Transport**: Buat `StdioServerParameters` untuk lokal atau `SseClientTransport` untuk remote.
2. **Koneksi & Handshake**: Inisialisasi `ClientSession` dan panggil `session.initialize()`.
3. **Penemuan Kapabilitas**: Panggil `session.list_tools()`, `session.list_resources()`, `session.list_prompts()`.
4. **Eksekusi & Sampling**: Eksekusi `session.call_tool(name, args)` atau sampaikan hasil data ke LLM.

---

## 3. Connect to Local Server

Koneksi ke **Local Server** umumnya menggunakan **Stdio Transport**:

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_local():
    # Menentukan perintah peluncuran server lokal
    server_params = StdioServerParameters(
        command="python3",
        args=["my_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # 1. Initialize
            await session.initialize()
            
            # 2. List tools
            tools = await session.list_tools()
            print("Server Tools:", [t.name for t in tools.tools])
```

---

## 4. Connect to Remote Server

Koneksi ke **Remote Server** menggunakan **SSE (Server-Sent Events) Transport** over HTTP:

```python
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def run_remote():
    url = "https://mcp-server.example.com/sse"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    
    async with sse_client(url, headers=headers) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            
            # Eksekusi tool di remote server
            result = await session.call_tool("remote_tool", arguments={"key": "val"})
            print("Remote Result:", result.content)
```

---

## 5. Pertimbangan Keamanan & Best Practices (Security Guidelines)

1. **Prinsip Hak Akses Terbatas (Least Privilege)**:
   - MCP Server lokal hanya boleh diberi akses ke direktori yang benar-benar dibutuhkan, bukan seluruh root filesystem (`/`).
2. **User Confirmation Prompting**:
   - MCP Host harus selalu meminta persetujuan manusia (*human-in-the-loop*) sebelum mengeksekusi *Tool* yang mengubah state (misalnya menulis file, membuat git commit, mengirim email, meretas server).
3. **Sanitasi Input & Output**:
   - Selalu validasi argumen input fungsi tool dengan JSON Schema (misal Pydantic di Python).
   - Hindari mengeksekusi string shell secara mentah (`eval()`, `exec()`, `subprocess.run(shell=True)`).
4. **Transport Security (TLS/HTTPS)**:
   - Koneksi remote SSE wajib menggunakan HTTPS (`https://`) dan token JWT/Bearer yang valid untuk mencegah Man-In-The-Middle (MITM) attack.
