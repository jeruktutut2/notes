import os
from openai import OpenAI

def main():
    print("=== 5.1 Conversation Memory (Riwayat Percakapan) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # CONVERSATION MEMORY (Short-Term Memory)
    # LLM secara default TIDAK punya memori. Setiap API call adalah
    # independen. Agar LLM "mengingat" percakapan, kita harus
    # mengirim seluruh riwayat di setiap request.
    #
    # Ini disebut "Short-Term Memory" atau "Conversation Memory".
    # ---------------------------------------------------------------

    system_prompt = {
        "role": "system",
        "content": (
            "Kamu adalah asisten pribadi bernama Aiko. "
            "Kamu ramah dan selalu mengingat detail dari percakapan sebelumnya. "
            "Jawab singkat dalam Bahasa Indonesia."
        )
    }

    # Riwayat percakapan (memory)
    conversation_history = [system_prompt]

    # Simulasi percakapan multi-turn
    percakapan = [
        "Halo Aiko! Nama saya Budi.",
        "Saya suka makan nasi goreng dan bakso.",
        "Saya tinggal di Bandung dan bekerja sebagai programmer.",
        "Apa saja yang kamu ingat tentang saya?",  # Test: apakah ingat info sebelumnya?
        "Rekomendasikan tempat makan di kota tempat saya tinggal.",  # Test: apakah ingat kota?
    ]

    print("=" * 60)
    print("DEMO: Percakapan dengan Conversation Memory")
    print("=" * 60)

    for user_msg in percakapan:
        print(f"\n👤 User: {user_msg}")

        # Tambahkan pesan user ke riwayat
        conversation_history.append({"role": "user", "content": user_msg})

        # Kirim SELURUH riwayat ke LLM
        response = client.chat.completions.create(
            model=model,
            messages=conversation_history,  # <-- Ini kuncinya!
            temperature=0.5
        )

        assistant_msg = response.choices[0].message.content
        print(f"🤖 Aiko: {assistant_msg}")

        # Tambahkan jawaban AI ke riwayat
        conversation_history.append({"role": "assistant", "content": assistant_msg})

    # Tampilkan statistik
    print(f"\n{'='*60}")
    print(f"STATISTIK MEMORY:")
    print(f"{'='*60}")
    print(f"  Total pesan dalam memory: {len(conversation_history)}")
    print(f"  Terdiri dari:")
    roles = [m['role'] for m in conversation_history]
    print(f"    - system   : {roles.count('system')}")
    print(f"    - user     : {roles.count('user')}")
    print(f"    - assistant: {roles.count('assistant')}")

    # ---------------------------------------------------------------
    # WINDOW MEMORY (Batasi jumlah pesan terakhir)
    # Masalah: Semakin panjang percakapan, semakin banyak token.
    # Solusi sederhana: Hanya simpan N pesan terakhir.
    # ---------------------------------------------------------------
    print(f"\n{'='*60}")
    print(f"DEMO: Window Memory (Hanya 4 pesan terakhir)")
    print(f"{'='*60}")

    WINDOW_SIZE = 4  # Simpan hanya 4 pesan terakhir (selain system)

    # Reset conversation
    windowed_history = [system_prompt]

    percakapan_panjang = [
        "Nama saya Rina.",
        "Saya suka kucing.",
        "Saya bekerja di bank.",
        "Hobi saya membaca buku.",
        "Saya baru pindah ke Surabaya.",
        "Apa saja yang kamu ingat tentang saya?",  # Hanya ingat 4 terakhir
    ]

    for user_msg in percakapan_panjang:
        print(f"\n👤 User: {user_msg}")

        windowed_history.append({"role": "user", "content": user_msg})

        # Trim: Simpan system + N pesan terakhir
        if len(windowed_history) > WINDOW_SIZE + 1:  # +1 untuk system
            windowed_history = [system_prompt] + windowed_history[-(WINDOW_SIZE):]
            print(f"  ✂️ [Memory trimmed ke {WINDOW_SIZE} pesan terakhir]")

        response = client.chat.completions.create(
            model=model,
            messages=windowed_history,
            temperature=0.5
        )

        assistant_msg = response.choices[0].message.content
        print(f"🤖 Aiko: {assistant_msg}")

        windowed_history.append({"role": "assistant", "content": assistant_msg})

    print(f"\n{'='*60}")
    print("✅ Selesai! Memahami Conversation Memory.")
    print("\nRingkasan:")
    print("- LLM tidak punya memori bawaan — kita harus mengirim riwayat percakapan")
    print("- Full Memory: Simpan semua pesan (mahal, bisa melebihi context window)")
    print("- Window Memory: Simpan N pesan terakhir (hemat, tapi lupa percakapan lama)")
    print("- Di script berikutnya: Summary Memory (ringkas percakapan lama)")

if __name__ == "__main__":
    main()
