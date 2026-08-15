"""
main.py
Master Interactive CLI Runner & Test Suite for 'What Are RAGs' Workspace
"""

import sys
import subprocess
import os

SCRIPTS = [
    ("01. RAG Usecases Demo", "01_rag_usecases/01_rag_usecases_demo.py"),
    ("02. RAG vs Fine-Tuning Matrix", "02_rag_vs_finetuning/01_rag_vs_finetuning_matrix.py"),
    ("03. Chunking Strategies (Fixed, Sentence, Recursive)", "03_implementing_rag/01_chunking_strategies.py"),
    ("04. Embedding Generation (Dense Vectors)", "03_implementing_rag/02_embedding_generation.py"),
    ("05. Vector Database Storage & Indexing", "03_implementing_rag/03_vector_database_storage.py"),
    ("06. Retrieval Process (Hybrid Search & Filtering)", "03_implementing_rag/04_retrieval_process.py"),
    ("07. Generation & Synthesis (Grounding & Citations)", "03_implementing_rag/05_generation_synthesis.py"),
    ("08. Implementing RAG: Using SDKs Directly", "04_ways_of_implementing/01_using_sdks_directly.py"),
    ("09. Implementing RAG: LangChain", "04_ways_of_implementing/02_langchain_rag.py"),
    ("10. Implementing RAG: LlamaIndex", "04_ways_of_implementing/03_llamaindex_rag.py"),
    ("11. Implementing RAG: Haystack & RAGFlow Overview", "04_ways_of_implementing/04_haystack_and_ragflow.py")
]

def print_header():
    print("=" * 75)
    print("🚀 WHAT ARE RAGS (RETRIEVAL-AUGMENTED GENERATION) - MASTER INTERACTIVE CLI")
    print("   Berdasarkan Roadmap AI Engineer (roadmap.sh/ai-engineer)")
    print("=" * 75)

def run_script(script_path: str):
    print(f"\n▶️ Menjalankan: {script_path}\n")
    try:
        res = subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error saat menjalankan {script_path}: {e}")

def run_all():
    print("\n🧪 MENJALANKAN SELURUH TEST SUITE MODUL RAG...\n")
    for title, script in SCRIPTS:
        print(f"\n--- {title} ---")
        run_script(script)
    print("\n✅ SELURUH TEST SUITE SELESAI MENJALANKAN TANPA ERROR!")

def main_menu():
    while True:
        print_header()
        print("Pilih modul interaktif yang ingin dijalankan:\n")
        for idx, (title, _) in enumerate(SCRIPTS, 1):
            print(f"  [{idx:2d}] {title}")
        print("  [ A] Jalankan Semua Modul (Automated Test Suite)")
        print("  [ Q] Keluar")
        print("-" * 75)
        
        choice = input("Masukkan pilihan Anda [1-11, A, Q]: ").strip().upper()
        if choice == 'Q':
            print("👋 Terima kasih! Selamat belajar RAG.")
            break
        elif choice == 'A':
            run_all()
            input("\nTekan Enter untuk kembali ke menu utama...")
        elif choice.isdigit() and 1 <= int(choice) <= len(SCRIPTS):
            _, script_path = SCRIPTS[int(choice) - 1]
            run_script(script_path)
            input("\nTekan Enter untuk kembali ke menu utama...")
        else:
            print("❌ Pilihan tidak valid, silakan coba lagi.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--all", "-a", "all"]:
        run_all()
    else:
        main_menu()
