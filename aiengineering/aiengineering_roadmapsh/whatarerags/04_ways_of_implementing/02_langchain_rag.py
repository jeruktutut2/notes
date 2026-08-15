"""
02_langchain_rag.py
Demonstrasi RAG Menggunakan LangChain Framework (RecursiveCharacterTextSplitter, VectorStores, Retrieval Chains)
"""

import sys

def run_langchain_demo():
    print("=" * 70)
    print("🦜🔗 DEMONSTRASI RAG MENGGUNAKAN LANGCHAIN FRAMEWORK")
    print("=" * 70)
    
    print("📌 Arsitektur LangChain RAG:")
    print("   DocumentLoader ➔ RecursiveCharacterTextSplitter ➔ VectorStore ➔ RetrievalQA Chain")
    print("-" * 50)
    
    # Try importing langchain if available, else show simulated output
    try:
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text = "LangChain menyediakan abstraksi komprehensif untuk RAG pipeline, termasuk document loader dan vector store retriever."
        splitter = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
        docs = splitter.create_documents([text])
        print(f"✅ LangChain terinstall! Hasil splitting ({len(docs)} chunks):")
        for i, d in enumerate(docs, 1):
            print(f"   [Chunk {i}] {d.page_content}")
    except ImportError:
        print("💡 (Simulasi LangChain Framework - Install 'langchain' untuk mode penuh)")
        print("   1. Document Splitter: RecursiveCharacterTextSplitter(chunk_size=100, overlap=20)")
        print("   2. VectorStore: Chroma.from_documents(docs, embedding_model)")
        print("   3. Retriever: vectorstore.as_retriever(search_type='similarity', search_kwargs={'k': 3})")
        print("   4. Chain: RetrievalQA.from_chain_type(llm, chain_type='stuff', retriever=retriever)")
        
    print("=" * 70)

if __name__ == "__main__":
    run_langchain_demo()
