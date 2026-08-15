import os
import json
from openai import OpenAI

def main():
    print("=== 4.1 ReAct Agent Manual (Reasoning + Acting) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # REACT PATTERN
    # ReAct = Reasoning + Acting
    # Pola: Thought → Action → Observation → Thought → ... → Final Answer
    #
    # Berbeda dengan function calling (tool otomatis), ReAct menggunakan
    # prompt engineering murni untuk membuat agent berpikir langkah
    # demi langkah dan memilih aksi.
    # ---------------------------------------------------------------

    # Definisi tools yang tersedia (sebagai teks, bukan JSON schema)
    TOOLS_DESCRIPTION = """
Tools yang tersedia:
1. kalkulator(ekspresi) - Menghitung ekspresi matematika. Input: string ekspresi.
2. cari_fakta(topik) - Mencari fakta tentang topik tertentu. Input: string topik.
"""

    # Simulasi eksekusi tool
    def eksekusi_tool(nama_tool, input_tool):
        if nama_tool == "kalkulator":
            try:
                allowed = set("0123456789+-*/().% ")
                if all(c in allowed for c in input_tool):
                    return str(eval(input_tool))
                return "Error: ekspresi tidak valid"
            except:
                return "Error: gagal menghitung"

        elif nama_tool == "cari_fakta":
            fakta_db = {
                "indonesia": "Indonesia punya 17.000+ pulau, populasi ~275 juta jiwa, ibukota Jakarta (pindah ke IKN).",
                "ai agent": "AI Agent menggunakan LLM sebagai otak, tools untuk berinteraksi, dan memory untuk konteks.",
                "python": "Python dibuat oleh Guido van Rossum tahun 1991. Versi terbaru Python 3.12+.",
            }
            for key, val in fakta_db.items():
                if key in input_tool.lower():
                    return val
            return f"Fakta tentang '{input_tool}' tidak ditemukan."

        return f"Tool '{nama_tool}' tidak dikenal."

    # System prompt yang mengajarkan pola ReAct
    REACT_SYSTEM_PROMPT = f"""Kamu adalah AI Agent yang menyelesaikan tugas langkah demi langkah.

{TOOLS_DESCRIPTION}

Untuk setiap langkah, gunakan format berikut PERSIS:
Thought: [pikiran kamu tentang apa yang harus dilakukan]
Action: [nama_tool(input)]
--- PAUSE ---

Setelah mendapat hasil (Observation), pikirkan lagi dan lanjutkan.

Jika sudah punya jawaban akhir, gunakan:
Thought: [pikiran akhir]
Final Answer: [jawaban lengkap untuk user]

PENTING:
- Selalu mulai dengan Thought
- Hanya satu Action per langkah
- Selalu tulis --- PAUSE --- setelah Action
- Jangan mengarang hasil tool, tunggu Observation dari sistem
"""

    # ---------------------------------------------------------------
    # AGENT LOOP
    # Ini adalah loop utama agent ReAct
    # ---------------------------------------------------------------
    pertanyaan = "Berapa populasi Indonesia dan berapa rata-rata jika dibagi 34 provinsi?"
    print(f"User: {pertanyaan}\n")
    print("=" * 60)

    messages = [
        {"role": "system", "content": REACT_SYSTEM_PROMPT},
        {"role": "user", "content": pertanyaan}
    ]

    MAX_ITERATIONS = 5  # Batas agar tidak loop selamanya
    iteration = 0

    while iteration < MAX_ITERATIONS:
        iteration += 1
        print(f"\n--- Iterasi {iteration} ---")

        # Kirim ke LLM
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.0,
            stop=["--- PAUSE ---"]  # Berhenti saat agent mau melakukan action
        )

        assistant_reply = response.choices[0].message.content
        print(f"Agent:\n{assistant_reply}")

        # Tambahkan ke riwayat
        messages.append({"role": "assistant", "content": assistant_reply})

        # Cek apakah sudah ada Final Answer
        if "Final Answer:" in assistant_reply:
            # Ekstrak jawaban akhir
            final_answer = assistant_reply.split("Final Answer:")[-1].strip()
            print(f"\n{'='*60}")
            print(f"✅ JAWABAN AKHIR: {final_answer}")
            break

        # Cek apakah ada Action yang perlu dieksekusi
        if "Action:" in assistant_reply:
            # Parse action dari teks
            action_line = ""
            for line in assistant_reply.split("\n"):
                if line.strip().startswith("Action:"):
                    action_line = line.split("Action:")[-1].strip()
                    break

            if action_line:
                # Parse nama_tool dan input dari format: nama_tool(input)
                if "(" in action_line and ")" in action_line:
                    tool_name = action_line.split("(")[0].strip()
                    tool_input = action_line.split("(", 1)[1].rsplit(")", 1)[0].strip()

                    print(f"\n  🔧 Eksekusi: {tool_name}({tool_input})")
                    observation = eksekusi_tool(tool_name, tool_input)
                    print(f"  📋 Observation: {observation}")

                    # Kirim Observation kembali ke agent
                    messages.append({
                        "role": "user",
                        "content": f"Observation: {observation}"
                    })
                else:
                    print(f"  [ERROR] Format action tidak valid: {action_line}")
                    break
        else:
            # Tidak ada action dan tidak ada final answer
            print("  [INFO] Agent tidak melakukan action. Menyelesaikan...")
            break

    if iteration >= MAX_ITERATIONS:
        print(f"\n⚠️ Agent mencapai batas maksimal iterasi ({MAX_ITERATIONS})")

    print(f"\n{'='*60}")
    print(f"Total iterasi: {iteration}")
    print(f"Total messages: {len(messages)}")

    print("\n✅ Selesai! Memahami pola ReAct Agent.")
    print("\nAlur ReAct:")
    print("  1. Thought: Agent berpikir tentang apa yang harus dilakukan")
    print("  2. Action: Agent memilih tool dan memberikan input")
    print("  3. --- PAUSE ---: Agent berhenti, kita eksekusi tool")
    print("  4. Observation: Hasil tool dikirim kembali ke agent")
    print("  5. Ulangi sampai agent memberikan Final Answer")

if __name__ == "__main__":
    main()
