"""
=================================================================
2. FEW-SHOT PROMPTING
=================================================================
Few-Shot = memberikan beberapa CONTOH (2-5) sebelum pertanyaan
utama, agar model memahami pola, format, dan gaya yang diinginkan.

Prinsip:
- Model "belajar" dari contoh yang diberikan di dalam prompt
- TIDAK perlu training ulang — contoh diberikan saat inference
- Semakin relevan contoh, semakin baik hasilnya

Kapan menggunakan Few-Shot:
✅ Perlu format output yang konsisten/spesifik
✅ Task yang tidak umum / domain-specific
✅ Model lebih kecil yang butuh "guidance"
✅ Konsistensi output penting (misalnya untuk parsing)
=================================================================
"""

import json

def demo_few_shot_klasifikasi():
    """Few-Shot untuk klasifikasi sentimen dengan format konsisten."""
    print("=" * 60)
    print("DEMO 1: Few-Shot Classification")
    print("=" * 60)

    # Contoh prompt few-shot (simulasi — di production dipakai dengan LLM API)
    prompt = """Klasifikasikan sentimen ulasan berikut.

Contoh 1:
Ulasan: "Sepatu ini sangat nyaman dan tahan lama!"
Sentimen: POSITIF

Contoh 2:
Ulasan: "Kualitasnya buruk, jahitannya berantakan."
Sentimen: NEGATIF

Contoh 3:
Ulasan: "Harganya standar, kualitas cukup."
Sentimen: NETRAL

Sekarang klasifikasikan:
Ulasan: "Pengiriman cepat tapi barangnya rusak saat sampai."
Sentimen: """

    print(f"\n📝 Prompt Few-Shot:\n{prompt}")
    print(f"\n💡 Model akan menjawab: NEGATIF")
    print(f"   (karena sudah belajar pola dari 3 contoh di atas)")

    print("""
    🔑 Anatomi Prompt Few-Shot:
    ┌──────────────────────────────────────┐
    │ 1. Instruksi umum                     │
    │ 2. Contoh 1: Input → Output           │
    │ 3. Contoh 2: Input → Output           │
    │ 4. Contoh 3: Input → Output           │
    │ 5. Input baru → [Model melengkapi]    │
    └──────────────────────────────────────┘
    """)


def demo_few_shot_structured_output():
    """Few-Shot untuk menghasilkan output terstruktur (JSON)."""
    print("=" * 60)
    print("DEMO 2: Few-Shot untuk Structured Output (JSON)")
    print("=" * 60)

    prompt = """Ekstrak informasi produk dari deskripsi berikut ke format JSON.

Contoh 1:
Deskripsi: "Laptop ASUS ROG 16 inch, RAM 32GB, SSD 1TB, harga 25 juta"
JSON: {"nama": "ASUS ROG", "kategori": "laptop", "ukuran_layar": "16 inch", "ram": "32GB", "storage": "1TB SSD", "harga": 25000000}

Contoh 2:
Deskripsi: "iPhone 15 Pro Max 256GB warna titanium natural, harga 22.5 juta"
JSON: {"nama": "iPhone 15 Pro Max", "kategori": "smartphone", "storage": "256GB", "warna": "titanium natural", "harga": 22500000}

Sekarang ekstrak:
Deskripsi: "Samsung Galaxy Tab S9 FE 10.9 inch, RAM 6GB, storage 128GB, warna mint, harga 7.5 juta"
JSON: """

    expected_output = {
        "nama": "Samsung Galaxy Tab S9 FE",
        "kategori": "tablet",
        "ukuran_layar": "10.9 inch",
        "ram": "6GB",
        "storage": "128GB",
        "warna": "mint",
        "harga": 7500000
    }

    print(f"\n📝 Prompt:\n{prompt}")
    print(f"\n✅ Expected Output:")
    print(f"   {json.dumps(expected_output, indent=2)}")

    print("""
    💡 Tips Structured Output dengan Few-Shot:
    - Berikan contoh JSON yang konsisten formatnya
    - Gunakan field name yang sama di semua contoh
    - Sertakan edge case (misal field optional)
    - Validasi output JSON di aplikasi Anda
    """)


def demo_few_shot_translation():
    """Few-Shot untuk style-specific translation."""
    print("=" * 60)
    print("DEMO 3: Few-Shot Translation (Style-Specific)")
    print("=" * 60)

    prompt = """Terjemahkan kalimat teknis berikut ke bahasa Indonesia yang mudah dipahami. Gunakan analogi sehari-hari jika memungkinkan.

Contoh 1:
English: "The API rate limit has been exceeded."
Indonesia: "Batas jumlah permintaan ke server sudah terlewati — seperti antrian yang terlalu panjang, perlu menunggu sebentar."

Contoh 2:
English: "The model is overfitting to the training data."
Indonesia: "Model terlalu menghafal data latihan — seperti murid yang hanya menghafal jawaban ujian tanpa benar-benar paham materinya."

Sekarang terjemahkan:
English: "The neural network's gradient vanishing problem prevents deep layers from learning effectively."
Indonesia: """

    expected = ("Masalah sinyal yang semakin melemah di jaringan saraf tiruan "
                "membuat lapisan-lapisan dalam tidak bisa belajar dengan baik — "
                "seperti pesan berantai yang semakin kabur setelah disampaikan "
                "ke banyak orang.")

    print(f"\n📝 Prompt:\n{prompt}")
    print(f"\n✅ Contoh jawaban yang diharapkan:")
    print(f"   {expected}")


def demo_tips_few_shot():
    """Tips dan best practices few-shot prompting."""
    print("\n" + "=" * 60)
    print("TIPS & BEST PRACTICES FEW-SHOT PROMPTING")
    print("=" * 60)

    print("""
    📌 BERAPA CONTOH YANG IDEAL?
       - 2-3 contoh: Cukup untuk kebanyakan task
       - 4-5 contoh: Untuk task kompleks atau format rumit
       - >5 contoh: Jarang diperlukan, hati-hati context limit

    📌 PEMILIHAN CONTOH
       - Pilih contoh yang BERAGAM (cover berbagai kasus)
       - Sertakan EDGE CASE (kasus khusus/sulit)
       - Contoh harus KONSISTEN formatnya
       - Urutan contoh bisa mempengaruhi hasil

    📌 FORMAT CONTOH
       - Gunakan separator yang jelas (---, Contoh N:, dsb.)
       - Label input dan output secara eksplisit
       - Pertahankan format yang IDENTIK di semua contoh

    📌 COMMON MISTAKES
       ❌ Contoh terlalu mirip satu sama lain
       ❌ Contoh tidak representatif dari kasus nyata
       ❌ Format antar contoh tidak konsisten
       ❌ Terlalu banyak contoh (membuang context window)

    📌 VARIASI FEW-SHOT
       - Few-Shot with CoT: Contoh + langkah berpikir
       - Dynamic Few-Shot: Pilih contoh berdasarkan input
       - Retrieval-Augmented Few-Shot: Ambil contoh dari database
    """)


def main():
    demo_few_shot_klasifikasi()
    print()
    demo_few_shot_structured_output()
    print()
    demo_few_shot_translation()
    print()
    demo_tips_few_shot()

    print("\n✅ Selesai! Lanjut ke: 3_chain_of_thought.py")

if __name__ == "__main__":
    main()
