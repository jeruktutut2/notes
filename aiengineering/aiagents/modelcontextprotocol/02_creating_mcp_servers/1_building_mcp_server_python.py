#!/usr/bin/env python3
"""
Modul 02: Creating MCP Servers - Part 1: Building MCP Server in Python (SDK Pattern)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & FastMCP / Anthropic MCP SDK Pattern

Skrip ini mendemonstrasikan:
1. Pembuatan Server MCP mandiri menggunakan pola dekorator SDK (`@mcp.tool`, `@mcp.resource`, `@mcp.prompt`).
2. Generasi skema JSON otomatis dari argumen fungsi Python.
3. Penanganan error (validation, exception capture, isError flag).
4. Lifecycle server (Init -> Register -> Dispatcher).
"""

import json
import inspect
from typing import Dict, Any, Callable, List

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"


class FastMCPServerSDK:
    """
    Simulasi FastMCP SDK (Python SDK untuk MCP).
    Menyediakan dekorator elegan `@server.tool()`, `@server.resource()`, dan `@server.prompt()`.
    """
    def __init__(self, name: str):
        self.name = name
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._resources: Dict[str, Dict[str, Any]] = {}
        self._prompts: Dict[str, Dict[str, Any]] = {}

    def tool(self, name: str = None, description: str = None):
        """Dekorator untuk mendaftarkan fungsi Python sebagai MCP Tool."""
        def decorator(func: Callable):
            tool_name = name or func.__name__
            tool_desc = description or (func.__doc__.strip() if func.__doc__ else "Tidak ada deskripsi.")
            
            # Extract parameters for inputSchema simulation
            sig = inspect.signature(func)
            properties = {}
            required = []
            for param_name, param in sig.parameters.items():
                param_type = "string"
                if param.annotation == int or param.annotation == float:
                    param_type = "number"
                elif param.annotation == bool:
                    param_type = "boolean"
                
                properties[param_name] = {"type": param_type}
                if param.default == inspect.Parameter.empty:
                    required.append(param_name)

            self._tools[tool_name] = {
                "description": tool_desc,
                "inputSchema": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                },
                "func": func
            }
            return func
        return decorator

    def resource(self, uri: str, name: str = None, mime_type: str = "text/plain"):
        """Dekorator untuk mendaftarkan Resource data read-only berbasis URI."""
        def decorator(func: Callable):
            res_name = name or func.__name__
            self._resources[uri] = {
                "name": res_name,
                "mimeType": mime_type,
                "func": func
            }
            return func
        return decorator

    def prompt(self, name: str = None, description: str = None):
        """Dekorator untuk mendaftarkan Template Prompt Reusable."""
        def decorator(func: Callable):
            p_name = name or func.__name__
            p_desc = description or (func.__doc__.strip() if func.__doc__ else "")
            self._prompts[p_name] = {
                "description": p_desc,
                "func": func
            }
            return func
        return decorator

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        if name not in self._tools:
            return {"isError": True, "content": f"Tool '{name}' tidak ditemukan."}
        try:
            func = self._tools[name]["func"]
            res = func(**arguments)
            return {"isError": False, "content": str(res)}
        except Exception as e:
            return {"isError": True, "content": f"Execution Error: {str(e)}"}

    def read_resource(self, uri: str) -> Dict[str, Any]:
        if uri not in self._resources:
            return {"isError": True, "content": f"Resource URI '{uri}' tidak ditemukan."}
        try:
            func = self._resources[uri]["func"]
            res = func()
            return {
                "uri": uri,
                "mimeType": self._resources[uri]["mimeType"],
                "text": str(res)
            }
        except Exception as e:
            return {"isError": True, "content": f"Read Resource Error: {str(e)}"}


# ---------------------------------------------------------
# PEMBUATAN SERVER DENGAN DEKORATOR FastMCP
# ---------------------------------------------------------
mcp = FastMCPServerSDK("Financial & Dev Tools Server")


@mcp.tool(description="Menghitung bunga majemuk (Compound Interest).")
def compound_interest(principal: float, rate: float, years: int) -> float:
    """Hitung A = P * (1 + r)^t"""
    return round(principal * ((1 + rate) ** years), 2)


@mcp.tool(description="Format teks ke slug URL ramah SEO.")
def generate_slug(text: str) -> str:
    return text.lower().replace(" ", "-").replace("/", "-")


@mcp.resource(uri="system://env/version", name="Environment Python Version", mime_type="text/plain")
def get_sys_version():
    return "Python 3.11.5 (GCC 11.2.0, 64 bit x86_64)"


@mcp.prompt(name="code_optimizer", description="Prompt pengoptimalan performa algoritma.")
def code_optimizer_prompt(code_snippet: str) -> str:
    return f"Optimalkan kompleksitas waktu (Big O) dan memori dari kode berikut:\n\n```\n{code_snippet}\n```"


def main():
    print("=" * 70)
    print(f"{BOLD}{HEADER}CREATING MCP SERVERS: BUILDING MCP SERVER IN PYTHON (SDK PATTERN){RESET}")
    print("Berdasarkan spesifikasi standar FastMCP / Model Context Protocol")
    print("=" * 70)

    # 1. Menampilkan daftar tools yang telah terdaftar secara otomatis
    print(f"\n{BOLD}{CYAN}--- 1. DAFTAR TOOLS TERDAFTAR SECARA OTOMATIS VIA SDK ---{RESET}")
    for tool_name, info in mcp._tools.items():
        print(f"  🛠️  {BOLD}{tool_name}{RESET}: {info['description']}")
        print(f"      Schema: {json.dumps(info['inputSchema']['properties'])}")

    # 2. Menguji Eksekusi Tool
    print(f"\n{BOLD}{CYAN}--- 2. EKSEKUSI TOOL 'compound_interest' ---{RESET}")
    result_tool = mcp.call_tool("compound_interest", {"principal": 10000000.0, "rate": 0.08, "years": 5})
    print(f"  {GREEN}Status Error : {result_tool['isError']}{RESET}")
    print(f"  {GREEN}Hasil Result : Rp {float(result_tool['content']):,.2f}{RESET}")

    # 3. Menguji Eksekusi Tool dengan Slug Generator
    print(f"\n{BOLD}{CYAN}--- 3. EKSEKUSI TOOL 'generate_slug' ---{RESET}")
    res_slug = mcp.call_tool("generate_slug", {"text": "Model Context Protocol Roadmap 2026"})
    print(f"  {GREEN}Hasil Slug   : {res_slug['content']}{RESET}")

    # 4. Membaca Resource URI
    print(f"\n{BOLD}{CYAN}--- 4. PEMBACAAN RESOURCE 'system://env/version' ---{RESET}")
    res_res = mcp.read_resource("system://env/version")
    print(f"  {GREEN}Resource Content : {res_res['text']}{RESET}")

    print("\n" + "=" * 70)
    print(f"{GREEN}✓ Pembuatan MCP Server dengan SDK Python Berhasil!{RESET}")
    print("=" * 70)


if __name__ == "__main__":
    main()
