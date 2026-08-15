"""
=================================================================
2. CHROMADB PERSISTENT — Menyimpan Data ke Disk
=================================================================
Pada demo sebelumnya, data hanya disimpan di memori (hilang saat 
program selesai). Demo ini menunjukkan cara menyimpan data secara 
persistent ke disk, sehingga data tetap ada saat program 
dijalankan ulang.
=================================================================
"""

import chromadb
import os
import shutil


def demo_persistent_storage():
    """Demo: ChromaDB dengan persistent storage."""
    print("=" * 60)
    print("DEMO: ChromaDB Persistent Storage")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "chroma_data")

    # Bersihkan data lama jika ada (untuk demo)
    if os.path.exists(db_path):
        shutil.rmtree(db_path)

    # ===== FASE 1: Simpan Data =====
    print(f"\n📁 FASE 1: Menyimpan data ke disk ({db_path})")
    print("-" * 60)

    client = chromadb.PersistentClient(path=db_path)
    collection = client.create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )

    dokumen = [
        "Python digunakan untuk machine learning dan data science",
        "JavaScript populer untuk pengembangan web frontend dan backend",
        "Docker memudahkan deployment aplikasi menggunakan container",
        "Kubernetes mengatur orkestrasi container dalam skala besar",
        "PostgreSQL adalah database relasional yang powerful",
        "Redis digunakan sebagai cache dan message broker",
        "Git adalah version control system yang wajib dikuasai developer",
        "Linux adalah sistem operasi yang banyak digunakan di server",
    ]

    metadatas = [
        {"topik": "programming", "tipe": "bahasa"},
        {"topik": "programming", "tipe": "bahasa"},
        {"topik": "devops", "tipe": "tools"},
        {"topik": "devops", "tipe": "tools"},
        {"topik": "database", "tipe": "tools"},
        {"topik": "database", "tipe": "tools"},
        {"topik": "devops", "tipe": "tools"},
        {"topik": "devops", "tipe": "os"},
    ]

    ids = [f"doc_{i}" for i in range(len(dokumen))]

    collection.add(documents=dokumen, metadatas=metadatas, ids=ids)
    print(f"   ✅ {collection.count()} dokumen disimpan ke disk")

    # Cek ukuran folder
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(db_path):
        for f in filenames:
            total_size += os.path.getsize(os.path.join(dirpath, f))
    print(f"   📦 Ukuran data di disk: {total_size / 1024:.1f} KB")

    # ===== FASE 2: Load Ulang Data =====
    print(f"\n📁 FASE 2: Memuat ulang data dari disk")
    print("-" * 60)

    # Simulasi: buat client baru (seolah program baru)
    client2 = chromadb.PersistentClient(path=db_path)
    collection2 = client2.get_collection("knowledge_base")

    print(f"   ✅ Collection '{collection2.name}' dimuat dari disk")
    print(f"   📊 Jumlah dokumen: {collection2.count()}")

    # Query dari data yang di-load
    query = "cara deploy aplikasi"
    print(f"\n🔍 Query: \"{query}\"")
    results = collection2.query(query_texts=[query], n_results=3)

    print("   Top-3 hasil:")
    for i, (doc, meta, dist) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), 1
    ):
        sim = 1 - dist
        print(f"   {i}. [{sim:.4f}] [{meta['topik']}] {doc}")

    # ===== FASE 3: Tambah Data Baru =====
    print(f"\n📁 FASE 3: Menambah data baru ke collection yang sudah ada")
    print("-" * 60)

    collection2.add(
        documents=[
            "FastAPI adalah framework Python untuk membuat REST API yang cepat",
            "Nginx sering digunakan sebagai reverse proxy dan web server",
        ],
        metadatas=[
            {"topik": "programming", "tipe": "framework"},
            {"topik": "devops", "tipe": "tools"},
        ],
        ids=["doc_8", "doc_9"]
    )
    print(f"   ✅ Total dokumen sekarang: {collection2.count()}")

    # Query lagi
    query2 = "cara membuat API"
    print(f"\n🔍 Query: \"{query2}\"")
    results2 = collection2.query(query_texts=[query2], n_results=3)

    print("   Top-3 hasil:")
    for i, (doc, dist) in enumerate(
        zip(results2["documents"][0], results2["distances"][0]), 1
    ):
        sim = 1 - dist
        print(f"   {i}. [{sim:.4f}] {doc}")

    # Cleanup
    print(f"\n🧹 Membersihkan data demo...")
    shutil.rmtree(db_path)
    print("   ✅ Data demo dihapus")

    print("\n💡 Kesimpulan:")
    print("   - PersistentClient menyimpan data ke disk secara otomatis")
    print("   - Data tetap ada meskipun program dijalankan ulang")
    print("   - Bisa menambah data baru ke collection yang sudah ada")
    print("   - Cocok untuk aplikasi yang butuh data bertahan lama")


def main():
    demo_persistent_storage()
    print("\n\n✅ Selesai! Lanjut ke modul berikutnya: 04_chunking/")


if __name__ == "__main__":
    main()
