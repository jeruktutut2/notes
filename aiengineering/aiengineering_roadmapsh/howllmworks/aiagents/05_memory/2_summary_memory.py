import os
from openai import OpenAI

def main():
    print("=== 5.2 Summary Memory (Ringkasan Percakapan) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # SUMMARY MEMORY
    # Masalah: Percakapan panjang → banyak token → mahal & bisa
    # melebihi context window.
    # Solusi: Ringkas percakapan lama menggunakan LLM, simpan
    # ringkasannya sebagai "memori" di system prompt.
    # ---------------------------------------------------------------

    def ringkas_percakapan(client, model, messages_to_summarize, existing_summary=""):
        """Meminta LLM meringkas percakapan menjadi poin-poin penting."""
        summary_prompt = "Ringkas percakapan berikut menjadi poin-poin penting tentang user (nama, preferensi, fakta yang disebutkan). Tulis ringkasan dalam format bullet points, singkat dan padat."

        if existing_summary:
            summary_prompt += f"\n\nRingkasan sebelumnya:\n{existing_summary}"

        # Format percakapan menjadi teks
        convo_text = ""
        for msg in messages_to_summarize:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role in ("user", "assistant"):
                label = "User" if role == "user" else "AI"
                convo_text += f"{label}: {content}\n"

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": summary_prompt},
                {"role": "user", "content": convo_text}
            ],
            temperature=0.0,
            max_tokens=300
        )

        return response.choices[0].message.content

    # --- SIMULASI PERCAKAPAN PANJANG ---
    system_prompt_template = (
        "Kamu adalah asisten pribadi bernama Aiko. "
        "Jawab singkat dalam Bahasa Indonesia. "
        "{summary_section}"
    )

    # Fase 1: Percakapan awal (akan diringkas)
    percakapan_awal = [
        ("Halo! Nama saya Dewi.", None),
        ("Saya tinggal di Yogyakarta.", None),
        ("Saya suka masakan Jepang, terutama sushi dan ramen.", None),
        ("Saya bekerja sebagai data scientist di startup.", None),
        ("Saya punya kucing bernama Mochi.", None),
    ]

    # Fase 2: Percakapan lanjutan (setelah ringkasan)
    percakapan_lanjutan = [
        "Apa saja yang kamu ingat tentang saya?",
        "Rekomendasikan restoran di kota saya.",
        "Ceritakan sesuatu yang lucu untuk kucing saya.",
    ]

    # --- JALANKAN FASE 1 ---
    print("=" * 60)
    print("FASE 1: Percakapan Awal (akan diringkas)")
    print("=" * 60)

    messages_fase1 = [
        {"role": "system", "content": system_prompt_template.format(summary_section="")}
    ]

    for user_msg, _ in percakapan_awal:
        print(f"\n👤 User: {user_msg}")

        messages_fase1.append({"role": "user", "content": user_msg})

        response = client.chat.completions.create(
            model=model,
            messages=messages_fase1,
            temperature=0.5
        )

        ai_msg = response.choices[0].message.content
        print(f"🤖 Aiko: {ai_msg}")
        messages_fase1.append({"role": "assistant", "content": ai_msg})

    # --- RINGKAS PERCAKAPAN ---
    print(f"\n{'='*60}")
    print("📝 Meringkas percakapan Fase 1...")
    print(f"{'='*60}")

    ringkasan = ringkas_percakapan(client, model, messages_fase1)
    print(f"\nRINGKASAN:\n{ringkasan}")
    print(f"\nJumlah pesan Fase 1: {len(messages_fase1)}")
    print("Semua pesan Fase 1 diganti dengan 1 ringkasan → hemat token!")

    # --- JALANKAN FASE 2 (menggunakan ringkasan) ---
    print(f"\n{'='*60}")
    print("FASE 2: Percakapan Lanjutan (menggunakan ringkasan)")
    print("=" * 60)

    # Buat system prompt baru yang menyertakan ringkasan
    summary_section = f"\n\nBerikut adalah ringkasan percakapan sebelumnya dengan user:\n{ringkasan}\n\nGunakan informasi ini untuk menjawab pertanyaan user."

    messages_fase2 = [
        {"role": "system", "content": system_prompt_template.format(summary_section=summary_section)}
    ]

    for user_msg in percakapan_lanjutan:
        print(f"\n👤 User: {user_msg}")

        messages_fase2.append({"role": "user", "content": user_msg})

        response = client.chat.completions.create(
            model=model,
            messages=messages_fase2,
            temperature=0.5
        )

        ai_msg = response.choices[0].message.content
        print(f"🤖 Aiko: {ai_msg}")
        messages_fase2.append({"role": "assistant", "content": ai_msg})

    # --- PERBANDINGAN ---
    print(f"\n{'='*60}")
    print("PERBANDINGAN: Full History vs Summary Memory")
    print(f"{'='*60}")

    total_full = len(messages_fase1) + len(percakapan_lanjutan) * 2  # user + assistant
    total_summary = len(messages_fase2)
    print(f"  Full History : ~{total_full} messages per request")
    print(f"  Summary Memory: ~{total_summary} messages per request")
    print(f"  Penghematan  : {total_full - total_summary} messages lebih sedikit")

    print("\n✅ Selesai! Memahami Summary Memory.")
    print("\nRingkasan:")
    print("- Summary Memory: Ringkas percakapan lama → masukkan ringkasan di system prompt")
    print("- Hemat token: Banyak pesan dikompress jadi 1 ringkasan")
    print("- Trade-off: Detail kecil mungkin hilang saat diringkas")
    print("- Strategi: Ringkas setiap N pesan atau saat mendekati batas context window")

if __name__ == "__main__":
    main()
