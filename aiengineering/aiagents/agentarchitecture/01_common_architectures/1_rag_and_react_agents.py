#!/usr/bin/env python3
"""
Modul 01: Common Architectures - Part 1
Simulasi RAG Agent & ReAct (Reason + Act) Agent
"""

import math
import json
import re
from typing import List, Dict, Any, Tuple

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
BOLD = "\033[1m"
RESET = "\033[0m"


# ============================================================================
# 1. RAG AGENT (Retrieval-Augmented Generation)
# ============================================================================
class SimpleVectorStore:
    """Simulasi Vector Database sederhana menggunakan Cosine Similarity."""

    def __init__(self):
        self.documents: List[Dict[str, Any]] = []

    def _pseudo_embed(self, text: str) -> List[float]:
        """Menghasilkan vector pseudo-embedding (32-dim) berdasarkan bag-of-words hash."""
        vec = [0.0] * 32
        words = re.findall(r'\w+', text.lower())
        for word in words:
            idx = sum(ord(c) for c in word) % 32
            vec[idx] += 1.0
        # Normalisasi ke unit vector
        norm = math.sqrt(sum(v * v for v in vec)) or 1.0
        return [v / norm for v in vec]

    def add_document(self, doc_id: str, content: str, metadata: Dict[str, Any] = None):
        vec = self._pseudo_embed(content)
        self.documents.append({
            "id": doc_id,
            "content": content,
            "metadata": metadata or {},
            "vector": vec
        })

    def search(self, query: str, top_k: int = 2) -> List[Tuple[Dict[str, Any], float]]:
        query_vec = self._pseudo_embed(query)
        results = []
        for doc in self.documents:
            # Cosine similarity: (A . B) / (||A|| * ||B||)
            dot = sum(q * d for q, d in zip(query_vec, doc["vector"]))
            results.append((doc, dot))
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:top_k]


class RAGAgent:
    """Agent yang mengambil konteks eksternal sebelum membuat jawaban."""

    def __init__(self, vector_store: SimpleVectorStore):
        self.vector_store = vector_store

    def query(self, user_question: str) -> str:
        print(f"\n{BOLD}{CYAN}=== RAG AGENT EXECUTION ==={RESET}")
        print(f"User Query: '{user_question}'")

        # Step 1: Retrieval
        retrieved_docs = self.vector_store.search(user_question, top_k=2)
        print(f"\n{YELLOW}[1. RETRIEVAL STEP]{RESET} Mengambil Top-K dokumen relevan...")
        context_chunks = []
        for i, (doc, score) in enumerate(retrieved_docs, 1):
            print(f"  Doc #{i} [{doc['id']}] (Similarity Score: {score:.4f}): '{doc['content'][:60]}...'")
            context_chunks.append(f"[{doc['id']}]: {doc['content']}")

        # Step 2: Context Injection & LLM Generation
        combined_context = "\n".join(context_chunks)
        prompt = (
            f"Gunakan konteks berikut untuk menjawab pertanyaan:\n"
            f"KONTEKS:\n{combined_context}\n\n"
            f"PERTANYAAN: {user_question}"
        )
        print(f"\n{GREEN}[2. GENERATION STEP]{RESET} Injeksi Konteks ke Prompt LLM:")
        print(f"{BLUE}--- Injected Prompt ---\n{prompt}\n----------------------{RESET}")

        response = f"Berdasarkan dokumen tepercaya, {context_chunks[0]}"
        return response


# ============================================================================
# 2. REACT AGENT (Reason + Act)
# ============================================================================
class ReActAgent:
    """Simulasi Agent berbasis ReAct Loop (Thought -> Action -> Observation)."""

    def __init__(self):
        self.tools = {
            "calculator": lambda expr: str(eval(expr, {"__builtins__": {}}, {})),
            "search_database": lambda q: "Stok laptop ThinkPad: 15 unit, Harga: Rp 18.000.000." if "thinkpad" in q.lower() else "Data tidak ditemukan."
        }

    def run(self, goal: str, max_steps: int = 4):
        print(f"\n{BOLD}{MAGENTA}=== REACT AGENT (REASON + ACT) EXECUTION ==={RESET}")
        print(f"Goal: {goal}\n")

        trajectory = []
        current_step = 1

        while current_step <= max_steps:
            print(f"{BOLD}--- Iterasi #{current_step} ---{RESET}")

            # Simulated LLM Thought & Action selection based on step
            if current_step == 1:
                thought = "Untuk menjawab total nilai inventaris ThinkPad, saya perlu mencari stok dan harga ThinkPad."
                action_name = "search_database"
                action_input = "ThinkPad"
            elif current_step == 2:
                thought = "Saya mendapatkan data: stok = 15, harga = 18000000. Sekarang saya harus mengalikan 15 * 18000000."
                action_name = "calculator"
                action_input = "15 * 18000000"
            else:
                thought = "Kalkulasi selesai. Saya dapat menyusun jawaban akhir."
                action_name = "FINISH"
                action_input = "Total nilai inventaris ThinkPad adalah Rp 270.000.000 (15 unit @ Rp 18.000.000)."

            print(f"  {YELLOW}THOUGHT:{RESET} {thought}")
            
            if action_name == "FINISH":
                print(f"  {GREEN}FINAL ANSWER:{RESET} {action_input}\n")
                trajectory.append({"step": current_step, "thought": thought, "answer": action_input})
                break

            print(f"  {CYAN}ACTION:{RESET} {action_name}({action_input})")

            # Execution & Observation
            if action_name in self.tools:
                obs = self.tools[action_name](action_input)
            else:
                obs = f"Error: Tool '{action_name}' tidak tersedia."

            print(f"  {BLUE}OBSERVATION:{RESET} {obs}\n")
            trajectory.append({"step": current_step, "thought": thought, "action": action_name, "observation": obs})
            current_step += 1


# ============================================================================
# DEMO EXECUTION
# ============================================================================
def main():
    print(f"{BOLD}{GREEN}===================================================={RESET}")
    print(f"{BOLD}{GREEN} MODUL 01.1: RAG AGENT & REACT AGENT SIMULATION    {RESET}")
    print(f"{BOLD}{GREEN}===================================================={RESET}")

    # Demo 1: RAG Agent
    vdb = SimpleVectorStore()
    vdb.add_document("DOC-01", "Kebijakan Garansi: Laptop Lenovo ThinkPad memiliki garansi resmi 3 tahun garansi onsite.", {"category": "policy"})
    vdb.add_document("DOC-02", "Prosedur Klaim: Klaim garansi membutuhkan nota pembelian dan nomor seri produk.", {"category": "procedure"})
    vdb.add_document("DOC-03", "Jam Operasional Service Center: Senin - Jumat pukul 08:00 - 17:00 WIB.", {"category": "info"})

    rag_agent = RAGAgent(vdb)
    rag_agent.query("Berapa lama masa garansi laptop ThinkPad?")

    # Demo 2: ReAct Agent
    react_agent = ReActAgent()
    react_agent.run("Berapa total nilai inventaris stok laptop ThinkPad yang ada di gudang?")


if __name__ == "__main__":
    main()
