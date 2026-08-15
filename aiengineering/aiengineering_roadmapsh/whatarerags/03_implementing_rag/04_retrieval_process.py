"""
04_retrieval_process.py
Proses Retrieval Lanjutan: Hybrid Search (Dense Vector + BM25 Keyword Search) & Metadata Filtering
"""

from typing import List, Dict, Any

class HybridRetriever:
    """Simulasi Hybrid Search (Dense Embedding + Keyword Match)"""
    def __init__(self, corpus: List[Dict[str, Any]]):
        self.corpus = corpus
        
    def search(self, query: str, category_filter: str = None, top_k: int = 2) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        scored_docs = []
        
        for doc in self.corpus:
            # Metadata filter
            if category_filter and doc.get("category") != category_filter:
                continue
                
            doc_words = set(doc["text"].lower().split())
            overlap = len(query_words.intersection(doc_words))
            
            # Sparse Keyword Score (BM25 mock)
            keyword_score = overlap / max(len(query_words), 1)
            
            # Simulated Dense Vector Score
            dense_score = 0.75 if "garansi" in query.lower() and "garansi" in doc["text"].lower() else 0.40
            
            # Reciprocal Rank Fusion / Combined Hybrid Score
            hybrid_score = (0.5 * dense_score) + (0.5 * keyword_score)
            
            scored_docs.append({
                "score": hybrid_score,
                "dense_score": dense_score,
                "keyword_score": keyword_score,
                "doc": doc
            })
            
        scored_docs.sort(key=lambda x: x["score"], reverse=True)
        return scored_docs[:top_k]

def run_retrieval_demo():
    print("=" * 70)
    print("🔎 DEMONSTRASI RETRIEVAL PROCESS (HYBRID SEARCH & FILTERING)")
    print("=" * 70)
    
    corpus = [
        {"id": "1", "text": "Laptop Gaming ASUS ROG memiliki garansi resmi 2 tahun di Service Center resmi.", "category": "hardware"},
        {"id": "2", "text": "Laptop Business ThinkPad dirancang tangguh dengan garansi 3 tahun onsite support.", "category": "hardware"},
        {"id": "3", "text": "Kebijakan lisensi software antivirus berlaku 1 tahun per perangkat.", "category": "software"}
    ]
    
    retriever = HybridRetriever(corpus)
    query = "Garansi laptop resmi"
    
    print(f"❓ Query Pengguna : \"{query}\"")
    print("⚡ Mode Search    : Hybrid (Dense Vector + BM25 Sparse Keyword)")
    print("🏷️ Metadata Filter: category == 'hardware'")
    print("-" * 50)
    
    results = retriever.search(query, category_filter="hardware", top_k=2)
    for rank, res in enumerate(results, 1):
        print(f"   Rank #{rank} [Hybrid Score: {res['score']:.4f} (Dense: {res['dense_score']:.2f}, BM25: {res['keyword_score']:.2f})]")
        print(f"     ID   : {res['doc']['id']}")
        print(f"     Teks : \"{res['doc']['text']}\"")
        print()
    print("=" * 70)

if __name__ == "__main__":
    run_retrieval_demo()
