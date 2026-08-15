#!/usr/bin/env python3
"""
Modul 3.3: Generation Controls - Stopping Criteria & Max Length
Simulasi Stop Sequences, Max Tokens Truncation & Truncated JSON Auto-Repair Parser
Berdasarkan Gambar 1 & Roadmap.sh / AI Agents - Generation Controls
"""

import sys
import json
import re
from typing import List, Tuple, Dict, Optional

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def simulate_react_agent_stop_criteria():
    print(f"\n{BOLD}{HEADER}=== DEMO 1: STOPPING CRITERIA DALAM AGENT REACT PATTERN ==={RESET}\n")
    
    full_llm_stream = [
        "Thought: Saya perlu mengeksekusi pencarian cuaca untuk Jakarta.\n",
        "Action: weather_tool\n",
        "Action Input: {\"location\": \"Jakarta\"}\n",
        "Observation: Temperatur saat ini 30 C, cerah berawan.\n",  # <-- LLM tidak boleh membuat sendiri Observation!
        "Thought: Berdasarkan data, cuaca cerah."
    ]

    stop_sequences = ["Observation:", "<|im_end|>"]
    
    print(f"Stop Sequences Terdaftar: {YELLOW}{stop_sequences}{RESET}\n")
    print(f"{BOLD}Simulasi Streaming LLM Output dengan Detection Engine:{RESET}")
    
    generated_text = ""
    stopped_by = None

    for chunk in full_llm_stream:
        generated_text += chunk
        for stop_seq in stop_sequences:
            if stop_seq in generated_text:
                # Potong teks tepat sebelum stop sequence
                stop_idx = generated_text.find(stop_seq)
                generated_text = generated_text[:stop_idx]
                stopped_by = stop_seq
                break
        if stopped_by:
            break

    print(f"\n{BOLD}{GREEN}--- HASIL TEKS GENERASI TERPOTONG ATAS STOP CRITERIA ---{RESET}")
    print(f"Teks Dihasilkan:\n{CYAN}{generated_text}{RESET}")
    print(f"Status Stop     : {GREEN}Dihentikan oleh Stop Sequence '{stopped_by}'{RESET}")
    print(f"Aksi Next Agent : {BOLD}Agent Executor mengambil alih untuk memanggil weather_tool secara nyata.{RESET}")

def repair_truncated_json(raw_json: str) -> Tuple[Optional[Dict], bool]:
    """
    Parser otomatis untuk memperbaiki JSON terpotong akibat Max Length / Max Tokens Limit
    """
    # Try direct parse first
    try:
        data = json.loads(raw_json)
        return data, False
    except json.JSONDecodeError:
        pass

    # Attempt Repair
    repaired_str = raw_json.strip()
    
    # 1. Close unclosed quotes
    quote_count = repaired_str.count('"') - repaired_str.count('\\"')
    if quote_count % 2 != 0:
        repaired_str += '"'

    # 2. Trim trailing comma
    repaired_str = re.sub(r',\s*$', '', repaired_str)

    # 3. Balance braces and brackets
    open_braces = repaired_str.count('{') - repaired_str.count('}')
    open_brackets = repaired_str.count('[') - repaired_str.count(']')

    repaired_str += ']' * max(0, open_brackets)
    repaired_str += '}' * max(0, open_braces)

    try:
        data = json.loads(repaired_str)
        return data, True
    except json.JSONDecodeError:
        return None, False

def demonstrate_max_length_json_repair():
    print(f"\n{BOLD}{HEADER}=== DEMO 2: MAX LENGTH TRUNCATION & TRUNCATED JSON REPAIR ==={RESET}\n")

    truncated_llm_json = '{\n  "status": "success",\n  "agent_response": "Analisis selesai",\n  "output_data": ["item1", "item2", "item3'  # Max tokens hit here!

    print(f"{BOLD}Response LLM Terpotong Akibat Reaching Max Length ({RED}finish_reason == 'length'{RESET}):")
    print(f"{YELLOW}{truncated_llm_json}{RESET}\n")

    repaired_data, was_repaired = repair_truncated_json(truncated_llm_json)

    if was_repaired:
        print(f"{BOLD}{GREEN}✔ TRUNCATED JSON REPAIR ENGINE BERHASIL REKONSTRUKSI!{RESET}")
        print(f"Data Terparsing:\n{CYAN}{json.dumps(repaired_data, indent=2)}{RESET}")
    else:
        print(f"{RED}❌ Gagal merekonstruksi JSON.{RESET}")

def interactive_stop_and_length_tester():
    print(f"\n{BOLD}{HEADER}=== INTERACTIVE JSON TRUNCATION TESTER ==={RESET}")
    print("Masukkan string JSON terpotong untuk diuji oleh Truncated JSON Repair Engine:")
    user_input = input("\nString JSON (misal: {\"name\": \"Agent\", \"tools\": [\"search\"): ").strip()
    
    res, is_repaired = repair_truncated_json(user_input)
    if res is not None:
        print(f"\n{BOLD}{GREEN}--- HASIL PARSING REPAIRED JSON ---{RESET}")
        print(json.dumps(res, indent=2))
        print(f"\nRepair Executed: {is_repaired}")
    else:
        print(f"\n{RED}JSON terlalu terdistorsi untuk direparasi secara otomatis.{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 3.3: GENERATION CONTROLS - STOPPING CRITERIA & MAX LENGTH{RESET}")
    print(f"{CYAN}Sesuai dengan Gambar 1 (Generation Controls: Stopping Criteria, Max Length){RESET}")
    print("█" * 75)

    simulate_react_agent_stop_criteria()
    demonstrate_max_length_json_repair()

    print("\nIngin mencoba Interactive JSON Truncation Tester?")
    ans = input("Jawab (y/n): ").strip().lower()
    if ans == 'y':
        interactive_stop_and_length_tester()

    print(f"\n{GREEN}✔ Modul 3.3 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
