#!/usr/bin/env python3
"""
Modul 01: Core Components - Part 1: MCP Hosts & MCP Client Simulation
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Model Context Protocol Specification

Skrip ini mendemonstrasikan:
1. Peran MCP Host (Aplikasi Utama AI yang mengelola UI & LLM Orchestration).
2. Peran MCP Client (Komponen internal pengelola protokol & koneksi 1:1).
3. Inisialisasi Koneksi Handshake & Negosiasi Kapabilitas (Capabilities Exchange).
4. Pencarian (Discovery) Tool, Resource, dan Prompt dari Server oleh Client.
"""

import json
import time
from typing import Dict, Any, List

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


class SimulatedMCPServerProcess:
    """Simulasi MCP Server sederhana yang berjalan sebagai proses terpisah."""
    def __init__(self, name: str, version: str):
        self.name = name
        self.version = version
        
    def handle_request(self, request_json: str) -> str:
        req = json.loads(request_json)
        req_id = req.get("id")
        method = req.get("method")
        
        if method == "initialize":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": True},
                        "resources": {"subscribe": True, "listChanged": True},
                        "prompts": {"listChanged": True}
                    },
                    "serverInfo": {
                        "name": self.name,
                        "version": self.version
                    }
                }
            }
        elif method == "tools/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": [
                        {
                            "name": "get_weather",
                            "description": "Mendapatkan data cuaca terkini untuk kota tertentu",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "city": {"type": "string", "description": "Nama kota"}
                                },
                                "required": ["city"]
                            }
                        },
                        {
                            "name": "query_database",
                            "description": "Menjalankan query database read-only",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "sql": {"type": "string", "description": "Query SQL"}
                                },
                                "required": ["sql"]
                            }
                        }
                    ]
                }
            }
        elif method == "resources/list":
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "resources": [
                        {
                            "uri": "file:///logs/system.log",
                            "name": "System Access Log",
                            "mimeType": "text/plain"
                        },
                        {
                            "uri": "db://analytics/daily_metrics",
                            "name": "Daily Metrics Table",
                            "mimeType": "application/json"
                        }
                    ]
                }
            }
        else:
            res = {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method '{method}' not found"
                }
            }
        return json.dumps(res, indent=2)


class MCPClient:
    """
    [ MCP Client ]
    Komponen protokol internal yang memelihara hubungan 1-ke-1 dengan Server MCP.
    Bertanggung jawab melakukan marshalling JSON-RPC 2.0 dan negosiasi kapabilitas.
    """
    def __init__(self, client_name: str = "AntigravityMCPClient", version: str = "1.0.0"):
        self.client_name = client_name
        self.version = version
        self.request_counter = 0
        self.server_process: SimulatedMCPServerProcess = None
        self.server_info: Dict[str, Any] = {}
        self.negotiated_capabilities: Dict[str, Any] = {}
        self.is_connected = False

    def connect(self, server_process: SimulatedMCPServerProcess):
        print(f"{CYAN}[MCP Client] Membuka channel koneksi dengan Server: '{server_process.name}'...{RESET}")
        self.server_process = server_process
        
        # 1. Inisialisasi Handshake
        self.request_counter += 1
        init_request = {
            "jsonrpc": "2.0",
            "id": self.request_counter,
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
        
        print(f"  {YELLOW}--> Send Request [initialize]{RESET}")
        raw_response = self.server_process.handle_request(json.dumps(init_request))
        response = json.loads(raw_response)
        
        if "result" in response:
            res = response["result"]
            self.server_info = res["serverInfo"]
            self.negotiated_capabilities = res["capabilities"]
            self.is_connected = True
            print(f"  {GREEN}<-- Received Handshake Response!{RESET}")
            print(f"      Connected Server : {BOLD}{self.server_info['name']} (v{self.server_info['version']}){RESET}")
            print(f"      Protocol Version : {res['protocolVersion']}")
            print(f"      Server Caps      : {list(self.negotiated_capabilities.keys())}")
        else:
            print(f"  {RED}Handshake gagal: {response.get('error')}{RESET}")

    def discover_tools(self) -> List[Dict[str, Any]]:
        if not self.is_connected:
            raise RuntimeError("Client belum terhubung ke Server MCP!")
            
        self.request_counter += 1
        req = {
            "jsonrpc": "2.0",
            "id": self.request_counter,
            "method": "tools/list"
        }
        print(f"\n{CYAN}[MCP Client] Meminta daftar Tools (`tools/list`)...{RESET}")
        raw_response = self.server_process.handle_request(json.dumps(req))
        res = json.loads(raw_response)
        tools = res.get("result", {}).get("tools", [])
        print(f"  {GREEN}Ditemukan {len(tools)} tools dari server MCP.{RESET}")
        return tools

    def discover_resources(self) -> List[Dict[str, Any]]:
        if not self.is_connected:
            raise RuntimeError("Client belum terhubung ke Server MCP!")
            
        self.request_counter += 1
        req = {
            "jsonrpc": "2.0",
            "id": self.request_counter,
            "method": "resources/list"
        }
        print(f"\n{CYAN}[MCP Client] Meminta daftar Resources (`resources/list`)...{RESET}")
        raw_response = self.server_process.handle_request(json.dumps(req))
        res = json.loads(raw_response)
        resources = res.get("result", {}).get("resources", [])
        print(f"  {GREEN}Ditemukan {len(resources)} resources dari server MCP.{RESET}")
        return resources


class MCPHost:
    """
    [ MCP Host ]
    Aplikasi AI utama (seperti Claude Desktop / IDE Extension) yang mengorkestrasikan
    pengguna, LLM model, dan menghubungkan satu atau banyak MCP Client.
    """
    def __init__(self, host_name: str = "Claude Desktop / Antigravity IDE"):
        self.host_name = host_name
        self.clients: Dict[str, MCPClient] = {}

    def register_and_connect_server(self, server_name: str, server_process: SimulatedMCPServerProcess):
        print(f"\n{HEADER}=== [MCP Host] Mendaftarkan Server Baru: '{server_name}' ==={RESET}")
        client = MCPClient(client_name=f"{self.host_name}_Client")
        client.connect(server_process)
        self.clients[server_name] = client

    def inspect_system_context(self):
        print(f"\n{BOLD}{HEADER}=== [MCP Host] Rangkuman Kapabilitas Terkoneksi ==={RESET}")
        for server_name, client in self.clients.items():
            print(f"\n{BOLD}📡 Server: {server_name}{RESET}")
            tools = client.discover_tools()
            for t in tools:
                print(f"   🛠️  Tool: {BOLD}{t['name']}{RESET} -> {t['description']}")
            
            resources = client.discover_resources()
            for r in resources:
                print(f"   📄 Resource: {BOLD}{r['uri']}{RESET} ({r['name']})")


def main():
    print("=" * 70)
    print(f"{BOLD}{HEADER}SIMULASI MCP CORE COMPONENTS: MCP HOST & MCP CLIENT{RESET}")
    print("Berdasarkan spesifikasi standar Model Context Protocol (Anthropic/Roadmap.sh)")
    print("=" * 70)

    # 1. Inisialisasi MCP Host Application
    host = MCPHost(host_name="Claude Desktop Simulator")
    
    # 2. Inisialisasi Simulasi MCP Servers
    analytics_server = SimulatedMCPServerProcess(name="Analytics & Database Server", version="2.1.0")
    
    # 3. Host menghubungkan MCP Client ke Server
    host.register_and_connect_server("AnalyticsServer", analytics_server)
    
    # 4. Host mengeksplorasi konteks & kapabilitas yang tersedia
    host.inspect_system_context()

    print("\n" + "=" * 70)
    print(f"{GREEN}✓ Simulasi MCP Host & Client Berhasil Selesai!{RESET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
