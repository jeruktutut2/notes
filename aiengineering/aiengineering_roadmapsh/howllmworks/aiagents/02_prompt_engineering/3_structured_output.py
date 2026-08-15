import os
import json
from openai import OpenAI

def main():
    print("=== 2.3 Structured Output (JSON Output dari LLM) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # STRUCTURED OUTPUT
    # Dalam banyak kasus, kita butuh output LLM dalam format
    # terstruktur (JSON) agar bisa diproses oleh program secara
    # otomatis, bukan hanya teks bebas.
    # ---------------------------------------------------------------

    # Contoh 1: Meminta JSON via Prompt (cara sederhana)
    print("=" * 60)
    print("Contoh 1: Meminta JSON via Prompt Engineering")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Kamu adalah ekstractor informasi. "
                    "Dari teks yang diberikan, ekstrak informasi dan kembalikan HANYA dalam format JSON. "
                    "Jangan tambahkan penjelasan atau markdown. Hanya JSON murni."
                )
            },
            {
                "role": "user",
                "content": (
                    "Budi berumur 25 tahun, bekerja sebagai software engineer di Jakarta. "
                    "Dia lulusan ITB jurusan Informatika dan hobi bermain gitar."
                )
            }
        ],
        temperature=0.0
    )

    jawaban_json_str = response.choices[0].message.content
    print(f"Output mentah:\n{jawaban_json_str}\n")

    # Parse JSON
    try:
        # Bersihkan markdown code block jika ada
        clean_str = jawaban_json_str.strip()
        if clean_str.startswith("```"):
            clean_str = clean_str.split("\n", 1)[1]  # Hapus baris pertama ```json
            clean_str = clean_str.rsplit("```", 1)[0]  # Hapus ``` terakhir

        data = json.loads(clean_str)
        print(f"Parsed JSON (sebagai Python dict):")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except json.JSONDecodeError as e:
        print(f"[ERROR] Gagal parse JSON: {e}")

    # Contoh 2: Menggunakan response_format (JSON mode - lebih reliable)
    print("\n" + "=" * 60)
    print("Contoh 2: Menggunakan JSON Mode (response_format)")
    print("=" * 60)
    print("(Catatan: Tidak semua provider mendukung fitur ini)\n")

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu adalah API yang menganalisis sentimen. "
                        "Kembalikan JSON dengan format: "
                        '{"sentimen": "positif/negatif/netral", "skor": 0.0-1.0, "alasan": "..."}'
                    )
                },
                {
                    "role": "user",
                    "content": "Review: Hotelnya bersih dan stafnya ramah, tapi lokasi agak jauh dari pusat kota."
                }
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        jawaban = response.choices[0].message.content
        print(f"Output JSON Mode:\n{jawaban}\n")

        data = json.loads(jawaban)
        print(f"Sentimen : {data.get('sentimen', 'N/A')}")
        print(f"Skor     : {data.get('skor', 'N/A')}")
        print(f"Alasan   : {data.get('alasan', 'N/A')}")

    except Exception as e:
        print(f"[INFO] JSON mode tidak didukung oleh provider ini: {e}")
        print("Fallback: Gunakan cara prompt engineering (Contoh 1)")

    # Contoh 3: Ekstraksi batch (banyak item sekaligus)
    print("\n" + "=" * 60)
    print("Contoh 3: Ekstraksi Batch (Banyak Item)")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Dari teks berikut, ekstrak semua tugas/task yang disebutkan. "
                    "Kembalikan JSON array dengan format:\n"
                    '[{"tugas": "...", "prioritas": "tinggi/sedang/rendah", "deadline": "..."}]\n'
                    "Jika deadline tidak disebutkan, isi dengan null. "
                    "Kembalikan HANYA JSON array, tanpa penjelasan tambahan."
                )
            },
            {
                "role": "user",
                "content": (
                    "Untuk minggu ini yang harus dikerjakan: deploy fitur login sebelum Jumat, "
                    "perbaiki bug pada halaman checkout (ini urgent!), "
                    "update dokumentasi API, dan meeting dengan tim design soal redesign dashboard."
                )
            }
        ],
        temperature=0.0
    )

    jawaban_batch = response.choices[0].message.content
    print(f"Output mentah:\n{jawaban_batch}\n")

    try:
        clean_str = jawaban_batch.strip()
        if clean_str.startswith("```"):
            clean_str = clean_str.split("\n", 1)[1]
            clean_str = clean_str.rsplit("```", 1)[0]

        tasks = json.loads(clean_str)
        print(f"Jumlah tugas diekstrak: {len(tasks)}")
        print(f"\n{'No':<4} {'Tugas':<45} {'Prioritas':<10} {'Deadline'}")
        print("-" * 80)
        for i, task in enumerate(tasks, 1):
            print(f"{i:<4} {task.get('tugas', ''):<45} {task.get('prioritas', ''):<10} {task.get('deadline', '-')}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] Gagal parse JSON: {e}")

    print("\n✅ Selesai! Memahami cara mendapatkan structured output dari LLM.")
    print("\nRingkasan:")
    print("- Prompt Engineering: Minta JSON via instruksi di prompt")
    print("- JSON Mode: Gunakan response_format={'type': 'json_object'}")
    print("- Selalu handle JSONDecodeError karena LLM bisa saja menghasilkan format yang salah")
    print("- Structured output penting untuk integrasi LLM dengan sistem/pipeline lain")

if __name__ == "__main__":
    main()
