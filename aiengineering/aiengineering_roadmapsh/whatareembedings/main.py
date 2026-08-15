#!/usr/bin/env python3
"""
main.py
-------
Master CLI Runner & Interactive Learning Hub untuk modul "What are Embeddings"
Berdasarkan Kurikulum Resmi roadmap.sh/ai-engineer.
"""

import os
import sys
import subprocess

# Auto-use .venv python executable if available and current python lacks required packages
VENV_PYTHON = os.path.join(os.path.dirname(__file__), ".venv", "bin", "python")
PYTHON_EXE = VENV_PYTHON if os.path.exists(VENV_PYTHON) else sys.executable

TOPICS = {
    "1": ("Embedding Fundamentals & Vector Space", "01_embedding_fundamentals", [
        ("01_vector_space_and_math.py", "Representasi Teks & Analogi Vektor (Raja-Pria+Wanita=Ratu)"),
        ("02_distance_metrics.py", "Kalkulator 4 Metrik Jarak (Cosine, Dot Product, L2, L1)"),
        ("03_normalization_and_dimensions.py", "Normalisasi L2 & Matryoshka Dimension Truncation"),
    ]),
    "2": ("Semantic Search", "02_semantic_search", [
        ("01_keyword_vs_semantic_search.py", "Keyword Search (Lexical) vs Vector Semantic Search"),
        ("02_chunking_and_embedding_pipeline.py", "Document Chunking & Vector Indexing Pipeline"),
        ("03_hybrid_search_bm25_dense.py", "Hybrid Search dengan Reciprocal Rank Fusion (RRF)"),
    ]),
    "3": ("Data Classification & Clustering", "03_data_classification", [
        ("01_embedding_intent_classifier.py", "Embedding + Logistic Regression Intent Classifier"),
        ("02_zero_shot_classification.py", "Zero-Shot Text Classification Berbasis Cosine Similarity"),
        ("03_semantic_clustering_kmeans.py", "Topic Modeling & Clustering Otomatis dengan K-Means"),
    ]),
    "4": ("Recommendation Systems", "04_recommendation_systems", [
        ("01_content_based_recommender.py", "Item-to-Item Content-Based Filtering Produk"),
        ("02_user_profile_vector_aggregation.py", "User Profile Vector Aggregation dari History"),
        ("03_top_n_item_ranking.py", "Top-N Ranking (Embedding Similarity + Popularity Boost)"),
    ]),
    "5": ("Anomaly Detection", "05_anomaly_detection", [
        ("01_centroid_distance_detector.py", "Deteksi Transaksi Anomali via Jarak ke Centroid"),
        ("02_ood_query_guardrail.py", "LLM Guardrail: Memblokir Query OOD & Prompt Injection"),
        ("03_log_event_outlier_scorer.py", "Skoring Outlier Log System via KNN Distance"),
    ]),
}

def print_header():
    print("\033[93m=" * 75)
    print("      🧠 WHAT ARE EMBEDDINGS - MASTER LEARNING HUB (ROADMAP.SH) 🧠")
    print("=" * 75 + "\033[0m")
    print(" Modul Praktis AI Engineering: Menguasai Vektor, Metrik Jarak & Kasus Penggunaan")
    print("-" * 75)

def run_script(folder: str, script_name: str):
    script_path = os.path.join(folder, script_name)
    print(f"\n\033[94m🚀 Menjalankan Script: {script_path}...\033[0m\n")
    try:
        result = subprocess.run([PYTHON_EXE, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n\033[91m❌ Gagal menjalankan script: {e}\033[0m")
    input("\nTekan [Enter] untuk kembali ke menu utama...")

def run_all_tests():
    print("\n\033[92m🧪 UTILITY TEST RUNNER: Menjalankan Seluruh Modul...\033[0m\n")
    total = 0
    passed = 0
    for key, (title, folder, scripts) in TOPICS.items():
        for script_file, desc in scripts:
            script_path = os.path.join(folder, script_file)
            total += 1
            print(f"Running [{total}] {script_path} ... ", end="", flush=True)
            res = subprocess.run([PYTHON_EXE, script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res.returncode == 0:
                print("\033[92m[PASSED]\033[0m")
                passed += 1
            else:
                print("\033[91m[FAILED]\033[0m")
    print(f"\n\033[93mHasil Pengujian: {passed}/{total} Script Berhasil Tanpa Error!\033[0m\n")
    return passed == total

def main_menu():
    while True:
        print_header()
        print("\nPilih Topik Pembelajaran:")
        for key, (title, folder, scripts) in TOPICS.items():
            print(f"  [{key}] {title}")
        print("  [6] Jalankan Interactive Web Visualizer (Local HTTP Server)")
        print("  [A] Jalankan Seluruh Test Suite (Automated Test)")
        print("  [Q] Keluar")

        choice = input("\nMasukkan Pilihan (1-5, 6, A, Q): ").strip().upper()

        if choice == "Q":
            print("\nTerima kasih telah belajar Embeddings! Sampai jumpa 👋\n")
            break
        elif choice == "A":
            run_all_tests()
            input("Tekan [Enter] untuk kembali...")
        elif choice == "6":
            print("\n\033[96m🌐 Membuka Web Visualizer...\033[0m")
            print("Silakan buka \033[93mweb_visualizer/index.html\033[0m di browser Anda atau jalankan:")
            print("👉 \033[92mpython3 -m http.server 8080 --directory web_visualizer\033[0m")
            input("\nTekan [Enter] untuk kembali...")
        elif choice in TOPICS:
            title, folder, scripts = TOPICS[choice]
            print(f"\n\033[93m--- {title.upper()} ---\033[0m")
            for idx, (s_file, s_desc) in enumerate(scripts, 1):
                print(f"  [{idx}] {s_file} - \033[90m{s_desc}\033[0m")
            print("  [B] Kembali ke Menu Utama")
            
            sub_choice = input("\nPilih Script yang ingin dijalankan (1-3): ").strip().upper()
            if sub_choice.isdigit() and 1 <= int(sub_choice) <= len(scripts):
                s_file, _ = scripts[int(sub_choice) - 1]
                run_script(folder, s_file)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ["--test", "-t"]:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    main_menu()
