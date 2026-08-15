#!/usr/bin/env python3
"""
02_developing_with_mcp/building_mcp_client.py
----------------------------------------------
Panduan & Skrip Lengkap Membangun MCP Client.
Mengimplementasikan Client yang mampu:
- Melakukan Discovery Kapabilitas (Resources, Prompts, Tools)
- Membaca Resource & Membuka Prompt
- Eksekusi Tool dan Penanganan Error
"""

import asyncio
import json
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from building_mcp_server import CompleteMCPServer

class MCPClientAgent:
    """Client MCP yang disimulasikan sebagai AI Agent Controller."""

    def __init__(self, agent_name: str = "AI-Developer-Agent"):
        self.agent_name = agent_name
        self.msg_id = 0

    def _get_id(self) -> int:
        self.msg_id += 1
        return self.msg_id

    async def run_discovery_flow(self, server: CompleteMCPServer):
        print("==================================================")
        print(f"🤖 BUILDING AN MCP CLIENT - AGENT: {self.agent_name}")
        print("==================================================")

        # 1. Inisialisasi Handshake
        print("\nStep 1: Melakukan Inisialisasi Jabat Tangan...")
        init_req = {
            "jsonrpc": "2.0",
            "id": self._get_id(),
            "method": "initialize",
            "params": {"clientInfo": {"name": self.agent_name, "version": "1.0.0"}}
        }
        res_init = server.process_jsonrpc(init_req)
        print(f"✅ Handshake Berhasil! Server Info: {res_init['result']['serverInfo']}")

        # 2. Discover Tools
        print("\nStep 2: Menemukan Tools Server...")
        tools_req = {"jsonrpc": "2.0", "id": self._get_id(), "method": "tools/list"}
        res_tools = server.process_jsonrpc(tools_req)
        available_tools = res_tools["result"]["tools"]
        print(f"Tool Ditemukan ({len(available_tools)}): {[t['name'] for t in available_tools]}")

        # 3. Discover Resources
        print("\nStep 3: Menemukan Resources Data Server...")
        res_req = {"jsonrpc": "2.0", "id": self._get_id(), "method": "resources/list"}
        res_resources = server.process_jsonrpc(res_req)
        available_res = res_resources["result"]["resources"]
        print(f"Resource Ditemukan ({len(available_res)}): {[r['uri'] for r in available_res]}")

        # 4. Membaca Salah Satu Resource
        target_uri = "notes://readme.md"
        print(f"\nStep 4: Membaca Konten Resource '{target_uri}'...")
        read_req = {"jsonrpc": "2.0", "id": self._get_id(), "method": "resources/read", "params": {"uri": target_uri}}
        read_res = server.process_jsonrpc(read_req)
        content_text = read_res["result"]["contents"][0]["text"]
        print(f"Isi File Resource:\n---\n{content_text}\n---")

        # 5. Memanggil Tool Kalkulasi
        print("\nStep 5: Mengeksekusi Tool 'calculate_expr'...")
        call_req = {
            "jsonrpc": "2.0",
            "id": self._get_id(),
            "method": "tools/call",
            "params": {
                "name": "calculate_expr",
                "arguments": {"expression": "(100 * 5) / 2 + 75"}
            }
        }
        tool_res = server.process_jsonrpc(call_req)
        print(f"Hasil Eksekusi Tool: {tool_res['result']['content'][0]['text']}")

if __name__ == "__main__":
    server = CompleteMCPServer()
    client = MCPClientAgent()
    asyncio.run(client.run_discovery_flow(server))
