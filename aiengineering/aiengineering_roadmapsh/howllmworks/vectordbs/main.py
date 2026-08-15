import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n{'='*50}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*50}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"{'='*50}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*50)
        print("=== AI Engineering Vector Databases Project ===")
        print("#"*50)
        print("Pilih modul / point yang ingin Anda jalankan:\n")
        
        print("[ Point 1: Embeddings ]")
        print("  11. Apa itu Embedding (Definisi & Konsep)")
        print("  12. Embedding Models (Sentence Transformers, Multilingual, Batch)")

        print("\n[ Point 2: Similarity Search ]")
        print("  21. Similarity Metrics (Cosine, Euclidean, Dot Product)")
        print("  22. Nearest Neighbor Search (Brute Force, IVF, FAISS Indexing)")

        print("\n[ Point 3: Vector Databases (ChromaDB) ]")
        print("  31. ChromaDB Dasar (CRUD, Query, Metadata Filtering)")
        print("  32. ChromaDB Persistent Storage (Persist & Reload Data)")

        print("\n[ Point 4: Chunking Strategies ]")
        print("  41. Chunking Strategies (Fixed-size, Sentence, Paragraph, Recursive)")

        print("\n[ Point 5: RAG Pipeline ]")
        print("  51. End-to-End RAG Pipeline (Ingestion, Retrieval, Generation)")

        print("\n[ Point 6: Optimization & Advanced Techniques ]")
        print("  61. Optimization Techniques (Hybrid Search, Reranking, Caching)")

        print("\n  0. Keluar")
        
        pilihan = input("\nMasukkan angka pilihan Anda: ").strip()
        
        # Mapping input ke path file
        scripts_map = {
            '11': "01-embeddings/1_apa_itu_embedding.py",
            '12': "01-embeddings/2_embedding_models.py",
            '21': "02-similarity/1_similarity_metrics.py",
            '22': "02-similarity/2_nearest_neighbor_search.py",
            '31': "03-vector-databases/1_chromadb_dasar.py",
            '32': "03-vector-databases/2_chromadb_persistent.py",
            '41': "04-chunking/1_chunking_strategies.py",
            '51': "05-rag-pipeline/1_rag_pipeline.py",
            '61': "06-optimization/1_optimization_techniques.py"
        }
        
        if pilihan == '0':
            print("Keluar dari program. Terima kasih!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia (misal: 11, 21, 31).")

if __name__ == "__main__":
    main()
