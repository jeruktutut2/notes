import json

def serialize_table_to_text(table_data: list) -> str:
    """
    Mengubah data tabel (list of dict) menjadi format narasi teks yang optimal untuk embedding RAG.
    Format narasi jauh lebih mudah dipahami oleh Embedding Model daripada raw JSON/CSV.
    """
    serialized_sentences = []
    for row in table_data:
        items = [f"{k}: {v}" for k, v in row.items()]
        sentence = "Entitas Data [" + ", ".join(items) + "]."
        serialized_sentences.append(sentence)
    return "\n".join(serialized_sentences)

def serialize_json_to_markdown_doc(json_obj: dict) -> str:
    """Mengubah objek JSON berstruktur menjadi dokumen Markdown ber-metadata."""
    lines = ["# Dokumentasi Data Produk\n"]
    for category, details in json_obj.items():
        lines.append(f"## Kategori: {category}")
        if isinstance(details, list):
            for item in details:
                lines.append(f"- {item}")
        elif isinstance(details, dict):
            for k, v in details.items():
                lines.append(f"- **{k}**: {v}")
        lines.append("")
    return "\n".join(lines)

def main():
    print("=== 03. Data Preparation: Structured & Multimodal Data ===")

    # Contoh 1: Data Tabel Produk
    product_table = [
        {"id": "PROD-01", "nama": "Laptop AI Pro", "harga": "Rp 18.000.000", "stok": 15, "kategori": "Elektronik"},
        {"id": "PROD-02", "nama": "Monitor 4K HDR", "harga": "Rp 5.500.000", "stok": 8, "kategori": "Periferal"},
    ]

    print("\n1. Serialisasi Data Tabel ke Format Narasi RAG:")
    narrative_output = serialize_table_to_text(product_table)
    print(narrative_output)

    # Contoh 2: Data JSON Hierarki API Response
    api_data = {
        "Sistem": {
            "status": "Aktif",
            "versi": "v2.4.1",
            "region": "ap-southeast-1"
        },
        "Fitur_Unggulan": [
            "Vector Search HNSW",
            "Hybrid Retrieval BM25",
            "Auto Reranking Cross-Encoder"
        ]
    }

    print("\n2. Serialisasi JSON ke Format Markdown Dokumentasi:")
    md_output = serialize_json_to_markdown_doc(api_data)
    print(md_output)

if __name__ == "__main__":
    main()
