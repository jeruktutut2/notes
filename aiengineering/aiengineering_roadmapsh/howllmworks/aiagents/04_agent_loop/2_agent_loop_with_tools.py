import os
import json
from datetime import datetime
from openai import OpenAI

# ---------------------------------------------------------------
# AGENT LOOP LENGKAP DENGAN FUNCTION CALLING
# Menggabungkan function calling (modul 03) dengan agent loop.
# Agent bisa memanggil tools berulang kali sampai tugas selesai.
# ---------------------------------------------------------------

# --- DEFINISI TOOLS ---
def kalkulator(ekspresi):
    """Menghitung ekspresi matematika."""
    try:
        allowed = set("0123456789+-*/().% ")
        if all(c in allowed for c in ekspresi):
            return json.dumps({"hasil": eval(ekspresi)})
        return json.dumps({"error": "Ekspresi tidak valid"})
    except Exception as e:
        return json.dumps({"error": str(e)})

def get_waktu(timezone="WIB"):
    """Mendapatkan waktu saat ini."""
    now = datetime.now()
    return json.dumps({
        "waktu": now.strftime("%H:%M:%S"),
        "tanggal": now.strftime("%d %B %Y"),
        "hari": now.strftime("%A"),
        "timezone": timezone
    }, ensure_ascii=False)

def buat_catatan(judul, isi):
    """Simulasi membuat catatan/note."""
    return json.dumps({
        "status": "berhasil",
        "pesan": f"Catatan '{judul}' berhasil dibuat",
        "judul": judul,
        "isi": isi,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }, ensure_ascii=False)

def cari_kontak(nama):
    """Simulasi pencarian kontak."""
    kontak_db = {
        "budi": {"nama": "Budi Santoso", "telepon": "081234567890", "email": "budi@email.com"},
        "ani": {"nama": "Ani Wijaya", "telepon": "082345678901", "email": "ani@email.com"},
        "cici": {"nama": "Cici Rahayu", "telepon": "083456789012", "email": "cici@email.com"},
    }
    result = kontak_db.get(nama.lower())
    if result:
        return json.dumps(result, ensure_ascii=False)
    return json.dumps({"error": f"Kontak '{nama}' tidak ditemukan"}, ensure_ascii=False)

# --- TOOL SCHEMA ---
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "kalkulator",
            "description": "Menghitung ekspresi matematika (tambah, kurang, kali, bagi).",
            "parameters": {
                "type": "object",
                "properties": {
                    "ekspresi": {"type": "string", "description": "Ekspresi matematika, misal: '100 * 5 + 20'"}
                },
                "required": ["ekspresi"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_waktu",
            "description": "Mendapatkan waktu dan tanggal saat ini.",
            "parameters": {
                "type": "object",
                "properties": {
                    "timezone": {"type": "string", "enum": ["WIB", "WITA", "WIT"]}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "buat_catatan",
            "description": "Membuat catatan/note baru.",
            "parameters": {
                "type": "object",
                "properties": {
                    "judul": {"type": "string", "description": "Judul catatan"},
                    "isi": {"type": "string", "description": "Isi catatan"}
                },
                "required": ["judul", "isi"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cari_kontak",
            "description": "Mencari informasi kontak seseorang berdasarkan nama.",
            "parameters": {
                "type": "object",
                "properties": {
                    "nama": {"type": "string", "description": "Nama orang yang dicari"}
                },
                "required": ["nama"]
            }
        }
    }
]

AVAILABLE_FUNCTIONS = {
    "kalkulator": kalkulator,
    "get_waktu": get_waktu,
    "buat_catatan": buat_catatan,
    "cari_kontak": cari_kontak,
}


def run_agent(client, model, pertanyaan):
    """Menjalankan agent loop untuk satu pertanyaan."""
    print(f"\n{'='*60}")
    print(f"📝 User: {pertanyaan}")
    print(f"{'='*60}")

    messages = [
        {
            "role": "system",
            "content": (
                "Kamu adalah asisten pribadi yang capable. "
                "Kamu punya akses ke tools: kalkulator, waktu, catatan, dan kontak. "
                "Gunakan tools yang diperlukan untuk menyelesaikan tugas user. "
                "Jika tugas membutuhkan beberapa langkah, lakukan semuanya. "
                "Jawab dalam Bahasa Indonesia."
            )
        },
        {"role": "user", "content": pertanyaan}
    ]

    MAX_LOOPS = 10  # Batas keamanan
    loop_count = 0

    while loop_count < MAX_LOOPS:
        loop_count += 1
        print(f"\n  --- Loop {loop_count} ---")

        # Panggil LLM
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        response_message = response.choices[0].message
        finish_reason = response.choices[0].finish_reason

        # Jika LLM mau panggil tool(s)
        if response_message.tool_calls:
            messages.append(response_message)

            print(f"  🔧 Agent memanggil {len(response_message.tool_calls)} tool(s):")

            for tool_call in response_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                print(f"     → {fn_name}({json.dumps(fn_args, ensure_ascii=False)})")

                # Eksekusi tool
                if fn_name in AVAILABLE_FUNCTIONS:
                    result = AVAILABLE_FUNCTIONS[fn_name](**fn_args)
                else:
                    result = json.dumps({"error": f"Tool '{fn_name}' tidak tersedia"})

                print(f"       Hasil: {result}")

                # Kirim hasil kembali
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Lanjut loop — LLM mungkin mau panggil tool lagi

        else:
            # LLM memberikan jawaban final (tidak ada tool_calls)
            jawaban = response_message.content
            print(f"\n  🤖 Jawaban Final:")
            print(f"  {jawaban}")
            return jawaban

    print(f"\n  ⚠️ Mencapai batas loop ({MAX_LOOPS})")
    return None


def main():
    print("=== 4.2 Agent Loop dengan Function Calling ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # --- Test 1: Tugas sederhana (1 tool call) ---
    run_agent(client, model, "Berapa hasil dari 1500 * 12 + 350?")

    # --- Test 2: Tugas multi-langkah (beberapa tool calls) ---
    run_agent(
        client, model,
        "Cari nomor telepon Budi, lalu buatkan catatan dengan judul 'Kontak Budi' yang isinya nomor teleponnya."
    )

    # --- Test 3: Tugas yang butuh reasoning + tools ---
    run_agent(
        client, model,
        "Hitung pajak 11% dari Rp 5.500.000 dan buatkan catatan 'Pajak Juli' dengan hasilnya."
    )

    # --- Test 4: Pertanyaan tanpa tool ---
    run_agent(client, model, "Apa tips untuk belajar programming?")

    print(f"\n{'='*60}")
    print("✅ Selesai! Agent loop berhasil dengan function calling.")
    print("\nPoin Penting:")
    print("- Agent loop = while loop yang memanggil LLM berulang kali")
    print("- Setiap iterasi: LLM bisa panggil tool ATAU memberikan jawaban final")
    print("- Loop berhenti saat LLM tidak meminta tool lagi (jawaban final)")
    print("- MAX_LOOPS mencegah infinite loop (keamanan)")
    print("- Agent bisa menyelesaikan tugas multi-langkah secara otonom")

if __name__ == "__main__":
    main()
