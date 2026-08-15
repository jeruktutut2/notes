"""
03_llm_as_a_judge_pairwise.py
-------------------------------------------------------------------
Contoh Pengujian Regresi AI: Pairwise Head-to-Head LLM-as-a-Judge
(Membandingkan Baseline vs Candidate menggunakan Model Evaluator).
-------------------------------------------------------------------
"""

import json
from typing import Dict, Any, List
from tabulate import tabulate

# 1. Test Dataset untuk Evaluasi Head-to-Head
PAIRWISE_BENCHMARK = [
    {
        "id": "PW-01",
        "instruction": "Tulis email penolakan lamaran kerja yang sopan dan profesional.",
        "baseline_output": "Yth. Pelamar, Terima kasih atas minat Anda. Kami mengapresiasi waktu Anda. Namun saat ini kami memutuskan untuk melanjutkan kandidat lain. Semoga sukses.",
        "candidate_output": "Halo! Terima kasih sudah melamar. Lamaran Anda bagus tapi kurang cocok saat ini. Jangan berkecil hati ya!",
        "criteria": "Kesopanan, profesionalisme, dan struktur bahasa."
    },
    {
        "id": "PW-02",
        "instruction": "Jelaskan konsep dasar Quantum Computing untuk anak umur 10 tahun.",
        "baseline_output": "Komputer biasa menggunakan bit 0 atau 1 seperti saklar lampu. Komputer kuantum menggunakan qubit yang bisa jadi 0 dan 1 bersamaan, seperti koin yang sedang berputar di udara!",
        "candidate_output": "Quantum computing mengimplementasikan mekanika kuantum dengan prinsip superposisi dan keterkaitan kuantum (entanglement) untuk memproses matriks kompleks.",
        "criteria": "Kemudahan dipahami anak-anak, analogi yang tepat, dan kejelasan."
    },
    {
        "id": "PW-03",
        "instruction": "Ringkas langkah-langkah mengatasi printer macet.",
        "baseline_output": "1. Matikan printer.\n2. Buka penutup dan tarik kertas pelan-pelan.\n3. Periksa sisa kotoran.\n4. Nyalakan kembali.",
        "candidate_output": "1. Matikan printer & cabut kabel daya.\n2. Buka pintu akses cartridge/kertas.\n3. Tarik kertas tersangkut searah jalur secara perlahan.\n4. Pastikan tidak ada serpihan kertas tersisa.\n5. Pasang kembali dan hidupkan printer.",
        "criteria": "Kelengkapan instruksi, keselamatan kerja, dan kerapihan poin."
    }
]

# 2. Simulator LLM-as-a-Judge (Dapat diganti dengan OpenAI/Gemini API di produksi)
def mock_llm_judge_eval(instruction: str, output_a: str, output_b: str, criteria: str) -> Dict[str, Any]:
    """
    Simulasi Evaluator LLM yang menerima Output A (Baseline) dan Output B (Candidate)
    dan mengembalikan pemenang (WINNER_A, WINNER_B, TIE) beserta alasannya.
    """
    # Kasus PW-01: Candidate terlalu santai -> Baseline Menang
    if "penolakan lamaran" in instruction:
        return {
            "winner": "WINNER_A",
            "score_a": 9,
            "score_b": 5,
            "reason": "Output A jauh lebih profesional dan formal untuk email penolakan kerja. Output B terlalu santai."
        }
    # Kasus PW-02: Candidate pakai bahasa akademis -> Baseline Menang
    elif "Quantum Computing" in instruction:
        return {
            "winner": "WINNER_A",
            "score_a": 10,
            "score_b": 3,
            "reason": "Output A menggunakan analogi koin berputar yang sangat bagus untuk anak 10 tahun. Output B terlalu teknis."
        }
    # Kasus PW-03: Candidate memberikan instruksi lebih rinci -> Candidate Menang!
    elif "printer macet" in instruction:
        return {
            "winner": "WINNER_B",
            "score_a": 7,
            "score_b": 9.5,
            "reason": "Output B lebih mendetail dan menyertakan langkah keselamatan penting (mencabut kabel)."
        }
        
    return {"winner": "TIE", "score_a": 7, "score_b": 7, "reason": "Kedua output seimbang."}

def run_pairwise_regression_test():
    print("=" * 80)
    print("⚖️ AI REGRESSION TEST: PAIRWISE LLM-AS-A-JUDGE EVALUATION")
    print("=" * 80)
    
    baseline_wins = 0
    candidate_wins = 0
    ties = 0
    
    table_rows = []
    
    for item in PAIRWISE_BENCHMARK:
        item_id = item["id"]
        inst = item["instruction"]
        base_out = item["baseline_output"]
        cand_out = item["candidate_output"]
        crit = item["criteria"]
        
        eval_res = mock_llm_judge_eval(inst, base_out, cand_out, crit)
        winner = eval_res["winner"]
        
        if winner == "WINNER_A":
            baseline_wins += 1
            status = "🚨 REGRESSION (Baseline Won)"
        elif winner == "WINNER_B":
            candidate_wins += 1
            status = "✨ IMPROVED (Candidate Won)"
        else:
            ties += 1
            status = "⚖️ TIE"
            
        table_rows.append([
            item_id,
            f"{eval_res['score_a']} vs {eval_res['score_b']}",
            winner,
            status,
            eval_res["reason"]
        ])
        
    print(tabulate(
        table_rows,
        headers=["Test ID", "Scores (A vs B)", "Winner", "Regression Outcome", "Judge Reason"],
        tablefmt="grid"
    ))
    
    total = len(PAIRWISE_BENCHMARK)
    win_rate_candidate = (candidate_wins / total) * 100
    regress_rate = (baseline_wins / total) * 100
    
    print("\n📊 RANGKUMAN WIN/LOSS PAIRWISE:")
    print(f"- Baseline Wins  (A) : {baseline_wins} ({regress_rate:.1f}%)")
    print(f"- Candidate Wins (B) : {candidate_wins} ({win_rate_candidate:.1f}%)")
    print(f"- Ties               : {ties}")
    
    if baseline_wins > candidate_wins:
        print("\n❌ KESIMPULAN: Candidate Prompt/Model baru mengalami REGRESI (Kalah dibanding Baseline pada mayoritas kasus).")
    else:
        print("\n✅ KESIMPULAN: Candidate Prompt/Model baru MENINGKATKAN kualitas sistem.")

if __name__ == "__main__":
    run_pairwise_regression_test()
