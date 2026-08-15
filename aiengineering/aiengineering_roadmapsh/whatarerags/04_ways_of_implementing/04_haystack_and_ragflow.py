"""
04_haystack_and_ragflow.py
Demonstrasi & Tinjauan Arsitektur Haystack (Deepset) dan RAGFlow (Agentic Deep Document Parsing)
"""

def run_haystack_ragflow_demo():
    print("=" * 70)
    print("🌾 & 🌊 DEMONSTRASI HAYSTACK & RAGFLOW")
    print("=" * 70)
    
    print("\n1. 🌾 HAYSTACK BY DEEPSET (Pipeline & Node Architecture):")
    print("   • Pendekatan: Menggunakan Pipeline eksplisit yang dihubungkan dengan Nodes.")
    print("   • Komponen Pipeline: DocumentCleaner ➔ DocumentSplitter ➔ DocumentEmbedder ➔ InMemoryDocumentStore ➔ PromptBuilder ➔ OpenAIGenerator")
    print("   • Keunggulan: Sangat modular, transparan dalam debugging, cocok untuk produksi skala besar.")
    
    print("\n2. 🌊 RAGFLOW (Agentic RAG & Deep Document Parsing):")
    print("   • Pendekatan: Berfokus pada ekstraksi dokumen tingkat lanjut (*Deep Document Parsing*).")
    print("   • Fitur Utama: Memahami layout PDF rumit (tabel, grafik, rumus, multi-kolom) tanpa merusak konteks.")
    print("   • Agentic Workflow: Mengintegrasikan alur kerja agen visual untuk pengambilan keputusan multi-langkah.")
    
    print("=" * 70)

if __name__ == "__main__":
    run_haystack_ragflow_demo()
