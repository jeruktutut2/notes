#!/usr/bin/env python3
"""
Modul 4.2: Reflection, Self-Correction & Termination Criteria
Demonstrasi bagaimana Agent mengevaluasi hasil observasi terhadap target goal (Self-Reflect),
merevisi strategi saat menemukan kesalahan (Self-Correction), serta menentukan kondisi berhenti (Termination).
"""

from typing import Dict, Any, List, Tuple
from dataclasses import dataclass

# ANSI Terminal Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class ReflectionResult:
    goal_achieved: bool
    should_terminate: bool
    reflection_notes: str
    suggested_correction: str = ""

class ReflectionEngine:
    def __init__(self, max_iterations: int = 5):
        self.max_iterations = max_iterations

    def reflect_on_observation(self, target_goal: str, iteration: int, last_action: str, observation: str) -> ReflectionResult:
        """Menganalisis apakah hasil observasi telah menyelesaikan goal atau memerlukan self-correction."""
        
        # 1. Cek Batas Maksimum Iterasi (Max Iteration Safeguard)
        if iteration >= self.max_iterations:
            return ReflectionResult(
                goal_achieved=False,
                should_terminate=True,
                reflection_notes=f"Terhenti: Telah mencapai batas maksimum iterasi ({self.max_iterations})."
            )

        # 2. Evaluasi Observasi (Mock LLM Judge)
        if "404 Not Found" in observation or "Error" in observation:
            return ReflectionResult(
                goal_achieved=False,
                should_terminate=False,
                reflection_notes=f"Tindakan '{last_action}' mengalami eror: {observation}",
                suggested_correction="Ubah parameter pencarian atau gunakan tool fallback alternative."
            )

        if "SUCCESS" in observation or "Selesai" in observation or "100%" in observation:
            return ReflectionResult(
                goal_achieved=True,
                should_terminate=True,
                reflection_notes="Target goal telah berhasil dicapai secara penuh berdasarkan observasi.",
                suggested_correction="Tampilkan jawaban akhir kepada pengguna."
            )

        return ReflectionResult(
            goal_achieved=False,
            should_terminate=False,
            reflection_notes="Hasil observasi parsial didapatkan. Diperlukan langkah tambahan.",
            suggested_correction="Lanjutkan ke sub-tugas berikutnya dalam plan."
        )

def main():
    print(f"\n{BOLD}{CYAN}=== MODUL 4.2: REFLECTION, SELF-CORRECTION & TERMINATION ==={RESET}\n")

    reflector = ReflectionEngine(max_iterations=4)
    target_goal = "Ekstrak file data_sales.csv dan kirim ringkasan"

    scenarios = [
        (1, "fetch_file('data_sales.csv')", "Error: File 404 Not Found"),
        (2, "search_file_alternative('sales_2026.csv')", "File found! Status: SUCCESS"),
        (3, "summarize_and_send()", "Email delivered 100%")
    ]

    for iteration, action, obs in scenarios:
        print(f"{BOLD}[Iterasi #{iteration}]{RESET} Action: {YELLOW}{action}{RESET}")
        print(f"  Observation: {obs}")
        
        res = reflector.reflect_on_observation(target_goal, iteration, action, obs)
        
        if res.goal_achieved:
            print(f"  {GREEN}🧠 Reflection: {res.reflection_notes}{RESET}")
            print(f"  {GREEN}🏁 Decision  : TERMINATE LOOP (Goal Achieved){RESET}")
            break
        elif not res.should_terminate:
            print(f"  {RED}🧠 Reflection  : {res.reflection_notes}{RESET}")
            print(f"  {CYAN}🛠 Self-Correction: {res.suggested_correction}{RESET}")
            print(f"  {YELLOW}🔄 Decision     : CONTINUE AGENT LOOP{RESET}")
        else:
            print(f"  {RED}🛑 Decision: TERMINATE LOOP (Max Limit Reached){RESET}")
            break
        print("-" * 65)

if __name__ == "__main__":
    main()
