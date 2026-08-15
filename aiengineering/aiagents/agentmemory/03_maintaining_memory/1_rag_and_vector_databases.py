#!/usr/bin/env python3
"""
Modul 03: Maintaining Memory
Skrip 1: RAG & Vector Databases (Retrieval-Augmented Generation)

Simulasi RAG dan Vector Database untuk pemeliharaan memori eksternal.
Fitur utama:
- Text Chunking & Simple Vector Embedding Simulation (TF-IDF / Frequency Vector).
- Perhitungan Cosine Similarity: Sim(A, B) = (A . B) / (||A|| * ||B||).
- Top-K Vector Nearest Neighbor Search.
- Dynamic Context Injection ke Prompt Short-Term Memory.
"""

import math
import re
from typing import List, Dict, Tuple, Any

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"


class SimpleVectorStore:
    """Vector Database sederhana menggunakan Cosine Similarity."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.vocabulary: List[str] = []

    def _tokenize(self, text: str) -> List[str]:
        """Tokenisasi kata sederhana (lowercase & alphanumeric)."""
        return re.findall(r'\w+', text.lower())

    def _build_vocabulary(self, texts: List[str]):
        """Membuat daftar kata unik (vocabulary)."""
        vocab_set = set()
        for t in texts:
            vocab_set.update(self._tokenize(t))
        self.vocabulary = sorted(list(vocab_set))

    def _get_embedding(self, text: str) -> List[float]:
        """Mengubah teks menjadi vektor frekuensi kata (Bag-of-Words Embedding)."""
        tokens = self._tokenize(text)
        vector = [0.0] * len(self.vocabulary)
        for token in tokens:
            if token in self.vocabulary:
                idx = self.vocabulary.index(token)
                vector[idx] += 1.0
        return vector

    def add_documents(self, docs: List[str]):
        """Memuat dan mengindeks dokumen ke dalam Vector Database."""
        self._build_vocabulary(docs)
        self.documents = []
        for doc_id, doc in enumerate(docs):
            vector = self._get_embedding(doc)
            self.documents.append({
                "id": doc_id,
                "text": doc,
                "vector": vector
            })

    def cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        """Menghitung Cosine Similarity antara dua vektor."""
        dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
        norm_a = math.sqrt(sum(a * a for a in vec_a))
        norm_b = math.sqrt(sum(b * b for b in vec_b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def search(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        """Mencari Top-K dokumen paling relevan dengan query."""
        query_vec = self._get_embedding(query)
        scored_docs = []
        for doc in self.documents:
            score = self.cosine_similarity(query_vec, doc["vector"])
            scored_docs.append((doc, score))
        
        # Sort berdasarkan score tertinggi
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[:top_k]


def run_demo():
    print(f"{BOLD}{CYAN}======================================================================{RESET}")
    print(f"{BOLD}{CYAN}  MODUL 03.1: RAG AND VECTOR DATABASES (COSINE SIMILARITY SEARCH)    {RESET}")
    print(f"{BOLD}{CYAN}======================================================================{RESET}\n")

    # Korpus Dokumen Pengetahuan Organisasi / Memory Bank
    knowledge_base_docs = [
        "SOP Keamanan: Seluruh kredensial database harus disimpan di Environment Variable dan tidak boleh ditaruh hardcoded di kode.",
        "Arsitektur Server: Server API berjalan di Kubernetes cluster region ap-southeast-1 dengan port internal 8080.",
        "Prosedur Deployment: Untuk mendeploy AI Agent ke staging, jalankan perintah 'make deploy-staging' setelah passing unit test.",
        "Penanganan Error: Jika agent mengalami 500 Internal Error, periksa file log di /var/log/aiagent/error.log.",
        "Panduan Model Context Protocol (MCP): MCP menggunakan JSON-RPC 2.0 untuk komunikasi antara Client dan Server."
    ]

    vector_db = SimpleVectorStore()
    print(f"{GREEN}[INDEXING]{RESET} Mengindeks {len(knowledge_base_docs)} dokumen ke dalam Vector Store...")
    vector_db.add_documents(knowledge_base_docs)
    print(f"{GREEN}[SUCCESS]{RESET} Vocab Size: {len(vector_db.vocabulary)} kata unik.\n")

    # User Query
    user_query = "Bagaimana cara menyimpan kredensial database sesuai SOP keamanan?"
    print(f"{BOLD}---> User Query:{RESET} \"{user_query}\"")
    print("Menjalankan Vector Embedding & Cosine Similarity Search (Top-K = 2)...\n")

    results = vector_db.search(user_query, top_k=2)

    print(f"{BOLD}[RAG RETRIEVAL RESULTS]{RESET}")
    for rank, (doc, score) in enumerate(results, 1):
        print(f"  Peringkat {rank} | Cosine Score: {score:.4f}")
        print(f"  Dokumen ID: {doc['id']}")
        print(f"  Isi Dokumen: \"{doc['text']}\"\n")

    # Dynamic Context Injection ke Prompt Agent
    retrieved_context = "\n".join([f"- {doc['text']}" for doc, _ in results])
    final_prompt = f"""=== SYSTEM PROMPT WITH RAG CONTEXT ===
Anda adalah AI Assistant Compliance & Ops.
Manfaatkan informasi memori eksternal berikut untuk menjawab pertanyaan:

<RETRIEVED_KNOWLEDGE>
{retrieved_context}
</RETRIEVED_KNOWLEDGE>

USER QUESTION: {user_query}
"""

    print(f"{BOLD}{CYAN}--- PROMPT AKHIR SETELAH DIBERIKAN RAG CONTEXT ---{RESET}")
    print(final_prompt)
    print(f"{GREEN}[KESIMPULAN]{RESET} RAG memampukan Agent mengambil fragmen memori spesifik tanpa membebani context window dengan seluruh basis data.")


if __name__ == "__main__":
    run_demo()
