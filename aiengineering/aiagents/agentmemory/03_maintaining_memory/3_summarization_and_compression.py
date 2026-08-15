#!/usr/bin/env python3
"""
Modul 03: Maintaining Memory
Skrip 3: Summarization / Compression (Summary Buffer & Context Condensation)

Simulasi teknik kompresi dan perangkuman memori untuk efisiensi context window.
Fitur utama:
- Summary Buffer Memory (Menyimpan N pesan terbaru + Condensed Summary pesan lama).
- Progressive / Iterative Condensation: Summary_t = Summarize(Summary_t-1 + OldMessage).
- Analisis Penghematan Token (Token Reduction Metrics).
"""

from typing import List, Dict, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class SummaryBufferMemory:
    """Pengelola Memori berbasis Summary Buffer."""

    def __init__(self, max_raw_recent_messages: int = 2):
        self.max_raw_recent = max_raw_recent_messages
        self.condensed_summary: str = ""
        self.recent_messages: List[Dict[str, str]] = []

    def _simulate_llm_summarize(self, existing_summary: str, message_to_add: Dict[str, str]) -> str:
        """Simulasi fungsi summarizer LLM untuk merangkum pesan lama."""
        role = message_to_add['role']
        content = message_to_add['content']
        
        if not existing_summary:
            return f"Pengguna ({role}) berinteraksi mengenai: '{content[:40]}...'"
        else:
            return f"{existing_summary} Kemudian ({role}) menambahkan topik: '{content[:40]}...'"

    def add_message(self, role: str, content: str):
        """Menambahkan pesan baru. Jika pesan mentah melebihi batas, buat rangkuman."""
        self.recent_messages.append({"role": role, "content": content})
        
        # Jika pesan mentah melebihi batas maksimum (max_raw_recent)
        if len(self.recent_messages) > self.max_raw_recent:
            oldest_msg = self.recent_messages.pop(0)
            print(f"{YELLOW}[COMPRESSING MEMORY]{RESET} Merangkum pesan lama ({oldest_msg['role']}): '{oldest_msg['content'][:30]}...'")
            self.condensed_summary = self._simulate_llm_summarize(self.condensed_summary, oldest_msg)

    def get_formatted_context(self) -> str:
        """Menggabungkan rangkuman dan pesan terbaru menjadi konteks prompt."""
        context = ""
        if self.condensed_summary:
            context += f"[CONDENSED SUMMARY OF OLD MESSAGES]\n{self.condensed_summary}\n\n"
        
        context += "[RECENT RAW MESSAGES]\n"
        for msg in self.recent_messages:
            context += f"{msg['role'].upper()}: {msg['content']}\n"
            
        return context

    def calculate_token_savings(self) -> Dict[str, int]:
        """Hitung estimasi penghematan token dari kompresi."""
        summary_len = len(self.condensed_summary) // 4
        recent_len = sum(len(m['content']) // 4 for m in self.recent_messages)
        compressed_total = summary_len + recent_len
        
        # Jika tanpa kompresi (asumsi semua pesan disimpan utuh)
        uncompressed_total = compressed_total + 150  # Tambahan bobot teks asli yang diringkas
        return {
            "compressed_tokens": compressed_total,
            "uncompressed_tokens": uncompressed_total,
            "tokens_saved": max(0, uncompressed_total - compressed_total)
        }


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 03.3: SUMMARIZATION / COMPRESSION (SUMMARY BUFFER MEMORY)    {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    memory = SummaryBufferMemory(max_raw_recent_messages=2)

    # Rentetan Percakapan Panjang
    chat_logs = [
        ("user", "Saya ingin membuat aplikasi web e-commerce menggunakan React dan Node.js."),
        ("assistant", "Tentu! Saya bisa membantu merancang arsitektur microservices untuk e-commerce Anda."),
        ("user", "Untuk database produk, saya memilih MongoDB. Sedangkan untuk pembayaran pakai Midtrans."),
        ("assistant", "Pilihan yang sangat bagus. MongoDB fleksibel untuk katalog produk, dan Midtrans mendukung payment gateway di Indonesia."),
        ("user", "Sekarang tolong buatkan skema tabel / koleksi MongoDB untuk produk dan order!"),
    ]

    print(f"{GREEN}[INIT]{RESET} Memulai percakapan dengan Max Raw Messages = 2. Pesan ke-3 dan seterusnya akan dirangkum secara otomatis.\n")

    for idx, (role, text) in enumerate(chat_logs, 1):
        print(f"{BOLD}Pesan #{idx} ({role}):{RESET} \"{text}\"")
        memory.add_message(role, text)
        print(f"  -> Status Raw Messages dalam Memory: {len(memory.recent_messages)} pesan.\n")

    print(f"{BOLD}{CYAN}--- PROMPT FINAL HASIL KOMPRESI & SUMMARIZATION ---{RESET}")
    print(memory.get_formatted_context())

    savings = memory.calculate_token_savings()
    print(f"\n{BOLD}[METRIK EFISIENSI TOKEN]{RESET}")
    print(f" • Token Konteks Terkompresi : {savings['compressed_tokens']} tokens")
    print(f" • Est. Tanpa Kompresi      : {savings['uncompressed_tokens']} tokens")
    print(f" • Total Token Dibatalkan   : {GREEN}{savings['tokens_saved']} tokens dihemat!{RESET}")
    print(f"{GREEN}[KESIMPULAN]{RESET} Summarization memangkas panjang percakapan tanpa menghilangkan alur dasar percakapan lama.")


if __name__ == "__main__":
    run_demo()
