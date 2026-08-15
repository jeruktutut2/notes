"""
=================================================================
2. HUGGING FACE MODEL HUB
=================================================================
Hugging Face Hub adalah "GitHub-nya model AI" — repositori terbesar
untuk model pre-trained, dataset, dan spaces (demo app).

Fitur utama:
- 500K+ model tersedia
- Filter berdasarkan task, bahasa, ukuran, lisensi
- Model card (dokumentasi model)
- Inference API (coba model tanpa download)
- Model versioning (seperti git)

Cara memilih model di Hub:
1. Tentukan TASK (text-generation, classification, dsb.)
2. Filter berdasarkan bahasa (jika perlu)
3. Urutkan berdasarkan downloads/likes
4. Cek model card (performa, limitasi, lisensi)
5. Coba via Inference API sebelum download
=================================================================
"""

from transformers import AutoTokenizer, AutoModel, AutoModelForSequenceClassification
from huggingface_hub import list_models, model_info
import torch

def demo_cari_model():
    """Mencari model di Hugging Face Hub secara programatis."""
    print("=" * 60)
    print("DEMO 1: Mencari Model di Hugging Face Hub")
    print("=" * 60)

    # Mencari model untuk task tertentu
    tasks = [
        "text-classification",
        "text-generation",
        "question-answering",
    ]

    for task in tasks:
        print(f"\n🔍 Task: {task}")
        print("-" * 40)
        
        # Ambil 5 model terpopuler untuk task ini
        models = list(list_models(
            task=task,
            sort="downloads",
            direction=-1,
            limit=5
        ))

        for i, m in enumerate(models, 1):
            downloads = getattr(m, 'downloads', 'N/A')
            likes = getattr(m, 'likes', 'N/A')
            print(f"   {i}. {m.id}")
            print(f"      Downloads: {downloads:,} | Likes: {likes}")


def demo_model_card_info():
    """Membaca informasi detail dari sebuah model (model card)."""
    print("\n" + "=" * 60)
    print("DEMO 2: Membaca Model Card / Info Model")
    print("=" * 60)

    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    print(f"\n📋 Info model: {nama_model}")

    info = model_info(nama_model)

    print(f"   ID          : {info.id}")
    print(f"   Author      : {info.author}")
    print(f"   Downloads   : {info.downloads:,}")
    print(f"   Likes       : {info.likes}")
    print(f"   Pipeline Tag: {info.pipeline_tag}")
    print(f"   Library     : {info.library_name}")
    print(f"   Tags        : {', '.join(info.tags[:10])}")
    print(f"   Last Update : {info.last_modified}")

    if info.card_data:
        print(f"   License     : {getattr(info.card_data, 'license', 'N/A')}")


def demo_download_dan_gunakan():
    """Mendownload model dari Hub dan langsung gunakan untuk inference."""
    print("\n" + "=" * 60)
    print("DEMO 3: Download & Gunakan Model dari Hub")
    print("=" * 60)

    nama_model = "distilbert-base-uncased-finetuned-sst-2-english"
    print(f"\n📦 Mengunduh model: {nama_model}")

    # Download otomatis dari Hub (di-cache setelah pertama kali)
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForSequenceClassification.from_pretrained(nama_model)
    model.eval()

    print("✅ Model berhasil dimuat!")
    print(f"   Tipe model     : {type(model).__name__}")
    print(f"   Jumlah parameter: {sum(p.numel() for p in model.parameters()):,}")

    # Jalankan inference
    teks = "Hugging Face makes AI accessible to everyone!"
    inputs = tokenizer(teks, return_tensors="pt")

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)
    label_id = torch.argmax(probs).item()
    label_map = {0: "NEGATIVE", 1: "POSITIVE"}

    print(f"\n   Input    : {teks}")
    print(f"   Prediksi : {label_map[label_id]} (confidence: {probs[0][label_id]:.4f})")


def demo_model_caching():
    """Menjelaskan mekanisme caching model Hugging Face."""
    print("\n" + "=" * 60)
    print("DEMO 4: Mekanisme Caching Model")
    print("=" * 60)

    print("""
    📦 Bagaimana Caching Bekerja:

    1. Pertama kali model.from_pretrained("model_name"):
       - Model diunduh dari Hugging Face Hub
       - Disimpan di cache lokal (~/.cache/huggingface/)
    
    2. Panggilan selanjutnya:
       - Model dimuat dari cache lokal (CEPAT!)
       - Tidak perlu internet
    
    3. Mengatur lokasi cache:
       - Set env: TRANSFORMERS_CACHE=/path/to/cache
       - Atau: HF_HOME=/path/to/hf_home
    
    4. Mengecek ukuran cache:
       - huggingface-cli scan-cache
    
    5. Membersihkan cache:
       - huggingface-cli delete-cache
    
    💡 Tips:
    - Model besar (7B+) bisa memakan 15-30 GB storage
    - Gunakan quantized model untuk menghemat ruang
    - Set cache di SSD untuk loading lebih cepat
    """)


def main():
    demo_cari_model()
    demo_model_card_info()
    demo_download_dan_gunakan()
    demo_model_caching()

    print("\n✅ Selesai! Lanjut ke: 3_ollama_local_inference.py")

if __name__ == "__main__":
    main()
