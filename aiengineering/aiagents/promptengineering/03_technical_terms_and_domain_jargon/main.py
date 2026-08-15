#!/usr/bin/env python3
"""
Modul 03: Use Relevant Technical Terms & Attention Steering
------------------------------------------------------------
Simulasi pilar ketiga Prompt Engineering dari roadmap.sh/ai-agents.
Menunjukkan bagaimana penggunaan kosakata teknis spesifik (Domain Jargon & Precise Terminology)
dapat mengarahkan pembobotan vektor perhatian (Attention Weights) LLM ke kluster pengetahuan tingkat lanjut.
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
class JargonExperiment:
    domain: str
    layman_prompt: str
    layman_response: str
    technical_prompt: str
    technical_response: str
    attention_shift_explanation: str

class TechnicalTermsSimulator:
    def __init__(self):
        self.experiments: List[JargonExperiment] = [
            JargonExperiment(
                domain="Database & Distributed Systems",
                layman_prompt="Bagaimana cara agar database saya tidak rusak saat mati listrik dan bisa menangani banyak pengguna bersamaan?",
                layman_response=(
                    "Anda harus rajin melakukan backup data tiap malam. Gunakan antivirus di server "
                    "dan gunakan komputer dengan RAM besar agar server tidak lambat saat diakses banyak orang."
                ),
                technical_prompt=(
                    "Jelaskan mekanisme pemeliharaan ACID Compliance (khususnya Atomicity dan Durability) "
                    "pada InnoDB engine MySQL menggunakan Write-Ahead Logging (WAL / Redo Log) "
                    "serta strategi Concurrency Control berikan penjelasan MVCC (Multi-Version Concurrency Control)."
                ),
                technical_response=(
                    "1. Atomicity & Durability via Redo Log (WAL):\n"
                    "   Setiap transaksi menulis perubahan ke Redo Log Buffer terlebih dahulu sebelum di-flush ke disk (fsync).\n"
                    "   Saat crash/power loss, InnoDB melakukan Crash Recovery via Redo Log (REDO phase) & Undo Log (UNDO phase).\n"
                    "2. Concurrency Control via MVCC:\n"
                    "   InnoDB memanfaatkan Undo Logs untuk membuat versi snapshot data historis. "
                    "   Operasi READ (SELECT) membaca Read View tanpa mengunci baris (Non-locking Consistent Read), "
                    "   sehingga Writer tidak memblokir Reader."
                ),
                attention_shift_explanation="Penggunaan istilah 'ACID', 'WAL', 'MVCC', 'fsync' secara instan memicu kluster memori Arsitek Database InnoDB."
            ),
            JargonExperiment(
                domain="Machine Learning & Optimization",
                layman_prompt="Bagaimana cara membuat model AI belajar lebih cepat dan tidak cepat lupa?",
                layman_response=(
                    "Beri model lebih banyak contoh gambar. Latih model selama beberapa jam lagi "
                    "dan pastikan laptop Anda tidak panas saat proses pembelajaran."
                ),
                technical_prompt=(
                    "Bagaimana cara mengatasi Gradient Vanishing dan Overfitting pada pelatihan Deep Neural Network? "
                    "Bahas penerapan Batch Normalization, Residual Connections (Skip Connections), "
                    "serta teknik Regularisasi L2 (Weight Decay) dan Learning Rate Cosine Annealing Schedule."
                ),
                technical_response=(
                    "1. Gradient Vanishing Mitigation:\n"
                    "   • Residual Connections: Memungkinkan gradien mengalir langsung tanpa tereduksi via identity mapping f(x) + x.\n"
                    "   • Batch Normalization: Menjaga standar deviasi dan mean aktivasi antar layer agar konstan.\n"
                    "2. Overfitting & Scheduler Optimization:\n"
                    "   • Weight Decay (L2 Regularization): Menambahkan penalti kuadrat bobot ||w||^2 pada loss function.\n"
                    "   • Cosine Annealing: Menurunkan learning rate secara mulus mengikuti kurva kosinus untuk stabilisasi konvergensi."
                ),
                attention_shift_explanation="Istilah 'Residual Connections', 'Batch Norm', 'Cosine Annealing' langsung mengaktifkan repositori riset ML terkemuka."
            )
        ]

    def render_header(self):
        print(f"\n{BOLD}{CYAN}=" * 75)
        print(f"{BOLD}{YELLOW}  PILAR 3: USE RELEVANT TECHNICAL TERMS & ATTENTION STEERING")
        print(f"{BOLD}{CYAN}=" * 75 + f"{RESET}\n")
        print(f"{GREEN}Prinsip Utama:{RESET} Istilah teknis yang presisi bertindak sebagai *Attention Steering Vector*")
        print(f"yang mengarahkan LLM langsung ke ruang pembobotan pakar spesifik.\n")

    def run_experiments(self):
        self.render_header()
        for idx, exp in enumerate(self.experiments, 1):
            print(f"{BOLD}{MAGENTA}[EKSPERIMEN #{idx}: DOMAIN {exp.domain.upper()}]{RESET}")
            
            print(f"{BOLD}{RED}🔴 Layman / Prompt Awam:{RESET}")
            print(f"   \"{exp.layman_prompt}\"")
            print(f"{RED}   Hasil Respon Generik:{RESET}")
            for line in exp.layman_response.split('\n'):
                print(f"     {line}")
                
            print(f"\n{BOLD}{GREEN}🟢 Technical / Prompt Presisi Tepat Istilah:{RESET}")
            print(f"   \"{exp.technical_prompt}\"")
            print(f"{CYAN}   Hasil Respon Pakar Tingkat Lanjut:{RESET}")
            for line in exp.technical_response.split('\n'):
                print(f"     {line}")
                
            print(f"\n{BOLD}{YELLOW}🧠 Mekanisme Attention Steering:{RESET}")
            print(f"   {exp.attention_shift_explanation}")
            print(f"{CYAN}-" * 75 + f"{RESET}\n")
            time.sleep(0.5)

    def print_jargon_dictionary_tips(self):
        print(f"{BOLD}{MAGENTA}💡 TIPS PRAKTIS UNTUK PROMPT ENGINEER AGEN AI:{RESET}")
        tips = [
            ("Ganti deskripsi samar dengan istilah standar ISO / RFC", "Contoh: Ganti 'kirim JSON rapi' dengan 'Kepatuhan RFC 8259 JSON Standard'."),
            ("Sebutkan nama Algoritma / Data Structure eksplisit", "Contoh: Ganti 'simpan urut' dengan 'Gunakan Min-Heap / Priority Queue O(log N)'."),
            ("Gunakan kata kunci arsitektur perangkat lunak", "Contoh: Ganti 'pisah kode' dengan 'Terapkan Dependency Injection & Clean Architecture'."),
        ]
        for idx, (title, detail) in enumerate(tips, 1):
            print(f"  {idx}. {BOLD}{GREEN}{title}{RESET}\n     {detail}")
        print()

def main():
    sim = TechnicalTermsSimulator()
    sim.run_experiments()
    sim.print_jargon_dictionary_tips()

if __name__ == "__main__":
    main()
