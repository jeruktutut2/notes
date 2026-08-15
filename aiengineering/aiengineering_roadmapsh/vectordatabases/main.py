#!/usr/bin/env python3
"""
MASTER INTERACTIVE RUNNER & TEST SUITE - VECTOR DATABASES WORKSPACE
Kurikulum AI Engineer (roadmap.sh/ai-engineer)
"""

import os
import sys
import subprocess

PYTHON_BIN = os.path.join(os.path.dirname(__file__), ".venv", "bin", "python")
if not os.path.exists(PYTHON_BIN):
    PYTHON_BIN = sys.executable

MODULES = [
    {
        "id": "1",
        "title": "Vector DB vs Traditional DB & Metrics",
        "path": "01_purpose_and_functionality/01_vector_db_vs_traditional_db.py"
    },
    {
        "id": "2",
        "title": "Distance Metrics & Payload Filtering Engine",
        "path": "01_purpose_and_functionality/02_distance_metrics_and_payloads.py"
    },
    {
        "id": "3",
        "title": "Pinecone Hands-On (Featured Vector DB)",
        "path": "02_popular_vector_dbs/01_pinecone_hands_on.py"
    },
    {
        "id": "4",
        "title": "Chroma DB Embedded Client Hands-On",
        "path": "02_popular_vector_dbs/02_chroma_db_hands_on.py"
    },
    {
        "id": "5",
        "title": "FAISS Fast In-Memory Search Hands-On",
        "path": "02_popular_vector_dbs/03_faiss_hands_on.py"
    },
    {
        "id": "6",
        "title": "Vector DB Ecosystem Comparison Matrix",
        "path": "02_popular_vector_dbs/04_ecosystem_comparison.py"
    },
    {
        "id": "7",
        "title": "Indexing Algorithms (HNSW vs IVF vs Flat)",
        "path": "03_implementing_vector_search/01_indexing_embeddings_hnsw_ivf.py"
    },
    {
        "id": "8",
        "title": "Similarity Search & Hybrid Dense-Sparse Search",
        "path": "03_implementing_vector_search/02_performing_similarity_search.py"
    }
]

def run_script(path: str):
    print(f"\n🚀 Running: python3 {path}\n" + "="*60)
    res = subprocess.run([PYTHON_BIN, path])
    print("="*60)
    return res.returncode == 0

def run_all():
    print("\n⚡ MENJALANKAN SELURUH TEST SUITE VECTOR DATABASES...\n")
    passed = 0
    failed = 0
    for mod in MODULES:
        ok = run_script(mod["path"])
        if ok:
            passed += 1
        else:
            failed += 1
    print(f"\n📊 HASIL TEST SUITE: {passed} PASSED, {failed} FAILED.")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        run_all()
        return

    while True:
        print("\n=========================================================")
        print("  🌲 VECTOR DATABASES LEARNING WORKSPACE - ROADMAP.SH")
        print("=========================================================")
        for mod in MODULES:
            print(f"  [{mod['id']}] {mod['title']}")
        print("  [A] Jalankan Seluruh Modul (Run All)")
        print("  [Q] Keluar (Quit)")
        print("---------------------------------------------------------")
        
        choice = input("Pilih modul yang ingin dijalankan (1-8 / A / Q): ").strip().upper()
        if choice == 'Q':
            print("Sampai jumpa dan selamat belajar AI Engineering!")
            break
        elif choice == 'A':
            run_all()
        else:
            found = False
            for mod in MODULES:
                if mod["id"] == choice:
                    run_script(mod["path"])
                    found = True
                    break
            if not found:
                print("❌ Pilihan tidak valid, silakan coba lagi.")

if __name__ == "__main__":
    main()
