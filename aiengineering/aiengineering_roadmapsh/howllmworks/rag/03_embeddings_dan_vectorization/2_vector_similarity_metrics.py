import numpy as np

def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Mengukur Cosine Similarity: cos(theta) = (A . B) / (||A|| * ||B||)"""
    dot_prod = np.dot(vec1, vec2)
    norm_a = np.linalg.norm(vec1)
    norm_b = np.linalg.norm(vec2)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(dot_prod / (norm_a * norm_b))

def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Mengukur Dot Product: sum(A_i * B_i)"""
    return float(np.dot(vec1, vec2))

def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """Mengukur Euclidean Distance (L2): sqrt(sum((A_i - B_i)^2))"""
    return float(np.linalg.norm(vec1 - vec2))

def main():
    print("=== 02. Vector Similarity Metrics ===")

    # Contoh 3 Vektor 3D sederhana
    v_query = np.array([1.0, 2.0, 0.5])
    v_doc1  = np.array([1.1, 1.9, 0.6]) # Sangat mirip dengan query
    v_doc2  = np.array([-1.0, -2.0, 0.0]) # Arah berlawanan

    print(f"Vector Query: {v_query}")
    print(f"Vector Doc 1: {v_doc1}")
    print(f"Vector Doc 2: {v_doc2}\n")

    print("[ Hasil Perhitungan Metrik untuk Query vs Doc 1 ]")
    print(f"  - Cosine Similarity: {cosine_similarity(v_query, v_doc1):.4f} (Rentang -1 s/d 1, mendekati 1 = makin mirip)")
    print(f"  - Dot Product       : {dot_product(v_query, v_doc1):.4f}")
    print(f"  - Euclidean Distance: {euclidean_distance(v_query, v_doc1):.4f} (Mendekati 0 = makin dekat/mirip)\n")

    print("[ Hasil Perhitungan Metrik untuk Query vs Doc 2 ]")
    print(f"  - Cosine Similarity: {cosine_similarity(v_query, v_doc2):.4f}")
    print(f"  - Dot Product       : {dot_product(v_query, v_doc2):.4f}")
    print(f"  - Euclidean Distance: {euclidean_distance(v_query, v_doc2):.4f}")

if __name__ == "__main__":
    main()
