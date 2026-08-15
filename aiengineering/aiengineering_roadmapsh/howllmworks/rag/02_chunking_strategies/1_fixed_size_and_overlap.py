def fixed_size_chunking(text: str, chunk_size: int = 100, chunk_overlap: int = 20) -> list:
    """
    Memotong teks menjadi chunk dengan ukuran tetap (karakter) dan overlap.
    """
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap harus lebih kecil dari chunk_size")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({
            "chunk_id": len(chunks) + 1,
            "text": chunk,
            "start_idx": start,
            "end_idx": end
        })
        start += (chunk_size - chunk_overlap)

    return chunks

def main():
    print("=== 01. Chunking: Fixed-Size & Overlap ===")

    sample_text = (
        "Retrieval-Augmented Generation (RAG) adalah arsitektur yang sangat populer dalam AI Engineering. "
        "Dengan RAG, Large Language Model (LLM) dapat mengakses pengetahuan eksternal dari Vector Database. "
        "Proses chunking yang tepat sangat menentukan presisi pencarian dokumen dan relevansi jawaban LLM. "
        "Overlap antar chunk memastikan tidak ada informasi penting yang terpotong di tengah kalimat."
    )

    chunk_size = 120
    overlap = 30

    print(f"Panjang Teks Asli: {len(sample_text)} karakter")
    print(f"Konfigurasi: Chunk Size = {chunk_size}, Overlap = {overlap}\n")

    chunks = fixed_size_chunking(sample_text, chunk_size=chunk_size, chunk_overlap=overlap)

    for c in chunks:
        print(f"--- Chunk #{c['chunk_id']} (Index {c['start_idx']}:{c['end_idx']}) ---")
        print(f"\"{c['text']}\"")
        print(f"Panjang: {len(c['text'])} karakter\n")

if __name__ == "__main__":
    main()
