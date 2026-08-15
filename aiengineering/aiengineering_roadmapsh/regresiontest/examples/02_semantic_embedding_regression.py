"""
02_semantic_embedding_regression.py
-------------------------------------------------------------------
Contoh Pengujian Regresi AI: Evaluasi Kemiripan Makna Kalimat
(Semantic Cosine Similarity) menggunakan Vector Space / Embeddings.
-------------------------------------------------------------------
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from tabulate import tabulate

# 1. Dataset Uji dengan Ground Truth (Jawaban Referensi Emas)
EVAL_CASES = [
    {
        "id": "SEM-01",
        "prompt": "Jelaskan definisi Machine Learning secara singkat.",
        "ground_truth": "Machine Learning adalah cabang kecerdasan buatan yang memungkinkan sistem belajar dari data dan meningkatkan akurasi secara otomatis tanpa diprogram secara eksplisit.",
        "baseline_output": "Machine Learning merupakan bagian dari AI di mana komputer belajar dari pola data untuk membuat prediksi tanpa perlu instruksi pemrograman langsung.",
        "candidate_output_good": "Machine learning adalah sub-bidang AI yang melatih algoritma menggunakan data agar komputer dapat mengambil keputusan secara mandiri.",
        "candidate_output_regressed": "Machine learning adalah proses membeli server berkecepatan tinggi untuk menjalankan script Python pada GPU mahal." # Meracau/Drift!
    },
    {
        "id": "SEM-02",
        "prompt": "Bagaimana cara meriset kata kunci SEO?",
        "ground_truth": "Riset kata kunci SEO dilakukan dengan mengidentifikasi topik relevan, menggunakan alat seperti Google Keyword Planner, menganalisis volume pencarian dan kompetisi.",
        "baseline_output": "Untuk meriset SEO, cari topik utama bisnis Anda, gunakan tool keyword planner untuk melihat volume pencarian, dan pilih keyword dengan tingkat kesulitan sedang.",
        "candidate_output_good": "Langkah riset kata kunci SEO meliputi penentuan topik, analisis volume pencarian lewat keyword tools, serta memilih kata kunci pencarian yang sesuai target.",
        "candidate_output_regressed": "Riset SEO dilakukan dengan memposting link website Anda ke sebanyak mungkin grup Facebook setiap hari." # Regresi total!
    }
]

class LocalEmbeddingEvaluator:
    """Evaluator kemiripan vektor sederhana berbasis TF-IDF & Cosine Similarity."""
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def calculate_similarity(self, text1: str, text2: str) -> float:
        tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
        sim = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(sim)

def run_semantic_regression_test():
    print("=" * 80)
    print("🧠 AI REGRESSION TEST: SEMANTIC EMBEDDING COSINE SIMILARITY")
    print("=" * 80)
    
    evaluator = LocalEmbeddingEvaluator()
    SIMILARITY_THRESHOLD = 0.70  # Batas ambang minimum kemiripan makna
    
    table_data = []
    
    for case in EVAL_CASES:
        case_id = case["id"]
        gt = case["ground_truth"]
        
        # Hitung Similarity Baseline vs Ground Truth
        score_base = evaluator.calculate_similarity(case["baseline_output"], gt)
        
        # Hitung Similarity Candidate Good vs Ground Truth
        score_cand_good = evaluator.calculate_similarity(case["candidate_output_good"], gt)
        
        # Hitung Similarity Candidate Regressed vs Ground Truth
        score_cand_bad = evaluator.calculate_similarity(case["candidate_output_regressed"], gt)
        
        # Status Regresi untuk Candidate Regressed
        reg_delta = score_cand_bad - score_base
        status = "🚨 REGRESSION" if score_cand_bad < SIMILARITY_THRESHOLD else "✅ OK"
        
        table_data.append([
            case_id,
            f"{score_base:.3f}",
            f"{score_cand_good:.3f} (Good)",
            f"{score_cand_bad:.3f} (Regressed)",
            f"{reg_delta:+.3f}",
            status
        ])
        
    print(tabulate(
        table_data,
        headers=["Test ID", "Baseline Score", "Cand Good Score", "Cand Regress Score", "Delta", "Regress Status"],
        tablefmt="grid"
    ))
    
    print("\n💡 PENJELASAN METRIK:")
    print(f"- Threshold Minimal Skor Kemiripan Makna : {SIMILARITY_THRESHOLD}")
    print("- Jika skor Candidate mengalami penurunan drastis (Delta negatif besar) di bawah threshold, terjadi SEMANTIC REGRESSION.")

if __name__ == "__main__":
    run_semantic_regression_test()
