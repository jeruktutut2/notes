"""
MODUL 6.3: Automatic Prompt Engineering (APE) & Meta-Prompting
=============================================================
Penjelasan:
Automatic Prompt Engineering (APE) menggunakan LLM untuk secara otomatis menghasilkan,
mengevaluasi, dan menyempurnakan prompt kandidat (Meta-Prompting) hingga menemukan
prompt dengan akurasi tertinggi untuk tugas tertentu.

Alur APE:
1. Meta-Prompt: LLM diminta membuat 3 variasi prompt instruksi berdasarkan contoh pasangan input-output.
2. Candidate Evaluation: Setiap variasi prompt diuji terhadap dataset evaluasi.
3. Selection: Memilih prompt dengan skor performa tertinggi.
"""

def meta_prompt_generator(task_description: str, test_cases: list) -> list:
    """Simulasi Meta-Prompt yang menghasilkan 3 kandidat prompt otomatis."""
    print("Executing Meta-Prompting Generator...")
    return [
        "Variasi 1 (Klasik): Ekstrak nama entitas dan peran dari teks.",
        "Variasi 2 (Terstruktur XML): <instruction>Identifikasi entitas nama dan posisi dalam tag <result></instruction>",
        "Variasi 3 (Few-shot CoT): Analisis hubungan kalimat secara bertahap, lalu keluarkan pasangan (Nama -> Peran)."
    ]


def evaluate_candidate(candidate_prompt: str) -> float:
    """Simulasi skor akurasi kandidat prompt pada dataset pengujian (0.0 - 1.0)."""
    if "XML" in candidate_prompt:
        return 0.94
    elif "Few-shot" in candidate_prompt:
        return 0.91
    else:
        return 0.78


def main():
    print("==========================================================")
    print(" DEMO 6.3: Automatic Prompt Engineering (APE) Loop")
    print("==========================================================\n")

    task = "Ekstraksi entitas nama dan jabatan dari email korporat."
    test_cases = [
        {"input": "Budi Rahardjo ditunjuk sebagai VP Engineering baru.", "expected": "Budi Rahardjo (VP Engineering)"}
    ]

    # Step 1: Generasi Kandidat Prompt via Meta-Prompting
    candidates = meta_prompt_generator(task, test_cases)
    
    print("\n[1] KANDIDAT PROMPT HASIL GENERASI APE:")
    for idx, c in enumerate(candidates, 1):
        print(f"  {idx}. {c}")
        
    print("\n" + "="*60 + "\n")

    # Step 2: Evaluasi Otomatis Terhadap Dataset
    print("[2] EVALUASI PERFORMA KANDIDAT PROMPT:")
    best_candidate = None
    best_score = -1.0

    for c in candidates:
        score = evaluate_candidate(c)
        print(f" Prompt: \"{c[:45]}...\" -> Accuracy Score: {score*100:.1f}%")
        if score > best_score:
            best_score = score
            best_candidate = c

    print("\n" + "="*60)
    print(f"[3] PROMPT TERBAIK HASIL APE (Skor {best_score*100:.1f}%):")
    print(f" >> {best_candidate}")
    print("==========================================================")

if __name__ == "__main__":
    main()
