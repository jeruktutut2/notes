import os
from openai import OpenAI

def main():
    print("=== 2.2 Chain-of-Thought (CoT) Prompting ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # CHAIN-OF-THOUGHT (CoT)
    # Teknik meminta LLM untuk berpikir langkah demi langkah sebelum
    # memberikan jawaban akhir. Sangat efektif untuk:
    # - Soal matematika / logika
    # - Analisis kompleks
    # - Pengambilan keputusan multi-langkah
    # ---------------------------------------------------------------

    soal = (
        "Di sebuah toko, harga 3 buku dan 2 pensil adalah Rp 45.000. "
        "Harga 1 buku dan 4 pensil adalah Rp 25.000. "
        "Berapa harga 1 buku dan 1 pensil masing-masing?"
    )

    # Contoh 1: TANPA Chain-of-Thought
    print("=" * 60)
    print("Contoh 1: TANPA Chain-of-Thought (Langsung Jawab)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Jawab pertanyaan berikut dengan singkat."},
            {"role": "user", "content": soal}
        ],
        temperature=0.0
    )
    print(f"Soal: {soal}")
    print(f"\nJawaban:\n{response.choices[0].message.content}\n")

    # Contoh 2: DENGAN Chain-of-Thought (Berpikir Langkah Demi Langkah)
    print("=" * 60)
    print("Contoh 2: DENGAN Chain-of-Thought (Step-by-Step)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah tutor matematika. Selesaikan soal langkah demi langkah. "
                    "Format jawabanmu:\n"
                    "Langkah 1: ...\n"
                    "Langkah 2: ...\n"
                    "...\n"
                    "Jawaban Akhir: ..."
                )
            },
            {"role": "user", "content": soal}
        ],
        temperature=0.0
    )
    print(f"Soal: {soal}")
    print(f"\nJawaban CoT:\n{response.choices[0].message.content}\n")

    # Contoh 3: Zero-Shot CoT (Cukup tambahkan "pikirkan langkah demi langkah")
    print("=" * 60)
    print("Contoh 3: Zero-Shot CoT (Trik Sederhana)")
    print("=" * 60)

    soal_logika = (
        "Ani lebih tua dari Budi. Budi lebih tua dari Cici. "
        "Dedi lebih muda dari Cici tapi lebih tua dari Evi. "
        "Siapa yang paling muda?"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": soal_logika + "\n\nMari kita pikirkan langkah demi langkah."}
        ],
        temperature=0.0
    )
    print(f"Soal: {soal_logika}")
    print(f"\nJawaban Zero-Shot CoT:\n{response.choices[0].message.content}\n")

    # Contoh 4: CoT untuk Analisis/Keputusan (bukan hanya matematika)
    print("=" * 60)
    print("Contoh 4: CoT untuk Pengambilan Keputusan")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah konsultan teknologi. Saat menjawab, gunakan framework ini:\n"
                    "1. Analisis Situasi: Pahami konteks\n"
                    "2. Identifikasi Opsi: Daftar pilihan yang tersedia\n"
                    "3. Pro & Kontra: Evaluasi setiap opsi\n"
                    "4. Rekomendasi: Berikan saran terbaik dengan alasan"
                )
            },
            {
                "role": "user",
                "content": (
                    "Startup saya punya 3 developer dan budget terbatas. "
                    "Kami ingin membuat chatbot customer service. "
                    "Apakah lebih baik pakai OpenAI API, self-host open source model, atau pakai platform no-code?"
                )
            }
        ],
        temperature=0.3
    )
    print(f"Jawaban CoT Keputusan:\n{response.choices[0].message.content}")

    print("\n✅ Selesai! Memahami teknik Chain-of-Thought prompting.")
    print("\nRingkasan:")
    print("- CoT: Minta LLM berpikir step-by-step → jawaban lebih akurat")
    print("- Zero-Shot CoT: Cukup tambahkan 'pikirkan langkah demi langkah'")
    print("- CoT bisa dipakai untuk matematika, logika, DAN keputusan bisnis")
    print("- Berikan format/framework agar output lebih terstruktur")

if __name__ == "__main__":
    main()
