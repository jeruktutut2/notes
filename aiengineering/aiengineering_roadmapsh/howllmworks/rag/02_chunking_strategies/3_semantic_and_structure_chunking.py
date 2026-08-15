import re

def markdown_header_chunking(md_text: str) -> list:
    """
    Memotong dokumen Markdown berdasarkan struktur Header (#, ##, ###).
    """
    lines = md_text.splitlines()
    chunks = []
    current_header = "Header Utama"
    current_content = []

    header_pattern = re.compile(r'^(#{1,6})\s+(.+)$')

    for line in lines:
        match = header_pattern.match(line)
        if match:
            if current_content:
                chunks.append({
                    "header": current_header,
                    "text": "\n".join(current_content).strip()
                })
                current_content = []
            current_header = match.group(2)
        else:
            current_content.append(line)

    if current_content:
        chunks.append({
            "header": current_header,
            "text": "\n".join(current_content).strip()
        })

    return [c for c in chunks if c["text"]]

def simulate_semantic_chunking(sentences: list, similarity_threshold: float = 0.5) -> list:
    """
    Simulasi Semantic Chunking: menggabungkan kalimat-kalimat yang berdekatan secara topik,
    dan membuat chunk baru saat terjadi shift topik (perubahan similaritas).
    """
    # Simulasi skor similaritas antar kalimat berurutan
    # Skor rendah mengindikasikan perubahan topik
    topic_change_indices = [2, 5] # Misal perubahan topik terjadi setelah kalimat 2 dan 5

    chunks = []
    current_chunk = []

    for idx, sentence in enumerate(sentences):
        current_chunk.append(sentence)
        if idx in topic_change_indices or idx == len(sentences) - 1:
            chunks.append(" ".join(current_chunk))
            current_chunk = []

    return chunks

def main():
    print("=== 03. Chunking: Structural & Semantic Chunking ===")

    # 1. Structural Markdown Chunking Demo
    sample_md = """# Panduan RAG System

## 1. Document Ingestion
Tahap pertama adalah memuat dokumen teks dari berbagai sumber data.

## 2. Vector Indexing
Tahap kedua adalah mengubah dokumen menjadi vektor dense dan menyimpannya di DB.

### 2.1 HNSW Algorithm
HNSW adalah algoritma graf bertingkat untuk pencarian nearest neighbor ter-akselerasi.
"""

    print("\n1. Hasil Markdown Structural Chunking:")
    md_chunks = markdown_header_chunking(sample_md)
    for c in md_chunks:
        print(f"  [Header: '{c['header']}']")
        print(f"   Text: {c['text'][:80]}...\n")

    # 2. Semantic Chunking Demo
    sentences = [
        "Python adalah bahasa pemrogramaan populer untuk AI.",
        "Library seperti NumPy dan PyTorch sangat banyak digunakan.",
        "Model Transformer mengubah lanskap pemrosesan bahasa alami.",
        "Resep membuat nasi goreng spesial memerlukan bumbu dapur.",
        "Bawang merah dan bawang putih ditumis hingga harum.",
        "Kembali ke dunia komputasi, GPU mempercepat pelatihan model."
    ]

    print("2. Hasil Semantic Chunking (Perubahan Topik):")
    semantic_chunks = simulate_semantic_chunking(sentences)
    for i, sc in enumerate(semantic_chunks, 1):
        print(f"  --- Semantic Chunk #{i} ---")
        print(f"  \"{sc}\"\n")

if __name__ == "__main__":
    main()
