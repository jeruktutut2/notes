#!/usr/bin/env python3
"""
Modul 01: Purpose and Functionality - Distance Metrics and Payload Filtering
Kalkulasi metrik jarak (Cosine, Dot Product, L2) dan mesin pencarian ber-filter payload metadata.
"""

import numpy as np

def cosine_similarity(v1: np.ndarray, v2: np.ndarray) -> float:
    """Kalkulasi Cosine Similarity: (v1 . v2) / (||v1|| * ||v2||)"""
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return float(np.dot(v1, v2) / (norm1 * norm2))

def dot_product(v1: np.ndarray, v2: np.ndarray) -> float:
    """Kalkulasi Inner Product / Dot Product: sum(v1_i * v2_i)"""
    return float(np.dot(v1, v2))

def euclidean_distance(v1: np.ndarray, v2: np.ndarray) -> float:
    """Kalkulasi Euclidean / L2 Distance: sqrt(sum((v1_i - v2_i)^2))"""
    return float(np.linalg.norm(v1 - v2))

class PayloadVectorEngine:
    """Mesin Vector Database dengan dukungan Filter Metadata Payload"""
    def __init__(self):
        self.records = [] # List of dict: {"id": str, "vector": np.ndarray, "payload": dict}

    def insert(self, record_id: str, vector: np.ndarray, payload: dict):
        self.records.append({
            "id": record_id,
            "vector": np.array(vector, dtype=np.float32),
            "payload": payload
        })

    def query(self, query_vector: np.ndarray, top_k: int = 3, metric: str = "cosine", filter_dict: dict = None):
        filtered_records = []
        for r in self.records:
            # Metadata filtering check
            match = True
            if filter_dict:
                for k, v in filter_dict.items():
                    if r["payload"].get(k) != v:
                        match = False
                        break
            if match:
                filtered_records.append(r)

        if not filtered_records:
            return []

        scored_results = []
        for r in filtered_records:
            v = r["vector"]
            if metric == "cosine":
                score = cosine_similarity(query_vector, v)
            elif metric == "dot":
                score = dot_product(query_vector, v)
            elif metric == "l2":
                score = -euclidean_distance(query_vector, v) # Negatif agar L2 terkecil menjadi skor tertinggi
            else:
                raise ValueError(f"Metrik tidak dikenal: {metric}")
            
            scored_results.append({
                "id": r["id"],
                "score": score,
                "payload": r["payload"]
            })

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]

def main():
    print("=========================================================")
    print("  02: DISTANCE METRICS & METADATA PAYLOAD FILTERING")
    print("=========================================================\n")

    # 1. Demonstrasi Metrik Jarak
    v1 = np.array([0.5, 0.8, 0.1, 0.3])
    v2 = np.array([0.4, 0.9, 0.0, 0.2])
    v3 = np.array([-0.5, -0.7, 0.8, 0.9])

    print("--- [1] KALKULASI METRIK JARAK VEKTOR ---")
    print(f"Vektor 1: {v1}")
    print(f"Vektor 2 (Mirip v1): {v2}")
    print(f"Vektor 3 (Beda v1) : {v3}\n")

    print(f"• Cosine Sim (v1, v2): {cosine_similarity(v1, v2):.4f}  |  (v1, v3): {cosine_similarity(v1, v3):.4f}")
    print(f"• Dot Product (v1, v2): {dot_product(v1, v2):.4f}  |  (v1, v3): {dot_product(v1, v3):.4f}")
    print(f"• L2 Distance (v1, v2): {euclidean_distance(v1, v2):.4f}  |  (v1, v3): {euclidean_distance(v1, v3):.4f}\n")

    # 2. Demonstrasi Engine Vector Search Ber-filter Payload
    print("--- [2] VECTOR QUERY DENGAN FILTER METADATA PAYLOAD ---")
    engine = PayloadVectorEngine()
    
    engine.insert("doc_1", np.array([0.9, 0.1, 0.0, 0.2]), {"title": "Paper Deep Learning", "category": "AI", "year": 2024})
    engine.insert("doc_2", np.array([0.8, 0.2, 0.1, 0.1]), {"title": "Tutorial Flask Web", "category": "Web", "year": 2024})
    engine.insert("doc_3", np.array([0.85, 0.15, 0.05, 0.15]), {"title": "Paper RAG Systems", "category": "AI", "year": 2023})

    query_v = np.array([0.88, 0.12, 0.02, 0.18])

    print("Pencarian Tanpa Filter (Top-2 Cosine):")
    res_no_filter = engine.query(query_v, top_k=2, metric="cosine")
    for r in res_no_filter:
        print(f"  • [{r['id']}] Skor: {r['score']:.4f} | {r['payload']['title']} ({r['payload']['category']}, {r['payload']['year']})")

    print("\nPencarian Dengan Filter ({'category': 'AI', 'year': 2024}):")
    res_filtered = engine.query(query_v, top_k=2, metric="cosine", filter_dict={"category": "AI", "year": 2024})
    for r in res_filtered:
        print(f"  • [{r['id']}] Skor: {r['score']:.4f} | {r['payload']['title']} ({r['payload']['category']}, {r['payload']['year']})")

if __name__ == "__main__":
    main()
