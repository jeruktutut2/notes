#!/usr/bin/env python3
"""
main.py - Master CLI Interactive Runner & Test Suite
Workspace: Embedding Models (por/aiengineering/embedingmodels)
Roadmap: https://roadmap.sh/ai-engineer
"""

import os
import sys
import subprocess
import time

MODULES = [
    # Subtopic 1: Proprietary Models
    ("1.1 OpenAI Embeddings API & Matryoshka Truncation", "01_proprietary_models/01_openai_embeddings_api.py"),
    ("1.2 Google Gemini Embedding API & Task-Aware Types", "01_proprietary_models/02_gemini_embedding_api.py"),
    ("1.3 Cohere Embed v3 & Int8/Binary Compression", "01_proprietary_models/03_cohere_embed_api.py"),
    
    # Subtopic 2: Open Source Models
    ("2.1 Sentence Transformers & CPU Local Inference", "02_open_source_models/01_sentence_transformers.py"),
    ("2.2 Models on Hugging Face & Manual Mean/CLS Pooling", "02_open_source_models/02_models_on_huggingface.py"),
    ("2.3 Jina AI Embeddings & 8k Long-Context Window", "02_open_source_models/03_jina_embeddings.py"),
    
    # Subtopic 3: Comparison & Benchmarks
    ("3.1 Comprehensive Model Comparison Benchmark", "03_comparison_and_benchmarks/01_model_comparison_benchmark.py"),
]

NOTES = [
    ("Proprietary Models Notes", "notes/01_proprietary_models.md"),
    ("Open Source Models Notes", "notes/02_open_source_models.md"),
    ("Embedding Comparison & Decision Matrix", "notes/03_embedding_comparison_matrix.md"),
]

def run_script(script_path: str):
    """Menjalankan file script Python."""
    full_path = os.path.join(os.path.dirname(__file__), script_path)
    if not os.path.exists(full_path):
        print(f"❌ File tidak ditemukan: {script_path}")
        return
        
    print(f"\n🚀 Executing: {script_path}\n" + "=" * 65)
    start = time.time()
    result = subprocess.run([sys.executable, full_path])
    duration = round(time.time() - start, 2)
    print("=" * 65)
    if result.returncode == 0:
        print(f"✅ Executed successfully in {duration}s")
    else:
        print(f"❌ Execution failed with return code {result.returncode}")

def run_all_modules():
    """Menjalankan seluruh modul pembelajaran secara berturutan."""
    print("\n🏃 RUNNING ALL EMBEDDING MODELS MODULES...")
    start_total = time.time()
    passed = 0
    
    for name, script_path in MODULES:
        full_path = os.path.join(os.path.dirname(__file__), script_path)
        if os.path.exists(full_path):
            print(f"\n▶️ Running {name} ({script_path})")
            res = subprocess.run([sys.executable, full_path])
            if res.returncode == 0:
                passed += 1
                
    total_duration = round(time.time() - start_total, 2)
    print("\n" + "=" * 65)
    print(f"🏁 TEST SUITE COMPLETED: {passed}/{len(MODULES)} modules passed in {total_duration}s")
    print("=" * 65)

def view_note(note_path: str):
    """Membaca catatan markdown."""
    full_path = os.path.join(os.path.dirname(__file__), note_path)
    if not os.path.exists(full_path):
        print(f"❌ File catatan tidak ditemukan: {note_path}")
        return
        
    print(f"\n📖 Reading Note: {note_path}\n" + "=" * 65)
    with open(full_path, "r", encoding="utf-8") as f:
        print(f.read())
    print("=" * 65)

def launch_web_visualizer():
    """Menjalankan server lokal Web Visualizer."""
    viz_dir = os.path.join(os.path.dirname(__file__), "web_visualizer")
    print(f"\n🌐 Membuka Interactive Web Visualizer...")
    print(f"📍 Directory: {viz_dir}")
    print("👉 Jalankan perintah berikut di terminal Anda untuk membuka visualizer:\n")
    print(f"   python3 -m http.server 8080 --directory {viz_dir}")
    print("   Buka http://localhost:8080 di browser pilihan Anda!\n")

def print_menu():
    print("\n" + "=" * 65)
    print("    🧠 EMBEDDING MODELS - AI ENGINEER ROADMAP MASTER CLI")
    print("=" * 65)
    print("  [Proprietary Models]")
    for i in range(3):
        print(f"   {i+1}. {MODULES[i][0]}")
        
    print("\n  [Open Source Models]")
    for i in range(3, 6):
        print(f"   {i+1}. {MODULES[i][0]}")
        
    print("\n  [Benchmarks & Comparison]")
    print(f"   7. {MODULES[6][0]}")
    
    print("\n  [Option Special & Tools]")
    print("   8. 🏃 Run All Modules (Test Suite Automation)")
    print("   9. 📖 Read Theory Notes (Catatan Pembelajaran)")
    print("  10. 🌐 Launch Interactive Web Visualizer Dashboard")
    print("   0. 🚪 Exit")
    print("=" * 65)

def main():
    while True:
        print_menu()
        try:
            choice = input("Pilih menu [0-10]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSampai jumpa!")
            sys.exit(0)
            
        if choice == "0":
            print("Terima kasih telah belajar Embedding Models! Selamat berkarya.")
            break
        elif choice in [str(i) for i in range(1, 8)]:
            idx = int(choice) - 1
            run_script(MODULES[idx][1])
        elif choice == "8":
            run_all_modules()
        elif choice == "9":
            print("\nCatatan Pembelajaran Tersedia:")
            for idx, (title, path) in enumerate(NOTES, 1):
                print(f"   {idx}. {title} ({path})")
            note_choice = input("Pilih nomor catatan [1-3]: ").strip()
            if note_choice in ["1", "2", "3"]:
                view_note(NOTES[int(note_choice)-1][1])
            else:
                print("❌ Pilihan catatan tidak valid.")
        elif choice == "10":
            launch_web_visualizer()
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
