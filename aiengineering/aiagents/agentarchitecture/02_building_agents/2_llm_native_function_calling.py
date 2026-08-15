#!/usr/bin/env python3
"""
Modul 02: Building Agents - Part 2
Simulasi LLM Native Function Calling across major providers:
- OpenAI Function Calling
- OpenAI Assistant API (Threads & Runs pattern)
- Gemini Function Calling (Google GenAI)
- Anthropic Tool Use (Messages API)
"""

import json
from typing import Dict, Any, List

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================================
# 1. OPENAI FUNCTION CALLING SCHEMA & SIMULATION
# ============================================================================
def demo_openai_function_calling():
    print(f"\n{BOLD}{CYAN}=== 1. OPENAI FUNCTION CALLING ==={RESET}")
    
    # Skema Definisi Tool (JSON Schema Standard)
    tools_schema = [
        {
            "type": "function",
            "function": {
                "name": "get_stock_price",
                "description": "Mendapatkan harga saham terkini berdasarkan ticker simbol.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ticker": {
                            "type": "string",
                            "description": "Simbol ticker saham, misal: AAPL, BBCA.JK"
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

    print(f"{YELLOW}[API REQUEST PAYLOAD]:{RESET} Sent `tools` schema with {len(tools_schema)} tool.")
    print(f"{BLUE}{json.dumps(tools_schema[0], indent=2)}{RESET}")

    # Simulated LLM Native Output with `tool_calls`
    simulated_response = {
        "id": "chatcmpl-9921",
        "object": "chat.completion",
        "choices": [{
            "finish_reason": "tool_calls",
            "message": {
                "role": "assistant",
                "content": None,
                "tool_calls": [{
                    "id": "call_abc123",
                    "type": "function",
                    "function": {
                        "name": "get_stock_price",
                        "arguments": '{"ticker": "BBCA.JK", "currency": "IDR"}'
                    }
                }]
            }
        }]
    }

    tool_call = simulated_response["choices"][0]["message"]["tool_calls"][0]
    print(f"\n{GREEN}[NATIVE MODEL RESPONSE]:{RESET} `finish_reason` = 'tool_calls'")
    print(f"  Tool Name: {tool_call['function']['name']}")
    print(f"  Arguments: {tool_call['function']['arguments']}")


# ============================================================================
# 2. OPENAI ASSISTANT API PATTERN
# ============================================================================
def demo_openai_assistant_api():
    print(f"\n{BOLD}{MAGENTA}=== 2. OPENAI ASSISTANT API PATTERN ==={RESET}")
    
    print(f"{YELLOW}[1. CREATE THREAD]:{RESET} thread_id = 'thread_xyz789'")
    print(f"{YELLOW}[2. ADD MESSAGE]:{RESET} role='user', content='Analisis performa server bulan ini.'")
    print(f"{YELLOW}[3. CREATE RUN]:{RESET} run_id = 'run_001', assistant_id = 'asst_prod_analytics'")
    
    # State machine polling
    states = ["queued", "in_progress", "requires_action", "completed"]
    for s in states:
        print(f"  └─ Run Status: {BLUE}{s}{RESET}")
        if s == "requires_action":
            print(f"     {CYAN}-> Submitting Tool Outputs for 'query_server_metrics'...{RESET}")

    print(f"{GREEN}✓ Assistant Run Completed Successfully!{RESET}")


# ============================================================================
# 3. GEMINI FUNCTION CALLING (GOOGLE GENAI)
# ============================================================================
def demo_gemini_function_calling():
    print(f"\n{BOLD}{GREEN}=== 3. GEMINI FUNCTION CALLING (GOOGLE GENAI) ==={RESET}")

    gemini_tool_declaration = {
        "function_declarations": [
            {
                "name": "search_knowledge_base",
                "description": "Cari dokumen internal perusahaan",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {"type": "STRING"}
                    },
                    "required": ["query"]
                }
            }
        ]
    }

    print(f"{YELLOW}[GEMINI TOOL DECLARATION]:{RESET}")
    print(f"{BLUE}{json.dumps(gemini_tool_declaration, indent=2)}{RESET}")
    print(f"{GREEN}[GEMINI RESPONSE]:{RESET} Function Call Request: `search_knowledge_base(query='SOP Libur')`")


# ============================================================================
# 4. ANTHROPIC TOOL USE (MESSAGES API)
# ============================================================================
def demo_anthropic_tool_use():
    print(f"\n{BOLD}{BLUE}=== 4. ANTHROPIC TOOL USE (CLAUDE MESSAGES API) ==={RESET}")

    anthropic_tool_schema = {
        "name": "send_email",
        "description": "Kirim email notifikasi ke pengguna",
        "input_schema": {
            "type": "object",
            "properties": {
                "to": {"type": "string"},
                "subject": {"type": "string"},
                "body": {"type": "string"}
            },
            "required": ["to", "subject", "body"]
        }
    }

    print(f"{YELLOW}[ANTHROPIC TOOL SCHEMA]:{RESET}")
    print(f"{BLUE}{json.dumps(anthropic_tool_schema, indent=2)}{RESET}")
    print(f"{GREEN}[CLAUDE RESPONSE BLOCK]:{RESET} `type`: 'tool_use', `name`: 'send_email', `input`: {{'to': 'user@domain.com', ...}}")


# ============================================================================
# DEMO EXECUTION
# ============================================================================
def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 02.2: LLM NATIVE FUNCTION CALLING FORMATS     {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    demo_openai_function_calling()
    demo_openai_assistant_api()
    demo_gemini_function_calling()
    demo_anthropic_tool_use()


if __name__ == "__main__":
    main()
