#!/usr/bin/env python3
"""
01_openai_response_api.py
Modul eksplorasi OpenAI Response API & Tool Calling:
- Standard Request Structure (`/v1/chat/completions`)
- Function Calling Tools Definition (JSON Schema)
- Response Parsing & Error Handling Strategy
"""

import json
from typing import Dict, Any, List

def build_openai_tool_definition() -> List[Dict[str, Any]]:
    """Membangun spesifikasi tool calling untuk OpenAI API."""
    return [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Mengambil harga saham terkini dari bursa efek pasar modal.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Kode saham (contoh: AAPL, NVDA, BBCA)"
                        },
                        "currency": {
                            "type": "string",
                            "enum": ["USD", "IDR"]
                        }
                    },
                    "required": ["ticker"]
                }
            }
        }
    ]

def main():
    print("=" * 65)
    print(" 🛠️ OPENAI RESPONSE API & FUNCTION CALLING SPECIFICATION")
    print("=" * 65)
    
    tools = build_openai_tool_definition()
    print("\n📋 Tools Parameter Definition (JSON Schema):")
    print(json.dumps(tools, indent=2))
    
    mock_llm_tool_call_response = {
        "id": "call_998811",
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "arguments": '{"ticker": "NVDA", "currency": "USD"}'
        }
    }
    
    print("\n🤖 Simulasi Respons Model ketika Memanggil Function Tool:")
    print(json.dumps(mock_llm_tool_call_response, indent=2))
    
    args = json.loads(mock_llm_tool_call_response["function"]["arguments"])
    print(f"\n✅ Peta Hasil Parsing Function: Eksekusi fungsi '{mock_llm_tool_call_response['function']['name']}' dengan argumen ticker={args['ticker']}!")

if __name__ == "__main__":
    main()
