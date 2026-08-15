#!/usr/bin/env python3
"""
Modul: Function Calling (Tools API)
Simulasi deklarasi Tool Schema, Penentuan Tool Call oleh LLM, dan Injeksi Tool Response.
"""

import json

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

# Fungsi Fisik di Backend
def get_stock_price(symbol: str) -> str:
    prices = {"BBCA": "Rp 10.250 (+1.2%)", "TLKM": "Rp 3.850 (-0.5%)", "GOTO": "Rp 68 (0.0%)"}
    return prices.get(symbol.upper(), "Simbol tidak ditemukan")

def main():
    print("=" * 70)
    print(color("  MODUL: FUNCTION CALLING (TOOLS API)", "1;34"))
    print("=" * 70)

    # 1. Deklarasi Tool Schema
    tools_declaration = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Mengambil harga saham terkini berdasarkan kode ticker (e.g. BBCA, TLKM)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "symbol": {"type": "string", "description": "Kode saham ticker Indonesia"}
                    },
                    "required": ["symbol"]
                }
            }
        }
    ]

    print(color("\n1. TOOL DECLARATION SCHEMA TO LLM:", "1;33"))
    print(json.dumps(tools_declaration, indent=2))

    # 2. User Query
    user_query = "Berapa harga saham BBCA hari ini?"
    print(color(f"\n2. USER QUERY: '{user_query}'", "1;33"))

    # 3. Simulated LLM Tool Decision Output
    simulated_llm_tool_call = {
        "id": "call_abc12399",
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "arguments": "{\"symbol\": \"BBCA\"}"
        }
    }
    print(color("\n3. LLM DECISION (TOOL CALL GENERATED):", "1;32"))
    print(json.dumps(simulated_llm_tool_call, indent=2))

    # 4. Backend Execution
    args = json.loads(simulated_llm_tool_call["function"]["arguments"])
    tool_output = get_stock_price(args["symbol"])
    print(color(f"\n4. BACKEND EXECUTION RESULT: {tool_output}", "1;35"))

    # 5. Final LLM Response Synthesis
    final_response = f"Harga saham BBCA saat ini tercatat sebesar {tool_output}."
    print(color(f"\n5. FINAL LLM RESPONSE TO USER: \"{final_response}\"", "1;32"))

    print("\n" + "=" * 70)
    print("✓ Function Calling mengizinkan LLM mengambil data riil dari sistem eksternal tanpa halusinasi.")

if __name__ == "__main__":
    main()
