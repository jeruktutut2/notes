"""
MODUL 2.3: Self-Consistency Sampling & Tree-of-Thought (ToT)
============================================================
Penjelasan:
- Self-Consistency: Menjalankan beberapa jalur penalaran (CoT) secara paralel
  dengan temperatur > 0, lalu melakukan Majority Voting pada jawaban akhir.
- Tree-of-Thought (ToT): Mengeksplorasi pohon keputusan (Node -> Evaluation -> Branching)
  untuk pemecahan masalah kompleks yang membutuhkan backtrack/search (seperti puzzle/strategi).
"""

from collections import Counter
import random

def self_consistency_simulation(question: str, num_samples: int = 5) -> dict:
    """Simulasi pengambilan N sampel CoT dengan variasi penalaran & majority voting."""
    possible_paths = [
        {"path": "50 - 12 = 38; 38 + 3 = 41; 41 + 20 = 61.", "answer": 61},
        {"path": "Total masuk = 50 + 3 + 20 = 73; Keluar = 12; 73 - 12 = 61.", "answer": 61},
        {"path": "50 - 12 = 38; 38 + 20 = 58; 58 + 3 = 61.", "answer": 61},
        {"path": "50 - 12 = 38; 38 - 3 = 35; 35 + 20 = 55.", "answer": 55}, # Jalur salah/hallucinated
        {"path": "50 - 12 = 38; 38 + 3 = 41; 41 + 20 = 61.", "answer": 61}
    ]
    
    samples = random.sample(possible_paths, num_samples)
    answers = [s["answer"] for s in samples]
    vote_counts = Counter(answers)
    majority_answer, highest_votes = vote_counts.most_common(1)[0]
    
    return {
        "samples": samples,
        "vote_counts": dict(vote_counts),
        "majority_answer": majority_answer,
        "confidence": highest_votes / num_samples
    }


def tree_of_thought_simulation(goal: str):
    """Simulasi eksplorasi pohon keputusan (ToT) untuk perencanaan strategis."""
    tree = {
        "Root": "Tujuan: Tingkatkan Conversions E-Commerce sebesar 20%",
        "Langkah_1_Cabang": [
            {"node": "Cabang A: Optimasi UI/UX Checkout", "skor": 0.85},
            {"node": "Cabang B: Diskon Besar-besaran (Price Cut)", "skor": 0.40},
            {"node": "Cabang C: Email Marketing Campaign", "skor": 0.65}
        ],
        "Langkah_2_Eksplorasi_Cabang_A": [
            {"subnode": "A1: Kurangi form checkout dari 5 input menjadi 2 input", "skor": 0.92},
            {"subnode": "A2: Tambahkan tombol One-Click Buy via E-Wallet", "skor": 0.95}
        ]
    }
    return tree


def main():
    print("==========================================================")
    print(" DEMO 2.3: Self-Consistency Voting & Tree-of-Thought (ToT)")
    print("==========================================================\n")

    question = "Hitung total stok barang (50 - 12 + 3 + 20)."
    
    # 1. Self-Consistency
    print("[1] SELF-CONSISTENCY SAMPLING & MAJORITY VOTING:")
    print("-" * 50)
    res = self_consistency_simulation(question, num_samples=5)
    for idx, sample in enumerate(res["samples"], 1):
        print(f" Sampel #{idx}: {sample['path']} -> Jawaban: {sample['answer']}")
        
    print(f"\nHasil Pemungutan Suara (Voting): {res['vote_counts']}")
    print(f"Jawaban Konsensus Terbaik: {res['majority_answer']} (Tingkat Kepercayaan: {res['confidence']*100:.0f}%)")

    print("\n" + "="*60 + "\n")

    # 2. Tree-of-Thought (ToT)
    print("[2] TREE-OF-THOUGHT (ToT) SEARCH & EVALUATION:")
    print("-" * 50)
    tot = tree_of_thought_simulation("Optimasi Conversions")
    print(f"Goal: {tot['Root']}")
    print("\n[Level 1 Branching & Evaluasi Skor]:")
    for branch in tot["Langkah_1_Cabang"]:
        print(f" - {branch['node']} (Evaluasi LLM: {branch['skor']})")
        
    print("\n[Level 2 Deep Search pada Cabang Tertinggi (Cabang A)]:")
    for sub in tot["Langkah_2_Eksplorasi_Cabang_A"]:
        print(f"   -> {sub['subnode']} (Skor Terpilih: {sub['skor']})")
        
    print("\nSolusi Optimal ToT: Terapkan 'One-Click Buy via E-Wallet' dan pangkas form checkout.")
    print("==========================================================")

if __name__ == "__main__":
    main()
