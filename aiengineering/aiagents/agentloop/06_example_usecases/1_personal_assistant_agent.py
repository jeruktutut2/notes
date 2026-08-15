#!/usr/bin/env python3
"""
Modul 6.1: Example Usecase - Personal Assistant Agent
Simulasi AI Agent yang berfungsi sebagai Asisten Pribadi (Personal Assistant) untuk
mengelola jadwal kalender, memeriksa email, dan mengatur daftar tugas harian melalui Agent Loop.
"""

import time
import json
from typing import Dict, Any, List

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

class PersonalAssistantAgent:
    def __init__(self):
        self.calendar = [
            {"time": "09:00", "event": "Daily Standup Meeting"},
            {"time": "14:00", "event": "Client Presentation"}
        ]
        self.tasks = ["Review pull request #42", "Update documentation"]

    def run_agent_loop(self, user_request: str):
        print(f"\n{BOLD}{CYAN}=== USECASE 1: PERSONAL ASSISTANT AGENT ==={RESET}")
        print(f"Request Pengguna: \"{YELLOW}{user_request}{RESET}\"\n")

        turns = [
            ("PERCEIVE", "Mengidentifikasi intent: 'Tambah jadwal baru & tampilkan agenda hari ini'"),
            ("THOUGHT", "Langkah 1: Periksa bentrok jadwal pada jam 11:00"),
            ("ACTION", "call check_calendar(time='11:00')"),
            ("OBSERVATION", "Slot 11:00 KOSONG (Bebas dari bentrok)"),
            ("THOUGHT", "Langkah 2: Tambahkan acara 'Rapat Strategi AI' pada jam 11:00"),
            ("ACTION", "call add_event(time='11:00', title='Rapat Strategi AI')"),
            ("OBSERVATION", "Jadwal berhasil ditambahkan. Total 3 agenda hari ini."),
            ("REFLECT", "Target penambahan jadwal selesai. Menyiapkan ringkasan untuk pengguna.")
        ]

        for step_type, text in turns:
            if step_type == "PERCEIVE":
                print(f"{BOLD}[Perception]{RESET} {text}")
            elif step_type == "THOUGHT":
                print(f"  🧠 {BLUE}Thought    :{RESET} {text}")
            elif step_type == "ACTION":
                print(f"  ⚡ {YELLOW}Action     :{RESET} {text}")
            elif step_type == "OBSERVATION":
                print(f"  👁 {CYAN}Observation:{RESET} {text}")
            elif step_type == "REFLECT":
                print(f"  🏁 {GREEN}Reflection :{RESET} {text}\n")
            time.sleep(0.2)

        print(f"{GREEN}{BOLD}✔ [HASIL AKHIR ASISTEN PRIBADI]:{RESET}")
        print(f"  Agenda Anda hari ini:")
        print(f"  • 09:00 - Daily Standup Meeting")
        print(f"  • 11:00 - Rapat Strategi AI (Baru)")
        print(f"  • 14:00 - Client Presentation\n")

if __name__ == "__main__":
    agent = PersonalAssistantAgent()
    agent.run_agent_loop("Tolong jadwalkan Rapat Strategi AI jam 11 siang dan beri tahu agenda saya hari ini.")
