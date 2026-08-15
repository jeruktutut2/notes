#!/usr/bin/env python3
"""
Modul 6.2: LLM-as-a-Judge & Evaluation Frameworks
Implementasi pattern LLM-as-a-Judge (Pairwise scoring, Absolute grading, Mitigasi Bias).
"""

from typing import Dict, List, Tuple

def demonstrate_llm_as_a_judge_pattern():
    print("\n" + "="*70)
    print(" 1. PATTERN LLM-AS-A-JUDGE (PAIRWISE SCORING & ABSOLUTE GRADING)")
    print("="*70)
    print("LLM-as-a-Judge menggunakan LLM yang lebih kuat (e.g. GPT-4o) untuk menilai respon agent lain.\n")
    
    prompt = "Jelaskan apa itu Tokenization dalam 1 kalimat ringkas."
    response_agent_a = "Tokenization adalah proses memecah teks menjadi potongan subword/id integer yang dipahami model."
    response_agent_b = "Tokenization adalah teknik mengubah teks menjadi bahasa mesin menggunakan algoritma biner komputer secara sangat cepat dan efisien tanpa batas."
    
    print(f"User Prompt: '{prompt}'\n")
    print(f"Respon Model A: '{response_agent_a}'")
    print(f"Respon Model B: '{response_agent_b}'\n")
    
    print("Evaluasi Judge Model (Kriteria: Kejelasan, Ketepatan, Ringkas):")
    print("  • Model A Score: \033[92m9.5 / 10\033[0m (Akurat, tepat sasaran, memenuhi kriteria 1 kalimat).")
    print("  • Model B Score: \033[91m6.0 / 10\033[0m (Bertele-tele, menggunakan istilah biner yang kurang tepat).")
    print("\nPemenang Pairwise: \033[92mModel A\033[0m")
    print()


def demonstrate_bias_mitigation():
    print("="*70)
    print(" 2. BIAS DALAM LLM-AS-A-JUDGE DAN TEKNIK MITIGASI")
    print("="*70)
    
    biases = [
        ("Position Bias", "Model Judge cenderung memilih opsi PERTAMA (Model A) lebih sering.", "Lakukan Swap Order Evaluation (Uji dua kali: A vs B lalu B vs A)."),
        ("Verbosity Bias", "Model Judge cenderung menyukai respon PANJANG padahal tidak relevan.", "Berikan instruksi explicit: 'Ganjarkan penalti pada jawaban yang bertele-tele'."),
        ("Self-Enhancement Bias", "Model Judge cenderung memberi skor lebih tinggi pada output keluaran dari keluarganya sendiri.", "Gunakan ensemble of judges (e.g. gabungan Claude + GPT + DeepSeek).")
    ]
    
    for name, problem, mitigation in biases:
        print(f" • \033[93m{name:<22}\033[0m")
        print(f"   Masalah : {problem}")
        print(f"   Mitigasi: \033[96m{mitigation}\033[0m")
        print("-" * 65)
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 6.2: LLM-AS-A-JUDGE & EVALUATION FRAMEWORKS")
    print("█"*70)
    
    demonstrate_llm_as_a_judge_pattern()
    demonstrate_bias_mitigation()
    
    print("="*70)
    print(" Kesimpulan:")
    print(" 1. LLM-as-a-Judge memiliki korelasi >80% dengan penilaian manusia jika dikalibrasi dengan baik.")
    print(" 2. Selalu gunakanSwap Position Test (A-B vs B-A) untuk menghilangkan Position Bias.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
