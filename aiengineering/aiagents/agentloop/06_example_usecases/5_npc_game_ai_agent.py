#!/usr/bin/env python3
"""
Modul 6.5: Example Usecase - NPC / Game AI Agent
Simulasi AI Agent untuk Non-Player Character (NPC) dalam game RPG/Petualangan yang mengamati
perubahan lingkungan (Perception), merencanakan taktik (Reason & Plan), dan mengeksekusi aksi (Act) dalam game.
"""

import time
import json
from typing import Dict, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

class NPCGameAIAgent:
    def __init__(self, name: str = "Aria the Guardian"):
        self.name = name
        self.hp = 45  # Low HP
        self.stamina = 80
        self.inventory = ["Health Potion", "Iron Sword", "Shield"]

    def run_agent_loop(self, world_event: str):
        print(f"\n{BOLD}{CYAN}=== USECASE 5: NPC / GAME AI AGENT ({self.name}) ==={RESET}")
        print(f"World Event: \"{RED}{world_event}{RESET}\"\n")

        ticks = [
            ("PERCEPTION", f"Mendeteksi ancaman musuh! World State: Enemy (Orc Warrior) mendekat pada jarak 5 meter. NPC HP: {self.hp}/100."),
            ("THOUGHT", "HP saya kritikal (45%). Bertarung langsung berisiko fatal. Saya harus menggunakan Health Potion terlebih dahulu."),
            ("ACTION", "call drink_potion(item='Health Potion')"),
            ("OBSERVATION", "HP bertambah +50. HP saat ini: 95/100. Potion dikonsumsi."),
            ("THOUGHT", "HP sudah aman. Sekarang bersiap menangkis serangan musuh dengan Shield."),
            ("ACTION", "call raise_shield_and_counter_attack(weapon='Iron Sword')"),
            ("OBSERVATION", "Serangan Orc berhasil ditangkis! Orc terkena Counter Attack -30 DMG."),
            ("REFLECTION", "Ancaman Orc dinetralkan. NPC kembali ke status Guard Mode.")
        ]

        for phase, text in ticks:
            if phase == "PERCEPTION":
                print(f"{BOLD}[Perception]{RESET} {text}")
            elif phase == "THOUGHT":
                print(f"  🧠 {BLUE}Thought    :{RESET} {text}")
            elif phase == "ACTION":
                print(f"  ⚡ {YELLOW}Action     :{RESET} {text}")
            elif phase == "OBSERVATION":
                print(f"  👁 {CYAN}Observation:{RESET} {text}")
            elif phase == "REFLECTION":
                print(f"  🏁 {GREEN}Reflection :{RESET} {text}\n")
            time.sleep(0.2)

        print(f"{GREEN}{BOLD}🎮 [STATUS AKHIR GAME NPC]:{RESET}")
        print(f"  • Status Karakter : Alive (HP: 95/100, Shield Active)")
        print(f"  • Keputusan AI   : {BOLD}Tactical Self-Heal & Counter Attack{RESET}\n")

if __name__ == "__main__":
    npc = NPCGameAIAgent()
    npc.run_agent_loop("Musuh Orc Warrior muncul secara mendadak dari semak-semak!")
