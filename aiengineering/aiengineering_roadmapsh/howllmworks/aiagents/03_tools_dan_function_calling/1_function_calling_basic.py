import os
import json
from openai import OpenAI

def main():
    print("=== 3.1 Function Calling - Dasar ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # APA ITU FUNCTION CALLING?
    # LLM sendiri tidak bisa mengakses internet, database, atau
    # menjalankan kode. Tapi LLM bisa MEMINTA kita untuk menjalankan
    # fungsi tertentu dengan parameter yang tepat.
    #
    # Alurnya:
    # 1. Kita DEFINISIKAN tools yang tersedia (nama, deskripsi, parameter)
    # 2. User bertanya → LLM menerima pertanyaan + daftar tools
    # 3. LLM MEMUTUSKAN apakah perlu memanggil tool atau cukup jawab langsung
    # 4. Jika perlu tool → LLM mengembalikan nama fungsi + argumen (bukan jawaban!)
    # 5. Kita EKSEKUSI fungsi tersebut dan kembalikan hasilnya ke LLM
    # 6. LLM membuat jawaban final berdasarkan hasil tool
    # ---------------------------------------------------------------

    # LANGKAH 1: Mendefinisikan Tool Schema
    # Format ini mengikuti standar OpenAI function calling
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_cuaca",
                "description": "Mendapatkan informasi cuaca terkini untuk kota tertentu di Indonesia",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "kota": {
                            "type": "string",
                            "description": "Nama kota, misal: Jakarta, Surabaya, Bandung"
                        },
                        "satuan": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "Satuan temperatur yang diinginkan"
                        }
                    },
                    "required": ["kota"]  # 'satuan' opsional
                }
            }
        }
    ]

    print("Tool yang didefinisikan:")
    print(json.dumps(tools, indent=2, ensure_ascii=False))
    print()

    # LANGKAH 2: Kirim pertanyaan + tools ke LLM
    print("=" * 60)
    print("Test 1: Pertanyaan yang MEMBUTUHKAN tool")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Kamu adalah asisten cuaca Indonesia."},
            {"role": "user", "content": "Bagaimana cuaca di Jakarta hari ini?"}
        ],
        tools=tools,
        tool_choice="auto"  # LLM memutuskan sendiri apakah perlu tool
    )

    message = response.choices[0].message

    # Cek apakah LLM memutuskan untuk memanggil tool
    if message.tool_calls:
        print("✅ LLM memutuskan untuk memanggil tool!\n")
        for tool_call in message.tool_calls:
            print(f"  Tool ID     : {tool_call.id}")
            print(f"  Nama Fungsi : {tool_call.function.name}")
            print(f"  Argumen     : {tool_call.function.arguments}")

            # Parse argumen
            args = json.loads(tool_call.function.arguments)
            print(f"  Argumen (parsed):")
            for key, value in args.items():
                print(f"    - {key}: {value}")
    else:
        print("LLM menjawab langsung tanpa tool:")
        print(f"  {message.content}")

    # LANGKAH 3: Test dengan pertanyaan yang TIDAK membutuhkan tool
    print("\n" + "=" * 60)
    print("Test 2: Pertanyaan yang TIDAK membutuhkan tool")
    print("=" * 60)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Kamu adalah asisten cuaca Indonesia."},
            {"role": "user", "content": "Apa itu hujan asam?"}
        ],
        tools=tools,
        tool_choice="auto"
    )

    message = response.choices[0].message
    if message.tool_calls:
        print("LLM memanggil tool (tidak seharusnya):")
        for tc in message.tool_calls:
            print(f"  {tc.function.name}({tc.function.arguments})")
    else:
        print("✅ LLM menjawab langsung (tanpa tool) - benar!")
        print(f"  Jawaban: {message.content[:200]}...")

    print("\n✅ Selesai! Memahami dasar function calling.")
    print("\nRingkasan:")
    print("- Tools didefinisikan sebagai JSON schema (nama, deskripsi, parameter)")
    print("- LLM TIDAK menjalankan fungsi — LLM hanya MEMINTA kita menjalankannya")
    print("- tool_choice='auto': LLM memutuskan sendiri perlu tool atau tidak")
    print("- LLM mengembalikan nama fungsi + argumen yang harus kita eksekusi")

if __name__ == "__main__":
    main()
