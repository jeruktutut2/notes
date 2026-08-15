import os
from openai import OpenAI

def main():
    print("=== 1.1 Memanggil LLM via API (OpenAI-Compatible) ===\n")

    # ---------------------------------------------------------------
    # KONFIGURASI
    # Menggunakan OpenAI-compatible API. Bisa dipakai untuk:
    # - OpenAI:    https://api.openai.com/v1
    # - Groq:      https://api.groq.com/openai/v1
    # - Together:  https://api.together.xyz/v1
    # - OpenRouter: https://openrouter.ai/api/v1
    # ---------------------------------------------------------------
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        print("Jalankan: export OPENAI_API_KEY='sk-xxx-your-key'")
        return

    # 1. Inisialisasi Client
    # Library `openai` bisa dipakai untuk provider manapun yang OpenAI-compatible
    client = OpenAI(
        api_key=api_key,
        base_url=base_url
    )

    print(f"Provider URL : {base_url}")
    print(f"Model        : {model}")
    print("-" * 50)

    # 2. Memanggil Chat Completion API
    # Ini adalah cara paling dasar berkomunikasi dengan LLM
    print("\n[Mengirim permintaan ke LLM...]")

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "Kamu adalah asisten yang menjawab dalam Bahasa Indonesia dengan singkat dan jelas."
            },
            {
                "role": "user",
                "content": "Apa itu AI Agent? Jelaskan dalam 2-3 kalimat."
            }
        ]
    )

    # 3. Mengambil Hasil Respons
    jawaban = response.choices[0].message.content
    print(f"\nJawaban LLM:\n{jawaban}")

    # 4. Informasi Penggunaan Token
    # Setiap API call mengonsumsi token (input + output)
    print(f"\n--- Info Penggunaan Token ---")
    print(f"Token Input  (Prompt) : {response.usage.prompt_tokens}")
    print(f"Token Output (Completion): {response.usage.completion_tokens}")
    print(f"Total Token            : {response.usage.total_tokens}")

    # 5. Contoh percakapan multi-turn (beberapa pesan bolak-balik)
    print("\n\n=== Contoh Percakapan Multi-Turn ===")
    print("-" * 50)

    messages = [
        {"role": "system", "content": "Kamu adalah guru AI yang sabar. Jawab singkat dalam Bahasa Indonesia."},
        {"role": "user", "content": "Apa perbedaan AI dan Machine Learning?"},
    ]

    # Turn 1
    print(f"User: {messages[-1]['content']}")
    response_1 = client.chat.completions.create(model=model, messages=messages)
    jawaban_1 = response_1.choices[0].message.content
    print(f"AI  : {jawaban_1}\n")

    # Tambahkan jawaban AI ke riwayat, lalu tanya lagi
    messages.append({"role": "assistant", "content": jawaban_1})
    messages.append({"role": "user", "content": "Lalu apa hubungannya dengan Deep Learning?"})

    # Turn 2
    print(f"User: {messages[-1]['content']}")
    response_2 = client.chat.completions.create(model=model, messages=messages)
    jawaban_2 = response_2.choices[0].message.content
    print(f"AI  : {jawaban_2}")

    print("\n✅ Selesai! LLM berhasil dipanggil via API.")
    print("Catatan: Perhatikan bahwa di Turn 2, LLM 'mengingat' konteks Turn 1")
    print("karena kita mengirim seluruh riwayat percakapan di setiap request.")

if __name__ == "__main__":
    main()
