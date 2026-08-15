#!/usr/bin/env python3
"""
Modul 5.1: Full Agent Loop Engine
Arsitektur terpadu yang memadukan 4 Pilar Utama Agent Loop:
(1) Perception -> (2) Reason & Plan -> (3) Acting / Tool Call -> (4) Observe & Reflect
menjadi satu runtime loop yang mandiri dan berinteraksi secara otomatis.
"""

import time
import json
from typing import Dict, Any, List

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

class FullAgentLoopEngine:
    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations
        self.memory: List[Dict[str, str]] = []

    def execute_loop(self, user_prompt: str):
        print(f"\n{'='*70}")
        print(f"{BOLD}{HEADER_TITLE if 'HEADER_TITLE' in globals() else CYAN}=== STARTING AUTONOMOUS AGENT LOOP RUNTIME ==={RESET}")
        print(f"{'='*70}\n")

        # -------------------------------------------------------------
        # TAHAP 1: PERCEPTION & USER INPUT
        # -------------------------------------------------------------
        print(f"{BOLD}[1. PERCEPTION / USER INPUT]{RESET}")
        print(f"  Raw Input    : \"{YELLOW}{user_prompt}{RESET}\"")
        target_goal = user_prompt.strip()
        intent = "COMPUTE_AND_NOTIFY"
        print(f"  Parsed Intent: {BOLD}{intent}{RESET}")
        print(f"  Target Goal  : {target_goal}\n")

        iteration = 0
        last_observation = None
        goal_completed = False

        while iteration < self.max_iterations and not goal_completed:
            iteration += 1
            print(f"{BOLD}{MAGENTA}┌──────────────────────────────────────────────────────────┐{RESET}")
            print(f"{BOLD}{MAGENTA}│ AGENT LOOP ITERATION #{iteration}                                   │{RESET}")
            print(f"{BOLD}{MAGENTA}└──────────────────────────────────────────────────────────┘{RESET}")

            # -------------------------------------------------------------
            # TAHAP 2: REASON AND PLAN
            # -------------------------------------------------------------
            print(f"  {BOLD}[2. REASON AND PLAN]{RESET}")
            if iteration == 1:
                thought = "Saya perlu membaca data nilai penjualan terlebih dahulu dari database."
                action = "read_sales_db"
                action_args = {"query": "SELECT sum(sales) FROM q3"}
            elif iteration == 2:
                thought = f"Data DB ditemukan ({last_observation}). Sekarang saya harus memformat teks laporan."
                action = "generate_report"
                action_args = {"raw_summary": last_observation}
            else:
                thought = f"Laporan sudah siap ({last_observation}). Sekarang saya kirim via email."
                action = "send_email"
                action_args = {"recipient": "manager@company.com", "body": last_observation}

            print(f"    🧠 {BLUE}Thought :{RESET} {thought}")
            print(f"    ⚡ {YELLOW}Action  :{RESET} `{action}` with {json.dumps(action_args)}")

            # -------------------------------------------------------------
            # TAHAP 3: ACTING / TOOL INVOCATION
            # -------------------------------------------------------------
            print(f"  {BOLD}[3. ACTING / TOOL INVOCATION]{RESET}")
            print(f"    ⚙ Executing tool `{action}`...")
            time.sleep(0.3)  # Simulasi Latensi Tool Execution
            
            if action == "read_sales_db":
                last_observation = "Total Sales Q3 = $450,000 USD (Growth +15%)"
            elif action == "generate_report":
                last_observation = "REPORT_DOC_V1: Q3 Sales reached $450k with 15% YoY growth."
            elif action == "send_email":
                last_observation = "Email successfully sent to manager@company.com (MessageID: #8841)"

            print(f"    👁 {CYAN}Observation:{RESET} {last_observation}")

            # -------------------------------------------------------------
            # TAHAP 4: OBSERVATION & REFLECTION
            # -------------------------------------------------------------
            print(f"  {BOLD}[4. OBSERVATION & REFLECTION]{RESET}")
            if action == "send_email":
                goal_completed = True
                print(f"    🧠 {GREEN}Reflection :{RESET} Email laporan telah terkirim. Target goal sepenuhnya tercapai.")
                print(f"    🏁 {GREEN}Decision   : TERMINATE LOOP (SUCCESS){RESET}\n")
            else:
                print(f"    🧠 {YELLOW}Reflection :{RESET} Sub-tugas `{action}` berhasil. Melanjutkan ke langkah berikutnya.")
                print(f"    🔄 {CYAN}Decision   : REPEAT AGENT LOOP{RESET}\n")

        if goal_completed:
            print(f"{GREEN}{BOLD}🎉 [SUCCESS] Agent Loop berhasil menyelesaikan goal dalam {iteration} iterasi!{RESET}\n")
        else:
            print(f"{RED}{BOLD}🛑 [STOP] Agent Loop terhenti karena batas max_iterations ({self.max_iterations}).{RESET}\n")

def main():
    engine = FullAgentLoopEngine(max_iterations=5)
    engine.execute_loop("Hitung penjualan Q3 dan kirimkan laporan ringkasan ke manager")

if __name__ == "__main__":
    main()
