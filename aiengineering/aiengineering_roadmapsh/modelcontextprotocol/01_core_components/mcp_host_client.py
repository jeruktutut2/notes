#!/usr/bin/env python3
"""
01_core_components/mcp_host_client.py
--------------------------------------
Simulasi Komponen MCP Host dan MCP Client.
Menunjukkan bagaimana MCP Host menginisialisasi MCP Client, mengelola lifecycle koneksi,
dan menangani negosiasi jabat tangan (handshake) JSON-RPC 2.0.
"""

import asyncio
import json
from typing import Dict, Any, List

class MCPMessageLogger:
    """Helper untuk menampilkan log pesan JSON-RPC dengan warna visual."""
    @staticmethod
    def log_send(msg: Dict[str, Any]):
        print(f"\033[94m[CLIENT ---> SERVER]\033[0m {json.dumps(msg, indent=2)}")

    @staticmethod
    def log_receive(msg: Dict[str, Any]):
        print(f"\033[92m[CLIENT <--- SERVER]\033[0m {json.dumps(msg, indent=2)}")


class SimulatedMCPServer:
    """Server MCP Sederhana dalam Memori untuk simulasi handshake & lifecycle."""
    def __init__(self, name: str = "Demo-MCP-Server", version: str = "1.0.0"):
        self.name = name
        self.version = version
        self.initialized = False

    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        msg_id = request.get("id")
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            self.initialized = True
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "resources": {"subscribe": True, "listChanged": True},
                        "prompts": {"listChanged": True},
                        "tools": {"listChanged": True},
                        "logging": {}
                    },
                    "serverInfo": {
                        "name": self.name,
                        "version": self.version
                    }
                }
            }
        elif method == "notifications/initialized":
            # Notification tidak memiliki return result JSON-RPC
            return None
        elif method == "ping":
            return {"jsonrpc": "2.0", "id": msg_id, "result": {}}
        else:
            return {
                "jsonrpc": "2.0",
                "id": msg_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            }


class MCPClient:
    """MCP Client yang mengelola koneksi 1:1 dengan server."""
    def __init__(self, client_name: str = "MCP-Demo-Client", version: str = "1.0.0"):
        self.client_name = client_name
        self.version = version
        self.request_id = 0
        self.is_connected = False
        self.server_info = {}

    def _next_id(self) -> int:
        self.request_id += 1
        return self.request_id

    async def initialize(self, server: SimulatedMCPServer):
        print(f"\n--- [1] MCP Client Initializing Handshake with '{server.name}' ---")
        init_req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "roots": {"listChanged": True},
                    "sampling": {}
                },
                "clientInfo": {
                    "name": self.client_name,
                    "version": self.version
                }
            }
        }
        MCPMessageLogger.log_send(init_req)
        response = await server.handle_request(init_req)
        MCPMessageLogger.log_receive(response)

        if "result" in response:
            self.is_connected = True
            self.server_info = response["result"]["serverInfo"]
            
            # Send notification initialized
            initialized_notif = {
                "jsonrpc": "2.0",
                "method": "notifications/initialized"
            }
            MCPMessageLogger.log_send(initialized_notif)
            await server.handle_request(initialized_notif)
            print("✅ Handshake MCP Selesai! Status Koneksi: TERHUBUNG")

    async def ping(self, server: SimulatedMCPServer):
        print("\n--- [2] Sending Ping Health Check ---")
        ping_req = {
            "jsonrpc": "2.0",
            "id": self._next_id(),
            "method": "ping"
        }
        MCPMessageLogger.log_send(ping_req)
        res = await server.handle_request(ping_req)
        MCPMessageLogger.log_receive(res)


class MCPHost:
    """
    MCP Host adalah aplikasi utama (misal Claude Desktop / IDE).
    Mengatur beberapa MCP Client dan mengintegrasikan konteks ke LLM.
    """
    def __init__(self, host_name: str = "Claude Desktop / Custom AI Agent"):
        self.host_name = host_name
        self.clients: Dict[str, MCPClient] = {}

    async def start(self):
        print(f"==================================================")
        print(f"🚀 Memulai MCP Host App: {self.host_name}")
        print(f"==================================================")
        
        # Inisialisasi Server & Client
        server = SimulatedMCPServer(name="System-Info-Server", version="2.1.0")
        client = MCPClient(client_name=f"{self.host_name}-Client")
        
        # Hubungkan Client ke Server
        await client.initialize(server)
        await client.ping(server)

        print("\n--- [3] Ringkasan Status Host ---")
        print(f"Host App         : {self.host_name}")
        print(f"Connected Server : {client.server_info.get('name')} v{client.server_info.get('version')}")
        print(f"Status           : Connected & Ready for LLM Queries")


if __name__ == "__main__":
    host = MCPHost()
    asyncio.run(host.start())
