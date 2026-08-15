#!/usr/bin/env python3
"""
Modul: Chain-of-Thought (CoT) & ReAct Framework
Simulasi perbandingan Standard vs CoT Reasoning dan ReAct Agent Execution Loop.
"""

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def main():
    print("=" * 70)
    print(color("  MODUL: CHAIN-OF-THOUGHT (CoT) & ReAct FRAMEWORK", "1;34"))
    print("=" * 70)

    problem = "Di gudang ada 40 kardus. Setiap kardus berisi 12 botol. 5 kardus rusak dan dibuang, lalu 50 botol eceran ditambahkan. Berapa total botol sekarang?"

    print(color("\n1. CHAIN-OF-THOUGHT (CoT) REASONING SIMULATION:", "1;33"))
    print(f"Soal: {problem}")
    
    print(color("\n[Tanpa CoT / Direct Output]:", "31"))
    print("Jawaban: 470 botol. (Risiko salah hitung)")
    
    print(color("\n[Dengan CoT / Step-by-Step Reasoning]:", "1;32"))
    cot_steps = [
        "Langkah 1: Hitung kardus utuh yang tersisa = 40 - 5 = 35 kardus.",
        "Langkah 2: Hitung total botol dari kardus utuh = 35 * 12 = 420 botol.",
        "Langkah 3: Tambahkan botol eceran baru = 420 + 50 = 470 botol.",
        "Kesimpulan Akhir: Total botol di gudang sekarang adalah 470 botol."
    ]
    for step in cot_steps:
        print(f"  • {step}")

    print(color("\n2. ReAct FRAMEWORK (Thought -> Action -> Observation):", "1;33"))
    user_query = "Siapa CEO Google saat ini dan berapa usianya di tahun 2026?"
    print(f"Query: '{user_query}'")

    react_loop = [
        ("Thought 1", "Saya perlu mencari tahu siapa CEO Google saat ini."),
        ("Action 1", "search_google('current CEO of Google')"),
        ("Observation 1", "Sundar Pichai adalah CEO Google dan Alphabet."),
        ("Thought 2", "Sekarang saya perlu mencari tanggal lahir Sundar Pichai untuk menghitung usianya di tahun 2026."),
        ("Action 2", "search_google('Sundar Pichai birth date')"),
        ("Observation 2", "Sundar Pichai lahir pada 10 Juni 1972."),
        ("Thought 3", "Saya akan menghitung usia: 2026 - 1972 = 54 tahun. Saya siap memberikan jawaban akhir."),
        ("Final Answer", "CEO Google saat ini adalah Sundar Pichai. Pada tahun 2026, beliau berusia 54 tahun.")
    ]

    for stage, text in react_loop:
        if stage == "Final Answer":
            print(color(f"\n  [{stage}]: {text}", "1;32"))
        elif "Thought" in stage:
            print(color(f"\n  [{stage}]: {text}", "36"))
        elif "Action" in stage:
            print(color(f"  [{stage}]: {text}", "33"))
        else:
            print(color(f"  [{stage}]: {text}", "35"))

    print("\n" + "=" * 70)
    print("✓ CoT memberikan komputasi token eksplisit untuk penalaran logika internal.")
    print("✓ ReAct menghubungkan penalaran internal dengan aksi dunia nyata (APIs / Web Search).")

if __name__ == "__main__":
    main()
