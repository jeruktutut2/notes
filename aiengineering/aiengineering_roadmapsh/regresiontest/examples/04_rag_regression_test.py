"""
04_rag_regression_test.py
-------------------------------------------------------------------
Contoh Pengujian Regresi AI: Evaluasi Regresi Pipeline RAG
(Retrieval-Augmented Generation) - Faithfulness, Context & Answer Relevancy.
-------------------------------------------------------------------
"""

from typing import Dict, Any, List
from tabulate import tabulate

# 1. Benchmark Test Cases RAG
RAG_TEST_CASES = [
    {
        "id": "RAG-01",
        "question": "Berapa lama garansi resmi laptop PT TechAI?",
        "ground_truth_answer": "Garansi resmi laptop PT TechAI adalah 24 bulan untuk hardware dan 12 bulan untuk baterai.",
        "config_v1_baseline": {
            "chunk_size": 500,
            "retrieved_context": [
                "PT TechAI memberikan garansi resmi selama 24 bulan untuk komponen hardware laptop.",
                "Baterai dan pengisi daya laptop PT TechAI dilindungi garansi terbatas selama 12 bulan."
            ],
            "generated_answer": "Garansi resmi laptop PT TechAI adalah 24 bulan untuk hardware dan 12 bulan untuk baterai."
        },
        "config_v2_candidate": {
            "chunk_size": 100, # Chunk terlalu kecil memotong konteks!
            "retrieved_context": [
                "PT TechAI memberikan garansi resmi laptop..." # Konteks terpotong!
            ],
            "generated_answer": "Garansi laptop PT TechAI biasanya 1 tahun." # HALLUCINATION / INACCURATE!
        }
    },
    {
        "id": "RAG-02",
        "question": "Syarat pengajuan refund lisensi software?",
        "ground_truth_answer": "Refund lisensi software dapat diajukan dalam waktu 7 hari jika lisensi belum diaktivasi.",
        "config_v1_baseline": {
            "chunk_size": 500,
            "retrieved_context": [
                "Pengajuan pengembalian dana (refund) lisensi software harus dilakukan maksimal 7 hari setelah pembelian dengan syarat kode lisensi belum pernah diaktivasi."
            ],
            "generated_answer": "Anda bisa mengajukan refund lisensi dalam 7 hari jika kode belum diaktivasi."
        },
        "config_v2_candidate": {
            "chunk_size": 500,
            "retrieved_context": [
                "Pengajuan pengembalian dana (refund) lisensi software harus dilakukan maksimal 7 hari setelah pembelian dengan syarat kode lisensi belum pernah diaktivasi."
            ],
            "generated_answer": "Refund lisensi software dapat diajukan dalam 7 hari selama belum diaktivasi." # Konsisten!
        }
    }
]

# 2. RAG Evaluator Metrics (Faithfulness & Context Precision)
def compute_rag_metrics(context_list: List[str], answer: str, gt_answer: str) -> Dict[str, float]:
    """
    Simulasi pengujian 3 Metrik Utama RAG (Skor 0.0 - 1.0):
    1. Faithfulness (Apakah jawaban bersumber murni dari konteks yang di-retrieve)
    2. Context Relevance (Apakah dokumen yang di-retrieve relevan dengan pertanyaan)
    3. Answer Relevance (Apakah jawaban menjawab pertanyaan dengan benar)
    """
    # Simple heuristic metrics simulation for demonstration
    faithfulness = 1.0
    context_relevance = 1.0
    answer_relevance = 1.0
    
    context_text = " ".join(context_list)
    
    # Check Faithfulness: apakah ada klaim di answer yang tidak ada di context
    if "1 tahun" in answer and "1 tahun" not in context_text:
        faithfulness = 0.20 # Hallucination detected!
        answer_relevance = 0.40
        
    if "..." in context_text or len(context_text) < 50:
        context_relevance = 0.30 # Context precision drop due to aggressive chunking
        
    return {
        "faithfulness": faithfulness,
        "context_relevance": context_relevance,
        "answer_relevance": answer_relevance,
        "overall_score": round((faithfulness + context_relevance + answer_relevance) / 3, 2)
    }

def run_rag_regression_test():
    print("=" * 85)
    print("📚 AI REGRESSION TEST: RAG RETRIEVAL & GENERATION EVALUATION")
    print("=" * 85)
    
    table_rows = []
    
    for case in RAG_TEST_CASES:
        case_id = case["id"]
        q = case["question"]
        gt = case["ground_truth_answer"]
        
        c_v1 = case["config_v1_baseline"]
        c_v2 = case["config_v2_candidate"]
        
        m_v1 = compute_rag_metrics(c_v1["retrieved_context"], c_v1["generated_answer"], gt)
        m_v2 = compute_rag_metrics(c_v2["retrieved_context"], c_v2["generated_answer"], gt)
        
        delta = m_v2["overall_score"] - m_v1["overall_score"]
        status = "🚨 REGRESSION" if delta < -0.15 else ("✅ STABLE" if abs(delta) <= 0.15 else "✨ IMPROVED")
        
        table_rows.append([
            case_id,
            f"{m_v1['overall_score']} (Faith: {m_v1['faithfulness']:.2f})",
            f"{m_v2['overall_score']} (Faith: {m_v2['faithfulness']:.2f})",
            f"{delta:+.2f}",
            status
        ])
        
    print(tabulate(
        table_rows,
        headers=["Test ID", "Baseline RAG Score", "Candidate RAG Score", "Score Delta", "Status"],
        tablefmt="grid"
    ))
    
    print("\n💡 CATATAN RAG REGRESSION:")
    print("- Penurunan Chunk Size di Candidate (v2) pada RAG-01 memotong konteks penting, memicu HALLUCINATION dan penurunan Faithfulness.")
    print("- Regression test RAG mencegah deploy perubahan chunking/embedding yang merusak akurasi informasi.")

if __name__ == "__main__":
    run_rag_regression_test()
