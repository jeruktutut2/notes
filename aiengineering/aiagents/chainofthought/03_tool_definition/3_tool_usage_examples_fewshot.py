#!/usr/bin/env python3
"""
SIMULASI MODUL 3.3: Tool Usage Examples & Few-Shot Demonstrations
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Visual

Modul ini mensimulasikan penambahan "Usage Examples" (Contoh Penggunaan) di dalam Tool Definition,
sehingga LLM dapat mempelajari format pemanggilan tool secara in-context learning.
"""

import json
import time
from typing import Dict, List, Any

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

TOOL_WITH_USAGE_EXAMPLES = {
    "tool_name": "send_slack_message",
    "description": "Mengirimkan pesan notifikasi atau laporan ke channel Slack internal perusahaan.",
    "usage_examples": [
        {
            "user_intent": "Kirim pesan salam ke channel #general",
            "llm_reasoning": "Pengguna ingin mengirim pesan ke channel Slack #general.",
            "tool_call": {
                "channel": "#general",
                "message": "Halo tim! Selamat pagi dan selamat beraktivitas."
            }
        },
        {
            "user_intent": "Beri tahu tim dev di channel #incident-alerts bahwa server DB down",
            "llm_reasoning": "Ini adalah lansiran mendesak untuk tim dev di channel #incident-alerts.",
            "tool_call": {
                "channel": "#incident-alerts",
                "message": "🚨 CRITICAL: Database primary mengalami kerusakaan connection pool. Tim SRE sedang menangani.",
                "urgency": "high"
            }
        }
    ]
}

def display_usage_examples_demo():
    print(f"\n{BOLD}{CYAN}=== TOOL DEFINITION WITH FEW-SHOT USAGE EXAMPLES ==={RESET}\n")
    print(f"Tool Name   : {BOLD}{TOOL_WITH_USAGE_EXAMPLES['tool_name']}{RESET}")
    print(f"Description : {TOOL_WITH_USAGE_EXAMPLES['description']}\n")
    
    print(f"{BOLD}{MAGENTA}--- USAGE EXAMPLES (FEW-SHOT DEMONSTRATIONS FOR ALIGNMENT) ---{RESET}")
    for idx, ex in enumerate(TOOL_WITH_USAGE_EXAMPLES["usage_examples"], 1):
        print(f"\n{BOLD}{YELLOW}Contoh #{idx}:{RESET}")
        print(f"  User Intent   : \"{ex['user_intent']}\"")
        print(f"  LLM Reasoning : \"{ex['llm_reasoning']}\"")
        print(f"  Tool Call     : {GREEN}{json.dumps(ex['tool_call'])}{RESET}")
        time.sleep(0.3)
        
    print(f"\n{BOLD}{GREEN}✓ Fungsi Usage Examples: Memastikan LLM tidak salah membuat nama channel atau salah format payload.{RESET}\n")

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}      SIMULASI TOOL DEFINITION: USAGE EXAMPLES & FEW-SHOT ALIGNMENT   {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    display_usage_examples_demo()

if __name__ == "__main__":
    main()
