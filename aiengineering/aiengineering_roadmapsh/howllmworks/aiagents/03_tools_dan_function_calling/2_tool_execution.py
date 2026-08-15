import os
import json
from openai import OpenAI

# ---------------------------------------------------------------
# TOOL FUNCTIONS (Fungsi-fungsi yang bisa dipanggil oleh LLM)
# Di dunia nyata, ini bisa memanggil API, database, dll.
# Di sini kita simulasikan dengan data dummy.
# ---------------------------------------------------------------

def get_cuaca(kota, satuan="celsius"):
    """Simulasi API cuaca - mengembalikan data cuaca palsu."""
    data_cuaca = {
        "jakarta": {"suhu": 32, "kondisi": "Cerah berawan", "kelembapan": 75},
        "bandung": {"suhu": 24, "kondisi": "Hujan ringan", "kelembapan": 85},
        "surabaya": {"suhu": 34, "kondisi": "Cerah", "kelembapan": 65},
        "yogyakarta": {"suhu": 30, "kondisi": "Berawan", "kelembapan": 70},
    }

    kota_lower = kota.lower()
    if kota_lower in data_cuaca:
        cuaca = data_cuaca[kota_lower]
        suhu = cuaca["suhu"]
        if satuan == "fahrenheit":
            suhu = round(suhu * 9/5 + 32, 1)
        return json.dumps({
            "kota": kota,
            "suhu": suhu,
            "satuan": satuan,
            "kondisi": cuaca["kondisi"],
            "kelembapan": cuaca["kelembapan"]
        }, ensure_ascii=False)
    else:
        return json.dumps({"error": f"Data cuaca untuk {kota} tidak tersedia"}, ensure_ascii=False)


def main():
    print("=== 3.2 Tool Execution (Eksekusi Fungsi dari Respons LLM) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # Definisi tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_cuaca",
                "description": "Mendapatkan informasi cuaca terkini untuk kota di Indonesia",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "kota": {
                            "type": "string",
                            "description": "Nama kota, misal: Jakarta, Bandung"
                        },
                        "satuan": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Satuan temperatur"
                        }
                    },
                    "required": ["kota"]
                }
            }
        }
    ]

    # Mapping nama fungsi ke fungsi Python yang sebenarnya
    available_functions = {
        "get_cuaca": get_cuaca,
    }

    # ---------------------------------------------------------------
    # ALUR LENGKAP FUNCTION CALLING
    # 1. User bertanya → kirim ke LLM + daftar tools
    # 2. LLM meminta panggil tool → kita eksekusi
    # 3. Kirim hasil tool ke LLM → LLM buat jawaban final
    # ---------------------------------------------------------------

    pertanyaan = "Bagaimana cuaca di Bandung sekarang?"
    print(f"User: {pertanyaan}\n")

    messages = [
        {"role": "system", "content": "Kamu adalah asisten cuaca Indonesia yang ramah."},
        {"role": "user", "content": pertanyaan}
    ]

    # LANGKAH 1: Kirim ke LLM
    print("[Langkah 1] Mengirim pertanyaan + tools ke LLM...")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    # LANGKAH 2: Cek apakah LLM mau panggil tool
    if response_message.tool_calls:
        print("[Langkah 2] LLM meminta untuk memanggil tool!\n")

        # Tambahkan respons LLM (yang berisi tool_calls) ke riwayat
        messages.append(response_message)

        # LANGKAH 3: Eksekusi setiap tool yang diminta
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            print(f"  Memanggil: {function_name}({function_args})")

            # Cari dan jalankan fungsi yang sesuai
            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                function_result = function_to_call(**function_args)
                print(f"  Hasil    : {function_result}\n")
            else:
                function_result = json.dumps({"error": f"Fungsi {function_name} tidak ditemukan"})
                print(f"  [ERROR] Fungsi tidak ditemukan: {function_name}\n")

            # LANGKAH 4: Kirim hasil tool kembali ke LLM
            # Role "tool" menandakan ini adalah hasil dari eksekusi tool
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,  # Harus cocok dengan ID dari LLM
                "content": function_result
            })

        # LANGKAH 5: LLM membuat jawaban final berdasarkan hasil tool
        print("[Langkah 3] Mengirim hasil tool ke LLM untuk jawaban final...")
        final_response = client.chat.completions.create(
            model=model,
            messages=messages
        )

        jawaban_final = final_response.choices[0].message.content
        print(f"\n{'='*60}")
        print(f"Jawaban Final AI:")
        print(f"{'='*60}")
        print(jawaban_final)

    else:
        # LLM menjawab langsung tanpa tool
        print("[Langkah 2] LLM menjawab langsung (tanpa tool):")
        print(response_message.content)

    # Tampilkan seluruh riwayat percakapan untuk memahami alurnya
    print(f"\n{'='*60}")
    print("RIWAYAT MESSAGES (untuk memahami alur):")
    print(f"{'='*60}")
    for i, msg in enumerate(messages):
        role = msg.get("role") if isinstance(msg, dict) else msg.role
        if role == "tool":
            print(f"  [{i}] role=tool, content={msg['content'][:80]}...")
        elif role == "assistant":
            tool_calls = msg.get("tool_calls") if isinstance(msg, dict) else getattr(msg, 'tool_calls', None)
            if tool_calls:
                for tc in tool_calls:
                    fn_name = tc.function.name if hasattr(tc, 'function') else tc['function']['name']
                    fn_args = tc.function.arguments if hasattr(tc, 'function') else tc['function']['arguments']
                    print(f"  [{i}] role=assistant, tool_call={fn_name}({fn_args})")
            else:
                content = msg.get("content") if isinstance(msg, dict) else msg.content
                print(f"  [{i}] role=assistant, content={str(content)[:80]}...")
        else:
            content = msg.get("content") if isinstance(msg, dict) else msg.content
            print(f"  [{i}] role={role}, content={str(content)[:80]}...")

    print("\n✅ Selesai! Memahami alur lengkap tool execution.")
    print("\nAlur Function Calling:")
    print("  1. User bertanya → Kirim pertanyaan + tool schema ke LLM")
    print("  2. LLM mengembalikan tool_call (nama fungsi + argumen)")
    print("  3. Kita eksekusi fungsi tersebut secara lokal")
    print("  4. Kirim hasil ke LLM dengan role='tool'")
    print("  5. LLM membuat jawaban final yang natural")

if __name__ == "__main__":
    main()
