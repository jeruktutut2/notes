"""
=================================================================
1. RAG PIPELINE (Retrieval-Augmented Generation)
=================================================================
RAG adalah arsitektur yang menggabungkan LLM dengan sistem retrieval
untuk menjawab pertanyaan berdasarkan data spesifik/privat.

Pipeline RAG:
┌────────────────────────────────────────────────────────────┐
│ INGESTION (Offline):                                       │
│   Load Docs → Chunk → Embed → Store di Vector DB          │
│                                                            │
│ RETRIEVAL + GENERATION (Online):                           │
│   User Query → Embed → Search Vector DB → Get Chunks      │
│                     → Gabung ke Prompt → LLM → Jawaban    │
└────────────────────────────────────────────────────────────┘

NOTE: Demo ini menggunakan ChromaDB untuk vector DB.
      Bagian LLM generation menggunakan simulasi (tanpa API key).
      Untuk versi dengan OpenAI, lihat komentar di dalam kode.
=================================================================
"""

import chromadb
import re
import os


# ===== SAMPLE DOCUMENTS (Simulasi knowledge base) =====
KNOWLEDGE_BASE = {
    "python_basics.txt": """
Python adalah bahasa pemrograman tingkat tinggi yang diciptakan oleh Guido van Rossum dan dirilis pertama kali pada tahun 1991. Python memiliki filosofi desain yang menekankan keterbacaan kode dengan penggunaan indentasi yang signifikan.

Python mendukung berbagai paradigma pemrograman termasuk pemrograman terstruktur, berorientasi objek, dan fungsional. Python sering digunakan untuk web development, data science, machine learning, scripting, dan otomasi.

Kelebihan Python antara lain sintaks yang sederhana dan mudah dipelajari, library yang sangat banyak (NumPy, Pandas, scikit-learn, dll), komunitas yang besar, dan dukungan cross-platform. Kekurangan Python adalah kecepatan eksekusi yang lebih lambat dibanding bahasa compiled seperti C++ atau Rust.
""",
    "machine_learning.txt": """
Machine Learning (ML) adalah cabang dari kecerdasan buatan yang memungkinkan komputer untuk belajar dari data tanpa diprogram secara eksplisit. ML menggunakan algoritma untuk menemukan pola dalam data dan membuat prediksi atau keputusan.

Ada tiga jenis utama machine learning: supervised learning (belajar dari data berlabel), unsupervised learning (belajar dari data tanpa label), dan reinforcement learning (belajar melalui reward dan punishment).

Contoh algoritma supervised learning: Linear Regression, Logistic Regression, Decision Tree, Random Forest, SVM, dan Neural Network. Contoh unsupervised: K-Means Clustering, DBSCAN, PCA. Contoh reinforcement: Q-Learning, Deep Q-Network (DQN).

Tools populer untuk ML: scikit-learn (algoritma klasik), TensorFlow dan PyTorch (deep learning), XGBoost (gradient boosting), dan Hugging Face Transformers (NLP).
""",
    "deep_learning.txt": """
Deep Learning adalah subset dari Machine Learning yang menggunakan neural network dengan banyak lapisan (deep neural network). Deep learning sangat efektif untuk data tidak terstruktur seperti gambar, teks, dan audio.

Arsitektur deep learning populer:
- CNN (Convolutional Neural Network): untuk pengolahan gambar dan video. Digunakan dalam pengenalan wajah, klasifikasi gambar, dan deteksi objek.
- RNN (Recurrent Neural Network): untuk data sekuensial. LSTM dan GRU mengatasi masalah vanishing gradient. Digunakan untuk terjemahan bahasa dan analisis sentiment.
- Transformer: arsitektur terbaru yang mendominasi NLP. Model seperti BERT, GPT, dan T5 berbasis Transformer. Menggunakan mekanisme self-attention.

Framework populer: TensorFlow (Google), PyTorch (Meta/Facebook), JAX (Google), dan Keras (high-level API).

Training deep learning membutuhkan GPU (Graphics Processing Unit) karena komputasi matriks yang intensif. Cloud provider seperti AWS, GCP, dan Azure menyediakan GPU instances untuk training.
""",
}


def chunk_document(text, chunk_size=300, overlap=50):
    """Recursive character splitting untuk chunking."""
    separators = ["\n\n", "\n", ". ", " "]
    
    def _split(text, seps):
        if len(text) <= chunk_size:
            return [text]
        sep = seps[-1]
        for s in seps:
            if s in text:
                sep = s
                break
        parts = text.split(sep)
        chunks, current = [], ""
        for part in parts:
            candidate = current + sep + part if current else part
            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current.strip())
                if len(part) > chunk_size and len(seps) > 1:
                    chunks.extend(_split(part, seps[1:]))
                    current = ""
                else:
                    current = part
        if current:
            chunks.append(current.strip())
        return chunks
    
    return [c for c in _split(text, separators) if c.strip()]


def demo_ingestion():
    """Demo Phase 1: Ingestion — Load, Chunk, Embed, Store."""
    print("=" * 60)
    print("PHASE 1: INGESTION — Menyiapkan Knowledge Base")
    print("=" * 60)

    # 1. Load dokumen
    print(f"\n📄 Step 1: Load {len(KNOWLEDGE_BASE)} dokumen")
    for name, content in KNOWLEDGE_BASE.items():
        print(f"   - {name} ({len(content.strip())} chars)")

    # 2. Chunk setiap dokumen
    print(f"\n✂️ Step 2: Chunking (recursive, size=300, overlap=50)")
    all_chunks = []
    all_metadatas = []
    all_ids = []
    chunk_idx = 0

    for filename, content in KNOWLEDGE_BASE.items():
        chunks = chunk_document(content.strip(), chunk_size=300, overlap=50)
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metadatas.append({
                "source": filename,
                "chunk_index": i,
            })
            all_ids.append(f"chunk_{chunk_idx}")
            chunk_idx += 1

    print(f"   Total chunks: {len(all_chunks)}")
    for i, (chunk, meta) in enumerate(zip(all_chunks, all_metadatas)):
        preview = chunk.replace('\n', ' ')[:60]
        print(f"   [{i:>2}] ({meta['source']}) \"{preview}...\"")

    # 3 & 4. Embed + Store ke ChromaDB
    print(f"\n💾 Step 3 & 4: Embed + Store ke ChromaDB")
    client = chromadb.Client()
    collection = client.create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )

    collection.add(
        documents=all_chunks,
        metadatas=all_metadatas,
        ids=all_ids,
    )
    print(f"   ✅ {collection.count()} chunks berhasil disimpan!")

    return client, collection


def demo_retrieval(collection):
    """Demo Phase 2: Retrieval — Cari dokumen relevan."""
    print("\n\n" + "=" * 60)
    print("PHASE 2: RETRIEVAL — Mencari Dokumen Relevan")
    print("=" * 60)

    queries = [
        "Apa itu machine learning dan jenis-jenisnya?",
        "Framework apa yang dipakai untuk deep learning?",
        "Apa kelebihan Python?",
        "Bagaimana cara kerja CNN?",
    ]

    all_results = []
    for query in queries:
        print(f"\n🔍 Query: \"{query}\"")
        print("-" * 60)

        results = collection.query(
            query_texts=[query],
            n_results=3,
            include=["documents", "metadatas", "distances"]
        )

        retrieved_chunks = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            sim = 1 - dist
            retrieved_chunks.append({
                "text": doc,
                "source": meta["source"],
                "similarity": sim,
            })
            preview = doc.replace('\n', ' ')[:65]
            print(f"   [{sim:.4f}] ({meta['source']}) \"{preview}...\"")

        all_results.append((query, retrieved_chunks))

    return all_results


def demo_generation(retrieval_results):
    """Demo Phase 3: Generation — Buat jawaban dari konteks."""
    print("\n\n" + "=" * 60)
    print("PHASE 3: GENERATION — Menghasilkan Jawaban")
    print("=" * 60)

    print("\n📌 NOTE: Demo ini menggunakan simulasi LLM (tanpa API key)")
    print("   Untuk produksi, ganti dengan OpenAI/Gemini API\n")

    for query, chunks in retrieval_results[:2]:  # ambil 2 contoh saja
        print(f"\n{'─' * 60}")
        print(f"❓ Pertanyaan: \"{query}\"")

        # Gabungkan konteks
        context = "\n\n---\n\n".join([
            f"[Sumber: {c['source']}]\n{c['text']}"
            for c in chunks
        ])

        # Buat prompt (yang akan dikirim ke LLM)
        prompt = f"""Jawab pertanyaan berdasarkan konteks berikut.
Jika jawaban tidak ada dalam konteks, katakan "Tidak ditemukan".

KONTEKS:
{context}

PERTANYAAN: {query}

JAWABAN:"""

        print(f"\n📋 Prompt yang dikirim ke LLM:")
        print(f"   (total {len(prompt)} karakter)")
        print(f"   Konteks dari {len(chunks)} chunks:")
        for c in chunks:
            print(f"   - {c['source']} (similarity: {c['similarity']:.4f})")

        # === Simulasi jawaban LLM ===
        # Di produksi, gunakan kode di bawah ini:
        #
        # from openai import OpenAI
        # client = OpenAI()
        # response = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": "system", "content": "Jawab berdasarkan konteks."},
        #         {"role": "user", "content": prompt}
        #     ],
        #     temperature=0.3,
        # )
        # answer = response.choices[0].message.content

        # Simulasi sederhana: ambil kalimat paling relevan dari konteks
        best_chunk = chunks[0]["text"]
        sentences = re.split(r'(?<=[.!?])\s+', best_chunk)
        simulated_answer = ' '.join(sentences[:3]) if sentences else best_chunk[:200]

        print(f"\n🤖 Jawaban (simulasi):")
        print(f"   {simulated_answer}")
        print(f"\n   📚 Sumber: {', '.join(set(c['source'] for c in chunks))}")


def demo_full_pipeline():
    """Demo: full RAG pipeline end-to-end."""
    print("\n\n" + "=" * 60)
    print("FULL PIPELINE: End-to-End RAG")
    print("=" * 60)

    # Setup
    client = chromadb.Client()
    collection = client.create_collection(
        name="rag_demo",
        metadata={"hnsw:space": "cosine"}
    )

    # Ingestion
    all_chunks = []
    all_metas = []
    all_ids = []
    idx = 0
    for filename, content in KNOWLEDGE_BASE.items():
        chunks = chunk_document(content.strip())
        for i, chunk in enumerate(chunks):
            all_chunks.append(chunk)
            all_metas.append({"source": filename, "chunk_index": i})
            all_ids.append(f"c_{idx}")
            idx += 1

    collection.add(documents=all_chunks, metadatas=all_metas, ids=all_ids)

    # Interactive-style query
    queries = [
        "Apa saja framework untuk deep learning?",
        "Jelaskan supervised vs unsupervised learning",
        "Kapan Python pertama kali dirilis?",
    ]

    for query in queries:
        print(f"\n{'─' * 60}")
        print(f"❓ {query}")

        # Retrieve
        results = collection.query(query_texts=[query], n_results=3)

        # Tampilkan konteks
        sources = set()
        context_parts = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            sources.add(meta["source"])
            context_parts.append(doc)

        # Simulasi jawaban
        best = context_parts[0]
        sentences = re.split(r'(?<=[.!?])\s+', best)
        answer = ' '.join(sentences[:2])

        print(f"💡 {answer}")
        print(f"📚 Sumber: {', '.join(sources)}")

    print(f"\n\n{'═' * 60}")
    print("💡 Poin Penting RAG:")
    print("═" * 60)
    print("   1. Ingestion: Load → Chunk → Embed → Store (offline)")
    print("   2. Retrieval: Query → Search → Get relevant chunks (online)")
    print("   3. Generation: Context + Query → LLM → Answer (online)")
    print("   4. Kualitas RAG sangat tergantung pada kualitas chunking")
    print("   5. Gunakan overlap agar konteks antar chunk tidak hilang")
    print("   6. Untuk produksi, ganti simulasi dengan OpenAI/Gemini API")


def main():
    client, collection = demo_ingestion()
    retrieval_results = demo_retrieval(collection)
    demo_generation(retrieval_results)
    demo_full_pipeline()
    print("\n\n✅ Selesai! Lanjut ke modul berikutnya: 06_optimization/")


if __name__ == "__main__":
    main()
