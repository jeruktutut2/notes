#!/usr/bin/env python3
"""
Modul 3.2: Generation Controls - Frequency Penalty & Presence Penalty
Simulasi Penyesuaian Logits & Mitigasi Looping pada Response AI Agent
Berdasarkan Gambar 1 & Roadmap.sh / AI Agents - Generation Controls
"""

import sys
import math
from typing import Dict, List, Tuple

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def apply_penalties(
    logits: Dict[str, float],
    counts: Dict[str, int],
    frequency_penalty: float,
    presence_penalty: float
) -> Dict[str, float]:
    """
    Menghitung penyesuaian logit:
    logit_i' = logit_i - (count_i * frequency_penalty) - (1(count_i > 0) * presence_penalty)
    """
    adjusted = {}
    for token, logit in logits.items():
        c_i = counts.get(token, 0)
        freq_penalty_val = c_i * frequency_penalty
        pres_penalty_val = (1.0 if c_i > 0 else 0.0) * presence_penalty
        
        adjusted_logit = logit - freq_penalty_val - pres_penalty_val
        adjusted[token] = adjusted_logit
        
    return adjusted

def demonstrate_penalty_math():
    print(f"\n{BOLD}{HEADER}=== DEMO 1: FORMULASI MATEMATIKA PENALTY LOGITS ==={RESET}\n")
    
    initial_logits = {
        "Jakarta": 5.0,
        "Indonesia": 3.0,
        "Surabaya": 2.5,
        "Bandung": 2.2,
        "Singapura": 1.5
    }
    
    # Skenario: Kata "Jakarta" sudah dihasilkan 4 kali (count = 4)
    counts = {"Jakarta": 4, "Indonesia": 1, "Surabaya": 0, "Bandung": 0, "Singapura": 0}

    print(f"Logit Awal  : {initial_logits}")
    print(f"Token Count : {counts}\n")

    print(f"{'Skenario Penalty':<30} | {'Logit Jakarta':<15} | {'Logit Indonesia':<16} | {'Pemenang (Argmax)':<20}")
    print("-" * 88)

    # 1. Without Penalty
    adj1 = apply_penalties(initial_logits, counts, frequency_penalty=0.0, presence_penalty=0.0)
    winner1 = max(adj1, key=adj1.get)
    print(f"{'Tanpa Penalty (Freq=0, Pres=0)':<30} | {adj1['Jakarta']:>15.2f} | {adj1['Indonesia']:>16.2f} | {RED}{winner1:<20}{RESET}")

    # 2. Presence Penalty Only
    adj2 = apply_penalties(initial_logits, counts, frequency_penalty=0.0, presence_penalty=2.0)
    winner2 = max(adj2, key=adj2.get)
    print(f"{'Presence Penalty Only (Pres=2.0)':<30} | {adj2['Jakarta']:>15.2f} | {adj2['Indonesia']:>16.2f} | {YELLOW}{winner2:<20}{RESET}")

    # 3. Frequency Penalty Only
    adj3 = apply_penalties(initial_logits, counts, frequency_penalty=1.0, presence_penalty=0.0)
    winner3 = max(adj3, key=adj3.get)
    print(f"{'Frequency Penalty Only (Freq=1.0)':<30} | {adj3['Jakarta']:>15.2f} | {adj3['Indonesia']:>16.2f} | {GREEN}{winner3:<20}{RESET}")

    # 4. Combined Penalties
    adj4 = apply_penalties(initial_logits, counts, frequency_penalty=1.0, presence_penalty=1.0)
    winner4 = max(adj4, key=adj4.get)
    print(f"{'Kombinasi (Freq=1.0, Pres=1.0)':<30} | {adj4['Jakarta']:>15.2f} | {adj4['Indonesia']:>16.2f} | {GREEN}{winner4:<20}{RESET}")

def demonstrate_text_looping_mitigation():
    print(f"\n{BOLD}{HEADER}=== DEMO 2: SIMULASI PENCEGAHAN LOOPING AI AGENT ==={RESET}\n")
    
    # Vocabulary & Transition rules
    base_vocab = ["Jakarta", "adalah", "ibu", "kota", "yang", "besar", "di", "Indonesia"]
    
    print(f"{BOLD}Analisis Perilaku Agent:{RESET}")
    print(f" • {BOLD}Tanpa Penalty (0.0, 0.0){RESET}: LLM rentan terjebak dalam siklus Paul-looping:")
    print(f"   {RED}'Jakarta adalah ibu kota. Jakarta adalah ibu kota Jakarta...'{RESET}")
    
    print(f"\n • {BOLD}Dengan Frequency Penalty (1.2){RESET}: Nilai logit token yang sudah pernah muncul terus diturunkan seiring waktu, memaksa model memilih frasa baru:")
    print(f"   {GREEN}'Jakarta adalah ibu kota yang besar di Indonesia. Kota ini pusat pemerintahan.'{RESET}")

def interactive_penalty_simulator():
    print(f"\n{BOLD}{HEADER}=== INTERACTIVE LOGIT SHIFT CALCULATOR ==={RESET}")
    try:
        freq_p = float(input("\nMasukkan Frequency Penalty (-2.0 s.d. 2.0): ").strip())
        pres_p = float(input("Masukkan Presence Penalty (-2.0 s.d. 2.0): ").strip())

        logits = {"AI": 4.0, "Agent": 3.8, "Sistem": 3.0, "Otomatis": 2.5}
        counts = {"AI": 3, "Agent": 2, "Sistem": 0, "Otomatis": 0}

        adjusted = apply_penalties(logits, counts, freq_p, pres_p)
        
        print(f"\n{BOLD}{CYAN}--- HASIL AKHIR MODIFIKASI LOGIT ---{RESET}")
        print(f"{'Token':<10} | {'Count':<6} | {'Logit Awal':<12} | {'Logit Penyesuaian':<18} | {'Perubahan':<10}")
        print("-" * 65)
        for tok in logits:
            diff = adjusted[tok] - logits[tok]
            print(f"{tok:<10} | {counts[tok]:<6} | {logits[tok]:>12.2f} | {BOLD}{adjusted[tok]:>18.2f}{RESET} | {YELLOW}{diff:>10.2f}{RESET}")

    except ValueError:
        print(f"{RED}Input tidak valid.{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 3.2: GENERATION CONTROLS - FREQUENCY & PRESENCE PENALTIES{RESET}")
    print(f"{CYAN}Sesuai dengan Gambar 1 (Generation Controls: Frequency Penalty, Presence Penalty){RESET}")
    print("█" * 75)

    demonstrate_penalty_math()
    demonstrate_text_looping_mitigation()

    print("\nIngin mencoba Kalkulator Penalty Interaktif?")
    ans = input("Jawab (y/n): ").strip().lower()
    if ans == 'y':
        interactive_penalty_simulator()

    print(f"\n{GREEN}✔ Modul 3.2 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
