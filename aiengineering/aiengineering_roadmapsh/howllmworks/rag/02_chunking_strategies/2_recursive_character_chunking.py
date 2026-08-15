class RecursiveCharacterTextSplitter:
    def __init__(self, chunk_size: int = 200, chunk_overlap: int = 30, separators: list = None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or ["\n\n", "\n", ". ", " ", ""]

    def split_text(self, text: str) -> list:
        final_chunks = []
        # Pilih separator pertama yang cocok
        separator = self.separators[-1]
        for s in self.separators:
            if s == "":
                separator = s
                break
            if s in text:
                separator = s
                break

        # Potong berdasarkan separator
        splits = text.split(separator) if separator != "" else list(text)

        good_splits = []
        for s in splits:
            if len(s) < self.chunk_size:
                good_splits.append(s)
            else:
                if good_splits:
                    merged = self._merge_splits(good_splits, separator)
                    final_chunks.extend(merged)
                    good_splits = []
                # Sub-split jika fragmen masih terlalu besar
                sub_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap,
                    separators=[sep for sep in self.separators if sep != separator] or [""]
                )
                final_chunks.extend(sub_splitter.split_text(s))

        if good_splits:
            merged = self._merge_splits(good_splits, separator)
            final_chunks.extend(merged)

        return final_chunks

    def _merge_splits(self, splits: list, separator: str) -> list:
        docs = []
        current_chunk = []
        current_len = 0

        for split in splits:
            len_split = len(split)
            if current_len + len_split + len(separator) > self.chunk_size:
                if current_chunk:
                    doc = separator.join(current_chunk)
                    docs.append(doc)
                    # Handle overlap
                    while current_len > self.chunk_overlap and len(current_chunk) > 1:
                        removed = current_chunk.pop(0)
                        current_len -= (len(removed) + len(separator))
            current_chunk.append(split)
            current_len += len_split + len(separator)

        if current_chunk:
            docs.append(separator.join(current_chunk))
        return docs

def main():
    print("=== 02. Chunking: Recursive Character Splitting ===")

    document = (
        "Paragraf 1: Pengenalan Vector Database.\nVector Database adalah database khusus yang dioptimalkan "
        "untuk menyimpan dan mengkueri data vektor berdimensi tinggi secara efisien.\n\n"
        "Paragraf 2: Pentingnya Chunking.\nSebelum dokumen dimasukkan ke dalam Vector Database, "
        "dokumen harus dipecah menjadi potongan-potongan kecil yang disebut chunk. "
        "Pemotongan berstruktur hierarki menjaga batas alami paragraf dan kalimat.\n\n"
        "Paragraf 3: Kesimpulan.\nStrategi chunking hierarkis mencegah terpisahnya kata-kata kunci utama."
    )

    splitter = RecursiveCharacterTextSplitter(chunk_size=180, chunk_overlap=30)
    chunks = splitter.split_text(document)

    print(f"Jumlah Chunk Dihasilkan: {len(chunks)}\n")
    for idx, c in enumerate(chunks, 1):
        print(f"--- Chunk #{idx} (Length: {len(c)}) ---")
        print(f"\"{c}\"\n")

if __name__ == "__main__":
    main()
