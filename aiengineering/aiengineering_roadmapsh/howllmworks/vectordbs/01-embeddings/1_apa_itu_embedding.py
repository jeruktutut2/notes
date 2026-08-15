"""
=================================================================
1. APA ITU EMBEDDINGS?
=================================================================
Embedding adalah representasi numerik (vektor) dari data seperti 
teks, gambar, atau audio, dalam ruang berdimensi tinggi.

Tujuannya: mengubah data tidak terstruktur menjadi angka-angka 
yang bisa dipahami dan diproses oleh komputer.

Analogi Sederhana:
- Bayangkan setiap kata/kalimat memiliki "koordinat" di peta
- Kata-kata yang maknanya mirip → koordinat berdekatan
- Kata-kata yang maknanya berbeda → koordinat berjauhan

Contoh (disederhanakan):
  "kucing" → [0.2, 0.8, 0.1, 0.5]
  "anjing" → [0.3, 0.7, 0.2, 0.4]   ← dekat dengan "kucing"
  "mobil"  → [0.9, 0.1, 0.8, 0.2]   ← jauh dari "kucing"
=================================================================
"""

from sentence_transformers import SentenceTransformer
import numpy as np


def demo_apa_itu_embedding():
    """Demo dasar: mengubah teks menjadi vektor embedding."""
    print("=" * 60)
    print("DEMO 1: Apa itu Embedding?")
    print("=" * 60)

    # 1. Load model embedding (open-source, gratis)
    nama_model = "all-MiniLM-L6-v2"
    print(f"\n📦 Memuat model: {nama_model}")
    model = SentenceTransformer(nama_model)
    print("✅ Model berhasil dimuat!")

    # 2. Siapkan teks
    teks_list = [
        "Kucing adalah hewan peliharaan yang populer",
        "Anjing adalah sahabat manusia",
        "Python adalah bahasa pemrograman",
    ]

    print(f"\n📝 Teks yang akan di-embed ({len(teks_list)} kalimat):")
    for i, t in enumerate(teks_list, 1):
        print(f"   {i}. {t}")

    # 3. Buat embedding
    print("\n⚡ Membuat embedding...")
    embeddings = model.encode(teks_list)

    # 4. Tampilkan hasil
    print(f"\n📊 Hasil Embedding:")
    print(f"   Shape: {embeddings.shape}")
    print(f"   Artinya: {embeddings.shape[0]} kalimat, masing-masing {embeddings.shape[1]} dimensi")
    print("-" * 60)

    for i, teks in enumerate(teks_list):
        vektor = embeddings[i]
        print(f"\n   Teks: \"{teks}\"")
        print(f"   Vektor (5 nilai pertama): {vektor[:5].tolist()}")
        print(f"   Panjang vektor (norm): {np.linalg.norm(vektor):.4f}")

    print("\n💡 Kesimpulan:")
    print("   - Setiap teks diubah menjadi array angka (vektor)")
    print(f"   - Model '{nama_model}' menghasilkan vektor {embeddings.shape[1]} dimensi")
    print("   - Vektor ini menangkap 'makna' dari teks")


def demo_perbandingan_embedding():
    """Demo: membandingkan kemiripan teks menggunakan embedding."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Membandingkan Kemiripan Teks via Embedding")
    print("=" * 60)

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Kalimat untuk dibandingkan
    kalimat = [
        "Saya suka kucing",                     # [0]
        "Kucing adalah hewan favorit saya",      # [1] — mirip dengan [0]
        "Saya ingin membeli mobil baru",          # [2] — berbeda
        "Hewan peliharaan sangat menggemaskan",   # [3] — agak mirip [0]
    ]

    print(f"\n📝 Kalimat:")
    for i, k in enumerate(kalimat):
        print(f"   [{i}] {k}")

    # Buat embedding
    embeddings = model.encode(kalimat)

    # Hitung cosine similarity manual
    print(f"\n📊 Cosine Similarity antar kalimat:")
    print("-" * 60)

    for i in range(len(kalimat)):
        for j in range(i + 1, len(kalimat)):
            # Cosine similarity = dot(a,b) / (norm(a) * norm(b))
            sim = np.dot(embeddings[i], embeddings[j]) / (
                np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[j])
            )
            emoji = "✅" if sim > 0.4 else "⚠️" if sim > 0.2 else "❌"
            print(f"   {emoji} [{i}] vs [{j}]: {sim:.4f}")
            print(f"      \"{kalimat[i][:30]}\" vs \"{kalimat[j][:30]}\"")

    print("\n💡 Kesimpulan:")
    print("   - Kalimat yang maknanya mirip → similarity tinggi (mendekati 1)")
    print("   - Kalimat yang maknanya berbeda → similarity rendah (mendekati 0)")
    print("   - Ini adalah dasar dari Semantic Search!")


def demo_dimensi_embedding():
    """Demo: perbedaan dimensi embedding antar model."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Dimensi Embedding dari Berbagai Model")
    print("=" * 60)

    teks = "Kucing adalah hewan peliharaan yang populer"
    print(f"\n📝 Teks: \"{teks}\"")

    # Coba beberapa model dengan dimensi berbeda
    models_info = [
        ("all-MiniLM-L6-v2", 384),
        ("all-MiniLM-L12-v2", 384),
        ("paraphrase-MiniLM-L6-v2", 384),
    ]

    print(f"\n📊 Perbandingan Model:")
    print("-" * 60)
    print(f"   {'Model':<35} {'Dimensi':>10} {'Status':>10}")
    print("-" * 60)

    for nama_model, expected_dim in models_info:
        try:
            model = SentenceTransformer(nama_model)
            embedding = model.encode([teks])
            actual_dim = embedding.shape[1]
            status = "✅"
            print(f"   {nama_model:<35} {actual_dim:>10} {status:>10}")
        except Exception as e:
            print(f"   {nama_model:<35} {'N/A':>10} {'❌':>10}")

    print("\n💡 Kesimpulan:")
    print("   - Dimensi lebih tinggi → representasi lebih detail, tapi lebih lambat")
    print("   - Dimensi lebih rendah → lebih cepat, hemat memori")
    print("   - Untuk belajar, 384 dimensi (MiniLM) sudah sangat cukup")


def main():
    demo_apa_itu_embedding()
    demo_perbandingan_embedding()
    demo_dimensi_embedding()
    print("\n\n✅ Selesai! Lanjut ke: 2_embedding_models.py")


if __name__ == "__main__":
    main()
