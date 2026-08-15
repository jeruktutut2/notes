#!/usr/bin/env python3
"""
Modul 1.1: Tokenization Algorithms - BPE, WordPiece, & SentencePiece
Simulasi visual cara kerja tokenizer dari string mentah hingga Subword Tokens dan Token IDs.
"""

import re
from typing import List, Dict, Tuple

# Warna Terminal untuk visualisasi token
COLORS = [
    "\033[91m", "\033[92m", "\033[93m", "\033[94m", 
    "\033[95m", "\033[96m", "\033[97m", "\033[100m"
]
RESET = "\033[0m"

class SimpleBPETokenizer:
    """
    Simulasi sederhana algoritma Byte Pair Encoding (BPE).
    Digunakan oleh model seperti GPT-2, GPT-3.5, GPT-4, LLaMA.
    """
    def __init__(self, vocab_size: int = 50):
        self.vocab_size = vocab_size
        self.merges: Dict[Tuple[str, str], str] = {}
        self.vocab: List[str] = []
        self.special_tokens = {"<BOS>": 0, "<EOS>": 1, "<PAD>": 2, "<UNK>": 3, "<|im_start|>": 4, "<|im_end|>": 5}

    def train(self, corpus: str, num_merges: int = 10):
        """Melatih BPE dengan menggabungkan pasang karakter yang paling sering muncul."""
        print("\n--- [TRAINING BPE TOKENIZER] ---")
        # Split teks menjadi kata-kata dan tambahkan penanda akhir kata '</w>'
        words = corpus.split()
        splits = [list(word) + ['</w>'] for word in words]
        
        for i in range(num_merges):
            pairs = {}
            for word_split in splits:
                for j in range(len(word_split) - 1):
                    pair = (word_split[j], word_split[j+1])
                    pairs[pair] = pairs.get(pair, 0) + 1
            
            if not pairs:
                break
            
            best_pair = max(pairs, key=pairs.get)
            merged_token = "".join(best_pair)
            self.merges[best_pair] = merged_token
            print(f"Iterasi {i+1:02d}: Merge {best_pair} -> '{merged_token}' (Frekuensi: {pairs[best_pair]})")
            
            new_splits = []
            for word_split in splits:
                new_word = []
                j = 0
                while j < len(word_split):
                    if j < len(word_split) - 1 and (word_split[j], word_split[j+1]) == best_pair:
                        new_word.append(merged_token)
                        j += 2
                    else:
                        new_word.append(word_split[j])
                        j += 1
                new_splits.append(new_word)
            splits = new_splits

    def tokenize(self, text: str) -> List[str]:
        """Memecah teks menjadi token subword berdasarkan aturan merge yang telah dilatih."""
        words = text.split()
        tokens = []
        for word in words:
            word_split = list(word) + ['</w>']
            for pair, merged in self.merges.items():
                j = 0
                new_split = []
                while j < len(word_split):
                    if j < len(word_split) - 1 and (word_split[j], word_split[j+1]) == pair:
                        new_split.append(merged)
                        j += 2
                    else:
                        new_split.append(word_split[j])
                        j += 1
                word_split = new_split
            tokens.extend(word_split)
        return tokens


def demonstrate_token_types():
    print("\n" + "="*70)
    print(" 1. PERBANDINGAN ALGORITMA TOKENISASI (BPE vs WordPiece vs SentencePiece)")
    print("="*70)
    
    sample_text = "Transformers dan AI Agents mengubah masa depan kecerdasan buatan"
    
    print(f"Teks Input: '{sample_text}'\n")
    
    # 1. Word-level
    words = sample_text.split()
    print(f"[Word-based Tokenizer] (Jumlah Token: {len(words)})")
    print(f"Tokens: {words}\n")

    # 2. Character-level
    chars = list(sample_text)
    print(f"[Character-based Tokenizer] (Jumlah Token: {len(chars)})")
    print(f"Tokens: {chars[:15]} ... (truncated)\n")

    # 3. Subword BPE Simulation
    bpe = SimpleBPETokenizer()
    training_corpus = "Transformers AI Agents kecerdasan buatan masa depan agen cerdas transformer model"
    bpe.train(training_corpus, num_merges=12)
    
    tokens = bpe.tokenize(sample_text)
    print(f"\n[Subword BPE Tokenizer] (Jumlah Token: {len(tokens)})")
    
    # Render Visual Tokenizer dengan Warna Alternatif
    colored_output = ""
    for idx, token in enumerate(tokens):
        color = COLORS[idx % len(COLORS)]
        colored_output += f"{color}[{token}]{RESET}"
    
    print(f"Visual Tokens: {colored_output}\n")


def demonstrate_special_tokens():
    print("="*70)
    print(" 2. MEMAHAMI SPECIAL TOKENS DALAM LLM AGENTS")
    print("="*70)
    
    special_tokens = {
        "<BOS> / <s>": "Beginning of Sequence - Penanda awal instruksi/percakapan",
        "<EOS> / </s>": "End of Sequence - Penanda LLM berhenti melakukan generasi text",
        "<PAD>": "Padding Token - Menyelaraskan panjang batch tensor pada training/inference",
        "<UNK>": "Unknown Token - Karakter di luar kosakata (vocabulary) tokenizer",
        "<|im_start|>": "ChatML System/User/Assistant turn separator (OpenAI / Qwen)",
        "<|im_end|>": "ChatML Turn Terminator",
        "<tool_call>": "Penanda eksekusi fungsi/tool oleh AI Agent (e.g. Function Calling)"
    }
    
    for token, desc in special_tokens.items():
        print(f" • \033[93m{token:<18}\033[0m : {desc}")
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 1.1: TOKENIZATION ALGORITHMS & MECHANICS")
    print("█"*70)
    
    demonstrate_token_types()
    demonstrate_special_tokens()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Tokenisasi subword (BPE/WordPiece) menyeimbangkan vocab size & panjang urutan.")
    print(" 2. Subword mengatasi OOV (Out-Of-Vocabulary) dengan memecah kata baru menjadi potongan suku kata.")
    print(" 3. Special tokens mengarahkan kontrol aliran percakapan dan agent tool calling.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
