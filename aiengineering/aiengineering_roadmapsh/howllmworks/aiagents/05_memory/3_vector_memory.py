import os
import json
import numpy as np

def main():
    print("=== 5.3 Vector Memory (Long-Term Memory dengan Vector Store) ===\n")

    # ---------------------------------------------------------------
    # VECTOR MEMORY (Long-Term Memory)
    # Menyimpan informasi secara permanen di vector database.
    # Ketika dibutuhkan, agent mencari informasi yang relevan
    # berdasarkan kesamaan semantik (bukan keyword matching).
    #
    # Script ini menggunakan implementasi sederhana TANPA ChromaDB
    # untuk menunjukkan konsep dasar. Di produksi, gunakan ChromaDB/Pinecone/dll.
    # ---------------------------------------------------------------

    # --- IMPLEMENTASI VECTOR STORE SEDERHANA ---
    class SimpleVectorStore:
        """Vector store sederhana menggunakan numpy (untuk belajar konsep)."""

        def __init__(self, embedding_dim=64):
            self.memories = []       # List of {"text": ..., "metadata": ...}
            self.vectors = []        # List of numpy arrays
            self.embedding_dim = embedding_dim

        def _simple_embedding(self, text):
            """
            Membuat embedding sederhana dari teks (untuk demo).
            Di produksi, gunakan model embedding seperti OpenAI text-embedding-3-small
            atau sentence-transformers.
            """
            # Hash-based pseudo-embedding (BUKAN embedding sebenarnya)
            # Ini hanya untuk menunjukkan konsep, bukan untuk produksi
            np.random.seed(hash(text.lower().strip()) % (2**31))
            vec = np.random.randn(self.embedding_dim).astype(np.float32)
            # Normalize
            vec = vec / (np.linalg.norm(vec) + 1e-8)
            return vec

        def add(self, text, metadata=None):
            """Menambahkan teks ke vector store."""
            vec = self._simple_embedding(text)
            self.memories.append({"text": text, "metadata": metadata or {}})
            self.vectors.append(vec)
            return len(self.memories) - 1  # Return index

        def search(self, query, top_k=3):
            """Mencari memori yang paling mirip dengan query."""
            if not self.vectors:
                return []

            query_vec = self._simple_embedding(query)
            # Cosine similarity
            similarities = []
            for i, vec in enumerate(self.vectors):
                sim = np.dot(query_vec, vec)
                similarities.append((i, sim))

            # Sort by similarity (descending)
            similarities.sort(key=lambda x: x[1], reverse=True)

            results = []
            for idx, sim in similarities[:top_k]:
                results.append({
                    "text": self.memories[idx]["text"],
                    "metadata": self.memories[idx]["metadata"],
                    "similarity": float(sim)
                })
            return results

        def get_all(self):
            """Mengembalikan semua memori."""
            return self.memories

    # --- DEMO ---
    store = SimpleVectorStore()

    # 1. Simpan memori (informasi tentang user)
    print("=" * 60)
    print("1. MENYIMPAN MEMORI")
    print("=" * 60)

    memori_user = [
        ("User bernama Andi dan tinggal di Jakarta", {"tipe": "profil", "tanggal": "2024-01-15"}),
        ("Andi suka makan rendang dan nasi padang", {"tipe": "preferensi", "tanggal": "2024-01-15"}),
        ("Andi bekerja sebagai machine learning engineer", {"tipe": "profil", "tanggal": "2024-01-16"}),
        ("Andi punya anjing bernama Rocky jenis golden retriever", {"tipe": "personal", "tanggal": "2024-01-17"}),
        ("Andi sedang belajar tentang AI Agent dan LangChain", {"tipe": "aktivitas", "tanggal": "2024-01-18"}),
        ("Andi berencana pindah ke Bali tahun depan", {"tipe": "rencana", "tanggal": "2024-01-20"}),
        ("Andi alergi seafood terutama udang", {"tipe": "kesehatan", "tanggal": "2024-01-21"}),
        ("Andi suka nonton film sci-fi dan horor", {"tipe": "hobi", "tanggal": "2024-01-22"}),
    ]

    for text, metadata in memori_user:
        idx = store.add(text, metadata)
        print(f"  ✅ Disimpan [{idx}]: {text}")

    print(f"\nTotal memori tersimpan: {len(store.get_all())}")

    # 2. Cari memori berdasarkan query
    print(f"\n{'='*60}")
    print("2. MENCARI MEMORI (Semantic Search)")
    print(f"{'='*60}")

    queries = [
        "makanan favorit user",
        "pekerjaan atau karir",
        "hewan peliharaan",
        "rencana masa depan",
    ]

    for query in queries:
        print(f"\n  🔍 Query: '{query}'")
        results = store.search(query, top_k=2)
        for i, r in enumerate(results):
            print(f"     [{i+1}] (sim={r['similarity']:.4f}) {r['text']}")
            print(f"          metadata: {r['metadata']}")

    # 3. Simulasi penggunaan di agent
    print(f"\n{'='*60}")
    print("3. SIMULASI: Agent Menggunakan Vector Memory")
    print(f"{'='*60}")

    def agent_with_memory(pertanyaan):
        """Simulasi agent yang menggunakan vector memory untuk menjawab."""
        print(f"\n  👤 User: {pertanyaan}")

        # Cari memori yang relevan
        relevant_memories = store.search(pertanyaan, top_k=3)

        print(f"  📚 Memori yang ditemukan:")
        memory_context = ""
        for r in relevant_memories:
            print(f"     - {r['text']} (sim={r['similarity']:.3f})")
            memory_context += f"- {r['text']}\n"

        # Susun prompt dengan konteks memori
        prompt = f"""Berdasarkan informasi yang kamu ingat tentang user:
{memory_context}

Jawab pertanyaan user: {pertanyaan}"""

        print(f"\n  📝 Prompt yang dikirim ke LLM (termasuk memori):")
        print(f"     {prompt[:200]}...")

        # Di sini seharusnya memanggil LLM, tapi kita skip agar tidak butuh API key
        print(f"  🤖 [LLM akan menjawab berdasarkan memori yang ditemukan]")

    agent_with_memory("Apa makanan yang harus dihindari untuk user?")
    agent_with_memory("Ceritakan tentang peliharaan user")
    agent_with_memory("User mau pindah ke mana?")

    # 4. Perbandingan jenis memory
    print(f"\n{'='*60}")
    print("4. PERBANDINGAN JENIS MEMORY")
    print(f"{'='*60}")

    print(f"""
    {'Jenis':<25} {'Durasi':<15} {'Kapasitas':<15} {'Kecepatan':<12} {'Contoh'}
    {'-'*85}
    {'Conversation (Full)':<25} {'Sementara':<15} {'Terbatas*':<15} {'Cepat':<12} {'Riwayat chat dalam prompt'}
    {'Window Memory':<25} {'Sementara':<15} {'N terakhir':<15} {'Cepat':<12} {'10 pesan terakhir'}
    {'Summary Memory':<25} {'Sementara':<15} {'Terkompresi':<15} {'Sedang':<12} {'Ringkasan percakapan'}
    {'Vector Memory':<25} {'Permanen':<15} {'Tak terbatas':<15} {'Sedang':<12} {'ChromaDB, Pinecone'}

    *Terbatas oleh context window model
    """)

    print("✅ Selesai! Memahami Vector Memory (Long-Term Memory).")
    print("\nRingkasan:")
    print("- Vector Memory menyimpan informasi sebagai vektor (embedding)")
    print("- Pencarian berdasarkan kesamaan semantik (bukan keyword)")
    print("- Di produksi, gunakan ChromaDB, Pinecone, Weaviate, atau Qdrant")
    print("- Cocok untuk menyimpan preferensi user, fakta, dokumen, dll.")

if __name__ == "__main__":
    main()
