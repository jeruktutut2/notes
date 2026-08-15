"""
07_llamaindex_multimodal.py
Modul Task & SDK: LlamaIndex for Multimodal Apps (MultiModalVectorStoreIndex & Query Engine)
"""

def simulate_llamaindex_multimodal_indexing():
    """Simulasi pengindeksan dokumen teks dan gambar menggunakan MultiModalVectorStoreIndex di LlamaIndex."""
    print("🦙 [LlamaIndex SDK] Menginisialisasi MultiModalVectorStoreIndex...")
    print("📁 Loading Documents & Images via SimpleDirectoryReader...")
    
    indexed_documents = [
        {"type": "TextDocument", "doc_id": "doc_01", "content": "Spesifikasi Teknis Kamera AI Vision Pro 2026"},
        {"type": "ImageDocument", "doc_id": "img_01", "path": "./data/images/diagram_hardware.png"},
        {"type": "ImageDocument", "doc_id": "img_02", "path": "./data/images/schematics.png"}
    ]
    
    print("🧠 Menghitung Embedding:")
    print("   • Text Embedding Model  : text-embedding-3-small (Dimensions: 1536)")
    print("   • Image Embedding Model : CLIP ViT-B/32 (Dimensions: 512)")
    print(f"📊 Storage Index Selesai: {len(indexed_documents)} item diindeks ke Vector Store.")
    return indexed_documents

def simulate_llamaindex_multimodal_query_engine(query_str: str) -> dict:
    """Simulasi query silang modalitas (Cross-modal Retrieval) dengan SimpleMultiModalQueryEngine."""
    print(f"\n🔍 [LlamaIndex Query Engine] Executing Query: '{query_str}'")
    print("   1. Retrieving top-k text nodes via Text Vector Index.")
    print("   2. Retrieving top-k image nodes via Image Vector Index.")
    print("   3. Synthesizing response using GPT-4o MultiModal LLM.")
    
    response = {
        "query": query_str,
        "retrieved_images": ["./data/images/diagram_hardware.png"],
        "retrieved_texts": ["Spesifikasi Teknis Kamera AI Vision Pro 2026"],
        "response_text": (
            "Berdasarkan dokumen dan diagram hardware yang ditemukan (img_01), "
            "Kamera AI Vision Pro mendukung pemrosesan 60 FPS pada resolusi 4K dengan sensor optik ganda."
        )
    }
    return response

def main():
    print("=" * 70)
    print("🦙 MODUL SDK 07: LLAMAINDEX FOR MULTIMODAL APPS")
    print("=" * 70)

    # 1. Indexing
    print("\n1. Pengindeksan Vektor Multimodal:")
    indexed_docs = simulate_llamaindex_multimodal_indexing()

    # 2. Query Execution
    print("\n2. Eksekusi Multimodal Query Engine:")
    query_result = simulate_llamaindex_multimodal_query_engine("Apa keunggulan spesifikasi hardware kamera ini?")
    
    print("\n💡 Response Synthesis:")
    print(f"   \"{query_result['response_text']}\"")
    print(f"🖼️ Linked Visual Evidence: {query_result['retrieved_images']}")

    print("\n✅ Modul LlamaIndex for Multimodal Apps Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
