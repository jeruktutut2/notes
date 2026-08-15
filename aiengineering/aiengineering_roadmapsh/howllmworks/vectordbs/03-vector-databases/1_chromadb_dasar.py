"""
=================================================================
1. CHROMADB — Vector Database Paling Mudah untuk Belajar
=================================================================
ChromaDB adalah vector database open-source yang berjalan secara
embedded (lokal, tanpa server). Sangat cocok untuk belajar dan
prototyping.

Fitur Utama:
- Otomatis menghasilkan embedding (built-in embedding function)
- Mendukung metadata filtering
- Persistent storage (data tersimpan di disk)
- API yang sangat sederhana

Operasi Dasar:
  1. Buat Collection (= tabel)
  2. Add dokumen (otomatis di-embed)
  3. Query (similarity search)
  4. Update & Delete
=================================================================
"""

import chromadb


def demo_chromadb_dasar():
    """Demo: operasi dasar ChromaDB."""
    print("=" * 60)
    print("DEMO 1: ChromaDB — Operasi Dasar")
    print("=" * 60)

    # 1. Buat client (in-memory untuk demo)
    print("\n📦 Membuat ChromaDB client (in-memory)...")
    client = chromadb.Client()
    print("✅ Client berhasil dibuat!")

    # 2. Buat collection
    print("\n📁 Membuat collection 'dokumen_belajar'...")
    collection = client.create_collection(
        name="dokumen_belajar",
        metadata={"hnsw:space": "cosine"}  # gunakan cosine similarity
    )
    print(f"✅ Collection '{collection.name}' berhasil dibuat!")

    # 3. Tambahkan dokumen (otomatis di-embed oleh ChromaDB)
    print("\n📝 Menambahkan dokumen...")
    collection.add(
        documents=[
            "Python adalah bahasa pemrograman populer untuk data science dan AI",
            "Machine learning menggunakan algoritma untuk belajar dari data",
            "Deep learning adalah subset dari machine learning menggunakan neural network",
            "Kucing dan anjing adalah hewan peliharaan yang populer di Indonesia",
            "Nasi goreng adalah makanan khas Indonesia yang sangat lezat",
            "JavaScript digunakan untuk membuat website interaktif",
            "TensorFlow dan PyTorch adalah framework populer untuk deep learning",
            "Ikan hias bisa dipelihara di akuarium rumah",
        ],
        metadatas=[
            {"kategori": "programming", "level": "beginner"},
            {"kategori": "ai", "level": "beginner"},
            {"kategori": "ai", "level": "intermediate"},
            {"kategori": "hewan", "level": "beginner"},
            {"kategori": "makanan", "level": "beginner"},
            {"kategori": "programming", "level": "beginner"},
            {"kategori": "ai", "level": "intermediate"},
            {"kategori": "hewan", "level": "beginner"},
        ],
        ids=["doc1", "doc2", "doc3", "doc4", "doc5", "doc6", "doc7", "doc8"]
    )
    print(f"✅ {collection.count()} dokumen berhasil ditambahkan!")

    # 4. Query (similarity search)
    print(f"\n🔍 Query: \"bagaimana cara belajar artificial intelligence?\"")
    print("-" * 60)
    results = collection.query(
        query_texts=["bagaimana cara belajar artificial intelligence?"],
        n_results=3
    )

    print("   Top-3 hasil:")
    for i, (doc, dist) in enumerate(
        zip(results["documents"][0], results["distances"][0]), 1
    ):
        similarity = 1 - dist  # ChromaDB returns distance, convert to similarity
        print(f"   {i}. [{similarity:.4f}] {doc}")

    # 5. Query lain
    print(f"\n🔍 Query: \"hewan peliharaan di rumah\"")
    print("-" * 60)
    results2 = collection.query(
        query_texts=["hewan peliharaan di rumah"],
        n_results=3
    )

    print("   Top-3 hasil:")
    for i, (doc, dist) in enumerate(
        zip(results2["documents"][0], results2["distances"][0]), 1
    ):
        similarity = 1 - dist
        print(f"   {i}. [{similarity:.4f}] {doc}")

    print("\n💡 Kesimpulan:")
    print("   - ChromaDB otomatis membuat embedding dari teks")
    print("   - Query mengembalikan dokumen yang paling mirip secara semantik")
    print("   - Tidak perlu setup server atau konfigurasi rumit!")

    return client, collection


def demo_metadata_filtering(client, collection):
    """Demo: filtering query berdasarkan metadata."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Metadata Filtering")
    print("=" * 60)

    # Query TANPA filter
    print(f"\n🔍 Query: \"teknologi terbaru\" (TANPA filter)")
    print("-" * 60)
    results = collection.query(
        query_texts=["teknologi terbaru"],
        n_results=5
    )
    print("   Hasil:")
    for i, (doc, meta, dist) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), 1
    ):
        sim = 1 - dist
        print(f"   {i}. [{sim:.4f}] [{meta['kategori']}] {doc[:60]}")

    # Query DENGAN filter kategori
    print(f"\n🔍 Query: \"teknologi terbaru\" (FILTER: kategori=ai)")
    print("-" * 60)
    results_filtered = collection.query(
        query_texts=["teknologi terbaru"],
        n_results=5,
        where={"kategori": "ai"}
    )
    print("   Hasil (hanya kategori AI):")
    for i, (doc, meta, dist) in enumerate(
        zip(
            results_filtered["documents"][0],
            results_filtered["metadatas"][0],
            results_filtered["distances"][0]
        ), 1
    ):
        sim = 1 - dist
        print(f"   {i}. [{sim:.4f}] [{meta['kategori']}] {doc[:60]}")

    # Query dengan filter kombinasi
    print(f"\n🔍 Query: \"belajar\" (FILTER: kategori=ai AND level=beginner)")
    print("-" * 60)
    results_combo = collection.query(
        query_texts=["belajar"],
        n_results=5,
        where={
            "$and": [
                {"kategori": "ai"},
                {"level": "beginner"}
            ]
        }
    )
    print("   Hasil (AI + Beginner):")
    for i, (doc, meta, dist) in enumerate(
        zip(
            results_combo["documents"][0],
            results_combo["metadatas"][0],
            results_combo["distances"][0]
        ), 1
    ):
        sim = 1 - dist
        print(f"   {i}. [{sim:.4f}] [{meta['kategori']}/{meta['level']}] {doc[:55]}")

    print("\n💡 Kesimpulan:")
    print("   - Metadata filtering mempersempit hasil pencarian")
    print("   - Bisa menggunakan $and, $or untuk kondisi kompleks")
    print("   - Sangat berguna untuk multi-tenant atau multi-category data")


def demo_crud_operations(client):
    """Demo: operasi CRUD (Create, Read, Update, Delete)."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: CRUD Operations")
    print("=" * 60)

    # Buat collection baru
    coll = client.create_collection(name="crud_demo")

    # CREATE
    print("\n📝 CREATE — Menambahkan 3 dokumen...")
    coll.add(
        documents=[
            "Python versi 3.11 sudah dirilis",
            "Java masih banyak digunakan di enterprise",
            "Rust adalah bahasa yang aman dan cepat",
        ],
        metadatas=[
            {"lang": "python", "year": 2023},
            {"lang": "java", "year": 2023},
            {"lang": "rust", "year": 2023},
        ],
        ids=["py1", "java1", "rust1"]
    )
    print(f"   ✅ Total dokumen: {coll.count()}")

    # READ
    print("\n📖 READ — Mengambil dokumen by ID...")
    doc = coll.get(ids=["py1"])
    print(f"   ID: {doc['ids'][0]}")
    print(f"   Dokumen: {doc['documents'][0]}")
    print(f"   Metadata: {doc['metadatas'][0]}")

    # UPDATE
    print("\n✏️ UPDATE — Mengupdate dokumen 'py1'...")
    coll.update(
        ids=["py1"],
        documents=["Python versi 3.12 adalah versi terbaru dengan fitur baru"],
        metadatas=[{"lang": "python", "year": 2024, "updated": True}]
    )
    doc_updated = coll.get(ids=["py1"])
    print(f"   Sebelum: 'Python versi 3.11 sudah dirilis'")
    print(f"   Sesudah: '{doc_updated['documents'][0]}'")
    print(f"   Metadata: {doc_updated['metadatas'][0]}")

    # DELETE
    print("\n🗑️ DELETE — Menghapus dokumen 'rust1'...")
    print(f"   Sebelum delete: {coll.count()} dokumen")
    coll.delete(ids=["rust1"])
    print(f"   Sesudah delete: {coll.count()} dokumen")

    # Verifikasi
    remaining = coll.get()
    print(f"\n   Dokumen tersisa:")
    for doc_id, doc_text in zip(remaining["ids"], remaining["documents"]):
        print(f"   - [{doc_id}] {doc_text}")

    print("\n💡 Kesimpulan:")
    print("   - ChromaDB mendukung operasi CRUD lengkap")
    print("   - add() untuk insert, get() untuk read, update() untuk edit, delete() untuk hapus")
    print("   - Semua operasi otomatis memperbarui embedding")


def main():
    client, collection = demo_chromadb_dasar()
    demo_metadata_filtering(client, collection)
    demo_crud_operations(client)
    print("\n\n✅ Selesai! Lanjut ke: 2_chromadb_persistent.py")


if __name__ == "__main__":
    main()
