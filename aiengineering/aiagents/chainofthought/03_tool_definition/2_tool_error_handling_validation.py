#!/usr/bin/env python3
"""
SIMULASI MODUL 3.2: Tool Error Handling & Validation Loop
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents) & Gambar Visual

Modul ini mensimulasikan mekanisme Error Handling ketika pemanggilan tool gagal
(misal: JSON argumen salah tipe, parameter wajib hilang, atau runtime error)
dan bagaimana pesan error dikembalikan ke loop CoT agar agen melakukan Self-Correction.
"""

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

# Expected Schema for database_query tool
DB_TOOL_SCHEMA = {
    "required_params": ["sql", "database_name"],
    "param_types": {
        "sql": str,
        "database_name": str,
        "limit": int
    }
}

# Test Scenarios
CALL_SCENARIOS = [
    {
        "scenario": "Pemanggilan Cacat 1: Parameter Wajib 'database_name' Hilang",
        "payload": {
            "sql": "SELECT * FROM users WHERE status = 'active'"
        }
    },
    {
        "scenario": "Pemanggilan Cacat 2: Tipe Data 'limit' Salah (String alih-alih Integer)",
        "payload": {
            "sql": "SELECT * FROM products",
            "database_name": "inventory_db",
            "limit": "sepuluh"
        }
    },
    {
        "scenario": "Pemanggilan Valid: Semua Argumen Sesuai Skema",
        "payload": {
            "sql": "SELECT * FROM inventory WHERE stock < 10",
            "database_name": "inventory_db",
            "limit": 10
        }
    }
]

def validate_and_execute_tool(payload: Dict[str, Any]) -> Tuple[bool, str, Dict[str, Any]]:
    # Check Required Params
    for req in DB_TOOL_SCHEMA["required_params"]:
        if req not in payload:
            return False, f"ValidationError: Parameter wajib '{req}' tidak ditemukan pada panggilan tool.", {}
            
    # Check Param Types
    for param_name, value in payload.items():
        expected_type = DB_TOOL_SCHEMA["param_types"].get(param_name)
        if expected_type and not isinstance(value, expected_type):
            return False, f"TypeError: Parameter '{param_name}' harus bertipe {expected_type.__name__}, tetapi menerima {type(value).__name__} ('{value}').", {}
            
    # Success Execution Mock
    result_data = {
        "status": "success",
        "rows_returned": 2,
        "data": [
            {"product_id": "P-101", "name": "Kabel Type-C", "stock": 4},
            {"product_id": "P-105", "name": "Mouse Wireless", "stock": 2}
        ]
    }
    return True, "Success", result_data

def run_error_handling_simulation():
    print(f"\n{BOLD}{CYAN}=== SIMULATOR TOOL ERROR HANDLING & SELF-CORRECTION LOOP ==={RESET}\n")
    
    for idx, case in enumerate(CALL_SCENARIOS, 1):
        print(f"{BOLD}{MAGENTA}----------------------------------------------------------------------{RESET}")
        print(f"{BOLD}KASUS #{idx}: {case['scenario']}{RESET}")
        print(f"Payload dari LLM: {json.dumps(case['payload'])}\n")
        
        time.sleep(0.3)
        success, error_msg, data = validate_and_execute_tool(case["payload"])
        
        if not success:
            print(f"{BOLD}{RED}❌ TOOL EXECUTION ERROR DETECTED:{RESET}")
            print(f"   Pesan Error: {RED}{error_msg}{RESET}")
            print(f"\n{YELLOW}🔁 Agent Feedback Loop Prompt Generated:{RESET}")
            print(f"   \"[SYSTEM ERROR FEEDBACK]: Panggilan tool 'database_query' gagal dengan error: {error_msg}. Harap perbaiki argumen JSON sesuai Tool Definition dan coba lagi.\"")
            print(f"   {CYAN}-> Agen CoT membaca feedback dan melakukan koreksi argumen (Self-Correction).{RESET}")
        else:
            print(f"{BOLD}{GREEN}✅ TOOL EXECUTION SUCCESS:{RESET}")
            print(f"   Hasil Eksekusi: {json.dumps(data, indent=6)}")
            
        time.sleep(0.4)

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}     SIMULASI TOOL ERROR HANDLING & SCHEMA VALIDATION RECOVERY LOOP    {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    run_error_handling_simulation()

if __name__ == "__main__":
    main()
