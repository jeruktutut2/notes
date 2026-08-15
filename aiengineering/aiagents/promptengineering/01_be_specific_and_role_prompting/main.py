#!/usr/bin/env python3
"""
Modul 01: Be Specific in What You Want & Role Prompting
------------------------------------------------------
Simulasi pilar pertama Prompt Engineering dari roadmap.sh/ai-agents.
Menunjukkan pentingnya kejelasan instruksi, penetapan persona/role, verba aksi spesifik,
dan pembatas tugas (task boundary) untuk menghindari respons ambigu LLM.
"""

import sys
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
class PromptComparison:
    title: str
    vague_prompt: str
    vague_output_simulated: str
    specific_prompt: str
    specific_output_simulated: str
    key_takeaway: str

class SpecificitySimulator:
    def __init__(self):
        self.comparisons: List[PromptComparison] = [
            PromptComparison(
                title="Analisis Kode Python (Code Review)",
                vague_prompt="Cek kode ini apakah sudah bagus?",
                vague_output_simulated=(
                    "Kode ini terlihat oke. Menggunakan loop untuk menghitung data. "
                    "Anda bisa menambahkan komentar agar lebih rapi."
                ),
                specific_prompt=(
                    "Anda adalah Senior Python Engineer & Security Auditor. "
                    "Analisis fungsi di bawah ini dari 3 aspek: "
                    "1. Kompleksitas Waktu & Memori (Big-O), "
                    "2. Potensi Vulnerabilitas Keamanan (seperti SQL Injection atau Memory Leak), "
                    "3. Kepatuhan Standar PEP8. "
                    "Berikan hasil dalam bentuk poin-poin dengan contoh perbaikan kode."
                ),
                specific_output_simulated=(
                    "[ROLE: Senior Python Engineer]\n"
                    "1. Kompleksitas Waktu & Memori: O(N^2) karena nested loop pada baris 14. Dicurigai memicu High CPU Usage.\n"
                    "2. Keamanan: Terdeteksi unescaped string formatting pada kueri SQL (Vulnerabilitas SQL Injection).\n"
                    "3. PEP8: Penamaan variabel `myList` tidak mematuhi snake_case convention.\n"
                    "--> Solusi Refaktoring terlampir menggunakan Parameterized Queries & List Comprehension."
                ),
                key_takeaway="Penetapan Role + 3 Aspek Evaluasi Spesifik menghasilkan analisis mendalam alih-alih saran umum."
            ),
            PromptComparison(
                title="Pembuatan Ringkasan Dokumen (Summarization)",
                vague_prompt="Tolong ringkas dokumen ini.",
                vague_output_simulated=(
                    "Dokumen ini membahas tentang tren artificial intelligence di tahun 2026. "
                    "Banyak perusahaan mulai menggunakan AI Agent untuk mempercepat bisnis."
                ),
                specific_prompt=(
                    "Bertindaklah sebagai Tech Journalist & Market Analyst. "
                    "Buat ringkasan eksekutif dari laporan ini khusus untuk jajaran Direksi (C-Level). "
                    "Ringkasan WAJIB memuat:\n"
                    "- 3 Tren Utama AI Agent 2026\n"
                    "- Estimasi Dampak ROI (Return on Investment)\n"
                    "- 2 Tantangan Keamanan Terbesar\n"
                    "Batasi panjang ringkasan maksimal 150 kata."
                ),
                specific_output_simulated=(
                    "[ROLE: Tech Journalist & Market Analyst]\n"
                    "EXECUTIVE SUMMARY (Untuk C-Level):\n"
                    "1. Tren Utama: Adopsi Multi-Agent System (84%), On-Device LLM, & Automated Guardrails.\n"
                    "2. Dampak ROI: Efisiensi operasional meningkat 38%, pengurangan waktu time-to-market 2.5x.\n"
                    "3. Tantangan Keamanan: Risk of Prompt Injection & Unintended Tool Calls.\n"
                    "Target Kata: 112 kata (Memenuhi batas < 150 kata)."
                ),
                key_takeaway="Menentukan Audiens Target + Komponen Wajib + Batas Kata menghasilkan ringkasan eksekutif siap pakai."
            )
        ]

    def render_header(self):
        print(f"\n{BOLD}{CYAN}=" * 75)
        print(f"{BOLD}{YELLOW}  PILAR 1: BE SPECIFIC IN WHAT YOU WANT & ROLE PROMPTING")
        print(f"{BOLD}{CYAN}=" * 75 + f"{RESET}\n")
        print(f"{GREEN}Prinsip Utama:{RESET} Hindari instruksi ambigu. Tentukan Peran (Role),")
        print(f"Instruksi Spesifik, Audiens Target, dan Pembatas Tugas (Task Boundary).\n")

    def run_comparison_demo(self):
        self.render_header()
        for idx, comp in enumerate(self.comparisons, 1):
            print(f"{BOLD}{MAGENTA}[KASUS UJI #{idx}: {comp.title}]{RESET}")
            print(f"{BOLD}{RED}❌ Vague Prompt (Ambigu):{RESET}")
            print(f"   \"{comp.vague_prompt}\"")
            print(f"{BLUE}   Hasil AI (Kurang Spesifik):{RESET}")
            for line in comp.vague_output_simulated.split('\n'):
                print(f"     {line}")
            
            print(f"\n{BOLD}{GREEN}✅ Specific Prompt (Presisi & Role-Based):{RESET}")
            print(f"   \"{comp.specific_prompt}\"")
            print(f"{CYAN}   Hasil AI (Sangat Presisi):{RESET}")
            for line in comp.specific_output_simulated.split('\n'):
                print(f"     {line}")
            
            print(f"\n{BOLD}{YELLOW}💡 Lesson Learned:{RESET} {comp.key_takeaway}")
            print(f"{CYAN}-" * 75 + f"{RESET}\n")
            time.sleep(0.5)

    def interactive_refactor_tool(self):
        print(f"{BOLD}{MAGENTA}🛠️ INTERACTIVE PROMPT REFACTORING ENGINE{RESET}")
        print("Transformasi prompt ambigu menjadi Prompt Spesifik berbasis Role & Action Verbs!\n")
        
        sample_inputs = [
            "Tolong buatkan deskripsi produk sepatu ini.",
            "Bantu perbaiki bug di aplikasi saya.",
            "Tuliskan artikel blog tentang AI."
        ]
        
        print("Pilih prompt ambigu untuk direfaktorisasi:")
        for idx, sample in enumerate(sample_inputs, 1):
            print(f"  {idx}. \"{sample}\"")
            
        choice = input(f"\n{BOLD}Masukkan nomor pilihan (1-{len(sample_inputs)}) [default: 1]: {RESET}").strip()
        selected_idx = 0
        if choice.isdigit() and 1 <= int(choice) <= len(sample_inputs):
            selected_idx = int(choice) - 1
            
        original = sample_inputs[selected_idx]
        print(f"\n{BOLD}{RED}Prompt Asal (Ambigu):{RESET} \"{original}\"")
        print(f"{YELLOW}Proses Refaktorisasi Otomatis...{RESET}")
        time.sleep(0.4)
        
        if selected_idx == 0:
            refactored = (
                "Anda adalah E-Commerce Copywriter Profesional. "
                "Tuliskan deskripsi produk sepatu lari 'UltraStride Pro' dengan gaya persuasif & meyakinkan.\n"
                "Target Audiens: Pelari maraton dan penggiat olahraga berusia 20-40 tahun.\n"
                "Komponen Wajib:\n"
                "- 3 Fitur Unggulan (Bahan Breathable Mesh, Carbon Plate, Cushion Shock-Absorb)\n"
                "- Call-to-Action (CTA) yang kuat di akhir deskripsi\n"
                "- Gunakan tone yang energik dan profesional."
            )
        elif selected_idx == 1:
            refactored = (
                "Anda adalah Expert Debugger & Software Architect. "
                "Di bawah ini adalah error stacktrace Node.js. "
                "Tugas Anda:\n"
                "1. Identifikasi Root Cause utama dari error tersebut.\n"
                "2. Jelaskan mengapa error tersebut terjadi pada event loop async.\n"
                "3. Berikan patch kode perbaikan dengan exception handling yang aman (try-catch)."
            )
        else:
            refactored = (
                "Anda adalah Technical Content Writer. "
                "Tulis artikel blog sepanjang 500 kata berjudul 'Dampak AI Agents pada Efisiensi Software Engineering'.\n"
                "Struktur Artikel:\n"
                "- Header H1 & H2 yang SEO-friendly\n"
                "- Studi Kasus Singkat (Peningkatan produktivitas developer)\n"
                "- Poin-poin Tantangan Kepatuhan Keamanan Kode\n"
                "- Kesimpulan & Prediksi Masa Depan."
            )

        print(f"\n{BOLD}{GREEN}✨ Hasil Prompt Hasil Refaktorisasi (Spesifik & Terstruktur):{RESET}")
        print(f"{CYAN}-----------------------------------------------------------------------{RESET}")
        print(refactored)
        print(f"{CYAN}-----------------------------------------------------------------------{RESET}\n")

def main():
    sim = SpecificitySimulator()
    sim.run_comparison_demo()
    sim.interactive_refactor_tool()

if __name__ == "__main__":
    main()
