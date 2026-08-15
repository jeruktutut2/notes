#!/usr/bin/env python3
"""
Modul 3: Fine-Tuning vs Prompt Engineering Decision Simulator
Simulasi komparatif antara Prompt Engineering (In-Context Learning / Few-Shot / RAG)
dengan Parameter-Efficient Fine-Tuning (LoRA / QLoRA) untuk adaptasi domain AI Agent.
"""

from dataclasses import dataclass
from typing import Dict, Any

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
class AdaptationApproach:
    name: str
    upfront_cost_usd: float
    time_to_deploy: str
    token_input_overhead_per_req: int
    format_consistency_score: int  # 1 - 10
    knowledge_update_ease: int     # 1 - 10
    catastrophic_forgetting_risk: str

def get_approaches() -> Dict[str, AdaptationApproach]:
    return {
        "prompt_eng": AdaptationApproach(
            name="Prompt Engineering (Few-Shot & System Instructions)",
            upfront_cost_usd=0.0,
            time_to_deploy="5 Menit",
            token_input_overhead_per_req=1500,  # Menyertakan instruksi panjang & 3 contoh Few-Shot
            format_consistency_score=7,
            knowledge_update_ease=10,  # Tinggal ubah teks prompt
            catastrophic_forgetting_risk="Tidak Ada (Bobot Asli Utuh)"
        ),
        "rag": AdaptationApproach(
            name="RAG + Prompt Engineering",
            upfront_cost_usd=50.0,  # Biaya setup vector DB awal
            time_to_deploy="1-2 Hari",
            token_input_overhead_per_req=1000,  # Context retrieval top-k
            format_consistency_score=8,
            knowledge_update_ease=10,  # Tinggal update dokumen di Vector DB
            catastrophic_forgetting_risk="Tidak Ada"
        ),
        "lora_ft": AdaptationApproach(
            name="LoRA Fine-Tuning (PEFT - Local 8B / Cloud API)",
            upfront_cost_usd=150.0,  # GPU Rent / Cloud FT job
            time_to_deploy="1-2 Minggu (Data prep + Training)",
            token_input_overhead_per_req=150,   # Hanya butuh prompt singkat, format sudah terkunci di bobot
            format_consistency_score=10,
            knowledge_update_ease=3,   # Perlu re-training dataset baru
            catastrophic_forgetting_risk="Sedang (Penalaran umum bisa berkurang)"
        )
    }

def calculate_roi_over_requests(requests_count: int, input_price_per_1m: float = 2.50) -> Dict[str, float]:
    """Menghitung total akumulasi biaya (Upfront + Token Input) untuk N requests."""
    approaches = get_approaches()
    results = {}
    
    for key, app in approaches.items():
        # Token cost = (Requests * Overhead per req / 1,000,000) * Price per 1M
        token_cost = (requests_count * app.token_input_overhead_per_req / 1_000_000) * input_price_per_1m
        total_cost = app.upfront_cost_usd + token_cost
        results[key] = total_cost
        
    return results

def run_demo():
    print(f"\n{BOLD}{HEADER}=== MATRIKS KEPUTUSAN: FINE-TUNING VS PROMPT ENGINEERING ==={RESET}\n")
    print(f"{CYAN}Membandingkan 3 pendekatan adaptasi domain untuk AI Agent:{RESET}")
    
    approaches = get_approaches()
    for app in approaches.values():
        print(f"\n{BOLD}🔹 {app.name}{RESET}")
        print(f"  • Biaya Awal (Upfront)      : ${app.upfront_cost_usd:.2f}")
        print(f"  • Waktu Implementasi        : {app.time_to_deploy}")
        print(f"  • Token Input Overhead      : {app.token_input_overhead_per_req} tokens/request")
        print(f"  • Konsistensi Format (1-10) : {GREEN}{app.format_consistency_score}/10{RESET}")
        print(f"  • Kemudahan Update Data     : {YELLOW}{app.knowledge_update_ease}/10{RESET}")
        print(f"  • Risiko Forgetting         : {app.catastrophic_forgetting_risk}")

    print(f"\n{'='*75}\n")
    print(f"{BOLD}{HEADER}=== SIMULASI ANGGARAN & TOTAL COST OF OWNERSHIP (TCO) ==={RESET}")
    print(f"{CYAN}Asumsi Harga Token Input: $2.50 / 1 Million Tokens (GPT-4o standard rate){RESET}\n")

    scenarios = [10_000, 100_000, 1_000_000]
    
    print(f"┌──────────────────────────────┬──────────────────┬──────────────────┬──────────────────┐")
    print(f"│ Jumlah Request               │ Prompt Eng       │ RAG + Prompt Eng │ LoRA Fine-Tuning │")
    print(f"├──────────────────────────────┼──────────────────┼──────────────────┼──────────────────┤")
    
    for req in scenarios:
        res = calculate_roi_over_requests(req)
        print(f"│ {req:<28,d} │ ${res['prompt_eng']:<15.2f} │ ${res['rag']:<16.2f} │ ${res['lora_ft']:<16.2f} │")
    print(f"└──────────────────────────────┴──────────────────┴──────────────────┴──────────────────┘")

    print(f"\n{BOLD}{GREEN}💡 KESIMPULAN STRATEGIS SKALABILITAS:{RESET}")
    print(" 1. Untuk skala < 100,000 request: Prompt Engineering & RAG jauh lebih MURAH dan CEPAT.")
    print(" 2. Untuk skala > 1,000,000 request dengan format yang sama: Fine-Tuning menjadi LEBIH HEMAT karena menghemat 90% token input overhead di setiap call!")

    print(f"\n{BOLD}[ RULE OF THUMB AI AGENT DEVELOPER ]{RESET}")
    print(" • Gunakan Prompt Engineering / RAG saat data dinamis & sering berubah.")
    print(" • Gunakan Fine-Tuning (LoRA) saat Anda ingin mengunci gaya penulisan, sintaks khusus (JSON/YAML), atau dialek tanpa perlu mengirim contoh prompt panjang di setiap request.")

if __name__ == "__main__":
    run_demo()
