"""
MODUL 2.1: Zero-Shot vs Few-Shot Prompting
==========================================
Penjelasan:
- Zero-Shot: Memberikan instruksi langsung tanpa contoh sebelumnya.
- Few-Shot (In-Context Learning): Memberikan 1 atau lebih contoh (exemplars)
  pasangan (Input -> Output) untuk membimbing LLM memahami format dan logika.
"""

def build_zero_shot_prompt(text: str) -> str:
    return f"""Klasifikasikan sentimen dari teks berikut menjadi [POSITIF, NEGATIF, NEUTRAL]:

Teks: "{text}"
Sentimen:"""


def build_few_shot_prompt(text: str, exemplars: list) -> str:
    prompt_lines = ["Klasifikasikan sentimen dari teks berikut sesuai pola contoh di bawah:\n"]
    
    for ex in exemplars:
        prompt_lines.append(f"Teks: \"{ex['text']}\"")
        prompt_lines.append(f"Sentimen: {ex['label']}\n")
        
    prompt_lines.append(f"Teks: \"{text}\"")
    prompt_lines.append("Sentimen:")
    
    return "\n".join(prompt_lines)


def main():
    print("==========================================================")
    print(" DEMO 2.1: Zero-Shot vs Few-Shot In-Context Learning")
    print("==========================================================\n")

    test_input = "Pelayanan restoran sangat lambat, tapi makanannya enak dan harganya terjangkau."
    
    exemplars = [
        {"text": "Aplikasi sering crash dan lambat sekali!", "label": "NEGATIF"},
        {"text": "Pengiriman cepat, kemasan rapi, barang original.", "label": "POSITIF"},
        {"text": "Ukuran bajunya pas di badan saya.", "label": "NEUTRAL"}
    ]

    zero_shot = build_zero_shot_prompt(test_input)
    few_shot = build_few_shot_prompt(test_input, exemplars)

    print("[1] ZERO-SHOT PROMPT:")
    print("-" * 40)
    print(zero_shot)
    print("\nHasil Klasifikasi Zero-Shot (Mungkin ambigu/terlalu umum): NEUTRAL / MIXED")

    print("\n" + "="*60 + "\n")

    print("[2] FEW-SHOT PROMPT (WITH 3 EXEMPLARS):")
    print("-" * 40)
    print(few_shot)
    print("\nHasil Klasifikasi Few-Shot (Konsisten mengikuti pola): POSITIF (dengan catatan minor)")
    print("==========================================================")

if __name__ == "__main__":
    main()
