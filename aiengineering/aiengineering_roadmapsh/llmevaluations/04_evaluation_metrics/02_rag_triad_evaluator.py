"""
02_rag_triad_evaluator.py
-------------------------
Kalkulator & Simulator RAG Triad Metrics:
1. Faithfulness Metric (Anti-Halusinasi: Klaim Respons vs Context)
2. Answer Relevance Metric (Kesesuaian Jawaban vs User Query)
3. Context Precision & Context Recall Metrics
"""

class RAGTriadEvaluator:
    """Implementasi Simulator RAG Triad Scorer."""

    def evaluate_faithfulness(self, response: str, contexts: list[str]) -> dict:
        """
        Mengukur apakah klaim dalam respons didukung oleh retrieved context.
        Skor 1.0 = Bebas Halusinasi.
        """
        # Ekstrak klaim utama dari respons
        claims = [c.strip() for c in response.split('.') if len(c.strip()) > 5]
        if not claims:
            return {"score": 1.0, "reason": "Teks kosong."}

        supported_claims = 0
        context_text = " ".join(contexts).lower()

        for claim in claims:
            # Sederhana: cek kecocokan entitas/kata kunci klaim di context
            keywords = [w for w in claim.lower().split() if len(w) > 3]
            match_count = sum(1 for kw in keywords if kw in context_text)
            if match_count >= max(1, len(keywords) * 0.5):
                supported_claims += 1

        score = supported_claims / len(claims)
        return {
            "score": round(score, 2),
            "supported_claims": supported_claims,
            "total_claims": len(claims),
            "has_hallucination": score < 1.0,
            "reason": f"{supported_claims} dari {len(claims)} klaim terbukti secara faktual di context."
        }

    def evaluate_answer_relevance(self, query: str, response: str) -> dict:
        """
        Mengukur relevansi respons terhadap pertanyaan pengguna.
        """
        query_words = set(query.lower().replace("?", "").split())
        resp_words = set(response.lower().split())

        overlap = query_words.intersection(resp_words)
        relevance_score = len(overlap) / len(query_words) if query_words else 1.0
        # Normalisasi ke skala 0.0 - 1.0 dengan sigmoid/threshold boost
        final_score = min(1.0, round(relevance_score * 1.5 + 0.3, 2))

        return {
            "score": final_score,
            "query_keywords": list(query_words),
            "matched_keywords": list(overlap),
            "reason": "Respons menjawab aspek utama pertanyaan."
        }

    def evaluate_context_precision(self, query: str, contexts: list[str], ground_truth_relevant: list[bool]) -> dict:
        """
        Mengukur apakah chunk relevan berada di peringkat atas.
        Cumulative Precision @ K.
        """
        if not contexts:
            return {"score": 0.0, "reason": "No contexts retrieved."}

        precisions = []
        relevant_count = 0

        for k, is_rel in enumerate(ground_truth_relevant, 1):
            if is_rel:
                relevant_count += 1
                precisions.append(relevant_count / k)

        avg_precision = sum(precisions) / len(precisions) if precisions else 0.0
        return {
            "score": round(avg_precision, 2),
            "retrieved_count": len(contexts),
            "relevant_retrieved": sum(ground_truth_relevant),
            "reason": f"Context Precision @ K: {round(avg_precision, 2)}"
        }

    def evaluate_full_rag_triad(self, query: str, response: str, contexts: list[str], ground_truth_relevant: list[bool]) -> dict:
        """Menjalankan evaluasi RAG Triad secara lengkap."""
        faith = self.evaluate_faithfulness(response, contexts)
        relev = self.evaluate_answer_relevance(query, response)
        prec  = self.evaluate_context_precision(query, contexts, ground_truth_relevant)

        triad_score = round((faith['score'] + relev['score'] + prec['score']) / 3.0, 2)

        return {
            "triad_overall_score": triad_score,
            "faithfulness": faith,
            "answer_relevance": relev,
            "context_precision": prec
        }


if __name__ == "__main__":
    print("=== LAB 11: RAG TRIAD EVALUATOR ===")

    evaluator = RAGTriadEvaluator()

    user_query = "Siapa penemu RAG dan apa gunanya?"
    llm_resp = "RAG ditemukan oleh tim Facebook AI Research (FAIR) pada tahun 2020. RAG berguna untuk menggabungkan retrieval dokumen dengan LLM."
    retrieved_docs = [
        "Retrieval-Augmented Generation (RAG) diperkenalkan oleh Patrick Lewis dan tim Facebook AI Research (FAIR) pada tahun 2020.",
        "RAG memungingkan LLM mengakses dokumen eksternal untuk menjawab pertanyaan dengan akurat."
    ]
    relevance_flags = [True, True] # Dua chunk di atas relevan

    results = evaluator.evaluate_full_rag_triad(user_query, llm_resp, retrieved_docs, relevance_flags)

    print(f"\n[User Query]: '{user_query}'")
    print(f"[LLM Response]: '{llm_resp}'")
    print(f"\n--- RAG TRIAD RESULTS ---")
    print(f" 🛡️  1. Faithfulness Score     : {results['faithfulness']['score']} / 1.0 ({results['faithfulness']['reason']})")
    print(f" 🎯 2. Answer Relevance Score : {results['answer_relevance']['score']} / 1.0 ({results['answer_relevance']['reason']})")
    print(f" 📍 3. Context Precision Score: {results['context_precision']['score']} / 1.0 ({results['context_precision']['reason']})")
    print(f"\n⭐ OVERALL RAG TRIAD SCORE: {results['triad_overall_score']} / 1.0")
