def route_query(query: str) -> str:
    """
    Router Decision Engine:
    Menganalisis intent query dan menentukan target retrieval (Vector DB internal vs Web Search vs SQL DB).
    """
    q_lower = query.lower()
    if any(k in q_lower for k in ["harga", "stok", "transaksi", "laporan"]):
        return "SQL_RELATIONAL_DATABASE"
    elif any(k in q_lower for k in ["kebijakan", "sop", "panduan", "arsitektur", "rag"]):
        return "VECTOR_DB_INTERNAL_DOCS"
    elif any(k in q_lower for k in ["cuaca", "berita", "hari ini", "terbaru"]):
        return "WEB_SEARCH_ENGINE"
    else:
        return "VECTOR_DB_INTERNAL_DOCS"

def execute_agentic_rag(query: str):
    target_destination = route_query(query)

    print(f"Query  : '{query}'")
    print(f"Route  : -> Destinasi terpilih: [{target_destination}]")

    if target_destination == "VECTOR_DB_INTERNAL_DOCS":
        return "Mengambil dokumen dari Vector Database internal perusahaan..."
    elif target_destination == "SQL_RELATIONAL_DATABASE":
        return "Menjalankan kueri SQL 'SELECT * FROM products WHERE ...'"
    elif target_destination == "WEB_SEARCH_ENGINE":
        return "Melakukan pencarian web real-time melalui SerpAPI / Tavily..."

def main():
    print("=== 03. Advanced RAG: Router RAG & Agentic Routing ===")

    test_queries = [
        "Bagaimana SOP pengajuan cuti karyawan?",
        "Berapa sisa stok laptop AI Pro bulan ini?",
        "Siapa pemenang pertandingan sepak bola tadi malam?"
    ]

    for q in test_queries:
        res = execute_agentic_rag(q)
        print(f"Action : {res}\n")

if __name__ == "__main__":
    main()
