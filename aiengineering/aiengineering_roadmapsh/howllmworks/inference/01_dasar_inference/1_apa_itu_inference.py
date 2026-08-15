"""
=================================================================
1. APA ITU INFERENCE?
=================================================================
Inference adalah proses menggunakan model ML/AI yang sudah dilatih
(pre-trained) untuk membuat prediksi atau menghasilkan output dari
data input baru.

Analogi Sederhana:
- Training  = Belajar di sekolah (membaca buku, mengerjakan latihan)
- Inference = Mengerjakan ujian (menggunakan ilmu yang sudah dipelajari)

Perbedaan Utama:
┌──────────────┬────────────────────┬─────────────────────┐
│   Aspek      │     Training       │     Inference       │
├──────────────┼────────────────────┼─────────────────────┤
│ Tujuan       │ Melatih bobot      │ Menghasilkan output │
│ Data         │ Dataset besar      │ Input tunggal/batch │
│ Waktu        │ Berjam-jam/hari    │ Milidetik/detik     │
│ GPU          │ Wajib (biasanya)   │ Opsional            │
│ Gradient     │ Dihitung (backprop)│ Tidak dihitung      │
│ Mode PyTorch │ model.train()      │ model.eval()        │
└──────────────┴────────────────────┴─────────────────────┘
=================================================================
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time

def demo_inference_sederhana():
    """Demo inference paling dasar: sentiment analysis."""
    print("=" * 60)
    print("DEMO 1: Inference Sederhana - Sentiment Analysis")
    print("=" * 60)

    # 1. Muat model dan tokenizer yang sudah pre-trained
    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    print(f"\n📦 Memuat model: {nama_model}")
    
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForSequenceClassification.from_pretrained(nama_model)

    # 2. Pindahkan model ke mode evaluasi (inference)
    # Ini mematikan dropout dan batch normalization training behavior
    model.eval()
    print("✅ Model dalam mode eval (inference)")

    # 3. Siapkan input teks
    teks_input = [
        "I love this product! It's amazing and works perfectly.",
        "This is terrible. Worst purchase I've ever made.",
        "The weather is okay today, nothing special."
    ]

    print(f"\n📝 Teks yang akan dianalisis ({len(teks_input)} kalimat):")
    for i, t in enumerate(teks_input, 1):
        print(f"   {i}. {t}")

    # 4. Tokenisasi (mengubah teks menjadi angka/tensor)
    inputs = tokenizer(teks_input, padding=True, truncation=True, return_tensors="pt")
    print(f"\n🔤 Hasil tokenisasi:")
    print(f"   Input IDs shape: {inputs['input_ids'].shape}")
    print(f"   Attention Mask shape: {inputs['attention_mask'].shape}")

    # 5. Jalankan inference (tanpa menghitung gradient)
    # torch.no_grad() menghemat memori dan mempercepat komputasi
    print("\n⚡ Menjalankan inference...")
    waktu_mulai = time.time()

    with torch.no_grad():  # KUNCI: tidak perlu gradient saat inference
        outputs = model(**inputs)

    waktu_selesai = time.time()
    latensi = (waktu_selesai - waktu_mulai) * 1000  # dalam milidetik

    # 6. Proses output (logits → probabilitas → label)
    logits = outputs.logits
    probabilitas = torch.softmax(logits, dim=-1)
    prediksi = torch.argmax(probabilitas, dim=-1)

    label_map = {0: "NEGATIF 😞", 1: "POSITIF 😊"}

    print(f"\n📊 Hasil Inference (latensi: {latensi:.2f} ms):")
    print("-" * 60)
    for i, teks in enumerate(teks_input):
        label = label_map[prediksi[i].item()]
        confidence = probabilitas[i][prediksi[i]].item() * 100
        print(f"   Teks    : {teks[:50]}...")
        print(f"   Prediksi: {label} (confidence: {confidence:.1f}%)")
        print()


def demo_perbedaan_train_vs_eval():
    """Menunjukkan perbedaan mode train vs eval pada model."""
    print("=" * 60)
    print("DEMO 2: Perbedaan Mode Training vs Inference")
    print("=" * 60)

    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    model = AutoModelForSequenceClassification.from_pretrained(nama_model)
    tokenizer = AutoTokenizer.from_pretrained(nama_model)

    teks = "This movie is great!"
    inputs = tokenizer(teks, return_tensors="pt")

    # Mode TRAINING (default saat model dimuat)
    model.train()
    print("\n🏋️ Mode Training (model.train()):")
    print(f"   - model.training = {model.training}")
    print("   - Dropout AKTIF (output bisa bervariasi)")
    
    hasil_train = []
    for i in range(3):
        with torch.no_grad():
            out = model(**inputs)
        prob = torch.softmax(out.logits, dim=-1)
        hasil_train.append(prob[0].tolist())
    
    print("   - 3x inference berturut-turut:")
    for i, h in enumerate(hasil_train):
        print(f"     Run {i+1}: NEG={h[0]:.6f}, POS={h[1]:.6f}")

    # Mode INFERENCE/EVAL
    model.eval()
    print(f"\n🎯 Mode Inference (model.eval()):")
    print(f"   - model.training = {model.training}")
    print("   - Dropout MATI (output konsisten)")
    
    hasil_eval = []
    for i in range(3):
        with torch.no_grad():
            out = model(**inputs)
        prob = torch.softmax(out.logits, dim=-1)
        hasil_eval.append(prob[0].tolist())
    
    print("   - 3x inference berturut-turut:")
    for i, h in enumerate(hasil_eval):
        print(f"     Run {i+1}: NEG={h[0]:.6f}, POS={h[1]:.6f}")

    print("\n💡 Kesimpulan:")
    print("   - Saat INFERENCE, selalu gunakan model.eval() + torch.no_grad()")
    print("   - model.eval() → mematikan dropout, stabilkan batch norm")
    print("   - torch.no_grad() → hemat memori, percepat komputasi")


def main():
    demo_inference_sederhana()
    print("\n")
    demo_perbedaan_train_vs_eval()
    print("\n✅ Selesai! Lanjut ke: 2_pipeline_inference.py")

if __name__ == "__main__":
    main()
