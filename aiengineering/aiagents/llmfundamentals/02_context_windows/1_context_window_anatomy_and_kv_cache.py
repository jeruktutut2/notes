#!/usr/bin/env python3
"""
Modul 2.1: Context Window Anatomy & KV-Cache Memory Calculation
Anatomi pembagian alokasi memori context window dan kalkulator kebutuhan VRAM KV-Cache LLM.
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class ContextBudget:
    system_prompt_tokens: int
    user_history_tokens: int
    rag_context_tokens: int
    scratchpad_tokens: int
    max_output_tokens: int
    total_window_limit: int

    @property
    def used_input_tokens(self) -> int:
        return (self.system_prompt_tokens + 
                self.user_history_tokens + 
                self.rag_context_tokens + 
                self.scratchpad_tokens)

    @property
    def remaining_space(self) -> int:
        return self.total_window_limit - (self.used_input_tokens + self.max_output_tokens)


def demonstrate_context_anatomy():
    print("\n" + "="*70)
    print(" 1. ANATOMI ALOKASI CONTEXT WINDOW AI AGENT")
    print("="*70)
    
    budget = ContextBudget(
        system_prompt_tokens=1500,  # Persona, kriteria, tool definitions
        user_history_tokens=3000,   # Percakapan sebelumnya
        rag_context_tokens=8000,    # Dokumen hasil pencarian / RAG
        scratchpad_tokens=1200,     # ReAct reasoning chain / step history
        max_output_tokens=4096,     # Batas generasi jawaban
        total_window_limit=32768    # Total limit model (e.g. 32K context)
    )
    
    print(f"Total Kapasitas Context Model : {budget.total_window_limit:,} Tokens\n")
    print(f" ├── System Prompt & Tools    : {budget.system_prompt_tokens:>6,} tokens ({budget.system_prompt_tokens/budget.total_window_limit*100:.1f}%)")
    print(f" ├── History Percakapan       : {budget.user_history_tokens:>6,} tokens ({budget.user_history_tokens/budget.total_window_limit*100:.1f}%)")
    print(f" ├── Dokumen RAG / Retrieval  : {budget.rag_context_tokens:>6,} tokens ({budget.rag_context_tokens/budget.total_window_limit*100:.1f}%)")
    print(f" ├── Working Memory Scratchpad: {budget.scratchpad_tokens:>6,} tokens ({budget.scratchpad_tokens/budget.total_window_limit*100:.1f}%)")
    print(f" ├── Reserved Max Output      : {budget.max_output_tokens:>6,} tokens ({budget.max_output_tokens/budget.total_window_limit*100:.1f}%)")
    print(" " + "─"*50)
    print(f" Total Digunakan              : {budget.used_input_tokens + budget.max_output_tokens:>6,} tokens")
    print(f" sisa Headroom (Aman)         : \033[92m{budget.remaining_space:>6,} tokens\033[0m\n")


def calculate_kv_cache_vram(
    num_layers: int,
    num_heads: int,
    head_dim: int,
    seq_len: int,
    batch_size: int = 1,
    precision_bytes: int = 2 # 2 bytes for FP16/BF16, 1 byte for INT8
) -> Dict[str, float]:
    """
    Menghitung ukuran KV-Cache dalam VRAM.
    Rumus: KV_size = 2 (Key & Value) * layers * heads * head_dim * seq_len * batch_size * precision_bytes
    """
    bytes_per_token = 2 * num_layers * num_heads * head_dim * precision_bytes
    total_bytes = bytes_per_token * seq_len * batch_size
    
    mb = total_bytes / (1024 ** 2)
    gb = total_bytes / (1024 ** 3)
    
    return {
        "bytes_per_token": bytes_per_token,
        "total_bytes": total_bytes,
        "size_mb": mb,
        "size_gb": gb
    }


def demonstrate_kv_cache_calculator():
    print("="*70)
    print(" 2. KALKULATOR VRAM KV-CACHE UNTUK VARIASI SEQUECE LENGTH")
    print("="*70)
    
    # Model Specs: LLaMA-3-8B (32 layers, 32 heads, head_dim 128)
    num_layers = 32
    num_heads = 32
    head_dim = 128
    
    sequence_lengths = [4096, 8192, 32768, 65536, 131072] # 4K to 128K
    
    print(f"Spesifikasi Model: LLaMA-3-8B (Layers: {num_layers}, Heads: {num_heads}, Head Dim: {head_dim})")
    print(f"Presisi Memori  : FP16 / BF16 (2 Bytes per element)\n")
    
    print(f"{'Sequence Length':<18} | {'KV-Cache Size (MB)':<22} | {'KV-Cache Size (GB)':<22} | {'Perlu Multi-GPU?':<18}")
    print("-" * 80)
    
    for seq_len in sequence_lengths:
        res = calculate_kv_cache_vram(num_layers, num_heads, head_dim, seq_len)
        needs_gpu = "Ya (>24GB VRAM)" if res["size_gb"] > 16 else "Tidak (Satu GPU)"
        print(f"{seq_len:>10,} tokens    | {res['size_mb']:>18.2f} MB | {res['size_gb']:>18.2f} GB | {needs_gpu:<18}")
    
    print("\n\033[93mCatatan Kunci:\033[0m Ukuran KV-Cache bertambah secara linier terhadap panjang konteks.")
    print("Pada 128K tokens, memori KV-Cache saja membutuhkan ~16GB VRAM (di luar memori bobot model 16GB!).")
    print()


def demonstrate_overflow_strategies():
    print("="*70)
    print(" 3. STRATEGI PENANGANAN CONTEXT OVERFLOW")
    print("="*70)
    
    strategies = [
        ("Naive Truncation", "Memotong pesan percakapan terlama secara langsung.", "Hilang ingatan instruksi awal & konteks kunci."),
        ("Sliding Window", "Mempertahankan N pesan terakhir saja.", "Sangat hemat, namun kehilangan konteks jangka panjang."),
        ("Summary Buffer", "Meringkas pesan lama menjadi ringkasan sistem saat mendekati limit.", "Keseimbangan terbaik antara pemahaman konteks & penggunaan token.")
    ]
    
    for title, method, downside in strategies:
        print(f" • \033[96m{title:<20}\033[0m: {method}")
        print(f"   \033[90mDampak: {downside}\033[0m")
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 2.1: CONTEXT WINDOW ANATOMY & KV-CACHE")
    print("█"*70)
    
    demonstrate_context_anatomy()
    demonstrate_kv_cache_calculator()
    demonstrate_overflow_strategies()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. Selalu sisakan headroom (~10-20%) pada context budget untuk kestabilan respon LLM.")
    print(" 2. Pengelolaan KV-Cache sangat krusial saat menyajikan context panjang (32K+ token).")
    print(" 3. Strategi Summary Buffer disarankan untuk percakapan AI Agent berdurasi panjang.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
