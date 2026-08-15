"""
==============================================================================
CONTOH MODUL 10B: MCP CLIENT (MODEL CONTEXT PROTOCOL CLIENT)
==============================================================================
MCP Client adalah aplikasi (seperti AI App kita, IDE Cursor, atau Claude Desktop)
yang terhubung ke MCP Server untuk melakukan discovery kemampuan tools secara otomatis.

ALUR WORKFLOW MCP CLIENT:
    1. Handshake Handshake Protocol (`initialize`).
    2. Discovery: Bertanya ke server "Tools apa saja yang kamu miliki?" (`tools/list`).
    3. Tool Call: Memanggil tool spesifik dengan parameter JSON (`tools/call`).
    4. Respon: Menerima hasil dan menggunakannya untuk menjawab pertanyaan pengguna.

CARA PAKAI:
    - Jalankan: python mcp_client.py
==============================================================================
"""

import json
from mcp_server import MCPServerSederhana, tool_hitung_diskon, tool_info_sistem


class MCPClientDemo:
    def __init__(self, server_target: MCPServerSederhana):
        self.server = server_target

    def hubungkan_dan_inisialisasi(self):
        print("\n--- [MCP CLIENT] Mengirim request Initialize ke MCP Server ---")
        req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        res = self.server.tangani_request_jsonrpc(req)
        data = json.loads(res)
        nama_server = data["result"]["serverInfo"]["name"]
        print(f"✅ Terhubung ke MCP Server: '{nama_server}' (Protocol v{data['result']['protocolVersion']})")

    def dapatkan_daftar_tools() -> list:
        pass

    def panggil_tool_mcp(self, nama_tool: str, argumen: dict) -> dict:
        print(f"\n--- [MCP CLIENT] Panggil Tool '{nama_tool}' dengan Argumen: {argumen} ---")
        req = json.dumps({
            "jsonrpc": "2.0",
            "id": 10,
            "method": "tools/call",
            "params": {
                "name": nama_tool,
                "arguments": argumen
            }
        })
        res_str = self.server.tangani_request_jsonrpc(req)
        res_json = json.loads(res_str)
        
        teks_hasil = res_json["result"]["content"][0]["text"]
        return json.loads(teks_hasil)


def main():
    print("=========================================================")
    print("DEMO MODUL 10: INTERAKSI MCP CLIENT DENGAN MCP SERVER")
    print("=========================================================")

    # 1. Menyiapkan instance MCP Server
    server = MCPServerSederhana("Local-Product-Server")
    server.mendaftarkan_tool(
        nama="hitung_diskon",
        deskripsi="Hitung diskon",
        arg_schema={},
        handler=tool_hitung_diskon
    )
    server.mendaftarkan_tool(
        nama="info_sistem",
        deskripsi="Ambil info sistem",
        arg_schema={},
        handler=tool_info_sistem
    )

    # 2. Inisialisasi MCP Client
    client = MCPClientDemo(server)
    client.hubungkan_dan_inisialisasi()

    # 3. Client memanggil tool info_sistem via protokol MCP
    hasil_sistem = client.panggil_tool_mcp("info_sistem", {})
    print("Hasil Respon MCP Server (System Info):")
    print(json.dumps(hasil_sistem, indent=2))

    # 4. Client memanggil tool hitung_diskon via protokol MCP
    hasil_diskon = client.panggil_tool_mcp("hitung_diskon", {"harga_awal": 500000, "persen_diskon": 15})
    print("Hasil Respon MCP Server (Kalkulasi Diskon):")
    print(json.dumps(hasil_diskon, indent=2))


if __name__ == "__main__":
    main()
