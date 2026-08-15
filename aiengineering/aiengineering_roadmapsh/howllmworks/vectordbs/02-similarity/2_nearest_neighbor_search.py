"""
=================================================================
2. NEAREST NEIGHBOR SEARCH
=================================================================
Nearest Neighbor Search adalah proses menemukan vektor yang paling 
dekat (mirip) dengan vektor query dari sekumpulan vektor.

Dua jenis utama:
1. Exact (Brute Force) — akurat 100%, lambat untuk data besar
2. Approximate (ANN)   — ~95-99% akurat, jauh lebih cepat

Algoritma ANN Populer:
┌──────────┬──────────────┬────────────┬───────────────────┐
│ Algoritma│ Kecepatan    │ Akurasi    │ Memori            │
├──────────┼──────────────┼────────────┼───────────────────┤
│ Flat     │ ⭐            │ ⭐⭐⭐⭐⭐     │ Tinggi            │
│ IVF      │ ⭐⭐⭐          │ ⭐⭐⭐⭐      │ Sedang            │
│ HNSW     │ ⭐⭐⭐⭐⭐       │ ⭐⭐⭐⭐⭐     │ Tinggi (graph)    │
│ PQ       │ ⭐⭐⭐⭐        │ ⭐⭐⭐        │ Sangat rendah     │
└──────────┴──────────────┴────────────┴───────────────────┘
=================================================================
"""

import numpy as np
import time


def demo_brute_force_search():
    """Demo: exact nearest neighbor search (brute force)."""
    print("=" * 60)
    print("DEMO 1: Brute Force Search (Exact)")
    print("=" * 60)

    # Simulasi database vektor
    np.random.seed(42)
    n_vectors = 10000
    n_dims = 128
    database = np.random.rand(n_vectors, n_dims).astype('float32')

    # Normalisasi agar bisa pakai cosine similarity via dot product
    norms = np.linalg.norm(database, axis=1, keepdims=True)
    database = database / norms

    # Query
    query = np.random.rand(1, n_dims).astype('float32')
    query = query / np.linalg.norm(query)

    print(f"\n📊 Database: {n_vectors} vektor, {n_dims} dimensi")
    print(f"📝 Query: 1 vektor, {n_dims} dimensi")

    # Brute force: hitung similarity dengan SEMUA vektor
    print(f"\n⚡ Menjalankan brute force search...")
    start = time.time()

    similarities = np.dot(database, query.T).flatten()
    top_k = 5
    top_indices = np.argsort(similarities)[-top_k:][::-1]

    elapsed = (time.time() - start) * 1000

    print(f"   ⏱️ Waktu: {elapsed:.2f} ms")
    print(f"\n📊 Top-{top_k} Nearest Neighbors:")
    print("-" * 40)
    for rank, idx in enumerate(top_indices, 1):
        print(f"   {rank}. Index: {idx:>5}, Similarity: {similarities[idx]:.4f}")

    print(f"\n💡 Catatan:")
    print(f"   - Brute force membandingkan query dengan SEMUA {n_vectors} vektor")
    print(f"   - Akurasi 100% (exact), tapi lambat untuk jutaan vektor")


def demo_ivf_simulation():
    """Demo: simulasi IVF (Inverted File Index) search."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Simulasi IVF Search (Approximate)")
    print("=" * 60)

    np.random.seed(42)
    n_vectors = 10000
    n_dims = 128
    n_clusters = 10

    # Buat database
    database = np.random.rand(n_vectors, n_dims).astype('float32')
    norms = np.linalg.norm(database, axis=1, keepdims=True)
    database = database / norms

    # Simulasi clustering (assign vektor ke cluster terdekat)
    # Dalam FAISS asli, ini dilakukan dengan K-Means
    centroids = np.random.rand(n_clusters, n_dims).astype('float32')
    centroids = centroids / np.linalg.norm(centroids, axis=1, keepdims=True)

    # Assign setiap vektor ke cluster terdekat
    assignments = np.argmax(np.dot(database, centroids.T), axis=1)

    # Buat inverted index
    clusters = {}
    for i, cluster_id in enumerate(assignments):
        if cluster_id not in clusters:
            clusters[cluster_id] = []
        clusters[cluster_id].append(i)

    print(f"\n📊 Database: {n_vectors} vektor, {n_clusters} cluster")
    print(f"   Distribusi per cluster:")
    for cid in sorted(clusters.keys()):
        print(f"   Cluster {cid}: {len(clusters[cid]):>5} vektor")

    # Query
    query = np.random.rand(1, n_dims).astype('float32')
    query = query / np.linalg.norm(query)

    # --- Brute force (untuk perbandingan) ---
    start = time.time()
    bf_similarities = np.dot(database, query.T).flatten()
    bf_top5 = set(np.argsort(bf_similarities)[-5:][::-1])
    bf_time = (time.time() - start) * 1000

    # --- IVF Search ---
    nprobe_values = [1, 3, 5, n_clusters]
    
    print(f"\n📊 Perbandingan nprobe (jumlah cluster yang dicek):")
    print("-" * 65)
    print(f"   {'nprobe':>6} {'Vektor Dicek':>14} {'Waktu (ms)':>12} {'Recall':>8}")
    print("-" * 65)

    for nprobe in nprobe_values:
        start = time.time()

        # Tentukan cluster terdekat untuk query
        query_to_centroid = np.dot(centroids, query.T).flatten()
        nearest_clusters = np.argsort(query_to_centroid)[-nprobe:]

        # Cek hanya vektor di cluster-cluster tersebut
        candidate_indices = []
        for cid in nearest_clusters:
            candidate_indices.extend(clusters[cid])

        candidates = database[candidate_indices]
        sims = np.dot(candidates, query.T).flatten()
        local_top5 = np.argsort(sims)[-5:][::-1]
        ivf_top5 = set(candidate_indices[i] for i in local_top5)

        elapsed = (time.time() - start) * 1000

        # Recall: berapa dari exact top-5 yang ditemukan?
        recall = len(bf_top5 & ivf_top5) / len(bf_top5)
        label = "(= brute force)" if nprobe == n_clusters else ""

        print(f"   {nprobe:>6} {len(candidate_indices):>14} {elapsed:>12.2f} {recall:>8.0%} {label}")

    print(f"\n   Brute force: {n_vectors} vektor, {bf_time:.2f} ms")

    print(f"\n💡 Kesimpulan:")
    print(f"   - nprobe rendah → cepat tapi recall rendah (bisa miss hasil)")
    print(f"   - nprobe tinggi → lambat tapi recall tinggi (lebih akurat)")
    print(f"   - Trade-off antara kecepatan dan akurasi!")


def demo_faiss_indexes():
    """Demo: menggunakan FAISS untuk berbagai jenis index."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: FAISS - Berbagai Jenis Index")
    print("=" * 60)

    try:
        import faiss
    except ImportError:
        print("\n⚠️ FAISS tidak terinstall. Install dengan:")
        print("   pip install faiss-cpu")
        print("\nMenampilkan penjelasan tanpa eksekusi...\n")
        print("Index yang tersedia di FAISS:")
        print("   1. IndexFlatL2     — Brute force, L2 distance")
        print("   2. IndexFlatIP     — Brute force, Inner Product (cosine)")
        print("   3. IndexIVFFlat    — IVF clustering + brute force per cluster")
        print("   4. IndexHNSWFlat   — Graph-based (HNSW), sangat cepat")
        print("   5. IndexIVFPQ      — IVF + Product Quantization (hemat memori)")
        return

    np.random.seed(42)
    n_vectors = 50000
    n_dims = 128
    data = np.random.rand(n_vectors, n_dims).astype('float32')
    query = np.random.rand(5, n_dims).astype('float32')
    k = 5

    print(f"\n📊 Database: {n_vectors} vektor, {n_dims} dimensi")
    print(f"📝 Query: 5 vektor")
    print(f"🔍 Top-{k}\n")

    results = {}

    # 1. Flat (Brute Force)
    print("   🔨 Building IndexFlatL2...")
    start = time.time()
    index_flat = faiss.IndexFlatL2(n_dims)
    index_flat.add(data)
    build_time = (time.time() - start) * 1000

    start = time.time()
    D_flat, I_flat = index_flat.search(query, k)
    search_time = (time.time() - start) * 1000
    results["Flat (Exact)"] = {
        "build": build_time, "search": search_time,
        "indices": I_flat, "recall": 1.0
    }
    print(f"      Build: {build_time:.1f}ms, Search: {search_time:.2f}ms")

    # 2. IVF
    print("   🔨 Building IndexIVFFlat...")
    nlist = 100
    start = time.time()
    quantizer = faiss.IndexFlatL2(n_dims)
    index_ivf = faiss.IndexIVFFlat(quantizer, n_dims, nlist)
    index_ivf.train(data)
    index_ivf.add(data)
    build_time = (time.time() - start) * 1000

    index_ivf.nprobe = 10
    start = time.time()
    D_ivf, I_ivf = index_ivf.search(query, k)
    search_time = (time.time() - start) * 1000

    # Hitung recall
    recall = sum(
        len(set(I_flat[i]) & set(I_ivf[i])) / k
        for i in range(len(query))
    ) / len(query)
    results["IVF (nprobe=10)"] = {
        "build": build_time, "search": search_time, "recall": recall
    }
    print(f"      Build: {build_time:.1f}ms, Search: {search_time:.2f}ms, Recall: {recall:.1%}")

    # 3. HNSW
    print("   🔨 Building IndexHNSWFlat...")
    start = time.time()
    index_hnsw = faiss.IndexHNSWFlat(n_dims, 32)
    index_hnsw.hnsw.efConstruction = 200
    index_hnsw.add(data)
    build_time = (time.time() - start) * 1000

    index_hnsw.hnsw.efSearch = 64
    start = time.time()
    D_hnsw, I_hnsw = index_hnsw.search(query, k)
    search_time = (time.time() - start) * 1000

    recall = sum(
        len(set(I_flat[i]) & set(I_hnsw[i])) / k
        for i in range(len(query))
    ) / len(query)
    results["HNSW (M=32)"] = {
        "build": build_time, "search": search_time, "recall": recall
    }
    print(f"      Build: {build_time:.1f}ms, Search: {search_time:.2f}ms, Recall: {recall:.1%}")

    # Rangkuman
    print(f"\n📊 Rangkuman:")
    print("-" * 60)
    print(f"   {'Index':<20} {'Build (ms)':>12} {'Search (ms)':>13} {'Recall':>8}")
    print("-" * 60)
    for name, r in results.items():
        print(f"   {name:<20} {r['build']:>12.1f} {r['search']:>13.2f} {r['recall']:>8.1%}")

    print(f"\n💡 Kesimpulan:")
    print("   - Flat: akurat tapi lambat → cocok untuk dataset kecil")
    print("   - IVF: balance → cocok untuk dataset menengah")
    print("   - HNSW: cepat & akurat → pilihan terbaik untuk produksi")


def main():
    demo_brute_force_search()
    demo_ivf_simulation()
    demo_faiss_indexes()
    print("\n\n✅ Selesai! Lanjut ke modul berikutnya: 03_vector_databases/")


if __name__ == "__main__":
    main()
