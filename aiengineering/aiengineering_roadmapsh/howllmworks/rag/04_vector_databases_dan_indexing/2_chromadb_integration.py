def main():
    print("=== 02. Integrasi ChromaDB Vector Database ===")

    try:
        import chromadb

        # Inisialisasi ChromaDB client in-memory
        client = chromadb.Client()
        collection = client.get_or_create_collection(name="rag_learning_collection")

        print("[OK] ChromaDB Client & Collection berhasil dibuat.")

        # Tambahkan dokumen
        docs = [
            "Retrieval-Augmented Generation meningkatkan akurasi LLM.",
            "Chunking dokumen membantu pencarian vektor yang lebih presisi.",
            "Embedding model memetakan kata ke ruang vektor kontinu.",
            "Sayur lodeh adalah makanan tradisional Indonesia."
        ]
        ids = ["doc1", "doc2", "doc3", "doc4"]
        metadatas = [
            {"topic": "rag"},
            {"topic": "rag"},
            {"topic": "embeddings"},
            {"topic": "kuliner"}
        ]

        collection.add(
            documents=docs,
            metadatas=metadatas,
            ids=ids
        )

        print(f"[OK] Memasukkan {len(docs)} dokumen ke ChromaDB Collection.\n")

        # Perform Query
        query_text = "Apa itu RAG dan chunking dokumen?"
        results = collection.query(
            query_texts=[query_text],
            n_results=2
        )

        print(f"Query: '{query_text}'")
        print("\nHasil Pencarian Top-2 ChromaDB:")
        for i in range(len(results["ids"][0])):
            doc_id = results["ids"][0][i]
            document = results["documents"][0][i]
            dist = results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
            meta = results["metadatas"][0][i]
            print(f"  - [{doc_id}] Distance: {dist:.4f}")
            print(f"    Dokumen : {document}")
            print(f"    Metadata: {meta}")

    except ImportError:
        print("[INFO] Library 'chromadb' tidak terpasang. Jalankan 'pip install chromadb' untuk mengaktifkan.")
        print("Kilas ChromaDB: Database vektor sumber terbuka terpopuler dengan fitur otomatis embedding, filtering, dan integrasi mudah.")

if __name__ == "__main__":
    main()
