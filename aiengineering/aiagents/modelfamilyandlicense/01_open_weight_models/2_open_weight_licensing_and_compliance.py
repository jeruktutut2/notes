#!/usr/bin/env python3
"""
Modul 1.2: Open Weight Licensing & Compliance Audit
Analisis Komparatif Lisensi Open Weight vs OSI Open Source & Simulasi Kepatuhan Legal
Berdasarkan Roadmap.sh / AI Agents - Model Families and Licences
"""

import sys
from dataclasses import dataclass
from typing import List, Dict

# ANSI Colors
HEADER = "\033[95m"
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

@dataclass
class LicenseProfile:
    name: str
    osi_approved: bool
    commercial_allowed: bool
    mau_threshold: str
    synthetic_data_restriction: str
    attribution_required: bool
    derivative_distribution_rule: str
    summary_id: str

LICENSES: Dict[str, LicenseProfile] = {
    "apache_2": LicenseProfile(
        name="Apache License 2.0",
        osi_approved=True,
        commercial_allowed=True,
        mau_threshold="Tidak ada batasan MAU",
        synthetic_data_restriction="Bebas digunakan untuk melatih model lain",
        attribution_required=True,
        derivative_distribution_rule="Bebas didistribusikan ulang dengan pemberitahuan lisensi asli",
        summary_id="Sangat Permisif (Ideal untuk Komersial & Enterprise)"
    ),
    "mit": LicenseProfile(
        name="MIT License",
        osi_approved=True,
        commercial_allowed=True,
        mau_threshold="Tidak ada batasan MAU",
        synthetic_data_restriction="Bebas digunakan tanpa batasan",
        attribution_required=True,
        derivative_distribution_rule="Bebas tanpa batasan khusus",
        summary_id="Sangat Permisif & Ringkas"
    ),
    "llama_3": LicenseProfile(
        name="Llama 3 Community License (Meta)",
        osi_approved=False,  # Memiliki batasan MAU & Penggunaan Nama
        commercial_allowed=True,
        mau_threshold="Dilarang jika MAU > 700 Juta pada bulan sebelumnya (wajib lisensi khusus dari Meta)",
        synthetic_data_restriction="Boleh pakai output Llama untuk melatih model lain KECUALI model kompetitor yang bernama Llama",
        attribution_required=True,
        derivative_distribution_rule="Wajib mencantumkan 'Built with Meta Llama 3'",
        summary_id="Open Weight Komersial dengan Threshold MAU Raksasa"
    ),
    "gemma": LicenseProfile(
        name="Gemma Terms of Use (Google)",
        osi_approved=False,
        commercial_allowed=True,
        mau_threshold="Tidak ada batasan MAU numerik",
        synthetic_data_restriction="Mematuhi Google Prohibited Use Policy (dilarang untuk pembuatan senjata, medis tanpa supervisi)",
        attribution_required=True,
        derivative_distribution_rule="Wajib menyertakan pemberitahuan hak cipta Google Gemma",
        summary_id="Open Weight Komersial dengan Restriction Ethic / Use-Case"
    ),
    "rail": LicenseProfile(
        name="OpenRAIL (Responsible AI License)",
        osi_approved=False,
        commercial_allowed=True,
        mau_threshold="Bervariasi",
        synthetic_data_restriction="Terikat klausa penggunaan etis (Anti-Surveillance, Anti-Deepfake berbahaya)",
        attribution_required=True,
        derivative_distribution_rule="Lisensi turunan wajib mewarisi pembatasan OpenRAIL yang sama",
        summary_id="Ethical Open License dengan Enforcement Penggunaan"
    )
}

def display_license_comparison_table():
    print(f"\n{BOLD}{HEADER}=== TABLE ANALISIS LISENSI MODEL OPEN WEIGHT ==={RESET}\n")
    print(f"{'Lisensi':<28} | {'OSI?':<5} | {'Komersial?':<10} | {'Aturan MAU & Batasan Khusus':<45}")
    print("-" * 95)
    for key, lic in LICENSES.items():
        osi_str = f"{GREEN}Ya{RESET}" if lic.osi_approved else f"{RED}Tidak{RESET}"
        comm_str = f"{GREEN}Ya{RESET}" if lic.commercial_allowed else f"{RED}Tidak{RESET}"
        print(f"{CYAN}{lic.name:<28}{RESET} | {osi_str:<14} | {comm_str:<19} | {YELLOW}{lic.mau_threshold[:45]:<45}{RESET}")

def run_compliance_audit_simulator():
    print(f"\n{BOLD}{HEADER}=== INTERACTIVE COMPLIANCE AUDIT TOOL UNTUK AI AGENTS ==={RESET}")
    print("Jawab pertanyaan berikut untuk mengevaluasi kepatuhan legal proyek Agent Anda:\n")
    
    try:
        print(f"{BOLD}1. Pilih Model Family yang digunakan dalam Agent Anda:{RESET}")
        print("   a) Llama 3.1 / 3.3 (Meta)")
        print("   b) DeepSeek R1 / V3 (MIT License)")
        print("   c) Mixtral 8x7B (Apache 2.0)")
        print("   d) Gemma 2 (Google)")
        choice_model = input("Pilihan (a/b/c/d): ").strip().lower()

        print(f"\n{BOLD}2. Berapa perkiraan Monthly Active Users (MAU) aplikasi Anda?:{RESET}")
        mau_input = float(input("Jumlah MAU (dalam jutaan, misal 0.5 atau 800): ").strip())

        print(f"\n{BOLD}3. Apakah Anda menggunakan output model ini untuk melatih model bahasa lain?:{RESET}")
        train_compete = input("Jawab (y/n): ").strip().lower() == 'y'

        print(f"\n{BOLD}4. Apakah Anda mencantumkan atribut nama lisensi asli pada aplikasi/SaaS Anda?:{RESET}")
        has_attribution = input("Jawab (y/n): ").strip().lower() == 'y'

        print(f"\n{BOLD}{GREEN}=================== LAPORAN HASIL AUDIT LEGAL ==================={RESET}")
        
        target_lic = None
        if choice_model == 'a':
            target_lic = LICENSES["llama_3"]
        elif choice_model == 'b':
            target_lic = LICENSES["mit"]
        elif choice_model == 'c':
            target_lic = LICENSES["apache_2"]
        else:
            target_lic = LICENSES["gemma"]

        issues = []
        warnings = []

        # Check MAU limit
        if choice_model == 'a' and mau_input > 700.0:
            issues.append(" ❌ Pelanggaran Llama 3 License: MAU pengguna melebihi 700 Juta/bulan. Anda WAJIB mengajukan lisensi enterprise khusus kepada Meta.")
        else:
            print("  ✔ Batasan MAU: AMAN")

        # Check Synthetic Data
        if train_compete:
            if choice_model == 'a':
                warnings.append(" ⚠️ Perhatian Llama 3 License: Output Llama dilarang digunakan untuk melatih model yang bersaing bernama Llama.")
            elif choice_model in ['b', 'c']:
                print("  ✔ Synthetic Data Training: BEBAS (Permissive MIT/Apache 2.0)")

        # Check Attribution
        if not has_attribution and target_lic.attribution_required:
            issues.append(f" ❌ Kurang Atribusi: Lisensi {target_lic.name} mengharuskan pemuatan teks hak cipta / 'Built with Meta Llama' pada dokumentasi/aplikasi.")

        print(f"\n  • Lisensi yang Berlaku : {BOLD}{CYAN}{target_lic.name}{RESET}")
        print(f"  • Kategori OSI Approved: {target_lic.osi_approved}")
        
        if not issues and not warnings:
            print(f"\n{GREEN}{BOLD}STATUS: FULLY COMPLIANT (Aman untuk Komersial & Production Deployment){RESET}")
        else:
            if issues:
                print(f"\n{RED}{BOLD}TEMUAN PELANGGARAN CRITICAL:{RESET}")
                for i in issues:
                    print(i)
            if warnings:
                print(f"\n{YELLOW}{BOLD}PERATURAN TAMBAHAN (WARNINGS):{RESET}")
                for w in warnings:
                    print(w)

    except ValueError:
        print(f"{RED}Input tidak valid.{RESET}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 1.2: OPEN WEIGHT LICENSING & COMPLIANCE AUDIT{RESET}")
    print(f"{CYAN}Berdasarkan roadmap.sh/ai-agents (Model Families and Licences){RESET}")
    print("█" * 75)

    display_license_comparison_table()
    run_compliance_audit_simulator()

    print(f"\n{GREEN}✔ Modul 1.2 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
