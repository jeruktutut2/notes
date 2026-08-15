#!/usr/bin/env python3
"""
Modul 2.1: ReAct Reasoning & Chain-of-Thought (CoT)
Demonstrasi siklus penalaran ReAct (Thought -> Action -> Observation) yang memungkinkan AI Agent
menganalisis masalah secara bertahap dan memikirkan tindakan terbaik sebelum mengeksekusi tool.
"""

import json
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class ReActStep:
    step_number: int
    thought: str
    action_name: Optional[str] = None
    action_input: Optional[Dict[str, Any]] = None
    observation: Optional[str] = None

class ReActReasoningEngine:
    def __init__(self, available_tools: List[str]):
        self.available_tools = available_tools
        self.history: List[ReActStep] = []

    def reason_step(self, user_goal: str, step_index: int, last_observation: Optional[str] = None) -> ReActStep:
        """Simulasi pembentukan Thought & Action oleh LLM berdasarkan riwayat observasi."""
        if step_index == 1:
            thought = f"Saya perlu menyelesaikan goal '{user_goal}'. Pertama, saya harus mencari data awal yang dibutuhkan."
            action_name = "search_database"
            action_input = {"query": user_goal}
        elif step_index == 2:
            thought = f"Berdasarkan observasi sebelumnya ({last_observation}), saya perlu memproses data tersebut dengan kalkulator."
            action_name = "calculate_summary"
            action_input = {"raw_data": last_observation}
        else:
            thought = f"Saya sudah memiliki semua informasi yang cukup dari observasi sebelumnya ({last_observation}). Saya siap memberikan jawaban akhir."
            action_name = "FINAL_ANSWER"
            action_input = {"result": f"Selesai memproses goal: '{user_goal}' dengan sukses."}

        return ReActStep(
            step_number=step_index,
            thought=thought,
            action_name=action_name,
            action_input=action_input
        )

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 2.1: REACT REASONING & CHAIN-OF-THOUGHT (CoT) ==={RESET}\n")

    tools = ["search_database", "calculate_summary", "send_email"]
    engine = ReActReasoningEngine(available_tools=tools)
    user_goal = "Hitung total penjualan produk Q3 dan buatkan ringkasan"

    print(f"{BOLD}User Goal:{RESET} {YELLOW}{user_goal}{RESET}\n")

    current_observation = None
    for step_num in range(1, 4):
        react_step = engine.reason_step(user_goal, step_num, current_observation)
        
        print(f"{BOLD}{MAGENTA}[Step {react_step.step_number}]{RESET}")
        print(f"  {BLUE}🧠 Thought:{RESET} {react_step.thought}")
        
        if react_step.action_name == "FINAL_ANSWER":
            print(f"  {GREEN}🏁 Final Answer:{RESET} {react_step.action_input['result']}")
            break
        else:
            print(f"  {YELLOW}⚡ Action  :{RESET} Call `{react_step.action_name}` with args {json.dumps(react_step.action_input)}")
            # Simulasi Observasi Lingkungan
            if react_step.action_name == "search_database":
                current_observation = "Found 3 transactions: [100, 250, 400]"
            elif react_step.action_name == "calculate_summary":
                current_observation = "Total Sum = 750, Average = 250"
            
            react_step.observation = current_observation
            print(f"  {CYAN}👁 Observation:{RESET} {current_observation}")
        print("-" * 65)

if __name__ == "__main__":
    main()
