import os
import json
import math
from datetime import datetime
from openai import OpenAI

# ---------------------------------------------------------------
# MULTIPLE TOOLS
# Agent dengan banyak tools — LLM memilih tool yang tepat
# berdasarkan pertanyaan user.
# ---------------------------------------------------------------

def kalkulator(ekspresi):
    """Menghitung ekspresi matematika sederhana."""
    try:
        # Hanya izinkan operasi aman (tanpa eval arbitrary code)
        allowed_chars = set("0123456789+-*/().% ")
        if not all(c in allowed_chars for c in ekspresi):
            return json.dumps({"error": "Ekspresi mengandung karakter tidak diizinkan"})
        hasil = eval(ekspresi)
        return json.dumps({"ekspresi": ekspresi, "hasil": hasil})
    except Exception as e:
        return json.dumps({"error": f"Gagal menghitung: {str(e)}"})

def get_waktu_sekarang(timezone="WIB"):
    """Mendapatkan waktu saat ini."""
    now = datetime.now()
    offset_map = {"WIB": 7, "WITA": 8, "WIT": 9}
    offset = offset_map.get(timezone.upper(), 7)
    return json.dumps({
        "waktu": now.strftime("%H:%M:%S"),
        "tanggal": now.strftime("%Y-%m-%d"),
        "hari": now.strftime("%A"),
        "timezone": timezone
    }, ensure_ascii=False)

def cari_kamus(kata):
    """Simulasi kamus - mencari definisi kata."""
    kamus = {
        "agent": "Entitas otonom yang merasakan lingkungannya dan mengambil tindakan untuk mencapai tujuan.",
        "llm": "Large Language Model - model AI yang dilatih pada data teks besar untuk memahami dan menghasilkan bahasa.",
        "prompt": "Instruksi atau masukan teks yang diberikan ke LLM untuk mendapatkan respons.",
        "token": "Unit terkecil teks yang dipahami oleh LLM, bisa berupa kata, subkata, atau karakter.",
        "rag": "Retrieval-Augmented Generation - teknik menggabungkan pencarian dokumen dengan generasi teks LLM.",
    }
    kata_lower = kata.lower()
    if kata_lower in kamus:
        return json.dumps({"kata": kata, "definisi": kamus[kata_lower]}, ensure_ascii=False)
    else:
        return json.dumps({"kata": kata, "definisi": f"Definisi untuk '{kata}' tidak ditemukan dalam kamus."}, ensure_ascii=False)


def main():
    print("=== 3.3 Multi-Tool Agent (Agent dengan Banyak Tools) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Definisi BANYAK tools sekaligus
    tools = [
        {
            "type": "function",
            "function": {
                "name": "kalkulator",
                "description": "Menghitung ekspresi matematika. Gunakan untuk penjumlahan, pengurangan, perkalian, pembagian.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "ekspresi": {
                            "type": "string",
                            "description": "Ekspresi matematika, misal: '2 + 3 * 4' atau '100 / 5'"
                        }
                    },
                    "required": ["ekspresi"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "get_waktu_sekarang",
                "description": "Mendapatkan waktu dan tanggal saat ini.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "enum": ["WIB", "WITA", "WIT"],
                            "description": "Zona waktu Indonesia"
                        }
                    },
                    "required": []
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "cari_kamus",
                "description": "Mencari definisi istilah/kata dalam kamus AI dan teknologi.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "kata": {
                            "type": "string",
                            "description": "Kata atau istilah yang ingin dicari definisinya"
                        }
                    },
                    "required": ["kata"]
                }
            }
        }
    ]

    # Mapping fungsi
    available_functions = {
        "kalkulator": kalkulator,
        "get_waktu_sekarang": get_waktu_sekarang,
        "cari_kamus": cari_kamus,
    }

    # Fungsi helper untuk menjalankan satu pertanyaan lengkap
    def tanya_agent(pertanyaan):
        print(f"\n{'='*60}")
        print(f"User: {pertanyaan}")
        print(f"{'='*60}")

        messages = [
            {
                "role": "system",
                "content": (
                    "Kamu adalah asisten AI yang helpful. "
                    "Kamu punya akses ke tools: kalkulator, waktu, dan kamus AI. "
                    "Gunakan tool yang sesuai untuk menjawab pertanyaan user. "
                    "Jawab dalam Bahasa Indonesia."
                )
            },
            {"role": "user", "content": pertanyaan}
        ]

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        response_message = response.choices[0].message

        # Jika LLM mau panggil tool(s)
        if response_message.tool_calls:
            messages.append(response_message)

            print(f"\n  🔧 LLM memilih {len(response_message.tool_calls)} tool(s):")

            for tool_call in response_message.tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)
                print(f"     → {fn_name}({fn_args})")

                # Eksekusi
                if fn_name in available_functions:
                    result = available_functions[fn_name](**fn_args)
                else:
                    result = json.dumps({"error": f"Tool '{fn_name}' tidak tersedia"})

                print(f"       Hasil: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

            # Jawaban final
            final = client.chat.completions.create(model=model, messages=messages)
            print(f"\n  🤖 Jawaban: {final.choices[0].message.content}")
        else:
            print(f"\n  🤖 Jawaban (langsung): {response_message.content}")

    # Test dengan berbagai pertanyaan
    # LLM harus memilih tool yang tepat berdasarkan konteks

    tanya_agent("Berapa hasil dari 245 * 18 + 37?")

    tanya_agent("Jam berapa sekarang di WIB?")

    tanya_agent("Apa definisi dari RAG?")

    tanya_agent("Halo, siapa kamu?")  # Tidak butuh tool

    tanya_agent("Hitung 15% dari 850000, itu untuk pajak")

    print(f"\n{'='*60}")
    print("✅ Selesai! Multi-tool agent berhasil memilih tool yang tepat.")
    print("\nRingkasan:")
    print("- LLM bisa memilih dari beberapa tools berdasarkan konteks pertanyaan")
    print("- Deskripsi tool yang jelas membantu LLM memilih tool yang tepat")
    print("- LLM bisa memutuskan TIDAK perlu tool jika pertanyaan bisa dijawab langsung")
    print("- Di script berikutnya (Agent Loop), kita akan membuat ini menjadi loop yang berulang")

if __name__ == "__main__":
    main()
