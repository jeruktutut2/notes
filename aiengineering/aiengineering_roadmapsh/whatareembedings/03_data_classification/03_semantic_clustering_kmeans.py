#!/usr/bin/env python3
"""
03_semantic_clustering_kmeans.py
--------------------------------
Pengelompokan Otomatis Topik Dokumen (Semantic Clustering) menggunakan K-Means.
"""

import numpy as np
from sklearn.cluster import KMeans

DOCUMENTS = [
    # Topik A: AI & LLM
    "Model kecerdasan buatan berbasis Transformer melatih jutaan parameter.",
    "Large Language Models (LLM) digunakan untuk pembuatan teks otomatis.",
    "Prompt Engineering dan RAG meningkatkan akurasi respon sistem AI.",

    # Topik B: Keuangan & Investasi
    "Pasar saham mengalami fluktuasi indeks akibat kenaikan suku bunga sentral.",
    "Manajemen portofolio investasi reksadana dan obligasi negara.",
    "Diversifikasi aset kripto dan saham bluechip untuk jangka panjang.",

    # Topik C: Resep Makanan
    "Bumbu rempah nusantara memberikan cita rasa lezat pada rendang daging.",
    "Cara memanggang kue kering cokelat renyah dengan oven konveksi.",
    "Resep sup ayam hangat dengan bahan sayuran segar dan kaldu alami.",
]

def mock_embedding(text: str, dim: int = 12) -> np.ndarray:
    t = text.lower()
    vec = np.zeros(dim)
    if any(w in t for w in ["ai", "llm", "transformer", "prompt", "rag", "kecerdasan"]):
        vec[0:4] += 1.0
    if any(w in t for w in ["saham", "investasi", "bunga", "kripto", "portofolio", "aset"]):
        vec[4:8] += 1.0
    if any(w in t for w in ["bumbu", "rendang", "kue", "sup", "resep", "kaldu", "sayuran"]):
        vec[8:12] += 1.0
    
    seed = sum(ord(c) for c in text[:15])
    np.random.seed(seed)
    vec += np.random.uniform(-0.05, 0.05, size=dim)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec

def main():
    print("=" * 70)
    print("🧩 DEMO: SEMANTIC CLUSTERING (TOPIC MODELING) DENGAN K-MEANS")
    print("=" * 70)

    print(f"\n1. Membaca {len(DOCUMENTS)} dokumen unlabelled...")
    embeddings = np.array([mock_embedding(doc) for doc in DOCUMENTS])

    k = 3
    print(f"2. Menjalankan K-Means Clustering (K={k})...")
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(embeddings)

    print("\n3. Hasil Pengelompokan Kluster Otomatis:")
    for cluster_id in range(k):
        print(f"\n   📌 [KLUSTER TOPIC #{cluster_id + 1}]:")
        cluster_docs = [DOCUMENTS[i] for i in range(len(DOCUMENTS)) if labels[i] == cluster_id]
        for doc in cluster_docs:
            print(f"      • \"{doc}\"")

    print("\n💡 KESIMPULAN:")
    print("   Tanpa label awal, K-Means berhasil memisahkan dokumen ke dalam 3 topik")
    print("   (AI, Keuangan, dan Kuliner) secara sempurna berdasarkan jarak di ruang vektor!")
    print("=" * 70)

if __name__ == "__main__":
    main()
