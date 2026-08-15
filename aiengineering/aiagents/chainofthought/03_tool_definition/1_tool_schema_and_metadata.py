#!/usr/bin/env python3
"""
SIMULASI MODUL 3.1: Tool Definition - Name, Description, Input & Output Schema
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Visual

Modul ini mendemonstrasikan komponen utama dari Tool Definition:
1. Name & Semantic Description (Memberi tahu LLM kapan tool harus dipanggil)
2. Input Schema (JSON Schema / Dataclass terstruktur untuk parameter)
3. Output Schema (Format respons yang diposisikan kembali ke prompt)
"""

import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, Any, List

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

@dataclass
class ToolDefinition:
    name: str
    description: str
    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]
    category: str

# Sample Standardized Tool Definitions for AI Agents
SAMPLE_TOOLS: List[ToolDefinition] = [
    ToolDefinition(
        name="web_search",
        category="Information Retrieval",
        description="Melakukan pencarian fakta, berita terkini, atau dokumen di internet. Gunakan tool ini jika informasi tidak tersedia dalam knowledge base internal.",
        input_schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Kata kunci pencarian yang spesifik"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Jumlah maksimum hasil pencarian (1 - 10)",
                    "default": 3
                }
            },
            "required": ["query"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "title": {"type": "string"},
                            "url": {"type": "string"},
                            "snippet": {"type": "string"}
                        }
                    }
                }
            }
        }
    ),
    ToolDefinition(
        name="execute_python_code",
        category="Code Execution",
        description="Menjalankan kode Python murni di dalam environment terisolasi (sandbox). Sangat berguna untuk matematika presisi tinggi, pemrosesan teks, dan manipulasi data.",
        input_schema={
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "Skrip Python yang valid yang akan dieksekusi"
                },
                "timeout_seconds": {
                    "type": "integer",
                    "description": "Batas waktu eksekusi skrip dalam detik",
                    "default": 5
                }
            },
            "required": ["code"]
        },
        output_schema={
            "type": "object",
            "properties": {
                "stdout": {"type": "string"},
                "stderr": {"type": "string"},
                "exit_code": {"type": "integer"}
            }
        }
    )
]

def display_tool_definition(tool: ToolDefinition):
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}TOOL DEFINITION: {CYAN}{tool.name}{RESET} [{YELLOW}{tool.category}{RESET}]")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    print(f"{BOLD}1. Name & Semantic Description:{RESET}")
    print(f"   Name        : {BOLD}{tool.name}{RESET}")
    print(f"   Description : {tool.description}\n")
    
    print(f"{BOLD}2. Input Schema (JSON Schema):{RESET}")
    print(f"{GREEN}{json.dumps(tool.input_schema, indent=6)}{RESET}\n")
    
    print(f"{BOLD}3. Output Schema (Expected Structure):{RESET}")
    print(f"{CYAN}{json.dumps(tool.output_schema, indent=6)}{RESET}")

def main():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}      SIMULASI TOOL DEFINITION (NAME, DESCRIPTION, INPUT/OUTPUT SCHEMA) {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    
    for tool in SAMPLE_TOOLS:
        display_tool_definition(tool)
        time.sleep(0.3)
        input(f"\n{YELLOW}Tekan [Enter] untuk melihat Tool Definition berikutnya...{RESET}")

if __name__ == "__main__":
    main()
