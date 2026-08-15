"""
=================================================================
1. CHUNKING STRATEGIES
=================================================================
Chunking = memecah dokumen besar menjadi potongan kecil (chunks)
sebelum dikonversi menjadi embedding dan disimpan ke vector DB.

Mengapa penting?
- Model embedding punya batas input (misal 512 token)
- Chunk kecil → pencarian lebih presisi
- Chunk besar → konteks lebih lengkap tapi kurang fokus

Strategi Chunking:
┌──────────────────┬────────────────────┬───────────────────┐
│ Strategi         │ Konsistensi Ukuran │ Kualitas Konteks  │
├──────────────────┼────────────────────┼───────────────────┤
│ Fixed-size       │ ⭐⭐⭐⭐⭐             │ ⭐⭐                │
│ Sentence-based   │ ⭐⭐⭐                │ ⭐⭐⭐               │
│ Paragraph-based  │ ⭐⭐                 │ ⭐⭐⭐⭐              │
│ Recursive        │ ⭐⭐⭐⭐              │ ⭐⭐⭐⭐              │
│ Semantic         │ ⭐⭐⭐                │ ⭐⭐⭐⭐⭐             │
└──────────────────┴────────────────────┴───────────────────┘
=================================================================
"""

import re

# Contoh dokumen panjang untuk demo
DOKUMEN_CONTOH = """
Kecerdasan Buatan (Artificial Intelligence / AI)

Kecerdasan buatan adalah cabang ilmu komputer yang bertujuan menciptakan mesin yang mampu melakukan tugas-tugas yang biasanya memerlukan kecerdasan manusia. AI mencakup berbagai subdisiplin seperti machine learning, natural language processing, computer vision, dan robotika.

Machine Learning

Machine learning adalah subset dari AI yang memungkinkan komputer untuk belajar dari data tanpa diprogram secara eksplisit. Algoritma ML dapat menemukan pola dalam data dan membuat prediksi. Contoh algoritma ML termasuk decision tree, random forest, support vector machine, dan neural network.

Supervised learning menggunakan data berlabel untuk melatih model. Contohnya adalah klasifikasi email spam dan prediksi harga rumah. Unsupervised learning bekerja dengan data tanpa label, seperti clustering pelanggan dan deteksi anomali.

Deep Learning

Deep learning adalah subset dari machine learning yang menggunakan jaringan saraf tiruan (neural network) dengan banyak lapisan (layer). Arsitektur deep learning yang populer antara lain:

CNN (Convolutional Neural Network) digunakan untuk pengolahan gambar dan video. CNN bekerja dengan mendeteksi fitur visual seperti garis, tepi, dan pola. Aplikasi CNN meliputi pengenalan wajah, klasifikasi gambar, dan deteksi objek.

RNN (Recurrent Neural Network) cocok untuk data sekuensial seperti teks dan time series. LSTM dan GRU adalah varian RNN yang mengatasi masalah vanishing gradient. Aplikasi RNN meliputi terjemahan bahasa dan prediksi saham.

Transformer adalah arsitektur terbaru yang merevolusi NLP. Model berbasis Transformer seperti BERT, GPT, dan T5 mencapai performa state-of-the-art di berbagai tugas NLP. Transformer menggunakan mekanisme attention yang memungkinkan model untuk memperhatikan seluruh konteks input secara paralel.

Natural Language Processing (NLP)

NLP adalah cabang AI yang berhubungan dengan interaksi antara komputer dan bahasa manusia. Tugas-tugas NLP meliputi sentiment analysis, named entity recognition, question answering, dan text summarization. Dengan kemajuan model bahasa besar (Large Language Model / LLM), NLP telah mengalami perkembangan yang sangat pesat.
""".strip()


def demo_fixed_size_chunking():
    """Demo: Fixed-size chunking."""
    print("=" * 60)
    print("DEMO 1: Fixed-Size Chunking")
    print("=" * 60)

    chunk_size = 200
    overlap = 50

    print(f"\n📏 Konfigurasi: chunk_size={chunk_size}, overlap={overlap}")
    print(f"📄 Panjang dokumen: {len(DOKUMEN_CONTOH)} karakter\n")

    chunks = []
    start = 0
    while start < len(DOKUMEN_CONTOH):
        end = start + chunk_size
        chunk = DOKUMEN_CONTOH[start:end]
        chunks.append(chunk)
        start = end - overlap

    print(f"📊 Hasil: {len(chunks)} chunks")
    print("-" * 60)
    for i, chunk in enumerate(chunks):
        # Tampilkan preview
        preview = chunk.strip().replace('\n', ' ')[:70]
        print(f"   Chunk {i+1:>2} ({len(chunk):>3} chars): \"{preview}...\"")

    print(f"\n⚠️ Masalah Fixed-Size:")
    print("   - Bisa memotong di tengah kata atau kalimat")
    print("   - Konteks bisa terpecah")
    print("   ✅ Kelebihan: Ukuran chunk sangat konsisten")


def demo_sentence_chunking():
    """Demo: Sentence-based chunking."""
    print("\n\n" + "=" * 60)
    print("DEMO 2: Sentence-Based Chunking")
    print("=" * 60)

    sentences_per_chunk = 3
    overlap_sentences = 1

    print(f"\n📏 Konfigurasi: {sentences_per_chunk} kalimat/chunk, overlap {overlap_sentences}")

    # Split berdasarkan kalimat (titik diikuti spasi/newline)
    sentences = re.split(r'(?<=[.!?])\s+', DOKUMEN_CONTOH.strip())
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]

    print(f"   Total kalimat terdeteksi: {len(sentences)}")

    chunks = []
    start = 0
    while start < len(sentences):
        end = min(start + sentences_per_chunk, len(sentences))
        chunk = ' '.join(sentences[start:end])
        chunks.append(chunk)
        start = end - overlap_sentences
        if start <= end - sentences_per_chunk:
            break

    print(f"\n📊 Hasil: {len(chunks)} chunks")
    print("-" * 60)
    for i, chunk in enumerate(chunks):
        preview = chunk.replace('\n', ' ')[:80]
        print(f"   Chunk {i+1:>2} ({len(chunk):>3} chars): \"{preview}...\"")

    print(f"\n✅ Kelebihan Sentence-Based:")
    print("   - Tidak memotong di tengah kalimat")
    print("   - Konteks per kalimat terjaga")
    print("   ⚠️ Kelemahan: Ukuran chunk bisa bervariasi")


def demo_paragraph_chunking():
    """Demo: Paragraph-based chunking."""
    print("\n\n" + "=" * 60)
    print("DEMO 3: Paragraph-Based Chunking")
    print("=" * 60)

    # Split berdasarkan paragraf (baris kosong)
    paragraphs = DOKUMEN_CONTOH.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]

    print(f"\n📄 Total paragraf terdeteksi: {len(paragraphs)}")
    print(f"\n📊 Hasil (setiap paragraf = 1 chunk):")
    print("-" * 60)
    for i, para in enumerate(paragraphs):
        preview = para.replace('\n', ' ')[:75]
        print(f"   Chunk {i+1:>2} ({len(para):>4} chars): \"{preview}...\"")

    # Gabungkan paragraf yang terlalu pendek
    print(f"\n📊 Dengan penggabungan (min 200 chars):")
    print("-" * 60)
    min_length = 200
    merged_chunks = []
    current = ""
    for para in paragraphs:
        if len(current) + len(para) < min_length:
            current = current + "\n\n" + para if current else para
        else:
            if current:
                merged_chunks.append(current)
            current = para
    if current:
        merged_chunks.append(current)

    for i, chunk in enumerate(merged_chunks):
        preview = chunk.replace('\n', ' ')[:75]
        print(f"   Chunk {i+1:>2} ({len(chunk):>4} chars): \"{preview}...\"")

    print(f"\n✅ Kelebihan Paragraph-Based:")
    print("   - Konteks per topik terjaga dengan baik")
    print("   ⚠️ Kelemahan: Ukuran sangat bervariasi")


def demo_recursive_chunking():
    """Demo: Recursive character text splitting (seperti LangChain)."""
    print("\n\n" + "=" * 60)
    print("DEMO 4: Recursive Character Splitting")
    print("=" * 60)

    chunk_size = 300
    print(f"\n📏 Konfigurasi: chunk_size={chunk_size}")
    print("   Separator hierarchy: [paragraph] → [newline] → [sentence] → [space]")

    def recursive_split(text, chunk_size, separators=None):
        if separators is None:
            separators = ["\n\n", "\n", ". ", " "]

        if len(text) <= chunk_size:
            return [text]

        # Cari separator yang cocok
        separator = separators[-1]
        for sep in separators:
            if sep in text:
                separator = sep
                break

        parts = text.split(separator)
        chunks = []
        current = ""

        for part in parts:
            candidate = current + separator + part if current else part
            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                if len(part) > chunk_size and len(separators) > 1:
                    sub_chunks = recursive_split(part, chunk_size, separators[1:])
                    chunks.extend(sub_chunks)
                    current = ""
                else:
                    current = part
        if current:
            chunks.append(current)

        return chunks

    chunks = recursive_split(DOKUMEN_CONTOH, chunk_size)

    print(f"\n📊 Hasil: {len(chunks)} chunks")
    print("-" * 60)
    for i, chunk in enumerate(chunks):
        preview = chunk.strip().replace('\n', ' ')[:70]
        print(f"   Chunk {i+1:>2} ({len(chunk):>4} chars): \"{preview}...\"")

    print(f"\n✅ Kelebihan Recursive:")
    print("   - Mencoba separator terbaik secara bertingkat")
    print("   - Balance antara ukuran konsisten dan konteks terjaga")
    print("   - Ini strategi DEFAULT yang direkomendasikan!")


def demo_perbandingan():
    """Demo: perbandingan semua strategi."""
    print("\n\n" + "=" * 60)
    print("DEMO 5: Perbandingan Semua Strategi")
    print("=" * 60)

    print(f"\n📄 Dokumen: {len(DOKUMEN_CONTOH)} karakter")
    print("-" * 65)
    print(f"   {'Strategi':<20} {'Chunks':>8} {'Min Chars':>10} {'Max Chars':>10} {'Avg Chars':>10}")
    print("-" * 65)

    # Fixed-size
    chunks = []
    start = 0
    while start < len(DOKUMEN_CONTOH):
        chunks.append(DOKUMEN_CONTOH[start:start+300])
        start += 250
    lens = [len(c) for c in chunks]
    print(f"   {'Fixed (300/50)':<20} {len(chunks):>8} {min(lens):>10} {max(lens):>10} {sum(lens)//len(lens):>10}")

    # Sentence
    sents = re.split(r'(?<=[.!?])\s+', DOKUMEN_CONTOH.strip())
    sents = [s.strip() for s in sents if s.strip() and len(s.strip()) > 10]
    chunks = []
    for si in range(0, len(sents), 3):
        chunks.append(' '.join(sents[si:si+3]))
    lens = [len(c) for c in chunks]
    print(f"   {'Sentence (3/grp)':<20} {len(chunks):>8} {min(lens):>10} {max(lens):>10} {sum(lens)//len(lens):>10}")

    # Paragraph
    paras = [p.strip() for p in DOKUMEN_CONTOH.split('\n\n') if p.strip()]
    lens = [len(p) for p in paras]
    print(f"   {'Paragraph':<20} {len(paras):>8} {min(lens):>10} {max(lens):>10} {sum(lens)//len(lens):>10}")

    # Recursive
    def recursive_split(text, sz, seps=None):
        if seps is None:
            seps = ["\n\n", "\n", ". ", " "]
        if len(text) <= sz:
            return [text]
        sep = seps[-1]
        for s in seps:
            if s in text:
                sep = s
                break
        parts = text.split(sep)
        chunks, cur = [], ""
        for part in parts:
            cand = cur + sep + part if cur else part
            if len(cand) <= sz:
                cur = cand
            else:
                if cur:
                    chunks.append(cur)
                if len(part) > sz and len(seps) > 1:
                    chunks.extend(recursive_split(part, sz, seps[1:]))
                    cur = ""
                else:
                    cur = part
        if cur:
            chunks.append(cur)
        return chunks

    chunks = recursive_split(DOKUMEN_CONTOH, 300)
    lens = [len(c) for c in chunks]
    print(f"   {'Recursive (300)':<20} {len(chunks):>8} {min(lens):>10} {max(lens):>10} {sum(lens)//len(lens):>10}")

    print(f"\n💡 Rekomendasi:")
    print("   - Untuk kebanyakan kasus → gunakan Recursive (chunk_size=300-500)")
    print("   - Untuk FAQ / data pendek → gunakan Sentence-based")
    print("   - Untuk dokumen terstruktur → gunakan Paragraph-based")
    print("   - Selalu tambahkan overlap (10-20%) agar konteks tidak hilang")


def main():
    demo_fixed_size_chunking()
    demo_sentence_chunking()
    demo_paragraph_chunking()
    demo_recursive_chunking()
    demo_perbandingan()
    print("\n\n✅ Selesai! Lanjut ke modul berikutnya: 05_rag_pipeline/")


if __name__ == "__main__":
    main()
