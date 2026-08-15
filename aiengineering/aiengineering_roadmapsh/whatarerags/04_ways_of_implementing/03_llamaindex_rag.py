"""
03_llamaindex_rag.py
Demonstrasi RAG Menggunakan LlamaIndex Framework (VectorStoreIndex, QueryEngine, Data Connectors)
"""

import sys

def run_llamaindex_demo():
    print("=" * 70)
    print("🦙 DEMONSTRASI RAG MENGGUNAKAN LLAMAINDEX FRAMEWORK")
    print("=" * 70)
    
    print("📌 Arsitektur LlamaIndex RAG:")
    print("   SimpleDirectoryReader ➔ VectorStoreIndex ➔ QueryEngine ➔ ResponseSynthesizer")
    print("-" * 50)
    
    try:
        from llama_index.core import Document, VectorStoreIndex
        print("✅ LlamaIndex terinstall!")
        doc = Document(text="LlamaIndex adalah framework berorientasi data yang mengoptimalkan pembuatan indeks dokumen dan query engine.")
        print(f"   Document ID: {doc.doc_id}")
    except ImportError:
        print("💡 (Simulasi LlamaIndex Framework - Install 'llama-index-core' untuk mode penuh)")
        print("   1. Data Connector: SimpleDirectoryReader('./data').load_data()")
        print("   2. Index Building: index = VectorStoreIndex.from_documents(documents)")
        print("   3. Query Engine: query_engine = index.as_query_engine(similarity_top_k=3)")
        print("   4. Response: response = query_engine.query('Apa keunggulan LlamaIndex?')")
        
    print("=" * 70)

if __name__ == "__main__":
    run_llamaindex_demo()
