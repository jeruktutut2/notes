import numpy as np

def l2_normalize(vector: np.ndarray) -> np.ndarray:
    """Mengubah magnitudo vektor menjadi 1 (L2 normalization)."""
    norm = np.linalg.norm(vector)
    if norm == 0:
        return vector
    return vector / norm

def main():
    print("=== 03. Embedding Normalization & Dimensions ===")

    # Vektor tak ternormalisasi
    raw_vec1 = np.array([3.0, 4.0, 0.0]) # Norm L2 = 5
    raw_vec2 = np.array([6.0, 8.0, 0.0]) # Norm L2 = 10 (Arah sama persis dengan vec1, hanya beda skala)

    print("1. Efek Normalisasi L2:")
    print(f"  Raw Vector 1: {raw_vec1}, Norm L2: {np.linalg.norm(raw_vec1)}")
    print(f"  Raw Vector 2: {raw_vec2}, Norm L2: {np.linalg.norm(raw_vec2)}")

    norm_vec1 = l2_normalize(raw_vec1)
    norm_vec2 = l2_normalize(raw_vec2)

    print(f"  Normalized Vector 1: {norm_vec1}, Norm L2: {np.linalg.norm(norm_vec1):.1f}")
    print(f"  Normalized Vector 2: {norm_vec2}, Norm L2: {np.linalg.norm(norm_vec2):.1f}")

    # Bukti Dot Product Vektor Ternormalisasi = Cosine Similarity
    dot_prod_normalized = np.dot(norm_vec1, norm_vec2)
    print(f"  Dot Product dari Vektor Ternormalisasi: {dot_prod_normalized:.4f}")
    print("  -> Keuntungan: Dot product dari vektor ternormalisasi dapat dihitung jauh lebih cepat tanpa pembagian berulang!")

    # 2. Dimensi Embedding
    print("\n2. Perbandingan Dimensi Embedding Model:")
    dimensions = {
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "bge-small-en-v1.5": 384,
        "all-MiniLM-L6-v2": 384
    }
    for model_name, dim in dimensions.items():
        print(f"  - {model_name:<25}: {dim} dimensi (RAM approx per 1M vectors: {(dim * 4 * 1e6) / (1024**2):.1f} MB)")

if __name__ == "__main__":
    main()
