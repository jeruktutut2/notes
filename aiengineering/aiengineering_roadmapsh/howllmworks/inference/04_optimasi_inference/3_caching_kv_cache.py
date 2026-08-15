"""
=================================================================
3. KV-CACHE (Key-Value Cache)
=================================================================
KV-Cache adalah optimasi KUNCI untuk mempercepat autoregressive
text generation (model GPT-style).

Masalah tanpa KV-Cache:
- Setiap kali generate 1 token baru, model harus menghitung
  ulang attention untuk SELURUH token sebelumnya
- Generating 100 token → menghitung attention 100 kali
- Sangat tidak efisien (O(n²) per token baru)

Solusi KV-Cache:
- Simpan Key (K) dan Value (V) dari attention layer
- Token baru hanya perlu menghitung Q × K^T untuk token baru
- Reuse K dan V dari token sebelumnya
- Speedup: 5-10x pada sequence panjang

Analogi:
- Tanpa cache: Membaca ulang seluruh buku setiap halaman baru
- Dengan cache: Cukup baca halaman baru, ingatan halaman lama tersimpan
=================================================================
"""

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import time


def demo_konsep_kv_cache():
    """Menjelaskan konsep KV-Cache secara visual."""
    print("=" * 60)
    print("DEMO 1: Konsep KV-Cache")
    print("=" * 60)

    print("""
    📝 CARA KERJA TEXT GENERATION (Autoregressive):

    Input: "AI is"
    Step 1: "AI is" → model → "great"      (hitung attention seluruh: AI, is)
    Step 2: "AI is great" → model → "for"   (hitung attention: AI, is, great)
    Step 3: "AI is great for" → model → ... (hitung attention: AI, is, great, for)
    
    ❌ TANPA KV-Cache (Naïf):
    ┌─────────────────────────────────────────────────────────┐
    │ Step 1: Compute K,V for [AI, is]           → predict   │
    │ Step 2: Compute K,V for [AI, is, great]    → predict   │  ← Redundant!
    │ Step 3: Compute K,V for [AI, is, great, for] → predict │  ← Redundant!
    └─────────────────────────────────────────────────────────┘
    Token "AI" dan "is" dihitung ulang di SETIAP step!

    ✅ DENGAN KV-Cache:
    ┌─────────────────────────────────────────────────────────┐
    │ Step 1: Compute K,V for [AI, is]       → CACHE & predict│
    │ Step 2: Load cache + Compute [great]   → CACHE & predict│  ← Hemat!
    │ Step 3: Load cache + Compute [for]     → CACHE & predict│  ← Hemat!
    └─────────────────────────────────────────────────────────┘
    Hanya token BARU yang dihitung, sisanya dari cache!

    📊 Perbandingan Komputasi:
    ┌──────────────────┬────────────────────┬──────────────────┐
    │ Sequence Length   │ Tanpa Cache (ops)  │ Dengan Cache     │
    ├──────────────────┼────────────────────┼──────────────────┤
    │ Generate 10 token│ 1+2+...+10 = 55    │ 10 (1 per step)  │
    │ Generate 100     │ 1+2+...+100 = 5050 │ 100              │
    │ Generate 1000    │ 500,500            │ 1,000            │
    └──────────────────┴────────────────────┴──────────────────┘
    Speedup: ~50x untuk 100 token, ~500x untuk 1000 token!
    """)


def demo_kv_cache_hf():
    """Demo KV-Cache dengan Hugging Face (use_cache parameter)."""
    print("=" * 60)
    print("DEMO 2: KV-Cache di Hugging Face Transformers")
    print("=" * 60)

    nama_model = "distilgpt2"
    print(f"\n📦 Memuat model: {nama_model}")
    
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForCausalLM.from_pretrained(nama_model)
    model.eval()

    prompt = "The future of artificial intelligence"
    inputs = tokenizer(prompt, return_tensors="pt")
    max_new_tokens = 50

    # Generate TANPA KV-Cache
    print(f"\n📝 Prompt: \"{prompt}\"")
    print(f"   Max new tokens: {max_new_tokens}")

    print(f"\n⏱️ Generate TANPA KV-Cache:")
    start = time.time()
    with torch.no_grad():
        output_no_cache = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            use_cache=False,  # Matikan KV-Cache
            do_sample=False
        )
    time_no_cache = (time.time() - start) * 1000
    text_no_cache = tokenizer.decode(output_no_cache[0], skip_special_tokens=True)
    print(f"   Waktu: {time_no_cache:.0f} ms")
    print(f"   Output: {text_no_cache[:100]}...")

    # Generate DENGAN KV-Cache
    print(f"\n⏱️ Generate DENGAN KV-Cache:")
    start = time.time()
    with torch.no_grad():
        output_cache = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            use_cache=True,  # Aktifkan KV-Cache (default)
            do_sample=False
        )
    time_cache = (time.time() - start) * 1000
    text_cache = tokenizer.decode(output_cache[0], skip_special_tokens=True)
    print(f"   Waktu: {time_cache:.0f} ms")
    print(f"   Output: {text_cache[:100]}...")

    # Perbandingan
    speedup = time_no_cache / time_cache if time_cache > 0 else 0
    print(f"\n📊 Perbandingan:")
    print(f"   Tanpa cache : {time_no_cache:.0f} ms")
    print(f"   Dengan cache: {time_cache:.0f} ms")
    print(f"   Speedup     : {speedup:.2f}x")
    print(f"   Output sama?: {'✅' if text_no_cache == text_cache else '❌ (bisa berbeda karena numerik)'}")


def demo_kv_cache_memory():
    """Estimasi memori yang digunakan KV-Cache."""
    print("\n" + "=" * 60)
    print("DEMO 3: Estimasi Memori KV-Cache")
    print("=" * 60)

    print("""
    📦 FORMULA MEMORI KV-CACHE:
    
    Memory = 2 × L × H × D × S × bytes_per_param
    
    Dimana:
    - 2     = Key + Value
    - L     = Jumlah layer
    - H     = Jumlah attention head
    - D     = Dimensi per head
    - S     = Sequence length (panjang teks)
    - bytes = FP16 (2 bytes) atau FP32 (4 bytes)
    """)

    # Estimasi untuk berbagai model
    models = [
        {"nama": "GPT-2 (117M)", "layers": 12, "heads": 12, "d_head": 64, "params": "117M"},
        {"nama": "Llama 7B", "layers": 32, "heads": 32, "d_head": 128, "params": "7B"},
        {"nama": "Llama 70B", "layers": 80, "heads": 64, "d_head": 128, "params": "70B"},
    ]

    seq_lengths = [512, 2048, 8192]

    print(f"\n📊 Estimasi KV-Cache Memory (FP16):")
    print(f"   {'Model':<20} | {'512 tokens':>12} | {'2K tokens':>12} | {'8K tokens':>12}")
    print(f"   {'-'*20}-+-{'-'*12}-+-{'-'*12}-+-{'-'*12}")

    for m in models:
        sizes = []
        for seq_len in seq_lengths:
            # 2 (K+V) × layers × heads × d_head × seq_len × 2 bytes (FP16)
            memory = 2 * m['layers'] * m['heads'] * m['d_head'] * seq_len * 2
            memory_mb = memory / (1024 * 1024)
            sizes.append(memory_mb)
        
        print(f"   {m['nama']:<20} | {sizes[0]:>10.1f}MB | {sizes[1]:>10.1f}MB | {sizes[2]:>10.1f}MB")

    print("""
    💡 Observasi:
    - KV-Cache untuk model 70B + 8K context = ~10 GB PER REQUEST!
    - Ini sebabnya batch serving LLM besar butuh banyak VRAM
    - Teknik seperti GQA (Grouped Query Attention) mengurangi cache
    - vLLM menggunakan PagedAttention untuk manajemen cache efisien
    """)


def main():
    demo_konsep_kv_cache()
    demo_kv_cache_hf()
    demo_kv_cache_memory()

    print("\n✅ Selesai! Lanjut ke: 4_streaming_output.py")

if __name__ == "__main__":
    main()
