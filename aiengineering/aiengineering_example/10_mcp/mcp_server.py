"""
==============================================================================
CONTOH MODUL 10A: MCP SERVER (MODEL CONTEXT PROTOCOL)
==============================================================================
MCP (Model Context Protocol) adalah standar universal terbuka (dibuat oleh Anthropic)
yang memungkinkan AI Assistant (Claude Desktop, Cursor, Custom Client) terhubung
secara seragam ke berbagai Tools dan Data Resources eksternal.

FUNGSI MCP SERVER:
    1. Mempublikasikan daftar Tools yang dapat dieksekusi (`@mcp.tool()`).
    2. Mempublikasikan daftar Resources yang dapat dibaca AI (`@mcp.resource()`).
    3. Berkomunikasi menggunakan protokol standar JSON-RPC via stdio / HTTP-SSE.

CARA PAKAI:
    - Menjalankan server: python mcp_server.py
==============================================================================
"""

import sys
import json
import platform
import datetime

# Kita buat implementasi MCP Server mandiri standar JSON-RPC
# agar dapat berjalan di lingkungan Python apapun tanpa dependensi berat.

class MCPServerSederhana:
    def __init__(self, nama_server: str):
        self.nama_server = nama_server
        self.tools = {}
        self.resources = {}

    def mendaftarkan_tool(self, nama: str, deskripsi: str, arg_schema: dict, handler):
        """Mendaftarkan fungsi tool ke registry MCP."""
        self.tools[nama] = {
            "name": nama,
            "description": deskripsi,
            "inputSchema": arg_schema,
            "handler": handler
        }

    def mendaftarkan_resource(self, uri: str, nama: str, handler):
        """Mendaftarkan sumber data ke registry MCP."""
        self.resources[uri] = {
            "uri": uri,
            "name": nama,
            "handler": handler
        }

    def tangani_request_jsonrpc(self, payload_str: str) -> str:
        """Menerima dan memproses pesan JSON-RPC dari MCP Client."""
        try:
            req = json.loads(payload_str)
            method = req.get("method")
            req_id = req.get("id", 1)

            # 1. MCP Initialization
            if method == "initialize":
                res = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {"tools": {}, "resources": {}},
                        "serverInfo": {"name": self.nama_server, "version": "1.0.0"}
                    }
                }
                return json.dumps(res)

            # 2. List Available Tools
            elif method == "tools/list":
                daftar_tools = [
                    {
                        "name": v["name"],
                        "description": v["description"],
                        "inputSchema": v["inputSchema"]
                    }
                    for v in self.tools.values()
                ]
                return json.dumps({"jsonrpc": "2.0", "id": req_id, "result": {"tools": daftar_tools}})

            # 3. Call Tool Execution
            elif method == "tools/call":
                params = req.get("params", {})
                nama_tool = params.get("name")
                arguments = params.get("arguments", {})

                tool_item = self.tools.get(nama_tool)
                if tool_item:
                    hasil = tool_item["handler"](**arguments)
                    return json.dumps({
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": json.dumps(hasil)}]
                        }
                    })
                else:
                    return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Tool tidak ditemukan"}})

            else:
                return json.dumps({"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method tidak didukung"}})

        except Exception as e:
            return json.dumps({"jsonrpc": "2.0", "id": 1, "error": {"code": -32603, "message": str(e)}})


# ------------------------------------------------------------------------------
# DEFINISI HANDLER TOOLS & RESOURCES AKURAT
# ------------------------------------------------------------------------------

def tool_hitung_diskon(harga_awal: float, persen_diskon: float) -> dict:
    potongan = harga_awal * (persen_diskon / 100)
    harga_akhir = harga_awal - potongan
    return {
        "harga_awal": harga_awal,
        "diskon_persen": persen_diskon,
        "potongan_harga": potongan,
        "harga_akhir": harga_akhir
    }


def tool_info_sistem() -> dict:
    return {
        "os": platform.system(),
        "os_version": platform.version(),
        "python_version": sys.version.split()[0],
        "waktu_server": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


# ------------------------------------------------------------------------------
# DEPLOY SERVER DEMO
# ------------------------------------------------------------------------------
def main():
    server = MCPServerSederhana("Server-MCP-AI-Engineering")

    # Registrasi Tool 1
    server.mendaftarkan_tool(
        nama="hitung_diskon",
        deskripsi="Menhitung potongan harga promo dan harga akhir setelah diskon",
        arg_schema={
            "type": "object",
            "properties": {
                "harga_awal": {"type": "number", "description": "Harga asli barang"},
                "persen_diskon": {"type": "number", "description": "Persentase diskon (1-100)"}
            },
            "required": ["harga_awal", "persen_diskon"]
        },
        handler=tool_hitung_diskon
    )

    # Registrasi Tool 2
    server.mendaftarkan_tool(
        nama="info_sistem",
        deskripsi="Mendapatkan informasi spesifikasi OS dan sistem tempat server berjalan",
        arg_schema={"type": "object", "properties": {}},
        handler=tool_info_sistem
    )

    print("=========================================================")
    print(f"🚀 {server.nama_server} BERJALAN DENGAN PROTOKOL MCP (JSON-RPC)")
    print("=========================================================")

    # Simulasi memproses request pembuka dari Client
    req_init = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
    req_tools = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
    req_exec = json.dumps({
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "hitung_diskon", "arguments": {"harga_awal": 200000, "persen_diskon": 25}}
    })

    print("\n--- [1. PROSES INITIALIZE CLIENT] ---")
    print("Response:", server.tangani_request_jsonrpc(req_init))

    print("\n--- [2. DISCOVERY DAFTAR TOOLS] ---")
    print("Response:", server.tangani_request_jsonrpc(req_tools))

    print("\n--- [3. EKSSEKUSI TOOL KHUSUS] ---")
    print("Response:", server.tangani_request_jsonrpc(req_exec))


if __name__ == "__main__":
    main()
