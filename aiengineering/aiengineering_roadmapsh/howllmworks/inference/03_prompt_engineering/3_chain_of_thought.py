"""
=================================================================
3. CHAIN-OF-THOUGHT (CoT) PROMPTING
=================================================================
Chain-of-Thought = meminta model untuk "berpikir langkah demi 
langkah" sebelum memberikan jawaban akhir.

Mengapa CoT penting:
- Meningkatkan akurasi pada masalah yang butuh reasoning
- Model "menunjukkan pekerjaannya" → lebih bisa diverifikasi
- Sangat efektif untuk: matematika, logika, analisis, coding

Variasi CoT:
1. Zero-Shot CoT: Cukup tambahkan "Let's think step by step"
2. Few-Shot CoT: Berikan contoh dengan langkah reasoning
3. Self-Consistency: Generate beberapa jawaban, ambil majority
=================================================================
"""


def demo_tanpa_vs_dengan_cot():
    """Perbandingan output tanpa dan dengan Chain-of-Thought."""
    print("=" * 60)
    print("DEMO 1: Tanpa CoT vs Dengan CoT")
    print("=" * 60)

    # Soal yang butuh reasoning
    soal = "Sebuah toko memberikan diskon 20%, lalu member card memberikan diskon tambahan 10% dari harga setelah diskon pertama. Jika harga asli sepatu adalah Rp 500.000, berapa yang harus dibayar?"

    print(f"\n📝 Soal: {soal}")

    # Tanpa CoT
    prompt_tanpa_cot = f"""
Jawab pertanyaan berikut:
{soal}
Jawaban: """

    print(f"\n❌ PROMPT TANPA CoT:")
    print(f"   {prompt_tanpa_cot.strip()}")
    print(f"\n   Kemungkinan jawaban model: 'Rp 350.000' (SALAH!)")
    print(f"   Model mungkin langsung menghitung 20%+10% = 30%")
    print(f"   500.000 x 0.7 = 350.000 → SALAH karena diskon bertingkat")

    # Dengan CoT
    prompt_dengan_cot = f"""
Jawab pertanyaan berikut. Pikirkan langkah demi langkah.

{soal}

Mari kita selesaikan langkah demi langkah:"""

    print(f"\n✅ PROMPT DENGAN CoT:")
    print(f"   {prompt_dengan_cot.strip()}")
    print(f"""
   Jawaban yang diharapkan:
   Langkah 1: Harga asli = Rp 500.000
   Langkah 2: Diskon pertama 20% = Rp 500.000 × 0.20 = Rp 100.000
   Langkah 3: Harga setelah diskon 1 = Rp 500.000 - Rp 100.000 = Rp 400.000
   Langkah 4: Diskon member 10% dari Rp 400.000 = Rp 400.000 × 0.10 = Rp 40.000
   Langkah 5: Harga final = Rp 400.000 - Rp 40.000 = Rp 360.000
   
   Jawaban: Rp 360.000 ✅ (BENAR!)
    """)


def demo_zero_shot_cot():
    """Zero-Shot CoT — cukup tambahkan magic phrase."""
    print("=" * 60)
    print("DEMO 2: Zero-Shot CoT (Magic Phrase)")
    print("=" * 60)

    print("""
    💡 Zero-Shot CoT sangat sederhana. Cukup tambahkan salah satu
       kalimat "ajaib" ini di akhir prompt:

    🔮 Magic Phrases:
       1. "Let's think step by step."        (paling populer)
       2. "Let's work this out step by step."
       3. "Think carefully and explain your reasoning."
       4. "Show your work."
       5. "Break this down into steps."

    📝 Contoh Penggunaan:
    """)

    contoh_soal = [
        {
            "soal": "Jika 3 orang bisa mengecat 1 rumah dalam 6 hari, berapa hari yang dibutuhkan 6 orang untuk mengecat rumah yang sama?",
            "tanpa_cot": "12 hari (SALAH — model keliru mengalikan)",
            "dengan_cot": """
            Langkah 1: 3 orang × 6 hari = 18 orang-hari total kerja
            Langkah 2: 6 orang × ? hari = 18 orang-hari
            Langkah 3: ? = 18 / 6 = 3 hari ✅"""
        },
        {
            "soal": "Di sebuah ruangan ada 3 switch. Masing-masing terhubung ke 1 dari 3 lampu di ruangan lain. Kamu hanya boleh masuk ruangan lampu 1 kali. Bagaimana cara tahu switch mana untuk lampu mana?",
            "tanpa_cot": "Coba satu per satu (tidak membantu, hanya boleh masuk 1x)",
            "dengan_cot": """
            Langkah 1: Nyalakan switch 1, tunggu 5 menit
            Langkah 2: Matikan switch 1, nyalakan switch 2
            Langkah 3: Masuk ruangan lampu
            Langkah 4: Lampu menyala = switch 2
            Langkah 5: Lampu mati tapi hangat = switch 1
            Langkah 6: Lampu mati dan dingin = switch 3 ✅"""
        }
    ]

    for i, c in enumerate(contoh_soal, 1):
        print(f"\n   Soal {i}: {c['soal']}")
        print(f"   ❌ Tanpa CoT: {c['tanpa_cot']}")
        print(f"   ✅ Dengan CoT: {c['dengan_cot']}")


def demo_few_shot_cot():
    """Few-Shot CoT — contoh dengan langkah reasoning."""
    print("\n" + "=" * 60)
    print("DEMO 3: Few-Shot CoT (Contoh + Reasoning)")
    print("=" * 60)

    prompt = """Selesaikan soal berikut dengan menunjukkan langkah-langkah.

Contoh 1:
Soal: Budi punya 15 apel. Dia memberikan 1/3 ke Ani dan 2/5 dari sisa ke Cici. Berapa apel yang tersisa?
Langkah:
1. Apel diberikan ke Ani: 15 × 1/3 = 5 apel
2. Sisa setelah Ani: 15 - 5 = 10 apel  
3. Apel diberikan ke Cici: 10 × 2/5 = 4 apel
4. Sisa akhir: 10 - 4 = 6 apel
Jawaban: 6 apel

Contoh 2:
Soal: Kereta A berangkat jam 08:00 dengan kecepatan 60 km/jam. Kereta B berangkat jam 09:00 dengan kecepatan 80 km/jam dari stasiun yang sama arah yang sama. Jam berapa Kereta B menyusul Kereta A?
Langkah:
1. Jam 09:00, Kereta A sudah berjalan 1 jam = 60 km di depan
2. Selisih kecepatan: 80 - 60 = 20 km/jam
3. Waktu menyusul: 60 km / 20 km/jam = 3 jam setelah jam 09:00
4. Jam menyusul: 09:00 + 3 jam = 12:00
Jawaban: Jam 12:00 siang

Sekarang selesaikan:
Soal: Sebuah tangki bisa diisi penuh oleh pipa A dalam 4 jam dan pipa B dalam 6 jam. Jika kedua pipa dibuka bersamaan, berapa lama tangki penuh?
Langkah:"""

    print(f"\n📝 Prompt Few-Shot CoT:\n{prompt}")

    print(f"""
    ✅ Expected Response:
    1. Pipa A mengisi 1/4 tangki per jam
    2. Pipa B mengisi 1/6 tangki per jam
    3. Bersama: 1/4 + 1/6 = 3/12 + 2/12 = 5/12 tangki per jam
    4. Waktu penuh: 12/5 = 2.4 jam = 2 jam 24 menit
    Jawaban: 2 jam 24 menit
    """)


def demo_self_consistency():
    """Self-Consistency — generate beberapa jawaban, ambil majority vote."""
    print("=" * 60)
    print("DEMO 4: Self-Consistency (Multiple CoT + Voting)")
    print("=" * 60)

    print("""
    💡 Self-Consistency menggabungkan CoT dengan sampling:

    Langkah:
    1. Generate N jawaban CoT (dengan temperature > 0)
    2. Ambil jawaban akhir dari masing-masing
    3. Pilih jawaban yang paling sering muncul (majority vote)

    Contoh: "Berapa 17 × 23?"

    Run 1 (CoT path A):
      17 × 23 = 17 × 20 + 17 × 3 = 340 + 51 = 391 ✅

    Run 2 (CoT path B):
      17 × 23 = (20-3) × 23 = 460 - 69 = 391 ✅

    Run 3 (CoT path C): 
      17 × 23 = 17 × 25 - 17 × 2 = 425 - 34 = 391 ✅

    Majority Vote: 391 (3/3 setuju) → High confidence!

    📌 Implementasi di kode:
    """)

    print("""
    from openai import OpenAI
    from collections import Counter

    def self_consistency(client, prompt, n=5, temperature=0.7):
        responses = []
        for _ in range(n):
            resp = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature
            )
            # Ekstrak jawaban akhir dari response
            answer = extract_final_answer(resp.choices[0].message.content)
            responses.append(answer)
        
        # Majority vote
        counter = Counter(responses)
        best_answer = counter.most_common(1)[0][0]
        confidence = counter.most_common(1)[0][1] / n
        
        return best_answer, confidence
    """)


def main():
    demo_tanpa_vs_dengan_cot()
    print()
    demo_zero_shot_cot()
    print()
    demo_few_shot_cot()
    print()
    demo_self_consistency()

    print("\n✅ Selesai! Lanjut ke: 4_system_prompt_design.py")

if __name__ == "__main__":
    main()
