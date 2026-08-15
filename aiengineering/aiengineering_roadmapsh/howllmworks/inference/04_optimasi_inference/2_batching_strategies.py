"""
=================================================================
2. BATCHING STRATEGIES
=================================================================
Batching = mengelompokkan beberapa request inference menjadi satu
batch untuk diproses bersamaan oleh GPU/CPU.

Mengapa batching penting?
- GPU sangat efisien untuk operasi paralel
- 1 request: GPU terpakai ~10%
- 32 request batch: GPU terpakai ~80-90%
- Throughput meningkat drastis (5-10x)

Jenis Batching:
1. Static Batching  → Kumpulkan N request, proses sekaligus
2. Dynamic Batching → Kumpulkan request dalam waktu T, proses
3. Continuous Batching → Slot kosong langsung diisi request baru
=================================================================
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time

def demo_single_vs_batch():
    """Perbandingan inference satu-per-satu vs batch."""
    print("=" * 60)
    print("DEMO 1: Single Request vs Batch Inference")
    print("=" * 60)

    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForSequenceClassification.from_pretrained(nama_model)
    model.eval()

    # 16 teks untuk di-inference
    teks_list = [
        "This movie was absolutely amazing!",
        "The food was terrible and overpriced.",
        "Average service, nothing special.",
        "I love this product so much!",
        "Worst experience of my life.",
        "It's okay, could be better.",
        "Fantastic quality and fast delivery!",
        "Very disappointing, would not recommend.",
        "Pretty good for the price.",
        "This exceeded all my expectations!",
        "Completely useless product.",
        "Not bad, not great either.",
        "The best purchase I ever made!",
        "Waste of money, returned immediately.",
        "Decent quality, fair price.",
        "Outstanding customer service!",
    ]

    # Metode 1: Satu per satu (Sequential)
    print(f"\n📝 Jumlah teks: {len(teks_list)}")
    print(f"\n⏱️ Metode 1: SEQUENTIAL (satu per satu)")
    
    start = time.time()
    hasil_seq = []
    for teks in teks_list:
        inputs = tokenizer(teks, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        pred = torch.argmax(torch.softmax(outputs.logits, dim=-1)).item()
        hasil_seq.append(pred)
    time_seq = (time.time() - start) * 1000

    print(f"   Waktu total : {time_seq:.0f} ms")
    print(f"   Waktu/request: {time_seq/len(teks_list):.1f} ms")

    # Metode 2: Batch (semua sekaligus)
    print(f"\n⏱️ Metode 2: BATCH (semua sekaligus)")
    
    start = time.time()
    inputs = tokenizer(teks_list, return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    preds = torch.argmax(torch.softmax(outputs.logits, dim=-1), dim=-1).tolist()
    time_batch = (time.time() - start) * 1000

    print(f"   Waktu total : {time_batch:.0f} ms")
    print(f"   Waktu/request: {time_batch/len(teks_list):.1f} ms")

    # Perbandingan
    speedup = time_seq / time_batch
    print(f"\n📊 Perbandingan:")
    print(f"   Sequential : {time_seq:.0f} ms")
    print(f"   Batch      : {time_batch:.0f} ms")
    print(f"   Speedup    : {speedup:.2f}x lebih cepat")
    print(f"   Hasil sama?: {'✅' if hasil_seq == preds else '❌'}")


def demo_batch_size_impact():
    """Pengaruh ukuran batch terhadap throughput dan latensi."""
    print("\n" + "=" * 60)
    print("DEMO 2: Pengaruh Batch Size")
    print("=" * 60)

    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForSequenceClassification.from_pretrained(nama_model)
    model.eval()

    teks_banyak = [f"This is test sentence number {i} with some padding text to make it longer." 
                   for i in range(64)]

    batch_sizes = [1, 2, 4, 8, 16, 32, 64]

    print(f"\n📊 Benchmark berbagai batch size ({len(teks_banyak)} teks total):")
    print(f"   {'Batch Size':>10} | {'Total (ms)':>10} | {'Per Item (ms)':>13} | {'Throughput':>12}")
    print(f"   {'-'*10}-+-{'-'*10}-+-{'-'*13}-+-{'-'*12}")

    for bs in batch_sizes:
        start = time.time()
        for i in range(0, len(teks_banyak), bs):
            batch = teks_banyak[i:i+bs]
            inputs = tokenizer(batch, return_tensors="pt", padding=True, truncation=True)
            with torch.no_grad():
                _ = model(**inputs)
        total_ms = (time.time() - start) * 1000
        per_item = total_ms / len(teks_banyak)
        throughput = len(teks_banyak) / (total_ms / 1000)

        print(f"   {bs:>10} | {total_ms:>10.0f} | {per_item:>13.2f} | {throughput:>10.1f}/s")

    print("""
    💡 Observasi:
    - Batch size KECIL: Latensi per-item rendah, throughput rendah
    - Batch size BESAR: Latensi per-item naik, throughput tinggi
    - Sweet spot biasanya di batch size 8-32
    - Terlalu besar → OOM (Out of Memory) pada GPU
    """)


def demo_strategi_batching():
    """Penjelasan berbagai strategi batching di production."""
    print("=" * 60)
    print("DEMO 3: Strategi Batching di Production")
    print("=" * 60)

    print("""
    📋 3 STRATEGI BATCHING UTAMA:

    ═══════════════════════════════════════════════════════
    1. STATIC BATCHING
    ═══════════════════════════════════════════════════════
    - Kumpulkan tepat N request, lalu proses sekaligus
    - Semua request dalam batch HARUS selesai bersamaan
    - Padding ditambahkan ke input yang lebih pendek

    Kelebihan: Implementasi sederhana
    Kekurangan: Request pendek menunggu yang panjang

    Visualisasi:
    ┌──────────┐
    │ Req 1 ██████████████████████████████│
    │ Req 2 ████████░░░░░░░░░░░░░░░░░░░░░│ ← Padding (wasted)
    │ Req 3 ████████████████░░░░░░░░░░░░░│ ← Padding (wasted)
    │ Req 4 ████████████████████████░░░░░│ ← Padding (wasted)
    └──────────┘
    ↑ Semua selesai bersamaan

    ═══════════════════════════════════════════════════════
    2. DYNAMIC BATCHING
    ═══════════════════════════════════════════════════════
    - Kumpulkan request selama T milidetik, lalu proses
    - Ukuran batch bervariasi (tergantung jumlah request)
    - Biasa dipakai: Triton Inference Server, TorchServe

    Kelebihan: Adaptif terhadap traffic
    Kekurangan: Tambahan latensi T ms

    Visualisasi:
    Timeline: |---T ms---|
    Req masuk:  1  2 3  4
              ↓         ↓
    Batch 1: [1, 2, 3, 4] → Process!

    ═══════════════════════════════════════════════════════
    3. CONTINUOUS BATCHING (State-of-the-Art)
    ═══════════════════════════════════════════════════════
    - Slot yang sudah selesai langsung diisi request baru
    - Tidak perlu menunggu seluruh batch selesai
    - Dipakai oleh: vLLM, TGI (Text Generation Inference)

    Kelebihan: Throughput tertinggi, utilisasi GPU optimal
    Kekurangan: Kompleks untuk diimplementasikan

    Visualisasi:
    ┌──────────────────────────────────────┐
    │ Slot 1: [Req A█████]→[Req E████████]│
    │ Slot 2: [Req B████████████]→[Req F█]│
    │ Slot 3: [Req C███████]→[Req G██████]│
    │ Slot 4: [Req D█████████████████████]│
    └──────────────────────────────────────┘
    ↑ Slot langsung diisi begitu selesai (tidak idle)

    ═══════════════════════════════════════════════════════
    REKOMENDASI:
    - Klasifikasi/embedding → Static/Dynamic Batching
    - Text generation (LLM) → Continuous Batching (vLLM)
    - Real-time inference → Dynamic Batching + timeout kecil
    ═══════════════════════════════════════════════════════
    """)


def main():
    demo_single_vs_batch()
    demo_batch_size_impact()
    demo_strategi_batching()

    print("\n✅ Selesai! Lanjut ke: 3_caching_kv_cache.py")

if __name__ == "__main__":
    main()
