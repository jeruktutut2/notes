#!/usr/bin/env python3
"""
02_developing_with_mcp/building_mcp_server.py
----------------------------------------------
Panduan & Skrip Lengkap Membangun MCP Server.
Mengimplementasikan MCP Server mandiri yang mengekspos:
- File System & DB Resources
- Refactoring & Review Prompts
- File & Math Calculation Tools
"""

import asyncio
import json
import os
import sys
from typing import Dict, Any, List

class CompleteMCPServer:
    """Implementasi MCP Server Produksi Siap Pakai."""
    
    def __init__(self, server_name: str = "Dev-Toolkit-Server", version: str = "1.0.0"):
        self.server_name = server_name
        self.version = version
        self.running = False
        
        # Internal Storage / State
        self.files_db = {
            "notes://readme.md": "# Project Roadmap\n1. Integrasi MCP Server\n2. Bangun AI Agent Client\n3. Deploy ke Cloud.",
            "notes://env_config.json": '{"APP_ENV": "development", "PORT": 8080}'
        }

    def process_jsonrpc(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Engine utama pengolahan protokol JSON-RPC 2.0."""
        msg_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "resources": {"listChanged": True},
                        "prompts": {"listChanged": True},
                        "tools": {"listChanged": True}
                    },
                    "serverInfo": {"name": self.server_name, "version": self.version}
                }
            }
        
        elif method == "notifications/initialized":
            return None

        # --- RESOURCES HANDLERS ---
        elif method == "resources/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "resources": [
                        {"uri": uri, "name": uri.split("//")[-1], "mimeType": "text/plain"}
                        for uri in self.files_db.keys()
                    ]
                }
            }
            
        elif method == "resources/read":
            uri = params.get("uri")
            if uri in self.files_db:
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "contents": [{"uri": uri, "mimeType": "text/plain", "text": self.files_db[uri]}]
                    }
                }
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32602, "message": f"Resource URI '{uri}' not found"}
            }

        # --- PROMPTS HANDLERS ---
        elif method == "prompts/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "prompts": [
                        {
                            "name": "code_review",
                            "description": "Membuat panduan review kode AI",
                            "arguments": [{"name": "language", "required": True}]
                        }
                    ]
                }
            }

        elif method == "prompts/get":
            p_name = params.get("name")
            args = params.get("arguments", {})
            lang = args.get("language", "python")
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "description": f"Prompt review kode untuk bahasa {lang}",
                    "messages": [
                        {
                            "role": "user",
                            "content": {"type": "text", "text": f"Lakukan code review berstandar tinggi untuk kode {lang} berikut."}
                        }
                    ]
                }
            }

        # --- TOOLS HANDLERS ---
        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "tools": [
                        {
                            "name": "calculate_expr",
                            "description": "Menghitung ekspresi matematika aman",
                            "inputSchema": {
                                "type": "object",
                                "properties": {"expression": {"type": "string"}},
                                "required": ["expression"]
                            }
                        },
                        {
                            "name": "write_note",
                            "description": "Menulis catatan baru ke database resource server",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "uri": {"type": "string"},
                                    "content": {"type": "string"}
                                },
                                "required": ["uri", "content"]
                            }
                        }
                    ]
                }
            }

        elif method == "tools/call":
            t_name = params.get("name")
            t_args = params.get("arguments", {})

            if t_name == "calculate_expr":
                expr = t_args.get("expression", "")
                try:
                    # Menghitung ekspresi matematika
                    res = eval(expr, {"__builtins__": None}, {})
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": f"Hasil Kalkulasi ({expr}) = {res}"}],
                            "isError": False
                        }
                    }
                except Exception as e:
                    return {
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "content": [{"type": "text", "text": f"Gagal menghitung: {str(e)}"}],
                            "isError": True
                        }
                    }
            elif t_name == "write_note":
                uri = t_args.get("uri")
                cnt = t_args.get("content")
                self.files_db[uri] = cnt
                return {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "content": [{"type": "text", "text": f"Catatan berhasil disimpan ke Resource URI: {uri}"}],
                        "isError": False
                    }
                }

        return {
            "jsonrpc": "2.0",
            "id": msg_id,
            "error": {"code": -32601, "message": f"Method '{method}' not implemented"}
        }


def main():
    print("==================================================")
    print("🏗️ BUILDING AN MCP SERVER (Standalone Demo)")
    print("==================================================")

    server = CompleteMCPServer()
    
    # Uji coba beberapa request JSON-RPC
    test_requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"clientInfo": {"name": "TestClient"}}},
        {"jsonrpc": "2.0", "id": 2, "method": "resources/list"},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/list"},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "calculate_expr", "arguments": {"expression": "25 * 4 + 50"}}},
        {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "write_note", "arguments": {"uri": "notes://todo.txt", "content": "Beli server baru"}}},
        {"jsonrpc": "2.0", "id": 6, "method": "resources/list"}
    ]

    for req in test_requests:
        print(f"\n➔ Request Method: \033[93m{req['method']}\033[0m")
        res = server.process_jsonrpc(req)
        print(json.dumps(res, indent=2))

if __name__ == "__main__":
    main()
