#!/usr/bin/env python3
"""
Modul 02: Provide Additional Context & Grounding
-----------------------------------------------
Simulasi pilar kedua Prompt Engineering dari roadmap.sh/ai-agents.
Menunjukkan bagaimana menyuntikkan konteks (Context Injection), memisahkan konteks dengan tag pemisah (Delimiters),
serta menetapkan guardrails untuk mencegah halusinasi data.
"""

import time
from dataclasses import dataclass
from typing import Dict, List

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
MAGENTA = "\033[95m"
BLUE = "\033[94m"

class ContextGroundingSimulator:
    def __init__(self):
        self.internal_knowledge_base = (
            "DOKUMEN KEBIJAKAN PENGEMBALIAN BARANG (RETURN POLICY) PT TECHNO-SHOP 2026:\n"
            "- Pengembalian fisik dapat dilakukan maksimal 14 hari setelah tanggal penerimaan barang.\n"
            "- Produk elektronik bernilai di atas Rp 5.000.000 wajib menyertakan video unboxing utuh tanpa cut.\n"
            "- Biaya pengiriman retur ditanggung pembeli, kecuali retur disebabkan kesalahan produk cacat pabrik.\n"
            "- Barang promosi (Flash Sale) bersifat Final Sale dan TIDAK DAPAAT dikembalikan."
        )

    def render_header(self):
        print(f"\n{BOLD}{CYAN}=" * 75)
        print(f"{BOLD}{YELLOW}  PILAR 2: PROVIDE ADDITIONAL CONTEXT & GROUNDING DATA")
        print(f"{BOLD}{CYAN}=" * 75 + f"{RESET}\n")
        print(f"{GREEN}Prinsip Utama:{RESET} Berikan fakta pendukung (Context Injection) & Delimiters")
        print(f"untuk mengikat (*grounding*) jawaban LLM pada kenyataan dan memotong halusinasi.\n")

    def run_grounding_experiment(self):
        self.render_header()
        user_query = "Saya membeli laptop Asus seharga Rp 8.000.000 pada Flash Sale 3 hari lalu tapi ingin retur. Bisakah?"
        
        print(f"{BOLD}{MAGENTA}[SKENARIO PENGUJIANKUERI CUSTOMER SERVICE]{RESET}")
        print(f"{BOLD}Pertanyaan Pengguna:{RESET} \"{user_query}\"\n")
        
        # Skenario A: Tanpa Konteks Tambahan (Zero-Context / Generic LLM)
        print(f"{BOLD}{RED}❌ Skenario A: Tanpa Context Ingestion (Halusinasi / Jawaban Generik):{RESET}")
        print(f"{BLUE}Prompt:{RESET} \"{user_query}\"")
        time.sleep(0.3)
        simulated_response_no_ctx = (
            "Ya, secara umum Anda bisa mengembalikan produk laptop dalam waktu 7-30 hari "
            "tergantung toko. Pastikan membawa nota pembelian dan garansi resmi ke customer service terdekat."
        )
        print(f"{RED}Hasil AI:{RESET} {simulated_response_no_ctx}")
        print(f"{RED}⚠️ MASALAH:{RESET} Jawaban salah & bertentangan dengan kebijakan toko (Flash Sale & Video Unboxing)!\n")
        
        # Skenario B: Dengan Context Ingestion + Tag Pemisah (Delimiters)
        print(f"{BOLD}{GREEN}✅ Skenario B: Dengan Context Ingestion & XML Delimiters (Grounded Response):{RESET}")
        prompt_with_context = (
            "Anda adalah AI Customer Support PT Techno-Shop.\n"
            "Jawab pertanyaan pengguna HANYA berdasarkan dokumen kebijakan di bawah ini.\n"
            "Jika jawaban tidak ada dalam dokumen, katakan secara jujur bahwa Anda tidak memiliki informasi tersebut.\n\n"
            "<context_document>\n"
            f"{self.internal_knowledge_base}\n"
            "</context_document>\n\n"
            f"<user_query>{user_query}</user_query>"
        )
        print(f"{BLUE}Prompt Terstruktur:{RESET}")
        for line in prompt_with_context.split('\n'):
            print(f"  {line}")
            
        time.sleep(0.4)
        simulated_response_grounded = (
            "Mohon maaf, pengajuan retur Anda TIDAK DAPAT diproses. Berdasarkan Kebijakan Pengembalian Barang PT Techno-Shop:\n"
            "1. Produk yang dibeli saat program Flash Sale bersifat Final Sale dan tidak dapat dikembalikan.\n"
            "2. Sebagai informasi tambahan untuk produk non-promosi bernilai di atas Rp 5.000.000, pengembalian juga memerlukan video unboxing utuh."
        )
        print(f"\n{CYAN}Hasil AI (Grounded 100% Akurat):{RESET}\n{simulated_response_grounded}")
        print(f"\n{BOLD}{YELLOW}💡 Lesson Learned:{RESET} Menyediakan konteks terisolasi dalam tag `<context>` mencegah LLM dari menebak-nebak fakta internal perusahaan.\n")

    def run_delimiter_isolation_demo(self):
        print(f"{BOLD}{CYAN}-" * 75)
        print(f"{BOLD}{MAGENTA}🛡️ PENERAPAN DELIMITERS UNTUK KEAMANAN & PISAHAN DATA{RESET}")
        print(f"{CYAN}-" * 75 + f"{RESET}\n")
        print("Penggunaan pemisah eksplisit (seperti XML Tags, Triple Quotes ```, atau Triple Dashes ---)")
        print("mencegah LLM membingungkan instruksi sistem dengan input dari pengguna.\n")
        
        delimiters = [
            ("XML Tags", "<document>...</document>", "Sangat direkomendasikan untuk LLM modern (Claude/GPT-4)."),
            ("Triple Backticks", "```json ... ```", "Bagus untuk kode program & skema terstruktur."),
            ("Markdown Headers", "### CONTEXT DATA ...", "Mudah dibaca oleh manusia & LLM.")
        ]
        
        for name, syntax, desc in delimiters:
            print(f"• {BOLD}{GREEN}{name}{RESET} (`{syntax}`): {desc}")
        print()

def main():
    sim = ContextGroundingSimulator()
    sim.run_grounding_experiment()
    sim.run_delimiter_isolation_demo()

if __name__ == "__main__":
    main()
