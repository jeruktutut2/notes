"""
MODUL 2.2: Chain-of-Thought (CoT) Prompting
===========================================
Penjelasan:
Chain-of-Thought (CoT) mendorong LLM untuk menguraikan tahapan berpikir (reasoning steps)
sebelum memberikan jawaban akhir.
- Zero-Shot CoT: Menambahkan kalimat pemicu seperti "Mari kita berpikir langkah demi langkah." (Let's think step by step).
- Manual CoT: Memberikan contoh penalaran eksplisit dalam contoh Few-Shot.
"""

def zero_shot_cot_prompt(question: str) -> str:
    return f"""Soal: {question}

Mari kita berpikir langkah demi langkah (step-by-step reasoning):"""


def manual_few_shot_cot_prompt(question: str) -> str:
    return f"""Soal: Budi memiliki 5 apel. Ia membeli 2 kantong apel lagi. Setiap kantong berisi 6 apel. Lalu ia membagikan 4 apel ke adiknya. Berapa sisa apel Budi?
Penalaran:
1. Budi mulai dengan 5 apel.
2. Ia membeli 2 kantong x 6 apel = 12 apel baru.
3. Total apel sebelum dibagi = 5 + 12 = 17 apel.
4. Ia membagikan 4 apel, maka sisa apel = 17 - 4 = 13 apel.
Jawaban: 13

Soal: {question}
Penalaran:"""


def simulate_cot_reasoning(prompt_type: str, question: str):
    if prompt_type == "standard":
        return "Jawaban: 27 (Tanpa urutan penalaran)"
    else:
        return """1. Toko memiliki stok awal 50 unit laptop.
2. Hari Senin terjual 12 unit -> Stok tersisa: 50 - 12 = 38 unit.
3. Hari Selasa ada pengembalian (retur) 3 unit -> Stok menjadi: 38 + 3 = 41 unit.
4. Hari Rabu toko menerima pasokan baru sebanyak 2 kardus (masing-masing 10 unit) -> Total pasokan = 2 x 10 = 20 unit.
5. Stok akhir toko = 41 + 20 = 61 unit.
Jawaban Akhir: 61 unit laptop."""


def main():
    print("==========================================================")
    print(" DEMO 2.2: Chain-of-Thought (CoT) Reasoning Mechanics")
    print("==========================================================\n")

    math_question = (
        "Sebuah toko elektronik memiliki 50 laptop. Hari Senin terjual 12 laptop. "
        "Hari Selasa ada retur 3 laptop. Hari Rabu datang stok baru 2 kardus (isi 10 laptop per kardus). "
        "Berapa jumlah laptop di toko sekarang?"
    )

    print("[1] PROMPT STANDAR (TANPA CoT):")
    print(f"Soal: {math_question}")
    print("\nRespon LLM:")
    print(simulate_cot_reasoning("standard", math_question))

    print("\n" + "="*60 + "\n")

    print("[2] ZERO-SHOT CoT ('Mari berpikir langkah demi langkah'):")
    zs_prompt = zero_shot_cot_prompt(math_question)
    print(zs_prompt)
    print("\nRespon LLM (Penalaran Kompleks):")
    print(simulate_cot_reasoning("cot", math_question))

    print("\n" + "="*60 + "\n")

    print("[3] MANUAL FEW-SHOT CoT:")
    fs_cot_prompt = manual_few_shot_cot_prompt(math_question)
    print(fs_cot_prompt)
    print("\nRespon LLM:")
    print(simulate_cot_reasoning("cot", math_question))
    print("==========================================================")

if __name__ == "__main__":
    main()
