#!/usr/bin/env python3
"""
02_developing_with_mcp/connect_local_server.py
-----------------------------------------------
Panduan & Skrip Menghubungkan MCP Client ke Local MCP Server via Subprocess (stdio transport).
Menyediakan simulasi subprocess stdin/stdout framing.
"""

import asyncio
import json
import subprocess
import sys
import os

class LocalServerConnection:
    """Mengelola koneksi lokal via Subprocess Stdio."""
    
    def __init__(self, command: str, args: list):
        self.command = command
        self.args = args
        self.process = None

    async def connect_and_exchange(self):
        print("==================================================")
        print("💻 CONNECT TO LOCAL MCP SERVER (STDIO IPC)")
        print("==================================================")
        print(f"Perintah Peluncuran Local Server: {self.command} {' '.join(self.args)}")
        
        # Simulasi konfigurasi claude_desktop_config.json
        config_example = {
            "mcpServers": {
                "local-dev-tools": {
                    "command": self.command,
                    "args": self.args,
                    "env": {"PYTHONUNBUFFERED": "1"}
                }
            }
        }
        print("\n--- 📋 Konfigurasi MCP Host (claude_desktop_config.json) ---")
        print(json.dumps(config_example, indent=2))

        print("\n--- 🔌 Membuka Subprocess Pipe (stdin/stdout) ---")
        print("1. Host meluncurkan subprocess MCP Server.")
        print("2. Stdio Pipe siap mentransmisikan frame JSON-RPC 2.0 per baris.")
        print("3. Mengirim payload inisialisasi...")

        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"clientInfo": {"name": "LocalHostApp", "version": "1.0"}}
        }
        
        frame = json.dumps(req) + "\n"
        print(f"\n[STDIN OUTBOUND]: {frame.strip()}")
        
        # Simulasi tanggapan instant
        response_frame = json.dumps({
            "jsonrpc": "2.0",
            "id": 1,
            "result": {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": "Local-Subprocess-Server", "version": "1.0.0"}
            }
        })
        print(f"[STDOUT INBOUND] : {response_frame}")
        print("\n✅ Koneksi ke Local Server via Stdio Berhasil & Terkonfirmasi!")

if __name__ == "__main__":
    conn = LocalServerConnection("python3", ["building_mcp_server.py"])
    asyncio.run(conn.connect_and_exchange())
