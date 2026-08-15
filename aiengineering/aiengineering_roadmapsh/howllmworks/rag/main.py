import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n{'='*60}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*60}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"{'='*60}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*65)
        print("=== RAG AI Engineering Learning Project (roadmap.sh) ===")
        print("#"*65)
        print("Pilih modul / point yang ingin Anda jalankan:\n")

        print("[ Point 1: Document Loading & Parsing ]")
        print("  11. Text & Markdown Loader dengan Ekstraksi Metadata  ** tanpa API key")
        print("  12. PDF & HTML Document Parsing                       ** tanpa API key")
        print("  13. Multimodal & Structured Data Preparation          ** tanpa API key")

        print("\n[ Point 2: Chunking Strategies ]")
        print("  21. Fixed-Size & Overlap Chunking                    ** tanpa API key")
        print("  22. Recursive Character Splitting                     ** tanpa API key")
        print("  23. Structural & Semantic Chunking                    ** tanpa API key")

        print("\n[ Point 3: Embeddings & Vectorization ]")
        print("  31. Text Embeddings API Call")
        print("  32. Vector Similarity Metrics (Cosine, Dot, Euclidean) ** tanpa API key")
        print("  33. Normalisasi Vektor & Dimensi                      ** tanpa API key")

        print("\n[ Point 4: Vector Databases & Indexing ]")
        print("  41. Custom In-Memory Vector Store                     ** tanpa API key")
        print("  42. Integrasi ChromaDB Vector Database                ** tanpa API key")
        print("  43. Algoritma Indeks: Flat vs HNSW / ANN               ** tanpa API key")

        print("\n[ Point 5: Retrieval Techniques ]")
        print("  51. Dense Semantic Retrieval                          ** tanpa API key")
        print("  52. Sparse Keyword Retrieval (BM25 & TF-IDF)          ** tanpa API key")
        print("  53. Hybrid Search dengan Reciprocal Rank Fusion (RRF) ** tanpa API key")

        print("\n[ Point 6: Reranking & Context Refinement ]")
        print("  61. Cross-Encoder Reranking Simulation                ** tanpa API key")
        print("  62. Maximal Marginal Relevance (MMR) Diversity        ** tanpa API key")
        print("  63. Context Compression & Filtering                   ** tanpa API key")

        print("\n[ Point 7: Advanced RAG Architectures ]")
        print("  71. Query Transformations (Multi-Query & Sub-Query)")
        print("  72. HyDE (Hypothetical Document Embeddings)")
        print("  73. Agentic RAG & Routing")

        print("\n[ Point 8: Generation & Grounding ]")
        print("  81. Anti-Hallucination RAG Prompting")
        print("  82. Citation & Source Attribution")
        print("  83. Structured RAG Output (JSON Schema)")

        print("\n[ Point 9: Evaluasi & Observability ]")
        print("  91. Evaluasi RAG Triad (LLM-as-a-Judge)")
        print("  92. Logging & Tracing Pipeline Performance           ** tanpa API key")

        print("\n  0. Keluar")

        pilihan = input("\nMasukkan angka pilihan Anda: ").strip()

        scripts_map = {
            '11': "01_document_loading_dan_parsing/1_text_and_markdown_loader.py",
            '12': "01_document_loading_dan_parsing/2_pdf_and_html_parsing.py",
            '13': "01_document_loading_dan_parsing/3_multimodal_data_prep.py",
            '21': "02_chunking_strategies/1_fixed_size_and_overlap.py",
            '22': "02_chunking_strategies/2_recursive_character_chunking.py",
            '23': "02_chunking_strategies/3_semantic_and_structure_chunking.py",
            '31': "03_embeddings_dan_vectorization/1_text_embeddings.py",
            '32': "03_embeddings_dan_vectorization/2_vector_similarity_metrics.py",
            '33': "03_embeddings_dan_vectorization/3_embedding_normalization_and_dimensions.py",
            '41': "04_vector_databases_dan_indexing/1_in_memory_vector_store.py",
            '42': "04_vector_databases_dan_indexing/2_chromadb_integration.py",
            '43': "04_vector_databases_dan_indexing/3_indexing_algorithms.py",
            '51': "05_retrieval_techniques/1_dense_semantic_retrieval.py",
            '52': "05_retrieval_techniques/2_sparse_keyword_retrieval.py",
            '53': "05_retrieval_techniques/3_hybrid_search_rrf.py",
            '61': "06_reranking_dan_context_refinement/1_cross_encoder_reranking.py",
            '62': "06_reranking_dan_context_refinement/2_maximal_marginal_relevance.py",
            '63': "06_reranking_dan_context_refinement/3_context_compression_and_filtering.py",
            '71': "07_advanced_rag_architectures/1_query_transformations.py",
            '72': "07_advanced_rag_architectures/2_hyde_hypothetical_document_embeddings.py",
            '73': "07_advanced_rag_architectures/3_agentic_rag_and_routing.py",
            '81': "08_generation_dan_grounding/1_rag_prompt_templates.py",
            '82': "08_generation_dan_grounding/2_citation_and_source_attribution.py",
            '83': "08_generation_dan_grounding/3_structured_rag_output.py",
            '91': "09_evaluasi_dan_observability/1_rag_triad_evaluation.py",
            '92': "09_evaluasi_dan_observability/2_logging_and_tracing.py",
        }

        if pilihan == '0':
            print("Keluar dari program. Terima kasih dan selamat belajar!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia (misal: 11, 21, 31).")

if __name__ == "__main__":
    main()
