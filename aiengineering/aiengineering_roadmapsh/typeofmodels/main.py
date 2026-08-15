#!/usr/bin/env python3
"""
======================================================================
  MASTER CLI INTERACTIVE RUNNER - TYPE OF MODELS LEARNING WORKSPACE
======================================================================
Berdasarkan Roadmap resmi AI Engineer (https://roadmap.sh/ai-engineer)
Menyediakan antarmuka interaktif untuk mengeksekusi modul pembelajaran,
membaca catatan teoritis, dan menjalankan kalkulator VRAM & benchmark.
"""

import os
import sys
import time
import subprocess

def color(text: str, code: str) -> str:
    """Utility ANSI Color Formatting"""
    return f"\033[{code}m{text}\033[0m"

def print_banner():
    print(color("""
======================================================================
   AI ENGINEER ROADMAP: TYPE OF MODELS MASTER LEARNING WORKSPACE
======================================================================
  Visual Roadmap Topics Covered:
  [1] Pre-trained Models      [2] Closed vs Open Source    [3] Self-Hosted
""", "1;36"))

MODULES = [
    # --- SUBTOPIK 1: PRE-TRAINED MODELS ---
    {
        "id": "1",
        "category": "01_PRETRAINED_MODELS",
        "title": "Base Model vs Instruct/Chat Model Simulation",
        "script": "01_pretrained_models/01_base_vs_instruct_models.py",
        "note": "notes/01_pretrained_models.md"
    },
    {
        "id": "2",
        "category": "01_PRETRAINED_MODELS",
        "title": "Arsitektur Transformer (Encoder vs Decoder vs Enc-Dec)",
        "script": "01_pretrained_models/02_model_architectures.py",
        "note": "notes/01_pretrained_models.md"
    },
    {
        "id": "3",
        "category": "01_PRETRAINED_MODELS",
        "title": "Quantization (FP32/FP16/INT8/INT4) & Format GGUF/AWQ/GPTQ",
        "script": "01_pretrained_models/03_quantization_and_formats.py",
        "note": "notes/01_pretrained_models.md"
    },
    {
        "id": "4",
        "category": "01_PRETRAINED_MODELS",
        "title": "Kalkulator Interaktif VRAM, Parameter & KV Cache",
        "script": "01_pretrained_models/04_model_size_and_vram_calculator.py",
        "note": "notes/01_pretrained_models.md"
    },

    # --- SUBTOPIK 2: CLOSED VS OPEN SOURCE ---
    {
        "id": "5",
        "category": "02_CLOSED_VS_OPEN_SOURCE",
        "title": "Unified Client Closed Proprietary API (OpenAI, Claude, Gemini)",
        "script": "02_closed_vs_open_source/01_closed_api_clients.py",
        "note": "notes/02_closed_vs_open_source.md"
    },
    {
        "id": "6",
        "category": "02_CLOSED_VS_OPEN_SOURCE",
        "title": "Inspektur Model Open-Weights Hugging Face Hub",
        "script": "02_closed_vs_open_source/02_open_weights_huggingface.py",
        "note": "notes/02_closed_vs_open_source.md"
    },
    {
        "id": "7",
        "category": "02_CLOSED_VS_OPEN_SOURCE",
        "title": "Simulator Benchmark TCO & Trade-Off Biaya vs Privasi",
        "script": "02_closed_vs_open_source/03_tradeoff_matrix_and_benchmark.py",
        "note": "notes/02_closed_vs_open_source.md"
    },
    {
        "id": "8",
        "category": "02_CLOSED_VS_OPEN_SOURCE",
        "title": "Analyzer Lisensi & Kepatuhan Legal (Apache 2.0, Llama, RAIL)",
        "script": "02_closed_vs_open_source/04_licensing_and_compliance_checker.py",
        "note": "notes/02_closed_vs_open_source.md"
    },

    # --- SUBTOPIK 3: SELF-HOSTED MODELS ---
    {
        "id": "9",
        "category": "03_SELF_HOSTED_MODELS",
        "title": "Serving Model Lokal via Ollama REST API Client",
        "script": "03_self_hosted_models/01_ollama_local_serving.py",
        "note": "notes/03_self_hosted_models.md"
    },
    {
        "id": "10",
        "category": "03_SELF_HOSTED_MODELS",
        "title": "vLLM Engine: PagedAttention & Continuous Batching",
        "script": "03_self_hosted_models/02_vllm_continuous_batching.py",
        "note": "notes/03_self_hosted_models.md"
    },
    {
        "id": "11",
        "category": "03_SELF_HOSTED_MODELS",
        "title": "Hardware & GPU Sizing Assistant (NVIDIA vs Apple Silicon)",
        "script": "03_self_hosted_models/03_vram_and_gpu_sizing.py",
        "note": "notes/03_self_hosted_models.md"
    },
    {
        "id": "12",
        "category": "03_SELF_HOSTED_MODELS",
        "title": "Production OpenAI-Compatible FastAPI Server",
        "script": "03_self_hosted_models/04_self_hosted_fastapi_server.py",
        "note": "notes/03_self_hosted_models.md"
    }
]

def list_menu():
    print_banner()
    current_cat = ""
    for m in MODULES:
        if m["category"] != current_cat:
            current_cat = m["category"]
            cat_title = current_cat.replace("_", " ")
            print(f"\n{color('=== ' + cat_title + ' ===', '1;33')}")
        print(f" [{color(m['id'], '1;32')}] {m['title']}")
        
    print(f"\n{color('=== FITUR & OPSI TAMBAHAN ===', '1;35')}")
    print(f" [{color('N', '1;36')}] Baca Catatan Pembelajaran (Notes)")
    print(f" [{color('W', '1;36')}] Buka Web Visualizer / Playground Dashboard")
    print(f" [{color('T', '1;36')}] Jalankan Test Suite Diagnosis Seluruh Modul")
    print(f" [{color('Q', '1;31')}] Keluar (Exit)")

def safe_input(prompt_text: str) -> str:
    try:
        return input(prompt_text)
    except (EOFError, KeyboardInterrupt):
        return "Q"

def run_script(script_path: str):
    if not os.path.exists(script_path):
        print(color(f"❌ File script '{script_path}' tidak ditemukan!", "1;31"))
        return
    print(color(f"\n▶️ Running: {script_path}\n", "1;32"))
    subprocess.run([sys.executable, script_path])
    print(color("\n✅ Eksekusi Selesai. Tekan Enter untuk kembali ke menu...", "1;32"))
    safe_input("")

def view_notes():
    notes_dir = "notes"
    if not os.path.exists(notes_dir):
        print("Folder notes belum ada.")
        return
    
    notes_files = sorted([f for f in os.listdir(notes_dir) if f.endswith('.md')])
    print(color("\n=== DAFTAR CATATAN PEMBELAJARAN ===", "1;33"))
    for idx, nf in enumerate(notes_files, 1):
        print(f" [{idx}] {nf}")
    
    choice = safe_input("\nPilih nomor catatan yang ingin dibaca (atau Enter untuk kembali): ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(notes_files):
        target_file = os.path.join(notes_dir, notes_files[int(choice) - 1])
        print(color(f"\n--- MEMBACA: {target_file} ---\n", "1;36"))
        with open(target_file, 'r', encoding='utf-8') as f:
            print(f.read())
        print(color("\n--- Selesai Membaca. Tekan Enter untuk kembali ---", "1;32"))
        safe_input("")

def run_all_tests():
    print(color("\n🧪 MENJALANKAN TEST SUITE DIAGNOSIS SELURUH MODUL...\n", "1;35"))
    success_count = 0
    fail_count = 0
    
    for m in MODULES:
        script = m["script"]
        print(f"Testing [{m['id']}] {m['title']}...", end=" ", flush=True)
        try:
            res = subprocess.run([sys.executable, script], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=10)
            if res.returncode == 0:
                print(color("PASS", "1;32"))
                success_count += 1
            else:
                print(color(f"FAIL (Code {res.returncode})", "1;31"))
                fail_count += 1
        except Exception as e:
            print(color(f"ERROR ({str(e)})", "1;31"))
            fail_count += 1

    print("\n" + "=" * 60)
    print(color(f"HASIL DIAGNOSIS: {success_count} Passed, {fail_count} Failed", "1;32" if fail_count == 0 else "1;31"))
    print("=" * 60)
    print("\nTekan Enter untuk kembali ke menu...")
    safe_input("")

def launch_web_visualizer():
    web_dir = "web_visualizer"
    index_path = os.path.join(web_dir, "index.html")
    if not os.path.exists(index_path):
        print(color("❌ Interactive Web Visualizer belum disiapkan.", "1;31"))
        return
    
    abs_path = os.path.abspath(index_path)
    print(color(f"\n🌐 Interactive Web Visualizer Siap!", "1;36"))
    print(f"File Path : file://{abs_path}")
    print("\nAnda juga dapat menjalankan Web Server lokal via terminal:")
    print(color(f"python3 -m http.server 8080 --directory {web_dir}\n", "1;33"))
    print("Tekan Enter untuk kembali...")
    safe_input("")

def main():
    while True:
        list_menu()
        choice = safe_input(color("\nPilih menu [1-12, N, W, T, Q]: ", "1;37")).strip().upper()
        
        if choice == 'Q':
            print(color("\nTerima kasih telah belajar Type of Models! Sampai jumpa.\n", "1;32"))
            break
        elif choice == 'N':
            view_notes()
        elif choice == 'W':
            launch_web_visualizer()
        elif choice == 'T':
            run_all_tests()
        else:
            selected = next((m for m in MODULES if m["id"] == choice), None)
            if selected:
                run_script(selected["script"])
            else:
                print(color("\nPilihan tidak valid, silakan coba lagi.", "1;31"))
                time.sleep(1)

if __name__ == "__main__":
    main()
