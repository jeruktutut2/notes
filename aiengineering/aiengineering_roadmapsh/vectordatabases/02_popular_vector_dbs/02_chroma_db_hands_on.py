#!/usr/bin/env python3
"""
Modul 02: Popular Vector DBs - Chroma DB Hands-On
Demonstrasi ChromaDB Persistent Client & Collections (Local Open Source Embedded Vector DB).
"""

import os
import shutil
import numpy as np

def main():
    print("=========================================================")
    print("  02: CHROMA DB HANDS-ON (EMBEDDED LOCAL VECTOR DB)")
    print("=========================================================\n")

    db_dir = "./chroma_demo_db"

    try:
        import chromadb
        print("📦 Library 'chromadb' terdeteksi! Menginisialisasi PersistentClient...")
        client = chromadb.PersistentClient(path=db_dir)
        collection = client.get_or_create_collection(name="ai_knowledge_base", metadata={"hnsw:space": "cosine"})
        
        # Add sample records
        collection.add(
            ids=["doc1", "doc2", "doc3"],
            embeddings=[
                [0.1, 0.8, 0.9, 0.2],
                [0.15, 0.85, 0.85, 0.1],
                [0.9, 0.1, 0.0, 0.3]
            ],
            metadatas=[
                {"category": "Vector DB", "author": "Alice"},
                {"category": "Vector DB", "author": "Bob"},
                {"category": "Frontend", "author": "Charlie"}
            ],
            documents=[
                "ChromaDB adalah embedded vector database open-source.",
                "HNSW digunakan oleh Chroma untuk pencarian ANN super cepat.",
                "CSS Grid dan Flexbox digunakan untuk merancang tata letak web."
            ]
        )

        print("✅ Berhasil menambahkan 3 dokumen & vektor ke ChromaDB collection!")

        # Query Collection
        results = collection.query(
            query_embeddings=[[0.12, 0.82, 0.88, 0.18]],
            n_results=2,
            where={"category": "Vector DB"}
        )

        print("\n🔍 Hasil Query ChromaDB (Top-2 Vector DB Category):")
        for i in range(len(results["ids"][0])):
            doc_id = results["ids"][0][i]
            doc_text = results["documents"][0][i]
            distance = results["distances"][0][i] if "distances" in results else 0.0
            print(f"  • ID: {doc_id} | Jarak: {distance:.4f}")
            print(f"    Dokumen: '{doc_text}'")

        # Cleanup
        if os.path.exists(db_dir):
            shutil.rmtree(db_dir)

    except ImportError:
        print("ℹ️  Package 'chromadb' belum di-install. Menjalankan Simulasi ChromaDB Python Lightweight Engine.\n")
        print("--- [SIMULASI CHROMA DB] ---")
        print("Collection: 'ai_knowledge_base' (HNSW Cosine Space)")
        print("  • Added Doc 'doc1': 'ChromaDB adalah embedded vector database open-source.'")
        print("  • Added Doc 'doc2': 'HNSW digunakan oleh Chroma untuk pencarian ANN super cepat.'")
        print("  • Added Doc 'doc3': 'CSS Grid dan Flexbox digunakan untuk merancang tata letak web.'")
        print("\nQuery Result for Vector Search ('Vector DB' Category Filter):")
        print("  1. Match: 'doc1' (Distance: 0.0042)")
        print("  2. Match: 'doc2' (Distance: 0.0089)")

    print("\n✅ Hands-on Chroma DB Selesai! Sangat fleksibel untuk local prototyping tanpa cloud API Key.")

if __name__ == "__main__":
    main()
