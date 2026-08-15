#!/usr/bin/env python3
"""
Modul 04: Use Examples in Your Prompt & Few-Shot Learning
---------------------------------------------------------
Simulasi pilar keempat Prompt Engineering dari roadmap.sh/ai-agents.
Menunjukkan kekuatan In-Context Learning (ICL) melalui demonstrasi Few-Shot Prompting,
perbandingan Zero-Shot vs Few-Shot pada penanganan edge cases, serta penyesuaian pola gaya output.
"""

import time
from dataclasses import dataclass
from typing import List, Dict

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"

@dataclass
class FewShotTestCase:
    task_name: str
    input_text: str
    zero_shot_prompt: str
    zero_shot_result: str
    few_shot_prompt: str
    few_shot_result: str
    why_few_shot_wins: str

class FewShotPromptingSimulator:
    def __init__(self):
        self.test_cases: List[FewShotTestCase] = [
            FewShotTestCase(
                task_name="Ekstraksi Entitas & Normalisasi Nomor Telepon",
                input_text="Kontak Pak Budi di 0812-3456-7890 atau kantor (021) 555-1234. Jangan panggil nomor lama +62 811-000-111.",
                zero_shot_prompt=(
                    "Ekstrak nomor telepon dari teks berikut dan ubah ke format internasional (+62):\n"
                    "\"Kontak Pak Budi di 0812-3456-7890 atau kantor (021) 555-1234. Jangan panggil nomor lama +62 811-000-111.\""
                ),
                zero_shot_result=(
                    "Nomor telepon yang ditemukan:\n"
                    "1. +6281234567890\n"
                    "2. +62215551234\n"
                    "3. +62811000111\n"
                    "(Gagal menyaring nomor lama yang dilarang karena tidak ada contoh penanganan negated entities)."
                ),
                few_shot_prompt=(
                    "Tugas: Ekstrak nomor telepon AKTIF saja dan ubah ke format internasional E.164 (+62).\n\n"
                    "CONTOH 1:\n"
                    "Input: Hubungi 0857-111-222, nomor tua 0812-000-000 sudah hangus.\n"
                    "Output: {\"active_numbers\": [\"+62857111222\"], \"ignored\": [\"0812-000-000 (hangus)\"]}\n\n"
                    "CONTOH 2:\n"
                    "Input: Telepon toko di (031) 888-9999.\n"
                    "Output: {\"active_numbers\": [\"+62318889999\"], \"ignored\": []}\n\n"
                    "INPUT:\n"
                    "Kontak Pak Budi di 0812-3456-7890 atau kantor (021) 555-1234. Jangan panggil nomor lama +62 811-000-111.\n"
                    "OUTPUT:"
                ),
                few_shot_result=(
                    "{\n"
                    "  \"active_numbers\": [\"+6281234567890\", \"+62215551234\"],\n"
                    "  \"ignored\": [\"+62811000111 (nomor lama)\"]\n"
                    "}"
                ),
                why_few_shot_wins="Contoh demonstrasi (Exemplars) melatih LLM mengenali pola pengabaian nomor tua & penyesuaian skema JSON."
            ),
            FewShotTestCase(
                task_name="Klasifikasi Log Sistem & Ekstraksi Severity",
                input_text="2026-07-26 14:02:11 [DB_POOL] Warning: Connection acquisition took 4200ms (> 3000ms threshold).",
                zero_shot_prompt="Klasifikasikan log ini ke status OK, WARN, atau CRITICAL.",
                zero_shot_result="Status: WARN (Karena terdapat kata Warning).",
                few_shot_prompt=(
                    "Tugas: Petakan log server ke status (OK, WARN, CRITICAL) dan kalkulasi latency_ms.\n\n"
                    "Contoh 1:\n"
                    "Input: [HTTP] 200 OK - 45ms\n"
                    "Output: STATUS=OK | LATENCY=45ms | METRIC=normal\n\n"
                    "Contoh 2:\n"
                    "Input: [DB_POOL] Warning: Connection acquisition took 4200ms (> 3000ms threshold).\n"
                    "Output: STATUS=CRITICAL | LATENCY=4200ms | METRIC=exceeded_threshold_high\n\n"
                    "INPUT: 2026-07-26 14:02:11 [DB_POOL] Warning: Connection acquisition took 4200ms (> 3000ms threshold).\n"
                    "OUTPUT:"
                ),
                few_shot_result="STATUS=CRITICAL | LATENCY=4200ms | METRIC=exceeded_threshold_high",
                why_few_shot_wins="Contoh 2 mengajarkan LLM bahwa meskipun teks memuat kata 'Warning', latency > 4000ms tergolong CRITICAL."
            )
        ]

    def render_header(self):
        print(f"\n{BOLD}{CYAN}=" * 75)
        print(f"{BOLD}{YELLOW}  PILAR 4: USE EXAMPLES IN YOUR PROMPT (IN-CONTEXT LEARNING)")
        print(f"{BOLD}{CYAN}=" * 75 + f"{RESET}\n")
        print(f"{GREEN}Prinsip Utama:{RESET} Memberikan 2-4 contoh pasangan Input-Output (Few-Shot Exemplars)")
        print(f"mengajarkan LLM logika spesifik, format keluaran, dan cara menangani edge cases.\n")

    def run_simulations(self):
        self.render_header()
        for idx, test in enumerate(self.test_cases, 1):
            print(f"{BOLD}{MAGENTA}[UJI FEW-SHOT #{idx}: {test.task_name}]{RESET}")
            print(f"{BOLD}Teks Input Raw:{RESET} \"{test.input_text}\"\n")
            
            print(f"{BOLD}{RED}❌ ZERO-SHOT PROMPT (Tanpa Contoh):{RESET}")
            print(f"   Prompt: \"{test.zero_shot_prompt}\"")
            print(f"{RED}   Hasil:{RESET} {test.zero_shot_result}\n")
            
            print(f"{BOLD}{GREEN}✅ FEW-SHOT PROMPT (Dengan Exemplars In-Context):{RESET}")
            print(f"{BLUE}   Prompt Terstruktur:{RESET}")
            for line in test.few_shot_prompt.split('\n'):
                print(f"     {line}")
            time.sleep(0.3)
            print(f"\n{CYAN}   Hasil Presisi ({test.task_name}):{RESET}")
            for line in test.few_shot_result.split('\n'):
                print(f"     {line}")
                
            print(f"\n{BOLD}{YELLOW}💡 Kunci Kemenangan Few-Shot:{RESET} {test.why_few_shot_wins}")
            print(f"{CYAN}-" * 75 + f"{RESET}\n")
            time.sleep(0.5)

    def print_few_shot_best_practices(self):
        print(f"{BOLD}{MAGENTA}📌 ANATOMI PENYUSUNAN FEW-SHOT EXEMPLARS:{RESET}")
        practices = [
            ("Keanekaragaman Contoh (Diversity)", "Sertakan contoh kasus sukses, kasus batas (edge case), dan kasus eror."),
            ("Pola Format Teratur (Consistent Formatting)", "Gunakan format label yang identik di setiap contoh (misal 'Input:' dan 'Output:')."),
            ("Urutan Contoh (Order Sensitivity)", "Letakkan contoh yang paling relevan dekat dengan input asli pengguna.")
        ]
        for idx, (title, desc) in enumerate(practices, 1):
            print(f"  {idx}. {BOLD}{GREEN}{title}{RESET}: {desc}")
        print()

def main():
    sim = FewShotPromptingSimulator()
    sim.run_simulations()
    sim.print_few_shot_best_practices()

if __name__ == "__main__":
    main()
