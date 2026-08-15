#!/usr/bin/env python3
"""
Modul 01: Core Components - Part 2: MCP Servers & Primitives (Tools, Resources, Prompts)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Model Context Protocol Specification

Skrip ini mendemonstrasikan:
1. Struktur internal MCP Server.
2. Tiga Primitif Utama MCP:
   - Tools: Fungsi eksekusi (Aksi).
   - Resources: Data read-only berbasis URI.
   - Prompts: Template prompt dinamis.
3. Alur eksekusi `tools/call`, pembacaan `resources/read`, dan pengambilan `prompts/get`.
"""

import json
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


class FullFeaturedMCPServer:
    """
    [ MCP Server ]
    Server serbaguna yang menyediakan 3 Primitif Utama MCP:
    1. Tools (Aksi eksekusi)
    2. Resources (Membaca file/data pasif)
    3. Prompts (Template instruksi reusable)
    """
    def __init__(self, server_name: str = "EnterpriseContextServer"):
        self.server_name = server_name
        self.version = "1.0.0"
        
        # 1. Pendaftaran Primitif: TOOLS
        self.tools = {
            "calculate_tax": {
                "description": "Menghitung pajak penghasilan berdasarkan tarif acuan.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "amount": {"type": "number", "description": "Jumlah pendapatan"},
                        "rate": {"type": "number", "description": "Persentase tarif (e.g. 0.11)"}
                    },
                    "required": ["amount", "rate"]
                },
                "handler": self._tool_calculate_tax
            },
            "system_health_check": {
                "description": "Memeriksa status CPU, RAM, dan storage server.",
                "inputSchema": {"type": "object", "properties": {}},
                "handler": self._tool_health_check
            }
        }
        
        # 2. Pendaftaran Primitif: RESOURCES
        self.resources = {
            "system://logs/app.log": {
                "name": "System Application Logs",
                "mimeType": "text/plain",
                "content": "[2026-07-26 10:00:01] INFO: App initialized.\n[2026-07-26 10:05:22] WARN: Memory usage high.\n[2026-07-26 10:12:00] ERROR: Connection timeout to DB."
            },
            "config://database/settings": {
                "name": "Database Configuration JSON",
                "mimeType": "application/json",
                "content": json.dumps({"host": "db.production.internal", "port": 5432, "max_connections": 100}, indent=2)
            }
        }
        
        # 3. Pendaftaran Primitif: PROMPTS
        self.prompts = {
            "code_review_prompt": {
                "description": "Template untuk meninjau kualitas kode Python.",
                "arguments": [
                    {"name": "language", "description": "Bahasa pemograman", "required": True},
                    {"name": "strictness", "description": "Tingkat ketat review (low/high)", "required": False}
                ],
                "handler": self._prompt_code_review
            }
        }

    # Handler Implementasi Tools
    def _tool_calculate_tax(self, args: Dict[str, Any]) -> str:
        amount = args.get("amount", 0)
        rate = args.get("rate", 0.0)
        tax = amount * rate
        return f"Perhitungan Pajak: Rp {tax:,.2f} (Total: Rp {amount:,.2f}, Tarif: {rate*100}%)"

    def _tool_health_check(self, args: Dict[str, Any]) -> str:
        return "System Health Status: OK (CPU: 12%, RAM Usage: 45%, Disk Free: 120 GB)"

    # Handler Implementasi Prompts
    def _prompt_code_review(self, args: Dict[str, Any]) -> str:
        lang = args.get("language", "Python")
        strict = args.get("strictness", "high")
        return (
            f"Anda adalah Senior Code Reviewer berpengalaman. Tinjau kode {lang} berikut dengan "
            f"tingkat ketelitian '{strict}'. Fokus pada: Security vulnerabilities, Memory efficiency, dan Type hints."
        )

    # Dispatcher Pesan JSON-RPC 2.0
    def handle_jsonrpc_request(self, raw_json: str) -> str:
        req = json.loads(raw_json)
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        print(f"\n{YELLOW}[MCP Server] Menerima Request JSON-RPC Method: '{method}' (ID: {req_id}){RESET}")

        # Dispatcher Method Protocol
        if method == "tools/list":
            tool_list = [
                {"name": name, "description": data["description"], "inputSchema": data["inputSchema"]}
                for name, data in self.tools.items()
            ]
            response = {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tool_list}}

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            
            if tool_name in self.tools:
                try:
                    result_text = self.tools[tool_name]["handler"](tool_args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": result_text}],
                            "isError": False
                        }
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [{"type": "text", "text": f"Error executing tool: {str(e)}"}],
                            "isError": True
                        }
                    }
            else:
                response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Tool '{tool_name}' not found"}}

        elif method == "resources/list":
            res_list = [
                {"uri": uri, "name": data["name"], "mimeType": data["mimeType"]}
                for uri, data in self.resources.items()
            ]
            response = {"jsonrpc": "2.0", "id": req_id, "result": {"resources": res_list}}

        elif method == "resources/read":
            uri = params.get("uri")
            if uri in self.resources:
                res_data = self.resources[uri]
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "contents": [
                            {
                                "uri": uri,
                                "mimeType": res_data["mimeType"],
                                "text": res_data["content"]
                            }
                        ]
                    }
                }
            else:
                response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": f"Resource URI '{uri}' not found"}}

        elif method == "prompts/list":
            prompt_list = [
                {"name": name, "description": data["description"], "arguments": data["arguments"]}
                for name, data in self.prompts.items()
            ]
            response = {"jsonrpc": "2.0", "id": req_id, "result": {"prompts": prompt_list}}

        elif method == "prompts/get":
            prompt_name = params.get("name")
            prompt_args = params.get("arguments", {})
            if prompt_name in self.prompts:
                prompt_text = self.prompts[prompt_name]["handler"](prompt_args)
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "description": self.prompts[prompt_name]["description"],
                        "messages": [
                            {
                                "role": "user",
                                "content": {"type": "text", "text": prompt_text}
                            }
                        ]
                    }
                }
            else:
                response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32602, "message": f"Prompt '{prompt_name}' not found"}}

        else:
            response = {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Unknown method '{method}'"}}

        return json.dumps(response, indent=2)


def main():
    print("=" * 70)
    print(f"{BOLD}{HEADER}SIMULASI MCP PRIMITIVES: TOOLS, RESOURCES, & PROMPTS{RESET}")
    print("Berdasarkan spesifikasi standar Model Context Protocol")
    print("=" * 70)

    server = FullFeaturedMCPServer()

    # ---------------------------------------------------------
    # DEMO 1: PRIMITIF TOOLS (`tools/list` & `tools/call`)
    # ---------------------------------------------------------
    print(f"\n{BOLD}{CYAN}--- 1. UJI PRIMITIF TOOLS (Fungsi Eksekusi / Aksi) ---{RESET}")
    req_call_tool = {
        "jsonrpc": "2.0",
        "id": 101,
        "method": "tools/call",
        "params": {
            "name": "calculate_tax",
            "arguments": {"amount": 25000000, "rate": 0.11}
        }
    }
    raw_res = server.handle_jsonrpc_request(json.dumps(req_call_tool))
    res = json.loads(raw_res)
    print(f"  {GREEN}Hasil Eksekusi Tool:{RESET}")
    print(f"  --> {res['result']['content'][0]['text']}")

    # ---------------------------------------------------------
    # DEMO 2: PRIMITIF RESOURCES (`resources/read`)
    # ---------------------------------------------------------
    print(f"\n{BOLD}{CYAN}--- 2. UJI PRIMITIF RESOURCES (Read-Only Data Pasif) ---{RESET}")
    req_read_resource = {
        "jsonrpc": "2.0",
        "id": 102,
        "method": "resources/read",
        "params": {"uri": "system://logs/app.log"}
    }
    raw_res = server.handle_jsonrpc_request(json.dumps(req_read_resource))
    res = json.loads(raw_res)
    print(f"  {GREEN}Isi Content Resource (`system://logs/app.log`):{RESET}")
    content = res['result']['contents'][0]['text']
    for line in content.split('\n'):
        print(f"      {line}")

    # ---------------------------------------------------------
    # DEMO 3: PRIMITIF PROMPTS (`prompts/get`)
    # ---------------------------------------------------------
    print(f"\n{BOLD}{CYAN}--- 3. UJI PRIMITIF PROMPTS (Template Prompt Reusable) ---{RESET}")
    req_get_prompt = {
        "jsonrpc": "2.0",
        "id": 103,
        "method": "prompts/get",
        "params": {
            "name": "code_review_prompt",
            "arguments": {"language": "Python 3.11", "strictness": "very high"}
        }
    }
    raw_res = server.handle_jsonrpc_request(json.dumps(req_get_prompt))
    res = json.loads(raw_res)
    print(f"  {GREEN}Hasil Prompt Template Generator:{RESET}")
    prompt_msg = res['result']['messages'][0]['content']['text']
    print(f"  --> \"{prompt_msg}\"")

    print("\n" + "=" * 70)
    print(f"{GREEN}✓ Simulasi MCP Primitives (Tools, Resources, Prompts) Selesai!{RESET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
