"""
MODUL 4.2: Negative Constraints & Guardrails Validation
======================================================
Penjelasan:
Negative Constraints mendefinisikan hal-hal yang TIDAK BOLEH dilakukan atau dimuat oleh LLM
(seperti: "Jangan gunakan jargon medis", "Jangan sebutkan kompetitor X", "Maksimal 3 kalimat").
Guardrails validator memeriksa apakah output akhir mematuhi batasan tersebut sebelum dikembalikan ke pengguna.
"""

def generate_constrained_prompt(product_info: str) -> str:
    return f"""Tugas: Buat deskripsi pemasaran untuk produk berikut.

Aturan & Batasan Wajib (Constraints & Guardrails):
1. [POSITIVE]: Jelaskan 2 fitur utama dengan gaya bahasa antusias.
2. [NEGATIVE]: JANGAN pernah menyebutkan kata atau produk pesaing ("Brand X", "Pesaing", "Kompetitor").
3. [NEGATIVE]: JANGAN menyajikan klaim medis yang belum teruji (misal: "Menyembuhkan penyakit").
4. [NEGATIVE]: Panjang jawaban MAKSIMAL 3 kalimat.

Informasi Produk:
"{product_info}"

Deskripsi Pemasaran:"""


def validate_guardrails(text: str, forbidden_words: list, max_sentences: int = 3) -> dict:
    """Validator independen untuk memastikan output LLM aman."""
    violations = []
    
    # Check forbidden words
    for word in forbidden_words:
        if word.lower() in text.lower():
            violations.append(f"Melanggar Negative Constraint: Terdeteksi kata dilarang '{word}'.")
            
    # Check sentence count
    sentences = [s.strip() for s in text.split(".") if s.strip()]
    if len(sentences) > max_sentences:
        violations.append(f"Melanggar Batasan Panjang: Jumlah kalimat ({len(sentences)}) melebihi batas {max_sentences}.")
        
    return {
        "passed": len(violations) == 0,
        "violations": violations
    }


def main():
    print("==========================================================")
    print(" DEMO 4.2: Negative Constraints & Algorithmic Guardrails")
    print("==========================================================\n")

    prod_info = "Minuman herbal rasa jahe merah cair siap minum dalam kemasan saset."
    prompt = generate_constrained_prompt(prod_info)
    
    print("[PROMPT DENGAN NEGATIVE CONSTRAINTS]:")
    print(prompt)
    print("\n" + "="*60 + "\n")

    # Skenario Respon LLM A (Lolos Guardrail)
    output_a = "Rasakan kesegaran hangat Jahe Merah siap minum dalam kemasan praktis saset! Dibuat dari jahe pilihan untuk menemani aktivitas harian Anda. Dapatkan sensasi stamina segar setiap hari!"
    
    # Skenario Respon LLM B (Melanggar Guardrail)
    output_b = "Minuman herbal jahe merah ini jauh lebih mantap daripada Brand X! Produk ini dapat menyembuhkan penyakit flu secara instan dalam 5 menit. Selain itu harganya sangat murah dan terjangkau di kantong. Mari beli sekarang juga di toko terdekat."

    forbidden = ["Brand X", "kompetitor", "pesaing", "menyembuhkan"]

    print("[TEST OUTPUT A]:")
    print(f"\"{output_a}\"")
    res_a = validate_guardrails(output_a, forbidden, max_sentences=3)
    print(f"Guardrail Check Result: {'PASSED' if res_a['passed'] else 'FAILED'}")
    if not res_a["passed"]:
        print(f"Pelanggaran: {res_a['violations']}")

    print("\n" + "-"*50 + "\n")

    print("[TEST OUTPUT B]:")
    print(f"\"{output_b}\"")
    res_b = validate_guardrails(output_b, forbidden, max_sentences=3)
    print(f"Guardrail Check Result: {'PASSED' if res_b['passed'] else 'FAILED'}")
    if not res_b["passed"]:
        print("Detail Pelanggaran:")
        for v in res_b["violations"]:
            print(f" - {v}")

    print("==========================================================")

if __name__ == "__main__":
    main()
