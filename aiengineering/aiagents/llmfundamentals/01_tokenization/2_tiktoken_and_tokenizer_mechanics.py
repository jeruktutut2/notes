#!/usr/bin/env python3
"""
Modul 1.2: Tiktoken & Byte-level BPE Tokenizer Mechanics
Analisis token-to-ID mapping, byte encoding, dan efisiensi tokenisasi (Bahasa Indonesia, Kode, JSON, Emoji).
"""

import sys
from typing import Dict, List, Tuple

class SimulatedTiktoken:
    """
    Simulasi logika Byte-level BPETokenizer seperti OpenAI Tiktoken (cl100k_base / o200k_base).
    """
    def __init__(self):
        # Kosakata simulasi dengan pemetaan kata/subword populer ke Token ID
        self.vocab: Dict[str, int] = {
            "The": 464, " quick": 2068, " brown": 7586, " fox": 21831,
            "Halo": 45120, " dunia": 32104, " kecerdasan": 89201, " buatan": 41203,
            "AI": 15592, " Agent": 17821, " System": 4421,
            "def": 662, " main": 1201, "():": 3291, " import": 1284,
            " {\n": 812, "  \"name\":": 9921, "  \"status\":": 14210,
            "🤖": 125102, "🔥": 125105, "🇮🇩": 128990
        }
        self.reverse_vocab = {v: k for k, v in self.vocab.items()}

    def encode(self, text: str) -> List[int]:
        """Melakukan encoding konversi string teks ke daftar Token ID integer."""
        token_ids = []
        words = text.split()
        for w in words:
            found = False
            for k in self.vocab:
                if k.strip() == w.strip():
                    token_ids.append(self.vocab[k])
                    found = True
                    break
            if not found:
                # Jika kata tidak ada di vocab simulasi, pecah berbasis byte/karakter
                for char in w:
                    byte_id = ord(char) + 1000  # Fallback byte offset ID
                    token_ids.append(byte_id)
        return token_ids

    def decode(self, token_ids: List[int]) -> str:
        """Mengubah daftar Token ID kembali menjadi string teks decoded."""
        result = []
        for tid in token_ids:
            if tid in self.reverse_vocab:
                result.append(self.reverse_vocab[tid])
            else:
                # Fallback char
                result.append(chr(tid - 1000) if tid > 1000 else "?")
        return "".join(result)

def analyze_token_efficiency():
    print("\n" + "="*70)
    print(" 1. ANALISIS EFISIENSI TOKENISASI BAHASA & FORMAT DATA")
    print("="*70)
    
    tokenizer = SimulatedTiktoken()
    
    samples = [
        ("Bahasa Inggris (English)", "The quick brown fox AI Agent System"),
        ("Bahasa Indonesia", "Halo dunia kecerdasan buatan AI Agent System"),
        ("Kode Python", "def main(): import os sys json time"),
        ("Payload JSON", "{\n  \"name\": \"Agent-1\",  \"status\": \"Active\"\n}"),
        ("Teks dengan Emoji & Unicode", "AI Agent Indonesia 🤖🔥 🇮🇩")
    ]
    
    print(f"{'Kategori Teks':<28} | {'Panjang Teks':<12} | {'Jumlah Token':<12} | {'Token/Karakter Ratio':<20}")
    print("-" * 80)
    
    for category, text in samples:
        tokens = tokenizer.encode(text)
        char_len = len(text)
        token_count = len(tokens)
        ratio = token_count / char_len if char_len > 0 else 0
        print(f"{category:<28} | {char_len:<12} | {token_count:<12} | {ratio:.3f} token/char")
    print()


def analyze_byte_overhead():
    print("="*70)
    print(" 2. BYTE OVERHEAD PADA UTF-8 & EMOJI MULTI-BYTE")
    print("="*70)
    
    emoji_str = "🤖 AI Agent 🇮🇩"
    raw_bytes = emoji_str.encode('utf-8')
    
    print(f"String Input   : '{emoji_str}'")
    print(f"Jumlah Karakter : {len(emoji_str)} karakter unicode")
    print(f"Jumlah Byte UTF-8: {len(raw_bytes)} bytes")
    print(f"Byte Sequence   : {list(raw_bytes)}")
    print("\nPenjelasan Byte Level BPE:")
    print(" • Karakter ASCII standar (A-Z, a-z, 0-9) memakan 1 byte.")
    print(" • Karakter ber-aksen / non-Latin memakan 2-3 bytes.")
    print(" • Emoji seperti 🤖 dan bendera 🇮🇩 memakan 4-8 bytes per simbol.")
    print(" • Byte-level BPE mencegah error OOV dengan menjamin seluruh 256 nilai byte mentah memiliki Token ID dasar.")
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 1.2: TIKTOKEN & BYTE-LEVEL BPE MECHANICS")
    print("█"*70)
    
    analyze_token_efficiency()
    analyze_byte_overhead()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Bahasa Inggris umumnya paling efisien (~1 token ≈ 4 karakter).")
    print(" 2. Bahasa Indonesia dan JSON payload mengonsumsi 30%-60% lebih banyak token per informasi.")
    print(" 3. Penggunaan Byte-level BPE memastikan LLM dapat memproses data biner/unicode apa pun tanpa crash.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
