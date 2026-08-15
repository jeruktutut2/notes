"""
=================================================================
1. ZERO-SHOT PROMPTING
=================================================================
Zero-Shot = memberikan instruksi ke model TANPA contoh apapun.
Model mengandalkan pengetahuan yang sudah dimiliki dari training.

Kapan efektif:
✅ Task umum yang sudah dipahami model (summarize, translate, classify)
✅ Menggunakan model besar (GPT-4, Claude, Llama 70B+)
✅ Task tidak memerlukan format output yang sangat spesifik

Kapan kurang efektif:
❌ Task sangat spesifik/domain-specific
❌ Perlu format output yang presisi
❌ Menggunakan model kecil (7B atau kurang)
=================================================================
"""

from transformers import pipeline


def demo_zero_shot_klasifikasi():
    """Zero-Shot Classification — klasifikasi tanpa contoh training."""
    print("=" * 60)
    print("DEMO 1: Zero-Shot Classification")
    print("=" * 60)

    classifier = pipeline("zero-shot-classification")

    # Contoh 1: Klasifikasi topik berita
    teks_berita = [
        "The new Tesla Model Y has broken sales records in Q3 2024.",
        "Barcelona won the Champions League final with a stunning comeback.",
        "The Federal Reserve decided to maintain interest rates unchanged.",
        "A new species of deep-sea fish was discovered near the Mariana Trench.",
    ]

    kategori = ["technology", "sports", "finance", "science", "politics"]

    print(f"\n🏷️ Kategori tersedia: {kategori}")
    print(f"\n📊 Hasil Klasifikasi Zero-Shot:")
    print("-" * 60)

    for teks in teks_berita:
        hasil = classifier(teks, kategori)
        top_label = hasil['labels'][0]
        top_score = hasil['scores'][0]
        print(f"   Teks : {teks[:60]}...")
        print(f"   Label: {top_label} (confidence: {top_score:.4f})")
        print()


def demo_zero_shot_sentiment():
    """Zero-Shot Sentiment — analisis sentimen tanpa fine-tuning."""
    print("=" * 60)
    print("DEMO 2: Zero-Shot Sentiment Analysis")
    print("=" * 60)

    classifier = pipeline("zero-shot-classification")

    ulasan = [
        "Makanan di restoran ini lezat sekali, pelayanannya ramah!",
        "Sangat mengecewakan, pesanan datang terlambat 2 jam.",
        "Biasa saja, tidak ada yang spesial dari tempat ini.",
    ]

    sentimen_labels = ["positif", "negatif", "netral"]

    print(f"\n📊 Analisis Sentimen Zero-Shot:")
    print(f"   Labels: {sentimen_labels}")
    print("-" * 60)

    for teks in ulasan:
        hasil = classifier(teks, sentimen_labels)
        top = hasil['labels'][0]
        skor = hasil['scores'][0]
        print(f"   Teks     : {teks}")
        print(f"   Sentimen : {top} (skor: {skor:.4f})")
        print()


def demo_zero_shot_prompt_patterns():
    """Berbagai pola prompt Zero-Shot yang umum digunakan."""
    print("=" * 60)
    print("DEMO 3: Pola-Pola Zero-Shot Prompt")
    print("=" * 60)

    print("""
    📝 Pola Zero-Shot yang Efektif:

    1. INSTRUKSI LANGSUNG
       "Terjemahkan ke bahasa Indonesia: Hello, how are you?"
    
    2. ROLE-BASED
       "Sebagai ahli nutrisi, jelaskan manfaat protein."
    
    3. FORMAT SPESIFIK
       "Klasifikasikan sentimen teks berikut sebagai POSITIF, NEGATIF, 
        atau NETRAL: [teks]"
    
    4. CONSTRAINT/BATASAN
       "Jelaskan quantum computing dalam maksimal 3 kalimat 
        yang bisa dipahami anak SD."
    
    5. TASK DECOMPOSITION
       "Berikan 3 poin utama dari artikel berikut: [artikel]"

    ⚡ Tips Zero-Shot yang Baik:
    - Gunakan instruksi yang JELAS dan SPESIFIK
    - Tentukan FORMAT output yang diinginkan
    - Berikan KONTEKS yang cukup
    - Gunakan BATASAN jika perlu (panjang, gaya, dll.)
    """)


def main():
    demo_zero_shot_klasifikasi()
    print()
    demo_zero_shot_sentiment()
    print()
    demo_zero_shot_prompt_patterns()

    print("\n✅ Selesai! Lanjut ke: 2_few_shot_prompting.py")

if __name__ == "__main__":
    main()
