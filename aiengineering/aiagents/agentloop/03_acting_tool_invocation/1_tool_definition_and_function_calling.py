#!/usr/bin/env python3
"""
Modul 3.1: Tool Definition & Function Calling
Demonstrasi bagaimana mendefinisikan tool dengan skema JSON (JSON Schema) dan membangun
Tool Registry yang mampu melakukan pemanggilan fungsi (Function Dispatching) secara dinamis.
"""

import json
from typing import Dict, Any, Callable

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

# Mock Implementasi Fungsi Nyata
def calculator(operation: str, a: float, b: float) -> str:
    if operation == "add":
        return str(a + b)
    elif operation == "multiply":
        return str(a * b)
    elif operation == "divide":
        if b == 0:
            return "Error: Division by zero"
        return str(a / b)
    return "Error: Unknown operation"

def fetch_weather(city: str) -> str:
    mock_weather = {
        "jakarta": "32°C, Cerah Berawan",
        "bandung": "22°C, Hujan Ringan",
        "surabaya": "34°C, Cerah Terik"
    }
    return mock_weather.get(city.lower(), f"Informasi cuaca untuk {city} tidak ditemukan.")

class ToolRegistry:
    def __init__(self):
        self.tools: Dict[str, Dict[str, Any]] = {}
        self.functions: Dict[str, Callable] = {}

    def register_tool(self, name: str, description: str, schema: Dict[str, Any], func: Callable):
        self.tools[name] = {
            "name": name,
            "description": description,
            "parameters": schema
        }
        self.functions[name] = func

    def get_tool_schemas(self) -> list:
        return list(self.tools.values())

    def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> str:
        if tool_name not in self.functions:
            return f"Error: Tool '{tool_name}' tidak terdaftar."
        try:
            return self.functions[tool_name](**arguments)
        except Exception as e:
            return f"Error saat mengeksekusi tool '{tool_name}': {str(e)}"

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 3.1: TOOL DEFINITION & FUNCTION CALLING ==={RESET}\n")

    registry = ToolRegistry()

    # 1. Pendaftaran Tool Calculator
    registry.register_tool(
        name="calculator",
        description="Melakukan operasi matematika dasar (add, multiply, divide)",
        schema={
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "multiply", "divide"]},
                "a": {"type": "number"},
                "b": {"type": "number"}
            },
            "required": ["operation", "a", "b"]
        },
        func=calculator
    )

    # 2. Pendaftaran Tool Weather
    registry.register_tool(
        name="fetch_weather",
        description="Mengambil data cuaca terkini berdasarkan kota",
        schema={
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        },
        func=fetch_weather
    )

    print(f"{BOLD}Daftar Skema Tool (JSON Schemas untuk LLM):{RESET}")
    print(f"{CYAN}{json.dumps(registry.get_tool_schemas(), indent=2)}{RESET}\n")

    print(f"{BOLD}Simulasi Invokasi Tool oleh Agent (Function Calling):{RESET}\n")

    invocations = [
        ("calculator", {"operation": "multiply", "a": 15, "b": 4}),
        ("fetch_weather", {"city": "Bandung"}),
        ("calculator", {"operation": "divide", "a": 10, "b": 0})
    ]

    for tool_name, args in invocations:
        print(f"-> Agent memanggil: {YELLOW}{tool_name}{RESET} dengan argumen {json.dumps(args)}")
        res = registry.execute_tool(tool_name, args)
        if "Error" in res:
            print(f"   {RED}Hasil Observasi: {res}{RESET}")
        else:
            print(f"   {GREEN}Hasil Observasi: {res}{RESET}")
        print("-" * 65)

if __name__ == "__main__":
    main()
