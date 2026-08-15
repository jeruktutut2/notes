#!/usr/bin/env python3
"""
SIMULASI MODUL 1.2: Self-Consistency Chain of Thought (CoT)
Berdasarkan AI Agent Roadmap (roadmap.sh/ai-agents)

Modul ini mensimulasikan teknik Self-Consistency (Wang et al., 2022) di mana agen
meregenerasi N jalur penalaran acak (Sampling dengan Temperature > 0) dan melakukan
Majority Voting (pilihan terbanyak) untuk menentukan kesimpulan akhir.
"""

import time
import random
from collections import Counter
from typing import List, Dict, Any

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"

# Complex riddle problem suitable for Self-Consistency
PROBLEM = {
    "question": "Di sebuah ruangan ada 4 orang: Alex, Bella, Candra, dan Dini. Alex melihat Bella dan Candra. Bella hanya melihat Dini. Candra melihat Alex dan Dini. Dini tidak melihat siapa pun. Jika seseorang bisa melihat orang lain, maka orang itu dianggap 'mengetahui posisi' orang tersebut. Berapa orang yang posisinya diketahui oleh setidaknya 2 orang lain?",
    "sample_paths": [
        {
            "path_id": 1,
            "reasoning": [
                "Siapa yang melihat Alex? Candra melihat Alex. (1 orang)",
                "Siapa yang melihat Bella? Alex melihat Bella. (1 orang)",
                "Siapa yang melihat Candra? Alex melihat Candra. (1 orang)",
                "Siapa yang melihat Dini? Bella melihat Dini DAN Candra melihat Dini. (2 orang: Bella & Candra)",
                "Jadi hanya Dini yang posisinya diketahui oleh 2 orang lain."
            ],
            "answer": "1 orang (Dini)"
        },
        {
            "path_id": 2,
            "reasoning": [
                "Mari daftar siapa saja yang dilihat oleh tiap orang:",
                "- Alex melihat: Bella, Candra",
                "- Bella melihat: Dini",
                "- Candra melihat: Alex, Dini",
                "- Dini melihat: (kosong)",
                "Sekarang hitung berapa kali nama muncul sebagai target penglihatan:",
                "- Alex: 1 kali (oleh Candra)",
                "- Bella: 1 kali (oleh Alex)",
                "- Candra: 1 kali (oleh Alex)",
                "- Dini: 2 kali (oleh Bella dan Candra)",
                "Maka hanya ada 1 orang (Dini) yang posisinya diketahui oleh setidaknya 2 orang."
            ],
            "answer": "1 orang (Dini)"
        },
        {
            "path_id": 3,
            "reasoning": [
                "Alex dipantau oleh Candra (1). Bella dipantau oleh Alex (1).",
                "Candra dipantau oleh Alex (1). Dini dipantau oleh Bella dan Candra (2).",
                "Alex juga tahu posisi Bella. Jadi Bella & Candra tahu Dini = 2 orang.",
                "Jawaban: 1 orang"
            ],
            "answer": "1 orang (Dini)"
        },
        {
            "path_id": 4,
            "reasoning": [
                "Masing-masing orang melihat 2 orang lain kecuali Dini. Jadi total ada 4 orang yang saling lihat.",
                "Maka jawabannya adalah 2 orang."
            ],
            "answer": "2 orang (Kesalahan Logika)"
        },
        {
            "path_id": 5,
            "reasoning": [
                "Penalaran: Dini dilihat oleh 2 orang (Bella dan Candra). Yang lain hanya dilihat oleh 1 orang.",
                "Hasil: 1 orang"
            ],
            "answer": "1 orang (Dini)"
        }
    ]
}

def run_self_consistency(problem: Dict[str, Any], num_samples: int = 5):
    print(f"\n{BOLD}{CYAN}=== MENJALANKAN SELF-CONSISTENCY CoT SAMPLING (N={num_samples}) ==={RESET}\n")
    print(f"{BOLD}Pertanyaan:{RESET} {problem['question']}\n")
    
    collected_answers = []
    
    for idx, path in enumerate(problem["sample_paths"], 1):
        print(f"{BOLD}{MAGENTA}--- Jalur Penalaran #{idx} (Temperature = 0.7) ---{RESET}")
        for step in path["reasoning"]:
            print(f"  💭 {step}")
            time.sleep(0.15)
        print(f"  {YELLOW}➔ Extracted Answer: {path['answer']}{RESET}\n")
        collected_answers.append(path['answer'])
    
    # Majority Voting
    print(f"{BOLD}{GREEN}======================================================================{RESET}")
    print(f"{BOLD}{GREEN}                 PROSES MAJORITY VOTING (CONSENSUS)                   {RESET}")
    print(f"{BOLD}{GREEN}======================================================================{RESET}")
    
    counts = Counter(collected_answers)
    for ans, count in counts.most_common():
        percentage = (count / num_samples) * 100
        bar = "█" * (count * 6)
        print(f"  {ans:<30} | {count}/{num_samples} vote ({percentage:.0f}%) {GREEN}{bar}{RESET}")
    
    final_winner, win_count = counts.most_common(1)[0]
    print(f"\n{BOLD}{GREEN}✓ Konsensus Akhir (Self-Consistency Winner): {final_winner} dengan {win_count}/{num_samples} suara.{RESET}")
    print(f"{CYAN}Keunggulan: Mengurangi dampak hallucinatory / salah satu jalur penalaran individual.{RESET}\n")

def main():
    print(f"\n{BOLD}{MAGENTA}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}   SIMULASI SELF-CONSISTENCY CHAIN OF THOUGHT (MAJORITY VOTING)       {RESET}")
    print(f"{BOLD}{MAGENTA}======================================================================{RESET}")
    
    run_self_consistency(PROBLEM, num_samples=5)

if __name__ == "__main__":
    main()
