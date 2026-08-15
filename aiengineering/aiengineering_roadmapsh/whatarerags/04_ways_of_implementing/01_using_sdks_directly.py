"""
01_using_sdks_directly.py
Membangun End-to-End RAG Pipeline Secara Langsung Menggunakan Standard SDKs (Pure Python + Vector Store)
Tanpa ketergantungan framework pihak ketiga seperti LangChain atau LlamaIndex.
"""

import math
from typing import List, Dict, Any

class PureSDKRAGPipeline:
    """RAG Pipeline Sederhana Menggunakan Standard SDK / Pure Python Logic"""
    def __init__(self):
        self.documents = []
        
    def add_document(self, doc_id: str, text: str):
        # 1. Chunking (Sentence split)
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        for idx, sentence in enumerate(sentences):
            self.documents.append({
                "doc_id": doc_id,
                "chunk_id": f"{doc_id}_c{idx+1}",
                "text": sentence + "."
            })
            
    def _cosine_similarity(self, words1: List[str], words2: List[str]) -> float:
        set1, set2 = set(words1), set(words2)
        intersection = set1.intersection(set2)
        if not intersection:
            return 0.0
        return len(intersection) / (math.sqrt(len(set1)) * math.sqrt(len(set2)))
        
    def retrieve(self, query: str, top_k: int = 2) -> List[Dict[str, Any]]:
        query_words = [w.lower() for w in query.split()]
        scored_chunks = []
        
        for chunk in self.documents:
            chunk_words = [w.lower() for w in chunk["text"].split()]
            sim = self._cosine_similarity(query_words, chunk_words)
            scored_chunks.append({"score": sim, "chunk": chunk})
            
        scored_chunks.sort(key=lambda x: x["score"], reverse=True)
        return [item["chunk"] for item in scored_chunks[:top_k] if item["score"] > 0]

    def generate(self, query: str) -> str:
        top_chunks = self.retrieve(query, top_k=2)
        if not top_chunks:
            return "Maaf, informasi tidak ditemukan dalam dokumen."
            
        context_str = "\n".join([f"- [{c['chunk_id']}] {c['text']}" for c in top_chunks])
        
        # Sintesis Jawaban
        response = f"Berdasarkan informasi internal:\n{context_str}\n\n[Jawaban disintesis secara langsung melalui Custom SDK Pipeline]"
        return response

def run_direct_sdk_demo():
    print("=" * 70)
    print("⚙️ DEMONSTRASI RAG MENGGUNAKAN SDK DIRECTLY (PURE PYTHON)")
    print("=" * 70)
    
    rag = PureSDKRAGPipeline()
    rag.add_document("POLICY-01", "Ketentuan garansi produk berlaku selama 12 bulan sejak tanggal pembelian. Klaim membutuhkan struk asli.")
    rag.add_document("POLICY-02", "Pengembalian produk dapat dilakukan dalam waktu 7 hari jika terdapat cacat pabrik.")
    
    query = "Berapa lama masa garansi produk dan apa syaratnya?"
    print(f"❓ Query: \"{query}\"")
    print("-" * 50)
    
    ans = rag.generate(query)
    print(ans)
    print("=" * 70)

if __name__ == "__main__":
    run_direct_sdk_demo()
