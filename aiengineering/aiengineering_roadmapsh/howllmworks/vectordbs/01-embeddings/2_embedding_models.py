"""
=================================================================
2. EMBEDDING MODELS: API vs Open-Source
=================================================================
Ada dua cara utama menghasilkan embedding:

A. API-Based (Berbayar, Mudah):
   - OpenAI text-embedding-3-small/large
   - Google Gemini Embedding
   - Cohere Embed

B. Open-Source (Gratis, Self-Hosted):
   - Sentence Transformers (all-MiniLM-L6-v2, dll)
   - HuggingFace models (BGE, E5, dll)

Perbandingan:
┌──────────────┬────────────────────┬─────────────────────┐
│   Aspek      │     API-Based      │     Open-Source      │
├──────────────┼────────────────────┼─────────────────────┤
│ Biaya        │ Berbayar per token │ Gratis               │
│ Kecepatan    │ Tergantung network │ Tergantung hardware  │
│ Privasi      │ Data dikirim keluar│ Data tetap lokal     │
│ Setup        │ Cukup API key      │ Perlu install model  │
│ Kualitas     │ Sangat baik        │ Baik - Sangat baik   │
└──────────────┴────────────────────┴─────────────────────┘

NOTE: Demo ini fokus pada Open-Source karena tidak butuh API key.
=================================================================
"""

from sentence_transformers import SentenceTransformer
import numpy as np
import time


def demo_sentence_transformers():
    """Demo: menggunakan Sentence Transformers (open-source)."""
    print("=" * 60)
    print("DEMO 1: Sentence Transformers (Open-Source)")
    print("=" * 60)

    model_name = "all-MiniLM-L6-v2"
    print(f"\n📦 Memuat model: {model_name}")
    model = SentenceTransformer(model_name)

    # Encode beberapa kalimat
    kalimat = [
        "Machine learning is a subset of artificial intelligence",
        "Deep learning uses neural networks with many layers",
        "Natural language processing deals with text data",
        "Computer vision processes image and video data",
        "I like to eat pizza on weekends",
    ]

    print(f"\n📝 Encoding {len(kalimat)} kalimat...")
    start = time.time()
    embeddings = model.encode(kalimat, show_progress_bar=False)
    elapsed = (time.time() - start) * 1000

    print(f"   ⏱️ Waktu encoding: {elapsed:.2f} ms")
    print(f"   📐 Shape: {embeddings.shape}")
    print(f"   📏 Dimensi per kalimat: {embeddings.shape[1]}")

    # Tampilkan similarity matrix
    print(f"\n📊 Similarity Matrix:")
    print(f"   {'':>5}", end="")
    for i in range(len(kalimat)):
        print(f"  [{i}]  ", end="")
    print()

    for i in range(len(kalimat)):
        print(f"   [{i}]", end="")
        for j in range(len(kalimat)):
            sim = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )
            print(f"  {sim:.3f}", end="")
        print(f"  ← {kalimat[i][:35]}...")
    
    print("\n💡 Perhatikan:")
    print("   - Kalimat [0]-[3] tentang AI/ML → similarity tinggi satu sama lain")
    print("   - Kalimat [4] tentang pizza → similarity rendah dengan yang lain")


def demo_batch_encoding():
    """Demo: encoding batch untuk efisiensi."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Batch Encoding (Efisiensi)")
    print("=" * 60)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Buat banyak kalimat
    kalimat = [f"Ini adalah kalimat contoh nomor {i}" for i in range(100)]
    print(f"\n📝 Encoding {len(kalimat)} kalimat...")

    # Encode satu per satu
    start = time.time()
    for k in kalimat:
        model.encode([k], show_progress_bar=False)
    waktu_satu = (time.time() - start) * 1000

    # Encode batch sekaligus
    start = time.time()
    model.encode(kalimat, batch_size=32, show_progress_bar=False)
    waktu_batch = (time.time() - start) * 1000

    print(f"\n📊 Perbandingan Kecepatan:")
    print("-" * 40)
    print(f"   Satu per satu : {waktu_satu:.2f} ms")
    print(f"   Batch (32)    : {waktu_batch:.2f} ms")
    print(f"   Speedup       : {waktu_satu / waktu_batch:.1f}x lebih cepat")

    print("\n💡 Kesimpulan:")
    print("   - Selalu gunakan batch encoding untuk banyak data")
    print("   - batch_size=32 adalah default yang bagus")


def demo_multilingual():
    """Demo: model multilingual untuk bahasa Indonesia."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Model Multilingual (Bahasa Indonesia)")
    print("=" * 60)

    # Model yang mendukung bahasa Indonesia
    model_name = "paraphrase-multilingual-MiniLM-L12-v2"
    print(f"\n📦 Memuat model multilingual: {model_name}")
    model = SentenceTransformer(model_name)

    # Kalimat dalam bahasa Indonesia
    kalimat_id = [
        "Saya suka belajar kecerdasan buatan",
        "Artificial intelligence sangat menarik untuk dipelajari",
        "Kucing saya suka tidur di sofa",
    ]

    print(f"\n📝 Kalimat (Bahasa Indonesia):")
    for i, k in enumerate(kalimat_id):
        print(f"   [{i}] {k}")

    embeddings = model.encode(kalimat_id, show_progress_bar=False)

    print(f"\n📊 Cosine Similarity:")
    print("-" * 60)
    for i in range(len(kalimat_id)):
        for j in range(i + 1, len(kalimat_id)):
            sim = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )
            emoji = "✅" if sim > 0.5 else "❌"
            print(f"   {emoji} [{i}] vs [{j}]: {sim:.4f}")

    # Cross-lingual: Indonesia vs English
    print(f"\n🌍 Cross-Lingual (Indonesia ↔ English):")
    print("-" * 60)
    kalimat_en = "I love learning artificial intelligence"
    emb_id = model.encode([kalimat_id[0]], show_progress_bar=False)
    emb_en = model.encode([kalimat_en], show_progress_bar=False)

    sim = np.dot(emb_id[0], emb_en[0]) / (
        np.linalg.norm(emb_id[0]) * np.linalg.norm(emb_en[0])
    )
    print(f"   ID: \"{kalimat_id[0]}\"")
    print(f"   EN: \"{kalimat_en}\"")
    print(f"   Similarity: {sim:.4f} ✅")

    print("\n💡 Kesimpulan:")
    print("   - Model multilingual bisa memahami berbagai bahasa")
    print("   - Kalimat bermakna sama dalam bahasa berbeda → similarity tinggi")
    print("   - Gunakan model multilingual untuk konten bahasa Indonesia")


def main():
    demo_sentence_transformers()
    demo_batch_encoding()
    demo_multilingual()
    print("\n\n✅ Selesai! Lanjut ke modul berikutnya: 02_similarity_search/")


if __name__ == "__main__":
    main()
