#!/usr/bin/env python3
"""
Modul 02: Popular Vector DBs - Pinecone Hands-On (Featured Highlight in Roadmap)
Simulasi & Integrasi Pinecone Client (Serverless Index, Upsert, Metadata Query, Namespaces).
"""

import os
import numpy as np

# Mock Engine untuk Pinecone jika pinecone-client tidak terinstal / API key tidak ada
class MockPineconeIndex:
    def __init__(self, index_name: str, dimension: int, metric: str = "cosine"):
        self.index_name = index_name
        self.dimension = dimension
        self.metric = metric
        self.namespaces = {} # namespace -> dict of id -> {vector, metadata}

    def upsert(self, vectors: list, namespace: str = "default"):
        if namespace not in self.namespaces:
            self.namespaces[namespace] = {}
        for item in vectors:
            v_id = item["id"]
            vec = np.array(item["values"], dtype=np.float32)
            meta = item.get("metadata", {})
            self.namespaces[namespace][v_id] = {"vector": vec, "metadata": meta}
        return {"upserted_count": len(vectors)}

    def query(self, vector: list, top_k: int = 3, include_metadata: bool = True, filter: dict = None, namespace: str = "default"):
        if namespace not in self.namespaces or not self.namespaces[namespace]:
            return {"matches": []}
        
        q_vec = np.array(vector, dtype=np.float32)
        records = self.namespaces[namespace]
        
        matches = []
        for v_id, data in records.items():
            meta = data["metadata"]
            # Apply metadata filter
            if filter:
                match_filter = True
                for k, v in filter.items():
                    if meta.get(k) != v:
                        match_filter = False
                        break
                if not match_filter:
                    continue

            # Compute score
            v = data["vector"]
            if self.metric == "cosine":
                score = float(np.dot(q_vec, v) / (np.linalg.norm(q_vec) * np.linalg.norm(v)))
            elif self.metric == "dotproduct":
                score = float(np.dot(q_vec, v))
            else:
                score = float(-np.linalg.norm(q_vec - v))

            matches.append({
                "id": v_id,
                "score": score,
                "metadata": meta if include_metadata else {}
            })

        matches.sort(key=lambda x: x["score"], reverse=True)
        return {"matches": matches[:top_k]}

def main():
    print("=========================================================")
    print("  01: PINECONE VECTOR DB HANDS-ON (FEATURED ROADMAP DB)")
    print("=========================================================\n")

    api_key = os.getenv("PINECONE_API_KEY")
    use_mock = True

    try:
        from pinecone import Pinecone, ServerlessSpec
        if api_key:
            print("🔑 API Key Pinecone ditemukan! Menghubungkan ke Pinecone Cloud Service...")
            pc = Pinecone(api_key=api_key)
            index_name = "ai-engineer-demo"
            if index_name not in [idx.name for idx in pc.list_indexes()]:
                pc.create_index(
                    name=index_name,
                    dimension=128,
                    metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1")
                )
            index = pc.Index(index_name)
            use_mock = False
        else:
            print("ℹ️  PINECONE_API_KEY tidak terdeteksi. Menggunakan Mock Engine Pinecone Serverless Simulator.\n")
    except ImportError:
        print("ℹ️  Package pinecone-client belum ter-install. Menggunakan Mock Engine Pinecone Serverless Simulator.\n")

    if use_mock:
        index = MockPineconeIndex(index_name="ai-engineer-demo", dimension=4, metric="cosine")

    # 1. Upsert Data Vektor ke Pinecone
    print("--- [1] UPSERT VECTOR DATA & METADATA (Namespace: 'finance-docs') ---")
    
    # Generate sample 4D vectors
    vectors_to_upsert = [
        {
            "id": "vec-1",
            "values": [0.9, 0.1, 0.0, 0.1],
            "metadata": {"doc_type": "report", "year": 2024, "title": "Laporan Keuangan Q1"}
        },
        {
            "id": "vec-2",
            "values": [0.85, 0.15, 0.05, 0.05],
            "metadata": {"doc_type": "report", "year": 2023, "title": "Laporan Keuangan Tahunan 2023"}
        },
        {
            "id": "vec-3",
            "values": [0.1, 0.9, 0.8, 0.2],
            "metadata": {"doc_type": "article", "year": 2024, "title": "Tren Pasar Saham Teknologi"}
        }
    ]

    res = index.upsert(vectors=vectors_to_upsert, namespace="finance-docs")
    print(f"✅ Upsert Berhasil! Jumlah Record: {res.get('upserted_count', 3)}\n")

    # 2. Querying Index dengan Metadata Filter
    print("--- [2] QUERY SIMILARITY SEARCH WITH METADATA FILTERING ---")
    query_vector = [0.88, 0.12, 0.02, 0.08]
    
    print("Query: Vector [0.88, 0.12, 0.02, 0.08] dengan Filter metadata {'doc_type': 'report', 'year': 2024}")
    query_response = index.query(
        vector=query_vector,
        top_k=2,
        include_metadata=True,
        filter={"doc_type": "report", "year": 2024},
        namespace="finance-docs"
    )

    print("\nHasil Match Pinecone:")
    for match in query_response["matches"]:
        print(f"  • ID: {match['id']} | Skor Cosine: {match['score']:.4f}")
        print(f"    Metadata: {match['metadata']}")

    print("\n✅ Hands-on Pinecone selesai! Pinecone merupakan pilihan utama untuk cloud-native managed vector storage.")

if __name__ == "__main__":
    main()
