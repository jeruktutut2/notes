#!/usr/bin/env python3
"""
Modul: RAG & Dynamic Filters
Simulasi Metadata Filtering + Dense Retrieval untuk menyusun RAG Context secara dinamis.
"""

import json

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

# Simulated Vector DB Index with Metadata
DOCUMENT_DATABASE = [
    {"id": 101, "tenant": "BANK_ABC", "category": "KREDIT", "content": "Bunga KPR BANK ABC adalah 4.5% fixed 3 tahun.", "year": 2026},
    {"id": 102, "tenant": "BANK_XYZ", "category": "KREDIT", "content": "Bunga KPR BANK XYZ adalah 7.2% floating.", "year": 2026},
    {"id": 103, "tenant": "BANK_ABC", "category": "TABUNGAN", "content": "Setoran awal Tabungan Utama BANK ABC minimal Rp 50.000.", "year": 2025},
]

def retrieve_with_dynamic_filter(query: str, tenant_filter: str, category_filter: str):
    """Filter metadata secara eksplisit sebelum melakukan pencarian vektor"""
    filtered_results = []
    for doc in DOCUMENT_DATABASE:
        if doc["tenant"] == tenant_filter and doc["category"] == category_filter:
            filtered_results.append(doc)
    return filtered_results

def main():
    print("=" * 70)
    print(color("  MODUL: RAG & DYNAMIC METADATA FILTERS", "1;34"))
    print("=" * 70)

    user_query = "Berapa suku bunga KPR yang berlaku?"
    tenant_id = "BANK_ABC"
    category = "KREDIT"

    print(color(f"\n1. QUERY: '{user_query}'", "1;33"))
    print(f"Dynamic Metadata Filter Applied -> Tenant: '{tenant_id}', Category: '{category}'")

    retrieved_docs = retrieve_with_dynamic_filter(user_query, tenant_id, category)
    print(color("\n2. FILTERED RAG RETRIEVAL RESULTS:", "1;32"))
    print(json.dumps(retrieved_docs, indent=2))

    assembled_rag_context = f"""<rag_retrieved_documents>
Dokumen #{retrieved_docs[0]['id']} ({retrieved_docs[0]['tenant']}): {retrieved_docs[0]['content']}
</rag_retrieved_documents>

<user_query>
{user_query}
</user_query>"""

    print(color("\n3. ASSEMBLED RAG CONTEXT FOR LLM:", "1;33"))
    print(assembled_rag_context)

    print("\n" + "=" * 70)
    print("✓ Dynamic Metadata Filtering mencegah kebocoran data antar-tenant dan membuang 90% pencarian sampah.")

if __name__ == "__main__":
    main()
