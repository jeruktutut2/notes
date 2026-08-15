"""
MODUL 3.3: Least-to-Most Prompting (Sub-problem Decomposition)
==============================================================
Penjelasan:
Least-to-Most Prompting memecah tugas kompleks menjadi sub-masalah yang lebih sederhana (dekomposisi),
lalu menyelesaikannya secara sekuensial di mana hasil dari sub-masalah sebelumnya digunakan
sebagai konteks untuk menyelesaikan sub-masalah berikutnya.
"""

def decompose_problem_prompt(complex_question: str) -> str:
    return f"""Tugas: Pecah masalah kompleks berikut menjadi urutan sub-pertanyaan dari yang paling sederhana hingga paling kompleks.

Masalah Utama: "{complex_question}"

Sub-pertanyaan Terurai:"""


def solve_subproblems_sequentially(subproblems: list):
    context = ""
    print("--- Solusi Sekuensial Least-to-Most ---")
    
    solutions = [
        "Jarak Jakarta ke Surabaya lewat jalan tol adalah 780 km.",
        "Konsumsi BBM mobil 15 km/liter, jadi butuh BBM = 780 / 15 = 52 liter.",
        "Harga pertamax Rp 13.500/liter, total biaya BBM = 52 x 13.500 = Rp 702.000."
    ]
    
    for idx, (sub, sol) in enumerate(zip(subproblems, solutions), 1):
        print(f"\n[Sub-Masalah {idx}]: {sub}")
        if context:
            print(f" (Konteks dari langkah sebelumnya: '{context}')")
        print(f" Solusi LLM: {sol}")
        context = sol
        
    return solutions[-1]


def main():
    print("==========================================================")
    print(" DEMO 3.3: Least-to-Most Prompting & Problem Decomposition")
    print("==========================================================\n")

    complex_q = "Berapa total biaya BBM untuk perjalanan mobil dari Jakarta ke Surabaya jika tarif Pertamax Rp 13.500/liter dan efisiensi mobil 15 km/liter?"

    print(f"Masalah Kompleks: {complex_q}\n")

    # Step 1: Dekomposisi
    subproblems = [
        "1. Berapa jarak tempuh dari Jakarta ke Surabaya?",
        "2. Berapa liter BBM yang dibutuhkan untuk menempuh jarak tersebut?",
        "3. Berapa total biaya dalam Rupiah untuk jumlah BBM tersebut?"
    ]
    
    print("[1] LANGKAH DEKOMPOSISI (Sub-masalah):")
    for sub in subproblems:
        print(f"  {sub}")

    print("\n" + "="*60 + "\n")

    # Step 2: Penyelesaian Sekuensial
    final_ans = solve_subproblems_sequentially(subproblems)
    
    print("\n" + "="*60)
    print(f"Hasil Akhir Terverifikasi: {final_ans}")
    print("==========================================================")

if __name__ == "__main__":
    main()
