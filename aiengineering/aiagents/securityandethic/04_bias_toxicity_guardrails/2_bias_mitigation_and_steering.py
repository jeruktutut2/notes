#!/usr/bin/env python3
"""
Modul 4.2: Bias Mitigation & Steering
Simulasi pendeteksian dan mitigasi bias demografis/gender pada hasil rekomendasi Agent
menggunakan System Prompt Steering dan Iterative Self-Correction.
"""

from typing import Dict, Any, List

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class BiasEvaluator:
    """Evaluator untuk mendeteksi stereotip gender atau bias pekerjaan."""

    GENDER_STEREOTYPES = {
        "perawat": "wanita",
        "sekretaris": "wanita",
        "insinyur": "pria",
        "ceo": "pria",
        "pilot": "pria"
    }

    def detect_bias(self, text: str) -> bool:
        lowered = text.lower()
        # Jika teks secara eksplisit mengasosiasikan peran tertentu secara eksklusif dengan satu gender
        if "perawat biasanya wanita" in lowered or "insinyur harus pria" in lowered or "hanya pria" in lowered:
            return True
        return False


class BiasedVsSteeredAgent:
    """Agent perbandingan antara Unsteered (Biased) dan Steered (Unbiased)."""

    def __init__(self):
        self.evaluator = BiasEvaluator()

    def generate_unsteered_recommendation(self, query: str) -> str:
        """Simulasi Agent tanpa System Steering (rentan terhadap bias data pelatihan)."""
        if "rekrutmen perawat dan insinyur" in query.lower():
            return "Untuk posisi perawat sebaiknya utamakan pelamar wanita, dan untuk insinyur utamakan pelamar pria."
        return "Rekomendasi standar."

    def generate_steered_recommendation(self, query: str) -> str:
        """Simulasi Agent dengan System Steering + Self-Correction Loop."""
        # Step 1: Generasi awal
        raw_output = self.generate_unsteered_recommendation(query)

        # Step 2: Bias Evaluation
        has_bias = self.evaluator.detect_bias(raw_output)

        if has_bias:
            # Step 3: Self-Correction / Steering Refinement Loop
            corrected_output = (
                "[STEERED & SELF-CORRECTED]: Rekomendasi kualifikasi rekrutmen berbasis kompetensi objektif:\n"
                "• Posisi Perawat: Terbuka untuk seluruh gender berdasarkan pengalaman klinis dan lisensi keperawatan.\n"
                "• Posisi Insinyur: Terbuka untuk seluruh gender berdasarkan kemampuan teknis dan portofolio rekayasa."
            )
            return corrected_output

        return raw_output


def main():
    print(f"\n{BOLD}{CYAN}=== DEMO 4.2: BIAS MITIGATION & STEERING ==={RESET}\n")

    agent = BiasedVsSteeredAgent()
    user_query = "Berikan saran kriteria awal untuk rekrutmen perawat dan insinyur di rumah sakit kami."

    print(f"User Query: {YELLOW}'{user_query}'{RESET}\n")

    # 1. Tanpa Steering (Unsteered / Biased Agent)
    print(f"{BOLD}[1] RESPON AGENT TANPA MITIGASI BIAS (UNSTEERED):{RESET}")
    unsteered_res = agent.generate_unsteered_recommendation(user_query)
    print(f"{RED}{unsteered_res}{RESET}\n")

    # 2. Dengan Steering & Self-Correction (Steered / Unbiased Agent)
    print(f"{BOLD}[2] RESPON AGENT DENGAN STEERING & SELF-CORRECTION (UNBIASED):{RESET}")
    steered_res = agent.generate_steered_recommendation(user_query)
    print(f"{GREEN}{steered_res}{RESET}\n")

    print(f"{BOLD}{GREEN}✔ Simulasi Modul 4.2 Selesai.{RESET}\n")


if __name__ == "__main__":
    main()
