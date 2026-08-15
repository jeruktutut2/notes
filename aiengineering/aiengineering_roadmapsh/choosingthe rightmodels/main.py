#!/usr/bin/env python3
"""
main.py - Master CLI Interactive Runner & Test Suite
Workspace: Choosing the Right Models (por/aiengineering/choosingthe rightmodels)
Roadmap: https://roadmap.sh/ai-engineer
"""

import os
import sys
import subprocess
import time

MODULES = [
    # Subtopic 1: Closed Models
    ("1.1 OpenAI Models (GPT-4o, o1, Structured Output)", "01_closed_models/01_openai_models.py"),
    ("1.2 Anthropic Claude (3.5 Sonnet, Prompt Caching)", "01_closed_models/02_anthropic_claude.py"),
    ("1.3 Google Gemini (1.5 Pro, Multimodal & 2M Context)", "01_closed_models/03_google_gemini.py"),
    ("1.4 Cohere & Mistral (Enterprise RAG & Citations)", "01_closed_models/04_cohere_and_mistral.py"),
    
    # Subtopic 2: Open Source Models
    ("2.1 Meta Llama Family & Hardware Sizing", "02_open_source_models/01_meta_llama.py"),
    ("2.2 DeepSeek V3 & R1 MoE Reasoning", "02_open_source_models/02_deepseek_models.py"),
    ("2.3 Alibaba Qwen 2.5 (Multilingual & Coder)", "02_open_source_models/03_qwen_multilingual.py"),
    ("2.4 Google Gemma 2 On-Device Ecosystem", "02_open_source_models/04_google_gemma.py"),
    
    # Subtopic 3: Platforms & Ecosystem
    ("3.1 Hugging Face Hub & Tasks Taxonomy", "03_platforms_and_ecosystem/01_huggingface_hub_and_tasks.py"),
    ("3.2 Transformers.js In-Browser Inference", "03_platforms_and_ecosystem/02_transformers_js_web.py"),
    ("3.3 Ollama & LM Studio Local Runtimes", "03_platforms_and_ecosystem/03_ollama_and_lmstudio.py"),
    ("3.4 OpenRouter Unified API Gateway", "03_platforms_and_ecosystem/04_openrouter_unified_gateway.py"),
    
    # Subtopic 4: APIs & SDKs
    ("4.1 OpenAI Response API & Function Calling", "04_apis_and_sdks/01_openai_response_api.py"),
    ("4.2 Anthropic Claude Messages API", "04_apis_and_sdks/02_claude_messages_api.py"),
    ("4.3 Google Gemini API & Safety Settings", "04_apis_and_sdks/03_gemini_api_integration.py"),
    ("4.4 HF Inference SDK & Custom OpenAI Server", "04_apis_and_sdks/04_hf_inference_sdk_and_compat.py"),
]

NOTES = [
    ("Closed Models Overview", "notes/01_closed_models.md"),
    ("Open Source Models Overview", "notes/02_open_source_models.md"),
    ("Platforms & Ecosystem Overview", "notes/03_platforms_and_ecosystem.md"),
    ("APIs & SDKs Overview", "notes/04_apis_and_sdks.md"),
    ("Decision Matrix & Framework", "notes/05_choosing_models_decision_matrix.md"),
]

def run_script(script_path: str):
    """Menjalankan file script Python."""
    full_path = os.path.join(os.path.dirname(__file__), script_path)
    if not os.path.exists(full_path):
        print(f"❌ File tidak ditemukan: {script_path}")
        return
        
    print(f"\n🚀 Executing: {script_path}\n" + "=" * 60)
    start = time.time()
    result = subprocess.run([sys.executable, full_path])
    duration = round(time.time() - start, 2)
    print("=" * 60)
    if result.returncode == 0:
        print(f"✅ Executed successfully in {duration}s")
    else:
        print(f"❌ Returned exit code {result.returncode}")

def run_all_tests():
    """Menjalankan seluruh modul untuk pengujian otomatis."""
    print("🧪 RUNNING ALL MODULE SUITE TESTS...\n")
    failed = 0
    passed = 0
    for name, path in MODULES:
        print(f"Testing [{name}] ({path})...")
        full_path = os.path.join(os.path.dirname(__file__), path)
        res = subprocess.run([sys.executable, full_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode == 0:
            print(f"  ✅ PASS")
            passed += 1
        else:
            print(f"  ❌ FAIL: {res.stderr.decode('utf-8')}")
            failed += 1
            
    print(f"\n📊 TEST RESULTS SUMMARY: Total={len(MODULES)} | Passed={passed} | Failed={failed}")
    return failed == 0

def show_menu():
    """Menampilkan menu interaktif utama."""
    while True:
        print("\n" + "=" * 65)
        print(" 🎯 CHOOSING THE RIGHT MODELS - MASTER CLI RUNNER")
        print("    [ roadmap.sh/ai-engineer - Model Selection Workspace ]")
        print("=" * 65)
        print(" 📌 PILIH MODUL PEMBELAJARAN:")
        for idx, (title, path) in enumerate(MODULES, 1):
            print(f"  [{idx:2d}] {title}")
            
        print("\n 📌 PILIH CATATAN DOKUMENTASI (NOTES):")
        for idx, (title, path) in enumerate(NOTES, len(MODULES) + 1):
            print(f"  [{idx:2d}] 📄 Note: {title}")
            
        print("\n 📌 PILIH OPSI LAINNYA:")
        print(f"  [ 0] 🧪 Jalankan Seluruh Test Suite ({len(MODULES)} Modul)")
        print(f"  [99] 🌐 Petunjuk Jalankan Interactive Web Visualizer")
        print(f"  [ q] 🚪 Keluar")
        
        choice = input("\nMasukkan pilihan Anda (0-21 / q): ").strip().lower()
        if choice in ['q', 'exit', 'quit']:
            print("Sampai jumpa & selamat belajar AI Engineering!")
            break
        elif choice == '0':
            run_all_tests()
        elif choice == '99':
            print("\n🌐 UNTUK MENJALANKAN INTERACTIVE WEB VISUALIZER:")
            print("   cd '/Users/bsa/Documents/por/aiengineering/choosingthe rightmodels'")
            print("   python3 -m http.server 8080 --directory web_visualizer")
            print("   Lalu buka browser di: http://localhost:8080\n")
            input("Tekan Enter untuk kembali ke menu...")
        elif choice.isdigit():
            val = int(choice)
            if 1 <= val <= len(MODULES):
                title, path = MODULES[val - 1]
                run_script(path)
                input("\nTekan Enter untuk kembali ke menu...")
            elif len(MODULES) < val <= len(MODULES) + len(NOTES):
                title, path = NOTES[val - len(MODULES) - 1]
                full_path = os.path.join(os.path.dirname(__file__), path)
                print(f"\n📖 Buka file catatan di editor Anda:\n{full_path}\n")
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(content[:1000] + "\n\n[... sisa catatan dapat dibaca di file ...]")
                input("\nTekan Enter untuk kembali ke menu...")
            else:
                print("⚠️ Pilihan tidak valid!")
        else:
            print("⚠️ Pilihan tidak valid!")

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--test", "-t", "test"]:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    else:
        show_menu()

if __name__ == "__main__":
    main()
