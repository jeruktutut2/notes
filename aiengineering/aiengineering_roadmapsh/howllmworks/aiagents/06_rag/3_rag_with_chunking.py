import os
import numpy as np
from openai import OpenAI

def main():
    print("=== 6.3 RAG dengan Chunking (Dokumen Panjang) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # CHUNKING
    # Dokumen panjang tidak bisa dimasukkan langsung ke embedding atau
    # prompt. Solusi: pecah menjadi potongan kecil (chunks).
    #
    # Strategi chunking:
    # - Fixed size: Setiap chunk punya jumlah karakter/kata tetap
    # - Overlap: Chunk saling tumpang tindih agar konteks tidak putus
    # - Semantic: Pecah berdasarkan paragraf/section
    # ---------------------------------------------------------------

    # 1. IMPLEMENTASI CHUNKING
    print("=" * 60)
    print("1. TEXT CHUNKING - Memecah Dokumen Panjang")
    print("=" * 60)

    def chunk_text(text, chunk_size=200, overlap=50):
        """
        Memecah teks menjadi chunks dengan overlap.

        Args:
            text: Teks yang akan dipecah
            chunk_size: Jumlah karakter per chunk
            overlap: Jumlah karakter yang overlap antar chunk
        """
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]

            # Coba potong di akhir kalimat (titik) agar lebih natural
            if end < len(text):
                last_period = chunk.rfind('.')
                if last_period > chunk_size * 0.5:  # Minimal 50% dari chunk_size
                    chunk = chunk[:last_period + 1]
                    end = start + last_period + 1

            chunks.append({
                "text": chunk.strip(),
                "start": start,
                "end": end,
                "index": len(chunks)
            })
            start = end - overlap  # Mundur sebanyak overlap

        return chunks

    # Dokumen contoh (panduan karyawan)
    dokumen_panjang = """
Panduan Onboarding Karyawan Baru

Bab 1: Hari Pertama
Selamat datang di PT Teknologi Maju! Pada hari pertama, Anda akan bertemu dengan HR untuk proses administrasi. Dokumen yang perlu dibawa: KTP, NPWP, ijazah terakhir, dan foto 3x4. Anda akan mendapatkan kartu akses gedung dan laptop kerja. Tim IT akan membantu setup email dan akun perusahaan.

Bab 2: Masa Percobaan
Masa percobaan berlangsung selama 3 bulan. Selama masa ini, Anda akan mendapat mentor yang ditugaskan oleh manajer. Evaluasi dilakukan di minggu ke-4 dan ke-12. Kriteria evaluasi meliputi: kemampuan teknis, kerja sama tim, inisiatif, dan kehadiran. Jika lulus evaluasi, Anda akan diangkat menjadi karyawan tetap.

Bab 3: Fasilitas Kantor
Kantor berlokasi di Gedung Graha Tekno Lt. 15, Jl. Sudirman No. 100, Jakarta. Jam operasional gedung 07:00-22:00. Fasilitas yang tersedia: ruang meeting (booking via app), pantry dengan kopi dan snack gratis, gym di Lt. 3, mushola di Lt. 10, dan parking area di basement (slot terbatas, first come first served).

Bab 4: Sistem Penggajian
Gaji dibayarkan setiap tanggal 25. Jika tanggal 25 jatuh pada hari libur, pembayaran dimajukan ke hari kerja sebelumnya. Komponen gaji: gaji pokok, tunjangan tetap, tunjangan makan Rp 35.000/hari kerja, tunjangan transport Rp 500.000/bulan. Slip gaji bisa diakses melalui portal HR. Pajak PPh 21 sudah dipotong otomatis.

Bab 5: Pengembangan Karir
Perusahaan menyediakan budget training Rp 10.000.000 per tahun per karyawan. Anda bisa mengikuti kursus online, seminar, atau sertifikasi profesional. Pengajuan training melalui form di portal HR dengan persetujuan manajer. Review performa dilakukan setiap 6 bulan (Mei dan November) yang mempengaruhi kenaikan gaji dan promosi.
""".strip()

    # Chunking
    chunks = chunk_text(dokumen_panjang, chunk_size=300, overlap=50)

    print(f"\nDokumen asli: {len(dokumen_panjang)} karakter")
    print(f"Jumlah chunks: {len(chunks)}")
    print(f"Chunk size: 300 karakter, Overlap: 50 karakter\n")

    for chunk in chunks:
        preview = chunk["text"][:80].replace("\n", " ")
        print(f"  Chunk [{chunk['index']}] ({len(chunk['text'])} chars): {preview}...")

    # 2. INDEX CHUNKS KE VECTOR STORE
    print(f"\n{'='*60}")
    print("2. INDEXING - Menyimpan Chunks sebagai Embedding")
    print(f"{'='*60}")

    def pseudo_embedding(text, dim=64):
        np.random.seed(hash(text.lower().strip()) % (2**31))
        vec = np.random.randn(dim).astype(np.float32)
        return vec / (np.linalg.norm(vec) + 1e-8)

    def cosine_similarity(a, b):
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))

    # Buat embedding untuk setiap chunk
    chunk_embeddings = []
    for chunk in chunks:
        emb = pseudo_embedding(chunk["text"])
        chunk_embeddings.append(emb)
        print(f"  ✅ Chunk [{chunk['index']}] diindex (embedding dim={len(emb)})")

    # 3. RAG PIPELINE DENGAN CHUNKING
    print(f"\n{'='*60}")
    print("3. RAG PIPELINE DENGAN CHUNKING")
    print(f"{'='*60}")

    def rag_with_chunks(pertanyaan, top_k=2):
        print(f"\n❓ Pertanyaan: {pertanyaan}\n")

        # RETRIEVE
        query_emb = pseudo_embedding(pertanyaan)
        similarities = []
        for i, chunk_emb in enumerate(chunk_embeddings):
            sim = cosine_similarity(query_emb, chunk_emb)
            similarities.append((i, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)

        print(f"📚 Top {top_k} chunks yang relevan:")
        context = ""
        for idx, sim in similarities[:top_k]:
            chunk = chunks[idx]
            print(f"   [{chunk['index']}] (sim={sim:.3f}) {chunk['text'][:60]}...")
            context += f"\n---\n{chunk['text']}\n"

        # AUGMENT + GENERATE
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "Kamu adalah asisten HR. Jawab berdasarkan dokumen yang diberikan. Bahasa Indonesia."
                },
                {
                    "role": "user",
                    "content": f"Berdasarkan dokumen berikut:\n{context}\n\nJawab: {pertanyaan}"
                }
            ],
            temperature=0.2
        )

        jawaban = response.choices[0].message.content
        print(f"\n💬 Jawaban:\n{jawaban}")
        return jawaban

    # Test
    rag_with_chunks("Kapan gaji dibayarkan?")
    rag_with_chunks("Apa saja fasilitas kantor yang tersedia?")
    rag_with_chunks("Berapa budget training per tahun?")

    # 4. TIPS CHUNKING
    print(f"\n{'='*60}")
    print("4. TIPS & BEST PRACTICES CHUNKING")
    print(f"{'='*60}")

    print("""
    Strategi Chunking:
    ┌────────────────────┬──────────────────────────────────────────┐
    │ Strategi           │ Kapan Digunakan                         │
    ├────────────────────┼──────────────────────────────────────────┤
    │ Fixed Size         │ Dokumen homogen, format seragam         │
    │ Fixed + Overlap    │ Paling umum, cegah konteks terpotong    │
    │ Paragraph-based    │ Dokumen dengan paragraf yang jelas      │
    │ Semantic (Section) │ Dokumen terstruktur (bab, heading)      │
    │ Recursive          │ Coba pemisah besar dulu, lalu kecil     │
    └────────────────────┴──────────────────────────────────────────┘

    Tips:
    - Chunk size 200-1000 karakter (tergantung use case)
    - Overlap 10-20% dari chunk size
    - Sertakan metadata (judul bab, nomor halaman)
    - Test dengan pertanyaan nyata untuk tuning
    """)

    print("✅ Selesai! Memahami RAG dengan chunking.")

if __name__ == "__main__":
    main()
