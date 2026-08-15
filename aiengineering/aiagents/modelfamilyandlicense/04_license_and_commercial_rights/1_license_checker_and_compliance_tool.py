#!/usr/bin/env python3
"""
Modul 4.1: License Checker & Commercial Compliance Tool
Audit Kepatuhan Lisensi Komersial, EU AI Act Risk Tier & Aturan Redistribusi Model Agent
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
class LicenseCheckResult:
    model_name: str
    license_name: str
    risk_level: str   # "LOW", "MEDIUM", "HIGH"
    compliance_items: List[str]
    prohibited_actions: List[str]
    required_attribution: str

def evaluate_project_scenario(
    model_choice: str,
    is_commercial: bool,
    mau_count_m: float,
    trains_other_models: bool,
    is_healthcare_or_finance: bool
) -> LicenseCheckResult:
    
    if model_choice == "llama3":
        risk = "LOW"
        prohibited = ["Dilarang melatih model bahasa lain dengan nama Llama"]
        compliance = [
            "Wajib menyertakan teks 'Built with Meta Llama 3' pada UI / dokumentasi",
            "Menyertakan salinan Llama 3 Community License pada redistribusi"
        ]
        if mau_count_m > 700.0:
            risk = "HIGH"
            prohibited.append("MAU > 700 Juta: WAJIB mengajukan lisensi khusus dari Meta sebelum launching!")
        
        return LicenseCheckResult(
            model_name="Llama 3.1 / 3.3",
            license_name="Llama 3 Community License",
            risk_level=risk,
            compliance_items=compliance,
            prohibited_actions=prohibited,
            required_attribution="Built with Meta Llama 3"
        )
        
    elif model_choice == "mixtral":
        return LicenseCheckResult(
            model_name="Mixtral 8x7B / Mistral 7B",
            license_name="Apache 2.0 License",
            risk_level="LOW",
            compliance_items=["Bebas digunakan secara komersial", "Bebas didistribusikan & diubah"],
            prohibited_actions=["Dilarang menghapus pemberitahuan Hak Cipta asli"],
            required_attribution="Apache 2.0 License Notice"
        )
        
    elif model_choice == "deepseek":
        prohibited = []
        if trains_other_models:
            prohibited.append("Perhatikan Syarat Layanan Cloud API jika menggunakan DeepSeek API komersial")
        return LicenseCheckResult(
            model_name="DeepSeek R1 / V3",
            license_name="MIT License (Open Weights)",
            risk_level="LOW",
            compliance_items=["Bebas komersial sepenuhnya", "Sangat permisif"],
            prohibited_actions=prohibited,
            required_attribution="MIT Copyright Notice"
        )
    else:  # Closed API (GPT-4o / Claude 3.5)
        risk = "MEDIUM" if is_healthcare_or_finance else "LOW"
        return LicenseCheckResult(
            model_name="Proprietary API (GPT-4o / Claude 3.5)",
            license_name="Commercial Terms of Service",
            risk_level=risk,
            compliance_items=[
                "Wajib menggunakan Business / Enterprise Plan dengan ZDR untuk privasi data",
                "Mematuhi Rate Limits (RPM/TPM) provider"
            ],
            prohibited_actions=[
                "Dilarang menggunakan output API untuk melatih model bahasa komersial yang bersaing"
            ],
            required_attribution="Tidak diwajibkan (bebas white-label)"
        )

def run_interactive_compliance_checker():
    print(f"\n{BOLD}{HEADER}=== INTERACTIVE LEGAL & COMPLIANCE AUDIT AUDITOR ==={RESET}\n")
    
    print(f"{BOLD}Pilih Model Family yang digunakan:{RESET}")
    print(" 1. Llama 3.1 / 3.3 (Meta)")
    print(" 2. Mixtral 8x7B (Mistral AI - Apache 2.0)")
    print(" 3. DeepSeek R1 / V3 (MIT License)")
    print(" 4. Proprietary API (OpenAI GPT-4o / Anthropic Claude 3.5)")
    
    choice = input("\nPilihan (1-4): ").strip()
    model_map = {"1": "llama3", "2": "mixtral", "3": "deepseek", "4": "closed_api"}
    selected_model = model_map.get(choice, "llama3")

    mau_input = float(input("Perkiraan Monthly Active Users (MAU) dalam jutaan (misal: 10 atau 800): ").strip())
    is_comm = input("Apakah produk bersifat Komersial / SaaS? (y/n): ").strip().lower() == 'y'
    trains_models = input("Apakah Anda melatih model turunan dari output LLM ini? (y/n): ").strip().lower() == 'y'
    is_regulated = input("Apakah dioperasikan di sektor teregulasi (Kesehatan/Perbankan)? (y/n): ").strip().lower() == 'y'

    res = evaluate_project_scenario(selected_model, is_comm, mau_input, trains_models, is_regulated)

    print(f"\n{BOLD}{GREEN}=================== HASIL AUDIT KEPATUHAN LEGAL ==================={RESET}")
    print(f" • Model Evaluasi       : {BOLD}{CYAN}{res.model_name}{RESET}")
    print(f" • Jenis Lisensi        : {res.license_name}")
    
    color_risk = GREEN if res.risk_level == "LOW" else (YELLOW if res.risk_level == "MEDIUM" else RED)
    print(f" • Tingkat Risiko Legal : {color_risk}{BOLD}{res.risk_level}{RESET}\n")

    print(f"{BOLD}Item Kepatuhan Yang Wajib Dipenuhi:{RESET}")
    for item in res.compliance_items:
        print(f"  ✔ {item}")

    if res.prohibited_actions:
        print(f"\n{BOLD}{RED}Tindakan Yang Dilarang (Prohibited Actions):{RESET}")
        for p in res.prohibited_actions:
            print(f"  ❌ {p}")

    print(f"\n{BOLD}Persyaratan Atribusi:{RESET}")
    print(f"  ℹ {res.required_attribution}")

def main():
    print("█" * 75)
    print(f"{BOLD}{HEADER}MODUL 4.1: LICENSE CHECKER & COMMERCIAL COMPLIANCE TOOL{RESET}")
    print(f"{CYAN}Berdasarkan roadmap.sh/ai-agents (Model Families and Licences){RESET}")
    print("█" * 75)

    run_interactive_compliance_checker()

    print(f"\n{GREEN}✔ Modul 4.1 Selesai.{RESET}\n")

if __name__ == "__main__":
    main()
