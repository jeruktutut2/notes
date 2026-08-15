#!/usr/bin/env python3
"""
Modul 02: Popular Vector DBs - FAISS Hands-On
In-Memory Fast Vector Search Library oleh Meta AI (IndexFlatL2, IndexIVFFlat, IndexHNSWFlat).
"""

import time
import numpy as np

def main():
    print("=========================================================")
    print("  03: FAISS HANDS-ON (IN-MEMORY HIGH PERFORMANCE SEARCH)")
    print("=========================================================\n")

    d = 64          # Dimensi vektor
    nb = 10000      # 10,000 Vektor di database
    nq = 1          # 1 Query Vector

    np.random.seed(42)
    xb = np.random.random((nb, d)).astype('float32')
    xq = np.random.random((nq, d)).astype('float32')

    try:
        import faiss
        print("⚡ Library 'faiss' terdeteksi! Menguji 3 Jenis Indeks FAISS...\n")

        # 1. IndexFlatL2 (Brute Force Exact Search)
        print("--- [1] FAISS IndexFlatL2 (Exact Match L2 Distance) ---")
        index_flat = faiss.IndexFlatL2(d)
        index_flat.add(xb)
        start = time.perf_counter()
        D_flat, I_flat = index_flat.search(xq, k=5)
        t_flat = (time.perf_counter() - start) * 1000
        print(f"Waktu Pencarian: {t_flat:.4f} ms")
        print(f"Top-5 Neighbor IDs: {I_flat[0]}")
        print(f"Distances L2        : {D_flat[0]}\n")

        # 2. IndexIVFFlat (Inverted File Index / Clustering ANN)
        print("--- [2] FAISS IndexIVFFlat (Voronoi Quantization ANN) ---")
        nlist = 50 # 50 Kluster Voronoi
        quantizer = faiss.IndexFlatL2(d)
        index_ivf = faiss.IndexIVFFlat(quantizer, d, nlist, faiss.METRIC_L2)
        index_ivf.train(xb) # Training centroids
        index_ivf.add(xb)
        index_ivf.nprobe = 10 # Cek 10 kluster terdekat
        start = time.perf_counter()
        D_ivf, I_ivf = index_ivf.search(xq, k=5)
        t_ivf = (time.perf_counter() - start) * 1000
        print(f"Waktu Pencarian: {t_ivf:.4f} ms")
        print(f"Top-5 Neighbor IDs: {I_ivf[0]}")
        print(f"Distances L2        : {D_ivf[0]}\n")

        # 3. IndexHNSWFlat (Hierarchical Small World Graph ANN)
        print("--- [3] FAISS IndexHNSWFlat (Graph-based ANN) ---")
        M = 16
        index_hnsw = faiss.IndexHNSWFlat(d, M)
        index_hnsw.add(xb)
        start = time.perf_counter()
        D_hnsw, I_hnsw = index_hnsw.search(xq, k=5)
        t_hnsw = (time.perf_counter() - start) * 1000
        print(f"Waktu Pencarian: {t_hnsw:.4f} ms")
        print(f"Top-5 Neighbor IDs: {I_hnsw[0]}")
        print(f"Distances L2        : {D_hnsw[0]}")

    except ImportError:
        print("ℹ️  Package 'faiss-cpu' belum ter-install. Menjalankan Simulasi FAISS Pure NumPy Engine.\n")
        print("Simulasi Benchmark 10,000 Vektor (64 Dimensions):")
        
        # NumPy Exact Flat Search
        start = time.perf_counter()
        diffs = xb - xq[0]
        dists = np.sum(diffs ** 2, axis=1)
        top5_idx = np.argsort(dists)[:5]
        t_numpy = (time.perf_counter() - start) * 1000
        
        print(f"  • Flat Exact L2 Scan Time: {t_numpy:.4f} ms")
        print(f"  • Top-5 IDs: {top5_idx}")
        print(f"  • Distances: {dists[top5_idx]}")

    print("\n✅ Hands-on FAISS Selesai! FAISS memberikan kontrol tingkat rendah pada algoritma indeks & GPU acceleration.")

if __name__ == "__main__":
    main()
