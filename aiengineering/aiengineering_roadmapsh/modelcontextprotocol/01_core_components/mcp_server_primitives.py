#!/usr/bin/env python3
"""
01_core_components/mcp_server_primitives.py
--------------------------------------------
Demonstrasi Primitif Data Layer MCP:
1. Resources (URI Read-only Data Sources)
2. Prompts (Reusable Instruction Templates)
3. Tools (Executable Functions with JSON Schema)
"""

import asyncio
import json
from typing import Dict, Any, List


class MCPServerDataPrimitives:
    """Implementasi lengkap 3 primitif data layer MCP pada server."""
    
    def __init__(self):
        # 1. Store Resources
        self.resources = {
            "config://system-metrics": {
                "name": "System Health Metrics",
                "mimeType": "application/json",
                "description": "Metrik performa CPU, Memory, dan Uptime server",
                "content": json.dumps({"cpu_usage": "18.4%", "memory_free": "12.8 GB", "status": "HEALTHY"})
            },
            "file:///logs/access.log": {
                "name": "HTTP Server Access Log",
                "mimeType": "text/plain",
                "description": "Log histori request server HTTP",
                "content": "[2026-07-26 10:00:01] GET /api/v1/users 200 OK\n[2026-07-26 10:05:12] POST /api/v1/login 200 OK"
            }
        }
        
        # 2. Store Prompts
        self.prompts = {
            "analyze_system_logs": {
                "name": "analyze_system_logs",
                "description": "Templat instruksi LLM untuk menganalisis log akses server.",
                "arguments": [
                    {"name": "severity", "description": "Tingkat keparahan anomaly (info/warning/error)", "required": False}
                ]
            },
            "summarize_metrics": {
                "name": "summarize_metrics",
                "description": "Templat instruksi untuk merangkum kesehatan server.",
                "arguments": []
            }
        }

        # 3. Store Tools
        self.tools = {
            "execute_query": {
                "name": "execute_query",
                "description": "Mengeksekusi SQL query sederhana pada database perusahaan.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Query SQL (misal SELECT * FROM users)"},
                        "limit": {"type": "integer", "description": "Batas jumlah baris", "default": 5}
                    },
                    "required": ["query"]
                }
            },
            "restart_service": {
                "name": "restart_service",
                "description": "Merestart layanan microservice tertentu.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "service_name": {"type": "string", "description": "Nama service (auth-service, pay-service)"}
                    },
                    "required": ["service_name"]
                }
            }
        }

    # --- HANDLERS FOR RESOURCES ---
    def list_resources(self) -> List[Dict[str, Any]]:
        return [
            {
                "uri": uri,
                "name": data["name"],
                "mimeType": data["mimeType"],
                "description": data["description"]
            }
            for uri, data in self.resources.items()
        ]

    def read_resource(self, uri: str) -> Dict[str, Any]:
        if uri not in self.resources:
            raise KeyError(f"Resource '{uri}' tidak ditemukan")
        res = self.resources[uri]
        return {
            "contents": [
                {
                    "uri": uri,
                    "mimeType": res["mimeType"],
                    "text": res["content"]
                }
            ]
        }

    # --- HANDLERS FOR PROMPTS ---
    def list_prompts(self) -> List[Dict[str, Any]]:
        return list(self.prompts.values())

    def get_prompt(self, name: str, arguments: Dict[str, Any] = None) -> Dict[str, Any]:
        if name not in self.prompts:
            raise KeyError(f"Prompt '{name}' tidak ditemukan")
        
        args = arguments or {}
        if name == "analyze_system_logs":
            sev = args.get("severity", "all")
            return {
                "description": "Hasil perakitan prompt log analysis",
                "messages": [
                    {
                        "role": "user",
                        "content": {
                            "type": "text",
                            "text": f"Harap analisis log akses sistem untuk tingkat filter '{sev}'. Laporkan bila ada kegagalan otentikasi."
                        }
                    }
                ]
            }
        elif name == "summarize_metrics":
            return {
                "messages": [
                    {
                        "role": "user",
                        "content": {"type": "text", "text": "Berikan ringkasan kesehatan server berdasarkan metrik terkini."}
                    }
                ]
            }

    # --- HANDLERS FOR TOOLS ---
    def list_tools(self) -> List[Dict[str, Any]]:
        return list(self.tools.values())

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self.tools:
            raise KeyError(f"Tool '{name}' tidak ditemukan")
        
        if name == "execute_query":
            q = arguments.get("query", "")
            lim = arguments.get("limit", 5)
            # Simulasi query execution
            mock_data = [
                {"id": 1, "username": "alice", "role": "admin"},
                {"id": 2, "username": "bob", "role": "developer"}
            ][:lim]
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"Eksekusi Query: '{q}' (Limit: {lim})\nHasil:\n{json.dumps(mock_data, indent=2)}"
                    }
                ],
                "isError": False
            }
        elif name == "restart_service":
            svc = arguments.get("service_name")
            return {
                "content": [
                    {
                        "type": "text",
                        "text": f"✅ Service '{svc}' berhasil di-restart pada {asyncio.get_event_loop().time()}!"
                    }
                ],
                "isError": False
            }


async def main():
    print("==================================================")
    print("🛠️ DEMO MCP SERVER DATA PRIMITIVES")
    print("==================================================")
    
    server = MCPServerDataPrimitives()
    
    # 1. Resources
    print("\n--- 📌 [1] DATA LAYER: RESOURCES ---")
    resources_list = server.list_resources()
    print("Daftar Resource Server:")
    print(json.dumps(resources_list, indent=2))
    
    uri_to_read = "config://system-metrics"
    print(f"\nMembaca Resource '{uri_to_read}':")
    read_res = server.read_resource(uri_to_read)
    print(json.dumps(read_res, indent=2))

    # 2. Prompts
    print("\n--- 📌 [2] DATA LAYER: PROMPTS ---")
    prompts_list = server.list_prompts()
    print("Daftar Prompts Server:")
    print(json.dumps(prompts_list, indent=2))
    
    prompt_res = server.get_prompt("analyze_system_logs", {"severity": "warning"})
    print("\nHasil Render Prompt 'analyze_system_logs':")
    print(json.dumps(prompt_res, indent=2))

    # 3. Tools
    print("\n--- 📌 [3] DATA LAYER: TOOLS ---")
    tools_list = server.list_tools()
    print("Daftar Tools Server:")
    print(json.dumps(tools_list, indent=2))
    
    print("\nMemanggil Tool 'execute_query':")
    tool_res = server.call_tool("execute_query", {"query": "SELECT * FROM users WHERE active = true", "limit": 2})
    print(json.dumps(tool_res, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
