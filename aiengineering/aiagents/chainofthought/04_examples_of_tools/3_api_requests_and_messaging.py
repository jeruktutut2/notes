#!/usr/bin/env python3
"""
SIMULASI MODUL 4.3: Examples of Tools - API Requests & Messaging (Email / Slack / SMS)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Visual (Tools 4 & 5)

Modul ini mensimulasikan 2 dari 6 kategori tool dasar pada AI Agent:
1. API Requests (HTTP Client Simulator untuk interaksi microservices)
2. Email / Slack / SMS (Communication Dispatcher untuk notifikasi sistem & Human-in-the-loop)
"""

import json
import time
from typing import Dict, Any

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

def tool_api_request(endpoint_url: str, method: str = "GET", payload: Dict[str, Any] = None) -> Dict[str, Any]:
    print(f"\n{BOLD}{CYAN}[ TOOL EXECUTION: API REQUESTS ]{RESET}")
    print(f"  🌐 {method} -> {endpoint_url}")
    if payload:
        print(f"  📦 Body Payload: {json.dumps(payload)}")
    time.sleep(0.3)
    
    # Mock REST API Response
    return {
        "status_code": 200,
        "status": "success",
        "url": endpoint_url,
        "response_time_ms": 45,
        "data": {
            "service": "Currency Exchange API",
            "base": "USD",
            "rates": {"IDR": 16250.0, "EUR": 0.92, "SGD": 1.34}
        }
    }

def tool_communication_dispatcher(channel_type: str, recipient: str, message: str) -> Dict[str, Any]:
    print(f"\n{BOLD}{GREEN}[ TOOL EXECUTION: EMAIL / SLACK / SMS DISPATCHER ]{RESET}")
    print(f"  📲 Channel : {BOLD}{channel_type.upper()}{RESET}")
    print(f"  👤 Recipient: {recipient}")
    print(f"  💬 Message  : '{message}'")
    time.sleep(0.3)
    
    channel_type_lower = channel_type.lower()
    if channel_type_lower in ["email", "slack", "sms"]:
        return {
            "status": "dispatched",
            "channel": channel_type_lower,
            "recipient": recipient,
            "message_id": f"MSG-{int(time.time())}",
            "delivered": True
        }
    else:
        return {"status": "error", "error_message": f"Channel '{channel_type}' tidak didukung."}

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   SIMULASI EXAMPLES OF TOOLS: API REQUESTS & MESSAGING DISPATCHER    {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    # Test API Request
    api_res = tool_api_request("https://api.exchangerate.id/v1/latest", method="GET")
    print(f"{GREEN}Hasil API Request:{RESET}\n{json.dumps(api_res, indent=4)}")
    
    input(f"\n{YELLOW}Tekan [Enter] untuk menguji Tool Messaging (Slack / Email / SMS)...{RESET}")
    
    # Test Messaging
    slack_res = tool_communication_dispatcher("slack", "#agent-alerts", "Laporan Keuangan Bulanan siap untuk di-review.")
    print(f"{GREEN}Hasil Dispatch Slack:{RESET}\n{json.dumps(slack_res, indent=4)}")
    
    sms_res = tool_communication_dispatcher("sms", "+628123456789", "OTP Verifikasi AI Agent: 482910")
    print(f"\n{GREEN}Hasil Dispatch SMS:{RESET}\n{json.dumps(sms_res, indent=4)}")
    
    print(f"\n{BOLD}{GREEN}✓ Simulasi Tools API Requests & Messaging Selesai!{RESET}\n")

if __name__ == "__main__":
    main()
