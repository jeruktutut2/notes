#!/usr/bin/env python3
"""
Modul 3.1: PII Detection & Redaction
Simulasi pendeteksian dan penyamaran PII (Personally Identifiable Information)
seperti Email, Nomor HP, KTP/NIK, Nomor Kartu Kredit, dan API Key sebelum diproses LLM.
"""

import re
from typing import Dict, Tuple

# ANSI Color formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


class PIIRedactor:
    """Mesin penyamar PII berbasis ekspresi reguler (Regex patterns)."""

    PII_PATTERNS = {
        "EMAIL": (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED_EMAIL]"),
        "PHONE": (r"(\+62|0)8[1-9][0-9]{7,10}", "[REDACTED_PHONE]"),
        "NIK_KTP": (r"\b[0-9]{16}\b", "[REDACTED_NIK]"),
        "CREDIT_CARD": (r"\b(?:\d[ -]*?){13,16}\b", "[REDACTED_CARD]"),
        "API_KEY": (r"(sk-[a-zA-Z0-9]{20,40}|SECRET_[a-zA-Z0-9_]+)", "[REDACTED_API_KEY]"),
    }

    def redact(self, text: str) -> Tuple[str, Dict[str, int]]:
        """Mengganti data PII dalam teks dengan token aman dan menghitung jumlah PII terdeteksi."""
        redacted_text = text
        stats = {}

        for pii_type, (pattern, replacement) in self.PII_PATTERNS.items():
            matches = re.findall(pattern, redacted_text)
            if matches:
                stats[pii_type] = len(matches)
                redacted_text = re.sub(pattern, replacement, redacted_text)

        return redacted_text, stats


def main():
    print(f"\n{BOLD}{CYAN}=== DEMO 3.1: PII DETECTION & REDACTION ==={RESET}\n")

    redactor = PIIRedactor()

    # Contoh Input User mengandung data PII sensitif
    raw_user_prompt = (
        "Halo, nama saya Budi Santoso. Email saya budi.santoso@gmail.com dan nomor telepon 081234567890. "
        "Nomor NIK KTP saya 3171012345670001. Untuk pembayaran transaksi, saya menggunakan kartu kredit 4532-1122-3344-5566. "
        "Tolong simpan juga API Key sk-proj99887766554433221100 ini."
    )

    print(f"{BOLD}[1] TEKS RAW UNTRUSTED SEBELUM SANITISASI:{RESET}")
    print(f"{RED}{raw_user_prompt}{RESET}\n")

    # Jalankan PII Redaction
    sanitized_prompt, stats = redactor.redact(raw_user_prompt)

    print(f"{BOLD}[2] RINGKASAN PII TERDETEKSI & DISAMARKAN:{RESET}")
    for pii_type, count in stats.items():
        print(f"  • {YELLOW}{pii_type}{RESET}: {count} item ditemukan & di-redact.")
    print()

    print(f"{BOLD}[3] TEKS AMAN YANG SIAP DIKIRIM KE LLM / MEMORY:{RESET}")
    print(f"{GREEN}{sanitized_prompt}{RESET}\n")

    print(f"{BOLD}{GREEN}✔ Simulasi Modul 3.1 Selesai.{RESET}\n")


if __name__ == "__main__":
    main()
