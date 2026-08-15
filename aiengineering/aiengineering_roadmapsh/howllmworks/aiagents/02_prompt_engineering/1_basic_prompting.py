import os
from openai import OpenAI

def main():
    print("=== 2.1 Basic Prompting (System / User / Assistant Roles) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # MEMAHAMI ROLE MESSAGES
    # Setiap pesan ke LLM punya "role":
    # - system  : Instruksi/persona untuk LLM (karakter, batasan, gaya)
    # - user    : Pesan dari pengguna (pertanyaan, permintaan)
    # - assistant: Jawaban sebelumnya dari LLM (untuk konteks multi-turn)
    # ---------------------------------------------------------------

    # Contoh 1: TANPA System Prompt (LLM menjawab apa adanya)
    print("=" * 60)
    print("Contoh 1: TANPA System Prompt")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Siapa presiden pertama Indonesia?"}
        ],
        temperature=0.3
    )
    print(f"Jawaban: {response.choices[0].message.content}\n")

    # Contoh 2: DENGAN System Prompt (Persona: guru sejarah)
    print("=" * 60)
    print("Contoh 2: DENGAN System Prompt (Persona: Guru Sejarah)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah guru sejarah Indonesia yang berpengalaman. "
                    "Jawab pertanyaan murid dengan gaya mengajar yang santai, "
                    "berikan fakta menarik, dan akhiri dengan pertanyaan refleksi."
                )
            },
            {"role": "user", "content": "Siapa presiden pertama Indonesia?"}
        ],
        temperature=0.5
    )
    print(f"Jawaban: {response.choices[0].message.content}\n")

    # Contoh 3: System prompt sebagai pembatas/batasan
    print("=" * 60)
    print("Contoh 3: System Prompt sebagai Pembatas (Hanya topik tertentu)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten khusus masak-memasak. "
                    "Kamu HANYA menjawab pertanyaan tentang resep, bahan makanan, dan teknik memasak. "
                    "Jika user bertanya di luar topik, tolak dengan sopan dan arahkan kembali ke topik memasak."
                )
            },
            {"role": "user", "content": "Bagaimana cara membuat nasi goreng?"}
        ],
        temperature=0.5
    )
    print(f"Pertanyaan ON-TOPIC:")
    print(f"Jawaban: {response.choices[0].message.content}\n")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten khusus masak-memasak. "
                    "Kamu HANYA menjawab pertanyaan tentang resep, bahan makanan, dan teknik memasak. "
                    "Jika user bertanya di luar topik, tolak dengan sopan dan arahkan kembali ke topik memasak."
                )
            },
            {"role": "user", "content": "Siapa presiden Indonesia?"}
        ],
        temperature=0.5
    )
    print(f"Pertanyaan OFF-TOPIC:")
    print(f"Jawaban: {response.choices[0].message.content}\n")

    # Contoh 4: Few-Shot Prompting (memberikan contoh)
    print("=" * 60)
    print("Contoh 4: Few-Shot Prompting (Memberikan Contoh di Prompt)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Kamu adalah pengklasifikasi sentimen. Jawab hanya dengan: POSITIF, NEGATIF, atau NETRAL."
            },
            # Few-shot examples (contoh di prompt)
            {"role": "user", "content": "Makanannya enak banget!"},
            {"role": "assistant", "content": "POSITIF"},
            {"role": "user", "content": "Pelayanannya sangat buruk dan lambat."},
            {"role": "assistant", "content": "NEGATIF"},
            {"role": "user", "content": "Restoran ini buka dari jam 9 pagi."},
            {"role": "assistant", "content": "NETRAL"},
            # Pertanyaan sebenarnya
            {"role": "user", "content": "Tempatnya nyaman tapi harganya terlalu mahal."},
        ],
        temperature=0.0
    )
    print(f"Input  : 'Tempatnya nyaman tapi harganya terlalu mahal.'")
    print(f"Output : {response.choices[0].message.content}")

    print("\n✅ Selesai! Memahami penggunaan System/User/Assistant roles.")
    print("\nRingkasan:")
    print("- System Prompt: Mengatur persona, batasan, dan gaya jawaban LLM")
    print("- Few-Shot: Memberikan contoh input-output agar LLM mengikuti pola")
    print("- Role 'assistant': Dipakai untuk menyisipkan contoh jawaban")

if __name__ == "__main__":
    main()
