"""
01_rag_vs_finetuning_matrix.py
Simulasi & Matriks Perbandingan RAG vs Fine-Tuning
"""

import sys

COMPARISON_MATRIX = [
    {
        "criterion": "Penambahan Data Fakta Baru",
        "rag": "Sangat Mudah (Instant Update di Vector DB)",
        "finetuning": "Sulit (Harus re-train model dengan dataset baru)",
        "winner": "RAG"
    },
    {
        "criterion": "Pengurangan Halusinasi",
        "rag": "Tinggi (Konteks eksplisit disediakan di prompt)",
        "finetuning": "Sedang (Model masih bisa mengalami hallucination)",
        "winner": "RAG"
    },
    {
        "criterion": "Transparansi & Sitasi Sumber",
        "rag": "Terdapat sitasi jelas (Nama dokumen, halaman)",
        "finetuning": "Tidak ada (Pengetahuan tersimpan di bobot implisit)",
        "winner": "RAG"
    },
    {
        "criterion": "Penyesuaian Style, Format, & Tone",
        "rag": "Keterbatasan prompt engineering",
        "finetuning": "Sangat Baik (Model terbiasa dengan struktur khusus)",
        "winner": "Fine-Tuning"
    },
    {
        "criterion": "Biaya Pelatihan & Komputasi",
        "rag": "Rendah (Hanya biaya embedding & pencarian)",
        "finetuning": "Tinggi (Membutuhkan GPU High-End jam/hari)",
        "winner": "RAG"
    }
]

def evaluate_decision_tree(has_frequent_data_change: bool, needs_format_style: bool, needs_citations: bool):
    print("\n🧠 KEPUTUSAN ARSITEKTUR TERIMA KHUSUS:")
    print(f"  • Data sering berubah? {has_frequent_data_change}")
    print(f"  • Butuh penyesuaian gaya/format ketat? {needs_format_style}")
    print(f"  • Butuh transparansi sitasi? {needs_citations}")
    print("-" * 50)
    
    if has_frequent_data_change or needs_citations:
        if needs_format_style:
            recommendation = "★ HYBRID APPROACH (RAG + Fine-Tuning) ★\n  Gunakan Fine-Tuning untuk mengajari gaya/format output, dan RAG untuk fakta terkini."
        else:
            recommendation = "★ RAG (Retrieval-Augmented Generation) ★\n  Pendekatan paling tepat, murah, dan cepat untuk data dinamis."
    else:
        if needs_format_style:
            recommendation = "★ FINE-TUNING ★\n  Cocok untuk membekukan gaya khusus pada model tanpa perlu RAG."
        else:
            recommendation = "★ PROMPT ENGINEERING ★\n  Cukup gunakan System Prompt yang efektif tanpa RAG maupun Fine-Tuning."
            
    print(f"👉 Rekomendasi: {recommendation}")

def run_matrix_demo():
    print("=" * 70)
    print("⚖️ MATRIKS PERBANDINGAN RAG VS FINE-TUNING")
    print("=" * 70)
    print(f"{'Kriteria':<30} | {'RAG':<20} | {'Fine-Tuning':<20}")
    print("-" * 75)
    for row in COMPARISON_MATRIX:
        print(f"{row['criterion']:<30} | {row['rag']:<20} | {row['finetuning']:<20}")
    print("=" * 70)
    
    # Run test cases
    evaluate_decision_tree(has_frequent_data_change=True, needs_format_style=False, needs_citations=True)
    evaluate_decision_tree(has_frequent_data_change=True, needs_format_style=True, needs_citations=True)
    evaluate_decision_tree(has_frequent_data_change=False, needs_format_style=True, needs_citations=False)

if __name__ == "__main__":
    run_matrix_demo()
