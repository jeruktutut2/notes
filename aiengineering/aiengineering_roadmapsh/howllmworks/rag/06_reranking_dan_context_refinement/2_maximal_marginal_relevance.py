import numpy as np

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))

def maximal_marginal_relevance(query_vec: np.ndarray, doc_vecs: list, lmbda: float = 0.5, top_k: int = 3) -> list:
    """
    Algoritma MMR (Maximal Marginal Relevance):
    MMR = argmax_{d in R \\ S} [ lambda * Sim1(d, Q) - (1 - lambda) * max_{d_j in S} Sim2(d, d_j) ]

    lmbda = 1.0 -> Murni pencarian relevansi terbanyak.
    lmbda = 0.0 -> Murni keberagaman (diversity) maksimal.
    lmbda = 0.5 -> Keseimbangan seimbang antara relevansi dan keberagaman.
    """
    unselected = list(range(len(doc_vecs)))
    selected = []

    while len(selected) < min(top_k, len(doc_vecs)):
        best_score = -float('inf')
        best_idx = -1

        for idx in unselected:
            doc_vec = doc_vecs[idx]
            sim_q = cosine_sim(query_vec, doc_vec)

            # Similarity terbanyak ke dokumen yang SUDAH terpilih sebelumnya
            if selected:
                sim_selected = max(cosine_sim(doc_vec, doc_vecs[s_idx]) for s_idx in selected)
            else:
                sim_selected = 0.0

            mmr_score = lmbda * sim_q - (1 - lmbda) * sim_selected

            if mmr_score > best_score:
                best_score = mmr_score
                best_idx = idx

        selected.append(best_idx)
        unselected.remove(best_idx)

    return selected

def main():
    print("=== 02. Maximal Marginal Relevance (MMR) Diversity ===")

    # Simulation Embeddings (3D)
    query_vec = np.array([1.0, 1.0, 0.0])

    docs = [
        "Doc 1: Tutorial FastAPI Python bagian 1.",
        "Doc 2: Tutorial FastAPI Python bagian 2 (Sangat mirip dengan Doc 1).",
        "Doc 3: Pengenalan Docker Containerization untuk Web.",
        "Doc 4: Panduan Dasar PostgreSQL Database."
    ]

    doc_vecs = [
        np.array([1.0, 0.9, 0.1]),   # Doc 1 (Sangat mirip query)
        np.array([1.0, 0.88, 0.12]),  # Doc 2 (Hampir identik dengan Doc 1)
        np.array([0.7, 0.7, 0.5]),   # Doc 3 (Cukup mirip & memberikan variasi topik)
        np.array([0.2, 0.3, 0.9])    # Doc 4 (Beda topik)
    ]

    print("Pengujian 1: Standard Retrieval (Tanpa MMR / Lambda = 1.0):")
    idx_standard = maximal_marginal_relevance(query_vec, doc_vecs, lmbda=1.0, top_k=3)
    for i in idx_standard:
        print(f"  - {docs[i]}")

    print("\nPengujian 2: MMR Retrieval dengan Diversity (Lambda = 0.5):")
    idx_mmr = maximal_marginal_relevance(query_vec, doc_vecs, lmbda=0.5, top_k=3)
    for i in idx_mmr:
        print(f"  - {docs[i]}")
    print("  -> Keuntungan MMR: Menghilangkan duplikasi redundant (Doc 2 dieliminasi, diganti Doc 3 yang memperkaya variasi!)")

if __name__ == "__main__":
    main()
