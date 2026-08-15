#!/usr/bin/env python3
"""
Modul 05: Iterate and Test Your Prompts & Automated Evaluation
--------------------------------------------------------------
Simulasi pilar kelima Prompt Engineering dari roadmap.sh/ai-agents.
Menunjukkan siklus pengembangan prompt melalui pengujian terotomatisasi (Prompt Benchmarking),
A/B testing antara Prompt v1 (Unoptimized) vs Prompt v2 (Optimized), serta pengukuran metrik kepatuhan.
"""

import time
from dataclasses import dataclass
from typing import List, Dict, Tuple

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
class EvalTestCase:
    test_id: str
    user_input: str
    expected_keyword: str
    expected_format: str

@dataclass
class PromptVersion:
    version_name: str
    prompt_template: str

class PromptBenchmarkSuite:
    def __init__(self):
        self.test_cases: List[EvalTestCase] = [
            EvalTestCase("TC-01", "Sensor suhu A3 mencatat 92C melebihi batas 85C", "CRITICAL", "JSON"),
            EvalTestCase("TC-02", "Server pings 24ms normal", "OK", "JSON"),
            EvalTestCase("TC-03", "Data kosong / null dari modem B12", "UNKNOWN", "JSON"),
            EvalTestCase("TC-04", "Percobaan login gagal 5x dari IP 192.168.1.50", "WARNING", "JSON"),
            EvalTestCase("TC-05", "Memory usage 99% swap active", "CRITICAL", "JSON")
        ]

        self.prompt_v1 = PromptVersion(
            version_name="Prompt v1.0 (Draft Awal - Tanpa Constraints)",
            prompt_template="Klasifikasikan log ini dan berikan output dalam JSON: {input}"
        )

        self.prompt_v2 = PromptVersion(
            version_name="Prompt v2.0 (Optimized - Role, Few-Shot, Guardrails)",
            prompt_template=(
                "Anda adalah Automated Log Classifier Agen.\n"
                "Ubah log berikut menjadi JSON murni dengan format: {\"status\": \"OK|WARNING|CRITICAL|UNKNOWN\", \"input\": \"...\"}\n"
                "Aturan Strict: Dilarang menyertakan teks pembuka/penutup markdown. HANYA valid JSON.\n"
                "Log: {input}"
            )
        )

    def render_header(self):
        print(f"\n{BOLD}{CYAN}=" * 75)
        print(f"{BOLD}{YELLOW}  PILAR 5: ITERATE AND TEST YOUR PROMPTS (AUTOMATED EVALUATION)")
        print(f"{BOLD}{CYAN}=" * 75 + f"{RESET}\n")
        print(f"{GREEN}Prinsip Utama:{RESET} Prompt adalah KODE. Wajib diuji menggunakan dataset pengujian (Eval Dataset)")
        print(f"untuk mengukur Akurasi Format, Kepatuhan Kata Kunci, dan Mencegah Regresi.\n")

    def simulate_llm_call(self, version: PromptVersion, test_case: EvalTestCase) -> Tuple[str, bool, bool]:
        """
        Mensimulasikan eksekusi LLM untuk Prompt v1 vs v2
        Mengembalikan: (output_text, is_format_valid, is_keyword_correct)
        """
        if version.version_name.startswith("Prompt v1.0"):
            # Prompt v1 sering menyertakan Markdown wrapper & salah klasifikasi pada edge case TC-03
            if test_case.test_id == "TC-01":
                out = "```json\n{\"status\": \"CRITICAL\"}\n```"
                return out, False, True # Markdown wrapper (Format failure)
            elif test_case.test_id == "TC-02":
                out = "Tentu, ini status log Anda: {\"status\": \"OK\"}"
                return out, False, True # Teks pembuka (Format failure)
            elif test_case.test_id == "TC-03":
                out = "{\"status\": \"OK\"}" # Halusinasi OK padahal data null/UNKNOWN
                return out, True, False # Format OK, Keyword Fail
            elif test_case.test_id == "TC-04":
                out = "{\"status\": \"WARN\"}" # Pakai WARN alih-alih WARNING
                return out, True, False
            else:
                out = "{\"status\": \"CRITICAL\"}"
                return out, True, True
        else:
            # Prompt v2.0 lulus seluruh pengujian
            out = f"{{\"status\": \"{test_case.expected_keyword}\", \"input\": \"{test_case.user_input[:20]}...\"}}"
            return out, True, True

    def run_ab_benchmark(self):
        self.render_header()
        
        versions = [self.prompt_v1, self.prompt_v2]
        
        for ver in versions:
            print(f"{BOLD}{MAGENTA}🧪 MENJALANKAN BENCHMARK EVALUASI: {ver.version_name}{RESET}")
            print(f"{BLUE}Template Prompt:{RESET}\n  \"{ver.prompt_template[:80]}...\"\n")
            
            format_passed = 0
            keyword_passed = 0
            total = len(self.test_cases)
            
            print(f"{BOLD}{'ID':<6} | {'Input snippet':<30} | {'Expected':<10} | {'Format Valid':<12} | {'Akurasi'}{RESET}")
            print("-" * 75)
            
            for tc in self.test_cases:
                time.sleep(0.15)
                output, fmt_ok, kw_ok = self.simulate_llm_call(ver, tc)
                
                fmt_str = f"{GREEN}PASS{RESET}" if fmt_ok else f"{RED}FAIL{RESET}"
                kw_str = f"{GREEN}PASS{RESET}" if kw_ok else f"{RED}FAIL{RESET}"
                
                if fmt_ok: format_passed += 1
                if kw_ok: keyword_passed += 1
                
                print(f"{tc.test_id:<6} | {tc.user_input[:28]:<30} | {tc.expected_keyword:<10} | {fmt_str:<21} | {kw_str}")
                
            fmt_rate = (format_passed / total) * 100
            kw_rate = (keyword_passed / total) * 100
            
            print("-" * 75)
            print(f"{BOLD}📊 STATISTIK HASIL EVALUASI ({ver.version_name[:11]}):{RESET}")
            print(f"   • Format Compliance Rate : {GREEN if fmt_rate == 100 else RED}{fmt_rate:.1f}%{RESET}")
            print(f"   • Accuracy Pass Rate      : {GREEN if kw_rate == 100 else RED}{kw_rate:.1f}%{RESET}")
            print(f"{CYAN}=" * 75 + f"{RESET}\n")

    def print_iteration_workflow(self):
        print(f"{BOLD}{MAGENTA}🔄 SKEMA DEDIKASI SIKLUS PROMPT ITERATION:{RESET}")
        steps = [
            ("1. Baseline Drafting", "Tulis prompt versi awal sederhana."),
            ("2. Test Dataset Creation", "Buat 10-50 kasus uji mencakup Happy Path & Edge Cases."),
            ("3. Automated Execution", "Jalankan skrip evaluasi & catat kegagalan."),
            ("4. Root Cause Failure Analysis", "Identifikasi penyebab eror (apakah kurang konteks, ambigu, atau format melenceng)."),
            ("5. Prompt Refinement & Regression Check", "Perbaiki prompt dan pastikan kasus uji lama tidak rusak (No Regression).")
        ]
        for step, desc in steps:
            print(f"  • {BOLD}{GREEN}{step}{RESET}: {desc}")
        print()

def main():
    suite = PromptBenchmarkSuite()
    suite.run_ab_benchmark()
    suite.print_iteration_workflow()

if __name__ == "__main__":
    main()
