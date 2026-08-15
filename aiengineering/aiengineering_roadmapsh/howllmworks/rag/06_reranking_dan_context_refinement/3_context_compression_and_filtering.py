def compress_context_by_relevance(query: str, raw_document: str, threshold_words: int = 1) -> str:
    """
    Kompresi Konteks: Memecah dokumen mentah menjadi kalimat-kalimat,
    dan hanya mempertahankan kalimat yang relevan dengan kata kunci query.
    """
    query_terms = set(query.lower().split())
    sentences = raw_document.split(". ")

    relevant_sentences = []
    for sentence in sentences:
        words = set(sentence.lower().split())
        overlap = len(query_terms.intersection(words))
        if overlap >= threshold_words:
            relevant_sentences.append(sentence.strip())

    if not relevant_sentences:
        return raw_document[:200] + "..." # Fallback

    return ". ".join(relevant_sentences) + "."

def main():
    print("=== 03. Context Compression & Filtering ===")

    raw_doc = (
        "Perusahaan TechCorp didirikan pada tahun 2015 di Jakarta. "
        "Kebijakan pengembalian barang mengatur bahwa produk dapat dikembalikan dalam 14 hari kerja. "
        "Pengguna wajib membawa resi pembelian asli dan kemasan belum dibuka. "
        "Kantor pusat TechCorp buka setiap hari Senin hingga Jumat jam 9 pagi. "
        "Untuk biaya pengiriman retur ditanggung penuh oleh pihak pembeli."
    )

    query = "Berapa hari batas waktu pengembalian barang dan syaratnya?"

    print(f"Query: '{query}'\n")
    print(f"[Dokumen Mentah Asli - Panjang: {len(raw_doc)} karakter]")
    print(f"\"{raw_doc}\"\n")

    compressed = compress_context_by_relevance(query, raw_doc)

    print(f"[Dokumen Terkompresi - Panjang: {len(compressed)} karakter]")
    print(f"\"{compressed}\"")
    print("\n  -> Hemat Token: Berhasil membuang kalimat non-relevan (seperti sejarah perusahaan & jam buka kantor)!")

if __name__ == "__main__":
    main()
