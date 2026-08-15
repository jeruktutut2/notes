#!/usr/bin/env python3
"""
SIMULASI MODUL 1.3: Thought Execution & Action Parsing
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents)

Modul ini mensimulasikan mekanisme ekstraksi tag <thought> dan <action> dari output LLM
sehingga penalaran internal agen (Chain of Thought) dapat dipisahkan secara bersih
dari perintah eksekusi aksi / pemanggilan tool.
"""

import re
import json
import time
from typing import Dict, Any, Tuple

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Mock LLM Raw Output Streams
RAW_LLM_OUTPUTS = [
    """
<thought>
Pengguna meminta pencarian harga saham PT Telkom Indonesia (TLKM) hari ini.
Saya tidak memiliki data pasar real-time di memori lokal saya.
Oleh karena itu, saya harus menggunakan tool 'web_search' untuk mencari harga TLKM terbaru.
</thought>
<action>
{
    "tool": "web_search",
    "parameters": {
        "query": "harga saham TLKM hari ini",
        "num_results": 3
    }
}
</action>
    """,
    """
<thought>
Perhitungan yang diminta adalah faktorial dari 12 dikurangi 450.
Kalkulasi mental rentan salah untuk angka besar, jadi saya akan mengeksekusinya via Python REPL tool.
</thought>
<action>
{
    "tool": "code_execution",
    "parameters": {
        "language": "python",
        "code": "import math; result = math.factorial(12) - 450; print(result)"
    }
}
</action>
    """
]

def parse_thought_and_action(raw_output: str) -> Tuple[str, Dict[str, Any]]:
    """
    Menggunakan regex untuk memisahkan blok <thought> dan <action>
    """
    thought_match = re.search(r"<thought>(.*?)</thought>", raw_output, re.DOTALL)
    action_match = re.search(r"<action>(.*?)</action>", raw_output, re.DOTALL)
    
    thought_text = thought_match.group(1).strip() if thought_match else ""
    
    action_json = {}
    if action_match:
        action_str = action_match.group(1).strip()
        try:
            action_json = json.loads(action_str)
        except json.JSONDecodeError as e:
            action_json = {"error": f"Failed to parse JSON action: {e}", "raw": action_str}
            
    return thought_text, action_json

def execute_parsed_agent_step(idx: int, raw_output: str):
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}AGENT EXECUTION STEP #{idx}{RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    print(f"{YELLOW}[1] MENERIMA UNPARSED RAW OUTPUT DARI LLM...{RESET}")
    print(raw_output.strip())
    time.sleep(0.3)
    
    print(f"\n{CYAN}[2] EKSTRAKSI & PARSING OLEH AGENT CONTROLLER...{RESET}")
    thought, action = parse_thought_and_action(raw_output)
    
    print(f"\n{BOLD}{MAGENTA}🧠 REASONING TRACE (<thought>):{RESET}")
    for line in thought.split("\n"):
        print(f"   {line}")
        
    print(f"\n{BOLD}{GREEN}⚙️ TARGET ACTION (<action>):{RESET}")
    print(f"   Tool Name  : {BOLD}{action.get('tool')}{RESET}")
    print(f"   Parameters : {json.dumps(action.get('parameters', {}), indent=6)}")
    
    time.sleep(0.3)
    print(f"\n{GREEN}✓ Parsing Berhasil: Thought dipisah dari Action Payload.{RESET}")

def main():
    print(f"\n{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}      SIMULASI THOUGHT EXECUTION & ACTION PARSER (XML / JSON TAGS)     {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    
    for idx, raw_text in enumerate(RAW_LLM_OUTPUTS, 1):
        execute_parsed_agent_step(idx, raw_text)
        input(f"\n{YELLOW}Tekan [Enter] untuk contoh parsing berikutnya...{RESET}")

if __name__ == "__main__":
    main()
