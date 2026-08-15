import os
from openai import OpenAI

def main():
    print("=== 7.1 Sequential Agents (Pipeline Agent Berantai) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # SEQUENTIAL AGENTS (Pipeline)
    # Beberapa agent dijalankan secara berurutan, di mana output
    # agent pertama menjadi input agent berikutnya.
    #
    # Contoh: Penulis → Editor → Reviewer
    # - Agent Penulis: Menulis draft artikel
    # - Agent Editor: Memperbaiki dan menyempurnakan tulisan
    # - Agent Reviewer: Memberikan penilaian dan skor akhir
    # ---------------------------------------------------------------

    def run_agent(name, system_prompt, user_input, emoji="🤖"):
        """Menjalankan satu agent dan mengembalikan hasilnya."""
        print(f"\n{emoji} [{name}] sedang bekerja...")
        print(f"   Input: {user_input[:100]}..." if len(user_input) > 100 else f"   Input: {user_input}")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7
        )

        output = response.choices[0].message.content
        print(f"   Output ({len(output)} karakter):")
        print(f"   {output[:300]}..." if len(output) > 300 else f"   {output}")
        return output

    # --- DEFINISI AGENT ---
    agents = [
        {
            "name": "Agent Penulis",
            "emoji": "✍️",
            "system_prompt": (
                "Kamu adalah penulis konten profesional. "
                "Tulis artikel blog pendek (3-4 paragraf) berdasarkan topik yang diberikan. "
                "Gunakan Bahasa Indonesia yang menarik dan informatif."
            )
        },
        {
            "name": "Agent Editor",
            "emoji": "📝",
            "system_prompt": (
                "Kamu adalah editor profesional. "
                "Terima draft artikel, lalu perbaiki: "
                "1. Perbaiki tata bahasa dan ejaan "
                "2. Tingkatkan kejelasan dan alur tulisan "
                "3. Tambahkan judul yang menarik jika belum ada "
                "4. Pastikan paragraf mengalir dengan baik "
                "Kembalikan artikel yang sudah diedit lengkap."
            )
        },
        {
            "name": "Agent Reviewer",
            "emoji": "⭐",
            "system_prompt": (
                "Kamu adalah reviewer konten. "
                "Review artikel yang diberikan dan berikan: "
                "1. Skor keseluruhan (1-10) "
                "2. Poin kuat artikel "
                "3. Poin yang bisa diperbaiki "
                "4. Kesimpulan: apakah layak dipublikasikan (YA/TIDAK) "
                "Format output dengan jelas."
            )
        }
    ]

    # --- JALANKAN PIPELINE ---
    topik = "Mengapa AI Agent Akan Mengubah Cara Kita Bekerja di Masa Depan"

    print("=" * 60)
    print(f"📋 TOPIK: {topik}")
    print("=" * 60)
    print(f"\nPipeline: {' → '.join([a['name'] for a in agents])}\n")

    # Agent 1: Penulis
    current_output = topik
    results = {}

    for agent in agents:
        current_output = run_agent(
            name=agent["name"],
            system_prompt=agent["system_prompt"],
            user_input=current_output,
            emoji=agent["emoji"]
        )
        results[agent["name"]] = current_output
        print(f"\n{'─'*40}")

    # --- HASIL AKHIR ---
    print(f"\n{'='*60}")
    print("📊 RINGKASAN PIPELINE")
    print(f"{'='*60}")
    print(f"  Topik awal  : {topik}")
    print(f"  Agent 1 (Penulis) : Menulis draft ({len(results.get('Agent Penulis', ''))} chars)")
    print(f"  Agent 2 (Editor)  : Mengedit draft ({len(results.get('Agent Editor', ''))} chars)")
    print(f"  Agent 3 (Reviewer): Memberikan review")

    print(f"\n{'='*60}")
    print("📄 REVIEW AKHIR:")
    print(f"{'='*60}")
    print(results.get("Agent Reviewer", ""))

    print(f"\n✅ Selesai! Sequential agents berhasil.")
    print("\nRingkasan:")
    print("- Sequential/Pipeline: Agent A → Agent B → Agent C")
    print("- Output agent sebelumnya = Input agent berikutnya")
    print("- Setiap agent punya spesialisasi (single responsibility)")
    print("- Mudah di-debug karena alur linear dan jelas")

if __name__ == "__main__":
    main()
