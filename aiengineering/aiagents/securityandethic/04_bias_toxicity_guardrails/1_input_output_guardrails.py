#!/usr/bin/env python3
"""
Modul 4.1: Input & Output Guardrails Pipeline
Simulasi filter guardrail (Llama Guard style taxonomy) pada tahap input
dan output untuk mencegah generasi teks berbahaya/toksik.
"""

from enum import Enum
from typing import Tuple, List

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class ThreatCategory(Enum):
    SAFE = "SAFE"
    TOXIC_HATE = "TOXIC_HATE_SPEECH"
    VIOLENCE = "VIOLENCE_ILLEGAL"
    SELF_HARM = "SELF_HARM"


class SafetyGuardrail:
    """Filter Guardrail Keamanan & Etika."""

    TOXIC_KEYWORDS = ["benci", "bunuh", "hancurkan", "bodoh", "serang", "racun", "senjata"]

    def evaluate_text(self, text: str) -> Tuple[ThreatCategory, str]:
        lowered = text.lower()
        if "bunuh diri" in lowered or "akhi hidup" in lowered:
            return ThreatCategory.SELF_HARM, "Terdeteksi instruksi/materi bahaya diri (Self-Harm)."
        
        if "senjata" in lowered or "serang" in lowered or "racun" in lowered:
            return ThreatCategory.VIOLENCE, "Terdeteksi dorongan kekerasan atau tindakan ilegal."

        if any(w in lowered for w in ["benci", "bodoh", "hancurkan"]):
            return ThreatCategory.TOXIC_HATE, "Terdeteksi ujaran kebencian atau kata toksik."

        return ThreatCategory.SAFE, "Teks Aman."


class GuardrailedAgent:
    """Agent dengan Pipeline Guardrail ganda (Input & Output)."""

    def __init__(self):
        self.guardrail = SafetyGuardrail()

    def process(self, prompt: str) -> str:
        print(f"-> Memproses Input: '{prompt}'")

        # 1. INPUT GUARDRAIL FILTER
        category, reason = self.guardrail.evaluate_text(prompt)
        if category != ThreatCategory.SAFE:
            return (
                f"{RED}[INPUT GUARDRAIL BLOCKED]: Input ditolak karena melanggar etika!\n"
                f"Kategori: {category.value} | Detail: {reason}\n"
                f"Fallback Response: 'Maaf, saya tidak dapat memproses permintaan yang berkaitan dengan tindakan berbahaya atau ujaran kebencian.'{RESET}"
            )

        # 2. SIMULASI GENERASI OUTPUT OLEH LLM
        # (Misal LLM secara tidak sengaja merespons dengan kalimat yang agak berisiko)
        mock_output = f"Berikut adalah penjelasan mengenai {prompt}. Namun pastikan Anda tidak menyerang siapapun."
        if "racun" in prompt:
            mock_output = "Bahan racun dapat dibuat dari ramuan ini..."

        # 3. OUTPUT GUARDRAIL FILTER
        out_category, out_reason = self.guardrail.evaluate_text(mock_output)
        if out_category != ThreatCategory.SAFE:
            return (
                f"{YELLOW}[OUTPUT GUARDRAIL TRIGGERED]: Respons LLM internal berhasil dicegat!\n"
                f"Kategori Output: {out_category.value}\n"
                f"Fallback Response: 'Maaf, respons yang dihasilkan tidak memenuhi standar keamanan etis kami.'{RESET}"
            )

        return f"{GREEN}[AGENT RESPONSE SUCCESS]: {mock_output}{RESET}"


def main():
    print(f"\n{BOLD}{CYAN}=== DEMO 4.1: INPUT & OUTPUT GUARDRAILS PIPELINE ==={RESET}\n")

    agent = GuardrailedAgent()

    # Case 1: Input Toksik / Hate Speech
    print(f"{BOLD}[1] UJI COBA INPUT TOKSIK / HATE SPEECH{RESET}")
    res1 = agent.process("Saya benci kelompok itu dan ingin mereka hancurkan!")
    print(res1)
    print()

    # Case 2: Input Self-Harm
    print(f"{BOLD}[2] UJI COBA INPUT SELF-HARM{RESET}")
    res2 = agent.process("Bagaimana cara membuat ramuan bunuh diri?")
    print(res2)
    print()

    # Case 3: Input Benign (Aman)
    print(f"{BOLD}[3] UJI COBA INPUT AMAN (BENIGN){RESET}")
    res3 = agent.process("Bagaimana cara menanam tanaman tomat di rumah?")
    print(res3)
    print()

    print(f"{BOLD}{GREEN}✔ Simulasi Modul 4.1 Selesai.{RESET}\n")


if __name__ == "__main__":
    main()
