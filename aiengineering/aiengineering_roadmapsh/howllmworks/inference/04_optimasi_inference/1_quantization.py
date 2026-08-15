"""
=================================================================
1. QUANTIZATION — Mengurangi Ukuran Model
=================================================================
Quantization = mengubah presisi numerik bobot model dari
floating point tinggi (FP32/FP16) ke integer yang lebih kecil
(INT8/INT4).

Analogi: Seperti mengompres foto dari RAW (50MB) ke JPEG (5MB)
— ukurannya jauh lebih kecil, kualitasnya sedikit berkurang
tapi masih bisa dipakai.

Tipe Quantization:
┌───────────────┬──────────┬────────────┬─────────────────┐
│ Presisi       │ Bit/Param│ Ukuran 7B  │ Kualitas        │
├───────────────┼──────────┼────────────┼─────────────────┤
│ FP32 (Full)   │ 32 bit   │ ~28 GB     │ Terbaik         │
│ FP16 (Half)   │ 16 bit   │ ~14 GB     │ Sangat baik     │
│ INT8          │ 8 bit    │ ~7 GB      │ Baik            │
│ INT4 (GPTQ/AWQ)│ 4 bit   │ ~3.5 GB   │ Cukup baik      │
│ GGUF Q4_K_M   │ ~4.5 bit │ ~4 GB     │ Baik (Ollama)   │
└───────────────┴──────────┴────────────┴─────────────────┘
=================================================================
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time
import sys


def demo_perbandingan_presisi():
    """Menunjukkan perbedaan presisi dan ukuran memori."""
    print("=" * 60)
    print("DEMO 1: Perbandingan Presisi Numerik")
    print("=" * 60)

    # Simulasi tensor dengan presisi berbeda
    nilai = 3.141592653589793

    tensor_fp32 = torch.tensor(nilai, dtype=torch.float32)
    tensor_fp16 = torch.tensor(nilai, dtype=torch.float16)
    tensor_int8 = torch.tensor(int(nilai * 100), dtype=torch.int8)  # Simulasi

    print(f"\n📊 Representasi nilai π = {nilai}:")
    print(f"   FP32 : {tensor_fp32.item():.15f}  ({tensor_fp32.element_size()} bytes)")
    print(f"   FP16 : {tensor_fp16.item():.15f}  ({tensor_fp16.element_size()} bytes)")
    print(f"   INT8 : {tensor_int8.item()} (scaled)       ({tensor_int8.element_size()} bytes)")

    # Perbandingan memori untuk sebuah tensor besar
    ukuran = (1000, 1000)  # 1M parameter
    t_fp32 = torch.randn(ukuran, dtype=torch.float32)
    t_fp16 = torch.randn(ukuran, dtype=torch.float16)
    t_int8 = torch.randint(-128, 127, ukuran, dtype=torch.int8)

    print(f"\n📦 Memori untuk tensor {ukuran[0]}x{ukuran[1]} (1M elemen):")
    print(f"   FP32 : {t_fp32.nelement() * t_fp32.element_size() / 1024:.0f} KB")
    print(f"   FP16 : {t_fp16.nelement() * t_fp16.element_size() / 1024:.0f} KB")
    print(f"   INT8 : {t_int8.nelement() * t_int8.element_size() / 1024:.0f} KB")


def demo_quantization_model():
    """Demo quantization pada model nyata."""
    print("\n" + "=" * 60)
    print("DEMO 2: Quantization Model (FP32 → FP16)")
    print("=" * 60)

    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(nama_model)

    # Model FP32 (default)
    print(f"\n📦 Memuat model FP32...")
    model_fp32 = AutoModelForSequenceClassification.from_pretrained(nama_model)
    model_fp32.eval()

    param_count = sum(p.numel() for p in model_fp32.parameters())
    mem_fp32 = sum(p.nelement() * p.element_size() for p in model_fp32.parameters())

    print(f"   Parameter : {param_count:,}")
    print(f"   Memori FP32: {mem_fp32 / 1024 / 1024:.2f} MB")

    # Quantize ke FP16
    print(f"\n⚡ Quantize ke FP16...")
    model_fp16 = model_fp32.half()  # Convert ke FP16
    mem_fp16 = sum(p.nelement() * p.element_size() for p in model_fp16.parameters())
    print(f"   Memori FP16: {mem_fp16 / 1024 / 1024:.2f} MB")
    print(f"   Pengurangan: {(1 - mem_fp16/mem_fp32) * 100:.1f}%")

    # Dynamic Quantization (INT8) — hanya untuk CPU
    print(f"\n⚡ Dynamic Quantization ke INT8...")
    model_int8 = torch.quantization.quantize_dynamic(
        model_fp32,
        {torch.nn.Linear},  # Layer yang akan di-quantize
        dtype=torch.qint8
    )

    # Bandingkan kecepatan inference
    teks = "This product is absolutely fantastic and works perfectly!"
    inputs_fp32 = tokenizer(teks, return_tensors="pt")

    print(f"\n⏱️ Perbandingan Kecepatan (100 iterasi):")

    # Benchmark FP32
    model_fp32.eval()
    start = time.time()
    for _ in range(100):
        with torch.no_grad():
            _ = model_fp32(**inputs_fp32)
    time_fp32 = (time.time() - start) * 1000

    # Benchmark INT8
    start = time.time()
    inputs_int8 = tokenizer(teks, return_tensors="pt")
    for _ in range(100):
        with torch.no_grad():
            _ = model_int8(**inputs_int8)
    time_int8 = (time.time() - start) * 1000

    print(f"   FP32 : {time_fp32:.0f} ms total ({time_fp32/100:.1f} ms/iter)")
    print(f"   INT8 : {time_int8:.0f} ms total ({time_int8/100:.1f} ms/iter)")
    print(f"   Speedup: {time_fp32/time_int8:.2f}x")

    # Verifikasi output masih konsisten
    print(f"\n🔍 Verifikasi Akurasi Output:")
    with torch.no_grad():
        out_fp32 = model_fp32(**inputs_fp32)
        out_int8 = model_int8(**inputs_int8)

    prob_fp32 = torch.softmax(out_fp32.logits, dim=-1)
    prob_int8 = torch.softmax(out_int8.logits, dim=-1)

    label_map = {0: "NEGATIVE", 1: "POSITIVE"}

    pred_fp32 = torch.argmax(prob_fp32).item()
    pred_int8 = torch.argmax(prob_int8).item()

    print(f"   FP32: {label_map[pred_fp32]} ({prob_fp32[0][pred_fp32]:.4f})")
    print(f"   INT8: {label_map[pred_int8]} ({prob_int8[0][pred_int8]:.4f})")
    print(f"   Prediksi sama? {'✅ Ya' if pred_fp32 == pred_int8 else '❌ Tidak'}")


def demo_quantization_methods():
    """Penjelasan berbagai metode quantization populer."""
    print("\n" + "=" * 60)
    print("DEMO 3: Metode Quantization Populer")
    print("=" * 60)

    print("""
    📋 METODE QUANTIZATION YANG UMUM:

    1. 🔧 DYNAMIC QUANTIZATION (PyTorch built-in)
       - Quantize saat inference (on-the-fly)
       - Tidak perlu calibration data
       - Cocok untuk: CPU deployment, model kecil-medium
       - Code: torch.quantization.quantize_dynamic(model, ...)

    2. 🔧 GPTQ (GPT Quantization)
       - Post-training quantization (INT4/INT8)
       - Butuh calibration dataset (128 sampel cukup)
       - Cocok untuk: LLM di GPU
       - Library: auto-gptq, optimum
       - Contoh: TheBloke/Llama-2-7B-GPTQ

    3. 🔧 AWQ (Activation-aware Weight Quantization)
       - Lebih akurat dari GPTQ (mempertahankan salient weights)
       - INT4 quantization
       - Cocok untuk: LLM yang butuh akurasi tinggi
       - Library: autoawq
       - Contoh: TheBloke/Llama-2-7B-AWQ

    4. 🔧 GGUF (GPT-Generated Unified Format)
       - Format file untuk model yang sudah di-quantize
       - Dipakai oleh: Ollama, llama.cpp
       - Berbagai level: Q2_K, Q4_K_M, Q5_K_M, Q8_0
       - Cocok untuk: CPU inference, Apple Silicon

    5. 🔧 bitsandbytes (BnB)
       - Quantization oleh library bitsandbytes
       - INT8 dan NF4 (4-bit NormalFloat)
       - Terintegrasi baik dengan Hugging Face
       - Cocok untuk: Fine-tuning dengan QLoRA

    ┌──────────────┬─────────┬──────────┬────────────────┐
    │ Metode       │ Presisi │ Target   │ Use Case       │
    ├──────────────┼─────────┼──────────┼────────────────┤
    │ Dynamic      │ INT8    │ CPU      │ Model kecil    │
    │ GPTQ         │ INT4/8  │ GPU      │ LLM serving    │
    │ AWQ          │ INT4    │ GPU      │ LLM high-acc   │
    │ GGUF         │ 2-8 bit │ CPU/Metal│ Local/edge     │
    │ bitsandbytes │ 4/8 bit │ GPU      │ Fine-tuning    │
    └──────────────┴─────────┴──────────┴────────────────┘
    """)


def main():
    demo_perbandingan_presisi()
    demo_quantization_model()
    demo_quantization_methods()

    print("\n✅ Selesai! Lanjut ke: 2_batching_strategies.py")

if __name__ == "__main__":
    main()
