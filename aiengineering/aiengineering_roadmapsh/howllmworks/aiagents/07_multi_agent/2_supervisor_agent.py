import os
import json
from openai import OpenAI

def main():
    print("=== 7.2 Supervisor Agent (Delegasi ke Agent Spesialis) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # SUPERVISOR PATTERN
    # Satu agent "Supervisor" menerima permintaan user, lalu
    # mendelegasikan ke agent spesialis yang tepat.
    #
    #              ┌─── Agent Coding
    # User → Supervisor ─── Agent Penerjemah
    #              └─── Agent Analisis
    #
    # Supervisor memutuskan agent mana yang harus menangani.
    # ---------------------------------------------------------------

    # --- DEFINISI AGENT SPESIALIS ---
    specialist_agents = {
        "coding": {
            "name": "Agent Coding",
            "system_prompt": (
                "Kamu adalah programmer expert. "
                "Tulis kode Python yang bersih dan terdokumentasi. "
                "Berikan penjelasan singkat tentang kode yang kamu tulis."
            )
        },
        "penerjemah": {
            "name": "Agent Penerjemah",
            "system_prompt": (
                "Kamu adalah penerjemah profesional. "
                "Terjemahkan teks antara Bahasa Indonesia dan Bahasa Inggris. "
                "Pertahankan nuansa dan konteks asli."
            )
        },
        "analisis": {
            "name": "Agent Analisis Data",
            "system_prompt": (
                "Kamu adalah analis data. "
                "Analisis data atau pertanyaan yang diberikan. "
                "Berikan insight, statistik, dan rekomendasi."
            )
        },
        "general": {
            "name": "Agent General",
            "system_prompt": (
                "Kamu adalah asisten AI umum yang membantu dengan berbagai pertanyaan. "
                "Jawab dengan informatif dalam Bahasa Indonesia."
            )
        }
    }

    # --- SUPERVISOR AGENT ---
    def supervisor_route(user_request):
        """Supervisor memutuskan agent mana yang harus menangani request."""
        print(f"\n  🧠 [Supervisor] Menganalisis permintaan...")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu adalah supervisor yang mengarahkan permintaan ke agent yang tepat. "
                        "Agent yang tersedia:\n"
                        "- coding: Untuk menulis kode, debugging, pertanyaan pemrograman\n"
                        "- penerjemah: Untuk menerjemahkan teks antar bahasa\n"
                        "- analisis: Untuk analisis data, statistik, insight\n"
                        "- general: Untuk pertanyaan umum lainnya\n\n"
                        "Kembalikan HANYA nama agent dalam format JSON: "
                        '{"agent": "nama_agent", "alasan": "alasan singkat"}\n'
                        "Jangan tambahkan penjelasan lain."
                    )
                },
                {"role": "user", "content": user_request}
            ],
            temperature=0.0
        )

        result = response.choices[0].message.content.strip()

        # Parse JSON
        try:
            clean = result
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            routing = json.loads(clean)
            agent_name = routing.get("agent", "general")
            alasan = routing.get("alasan", "")
            print(f"  🧠 [Supervisor] Keputusan: {agent_name} — {alasan}")
            return agent_name
        except json.JSONDecodeError:
            print(f"  🧠 [Supervisor] Gagal parse, fallback ke 'general'")
            return "general"

    def run_specialist(agent_key, user_request):
        """Menjalankan agent spesialis."""
        agent = specialist_agents.get(agent_key, specialist_agents["general"])
        print(f"  🤖 [{agent['name']}] sedang bekerja...")

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": agent["system_prompt"]},
                {"role": "user", "content": user_request}
            ],
            temperature=0.5
        )

        return response.choices[0].message.content

    def handle_request(user_request):
        """Alur lengkap: User → Supervisor → Specialist → Response."""
        print(f"\n{'='*60}")
        print(f"👤 User: {user_request}")
        print(f"{'='*60}")

        # 1. Supervisor menentukan routing
        agent_key = supervisor_route(user_request)

        # 2. Jalankan agent spesialis
        result = run_specialist(agent_key, user_request)

        # 3. Tampilkan hasil
        agent_name = specialist_agents.get(agent_key, specialist_agents["general"])["name"]
        print(f"\n  💬 [{agent_name}] Jawaban:")
        print(f"  {result}")

        return result

    # --- DEMO ---
    print("=" * 60)
    print("DEMO: Supervisor Agent Pattern")
    print("=" * 60)

    requests = [
        "Buatkan fungsi Python untuk mengurutkan list menggunakan bubble sort",
        "Terjemahkan ke bahasa Inggris: 'AI Agent adalah sistem cerdas yang bisa bertindak secara otonom'",
        "Berikan analisis tren penggunaan AI di Indonesia tahun 2024-2025",
        "Apa tips untuk menjaga kesehatan mental?",
    ]

    for req in requests:
        handle_request(req)

    print(f"\n{'='*60}")
    print("✅ Selesai! Supervisor agent pattern berhasil.")
    print("\nRingkasan:")
    print("- Supervisor: Agent yang memutuskan routing (bukan mengerjakan)")
    print("- Specialists: Agent dengan keahlian spesifik")
    print("- Supervisor menganalisis request dan memilih specialist yang tepat")
    print("- Scalable: Mudah menambah specialist baru tanpa mengubah supervisor")
    print("\nPola Multi-Agent lainnya:")
    print("- Sequential: A → B → C (pipeline)")
    print("- Supervisor: S → A/B/C (routing)")
    print("- Debate: A ↔ B (diskusi/argumentasi)")
    print("- Hierarchical: Manager → Team Lead → Workers")

if __name__ == "__main__":
    main()
