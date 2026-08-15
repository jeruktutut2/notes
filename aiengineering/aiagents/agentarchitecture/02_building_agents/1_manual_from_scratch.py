#!/usr/bin/env python3
"""
Modul 02: Building Agents - Part 1
Simulasi Manual Agent Construction (From Scratch):
- Direct LLM API Calls
- Custom Agent Loop Implementation
- Parsing Model Output (Regex / JSON Extractor)
- Error & Rate-Limit Handling (Exponential Backoff with Jitter)
"""

import json
import random
import re
import time
from typing import Dict, Any, Optional

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================================
# 1. ERROR & RATE-LIMIT HANDLING WITH EXPONENTIAL BACKOFF + JITTER
# ============================================================================
def call_llm_api_with_retry(prompt: str, max_retries: int = 3) -> str:
    """Simulasi panggilan API LLM tingkat rendah dengan penanganan Rate Limit (429)."""
    base_delay = 0.5  # detik
    max_delay = 5.0

    for attempt in range(1, max_retries + 1):
        try:
            print(f"  [API CALL] Mengirim request ke LLM Endpoint (Percobaan #{attempt})...")
            
            # Simulasi transient Rate Limit Error pada percobaan pertama
            if attempt == 1:
                raise Exception("429 Too Many Requests - Rate limit exceeded")
            
            # Simulated Successful API Response Payload
            simulated_response = (
                "```json\n"
                "{\n"
                '  "thought": "User ingin menghitung total biaya transaksi.",\n'
                '  "action": "calculate",\n'
                '  "action_input": {"expression": "250 * 15000"}\n'
                "}\n"
                "```"
            )
            print(f"  {GREEN}[API 200 OK]{RESET} Respon berhasil diterima.")
            return simulated_response

        except Exception as e:
            print(f"  {RED}[API ERROR]: {e}{RESET}")
            if attempt == max_retries:
                raise e
            
            # Formulasi Exponential Backoff dengan Jitter:
            # wait_time = min(max_delay, base_delay * 2^(attempt-1)) + random_jitter
            jitter = random.uniform(0, 0.2)
            wait_time = min(max_delay, base_delay * (2 ** (attempt - 1))) + jitter
            print(f"  {YELLOW}[EXPONENTIAL BACKOFF]{RESET} Menunggu {wait_time:.2f} detik sebelum retry...")
            time.sleep(wait_time)


# ============================================================================
# 2. PARSING MODEL OUTPUT (REGEX & JSON EXTRACTOR)
# ============================================================================
class OutputParser:
    """Robust parser untuk mengekstrak JSON dari respon LLM yang mengandung markdown/teks ekstra."""

    @staticmethod
    def parse_action(raw_llm_output: str) -> Dict[str, Any]:
        print(f"\n{CYAN}[OUTPUT PARSER]{RESET} Memparsing teks mentah LLM...")
        
        # Pattern RegEx untuk menangkap blok ```json ... ``` atau { ... }
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_llm_output, re.DOTALL)
        if not json_match:
            json_match = re.search(r'(\{.*?\})', raw_llm_output, re.DOTALL)

        if json_match:
            json_str = json_match.group(1)
            try:
                data = json.loads(json_str)
                print(f"  {GREEN}✓ Parsed JSON Data:{RESET} Action='{data.get('action')}', Input={data.get('action_input')}")
                return data
            except json.JSONDecodeError as err:
                print(f"  {RED}✖ JSON Decode Error: {err}{RESET}")
        
        # Fallback jika parsing JSON gagal
        return {"action": "UNKNOWN", "action_input": {}, "raw": raw_llm_output}


# ============================================================================
# 3. MANUAL AGENT LOOP IMPLEMENTATION FROM SCRATCH
# ============================================================================
class ManualAgentFromScratch:
    """Agent yang dibangun secara manual tanpa framework (Pure Loop Engine)."""

    def __init__(self, max_iterations: int = 3):
        self.max_iterations = max_iterations
        self.history = []

    def execute_tool(self, action: str, action_input: Dict[str, Any]) -> str:
        if action == "calculate":
            expr = action_input.get("expression", "0")
            return f"Hasil kalkulasi '{expr}' = {eval(expr)}"
        return "Tool tidak dikenal."

    def run(self, user_query: str):
        print(f"\n{BOLD}{MAGENTA}=== MANUAL AGENT LOOP FROM SCRATCH ==={RESET}")
        print(f"User Query: '{user_query}'\n")

        self.history.append({"role": "user", "content": user_query})
        iteration = 1

        while iteration <= self.max_iterations:
            print(f"{BOLD}--- Agent Loop Iteration #{iteration} ---{RESET}")
            
            # 1. LLM API Call with Error & Backoff Handling
            raw_response = call_llm_api_with_retry(user_query)

            # 2. Output Parsing
            parsed = OutputParser.parse_action(raw_response)

            action = parsed.get("action")
            action_input = parsed.get("action_input")

            # 3. Tool Execution & Observation Loop
            obs = self.execute_tool(action, action_input)
            print(f"  {BLUE}[OBSERVATION]:{RESET} {obs}")

            # Simulated final answer step
            print(f"  {GREEN}[FINAL ANSWER]:{RESET} Biaya total 250 unit adalah Rp 3.750.000.\n")
            break


# ============================================================================
# DEMO EXECUTION
# ============================================================================
def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 02.1: MANUAL AGENT BUILDING FROM SCRATCH     {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    agent = ManualAgentFromScratch(max_iterations=3)
    agent.run("Hitung total biaya lisensi untuk 250 pengguna seharga Rp 15.000 per pengguna.")


if __name__ == "__main__":
    main()
