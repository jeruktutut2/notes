#!/usr/bin/env python3
"""
Interactive Master CLI Runner untuk Workspace Prompt vs Context Engineering
Berdasarkan Roadmap AI Engineer (https://roadmap.sh/ai-engineer)
"""

import os
import sys
import time
import subprocess

def color(text: str, code: str) -> str:
    return f"\033[{code}m{text}\033[0m"

def print_banner():
    print(color("""
======================================================================
  PROMPT ENGINEERING VS CONTEXT ENGINEERING - ROADMAP AI ENGINEER
======================================================================
  Workspace Pembelajaran Komprehensif Berdasarkan Roadmap.sh/ai-engineer
""", "1;36"))

MODULES = [
    # --- 01_PROMPT_ENGINEERING ---
    {
        "id": "1",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Zero-Shot & Few-Shot Prompting",
        "script": "01_prompt_engineering/01_zero_shot_and_few_shot/main.py"
    },
    {
        "id": "2",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Chain-of-Thought (CoT) & ReAct Framework",
        "script": "01_prompt_engineering/02_cot_and_react/main.py"
    },
    {
        "id": "3",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Input Format & Structured Output (JSON Repair Loop)",
        "script": "01_prompt_engineering/03_input_format_and_structured_output/main.py"
    },
    {
        "id": "4",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Function Calling (Tools API & Tool Choice)",
        "script": "01_prompt_engineering/04_function_calling/main.py"
    },
    {
        "id": "5",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Prompt Caching (KV Cache Optimization & Cost Savings)",
        "script": "01_prompt_engineering/05_prompt_caching/main.py"
    },
    {
        "id": "6",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Streaming Responses (SSE Stream Simulation)",
        "script": "01_prompt_engineering/06_streaming_responses/main.py"
    },
    {
        "id": "7",
        "category": "01_PROMPT_ENGINEERING",
        "title": "System Prompting, Role & Behavior Alignment",
        "script": "01_prompt_engineering/07_system_prompting_role_behavior/main.py"
    },
    {
        "id": "8",
        "category": "01_PROMPT_ENGINEERING",
        "title": "Context & Constraints (Hard & Soft Constraints)",
        "script": "01_prompt_engineering/08_context_and_constraints/main.py"
    },

    # --- 02_CONTEXT_ENGINEERING ---
    {
        "id": "9",
        "category": "02_CONTEXT_ENGINEERING",
        "title": "External Memory (Redis & Vector Session Memory)",
        "script": "02_context_engineering/01_external_memory/main.py"
    },
    {
        "id": "10",
        "category": "02_CONTEXT_ENGINEERING",
        "title": "RAG and Dynamic Filters (Metadata Filter + Dense Retrieval)",
        "script": "02_context_engineering/02_rag_and_dynamic_filters/main.py"
    },
    {
        "id": "11",
        "category": "02_CONTEXT_ENGINEERING",
        "title": "Context Compaction (LLMLingua Token Density Pruning)",
        "script": "02_context_engineering/03_context_compaction/main.py"
    },
    {
        "id": "12",
        "category": "02_CONTEXT_ENGINEERING",
        "title": "Context Isolation (Multi-Tenant & PII Masking)",
        "script": "02_context_engineering/04_context_isolation/main.py"
    },

    # --- 03_MODEL_SELECTION_AND_HOSTING ---
    {
        "id": "13",
        "category": "03_MODEL_SELECTION",
        "title": "Pre-trained Models (7B, 70B, 405B Capabilities)",
        "script": "03_model_selection_and_hosting/01_pretrained_models/main.py"
    },
    {
        "id": "14",
        "category": "03_MODEL_SELECTION",
        "title": "Closed vs Open Source Models (TCO Calculator)",
        "script": "03_model_selection_and_hosting/02_closed_vs_open_source_models/main.py"
    },
    {
        "id": "15",
        "category": "03_MODEL_SELECTION",
        "title": "Self-Hosted Models & Inference Engines (vLLM VRAM Calculator)",
        "script": "03_model_selection_and_hosting/03_self_hosted_models/main.py"
    },

    # --- 04_PROMPT_VS_CONTEXT_ENGINEERING ---
    {
        "id": "16",
        "category": "04_HYBRID_COMPARISON",
        "title": "Perbandingan Paradigma & Tradeoffs (Cost/Latency Benchmark)",
        "script": "04_prompt_vs_context_engineering/01_perbandingan_paradigma_dan_tradeoffs.py"
    },
    {
        "id": "17",
        "category": "04_HYBRID_COMPARISON",
        "title": "Architectural Decision Matrix & Routing Engine",
        "script": "04_prompt_vs_context_engineering/02_decision_matrix_dan_routing.py"
    },
    {
        "id": "18",
        "category": "04_HYBRID_COMPARISON",
        "title": "End-to-End Production Hybrid Pipeline (Prompt + Context)",
        "script": "04_prompt_vs_context_engineering/03_hybrid_prompt_context_architecture.py"
    }
]

NOTES = [
    ("N1", "Dokumentasi 13 Elemen Prompt Engineering", "notes/01_prompt_engineering_roadmap.md"),
    ("N2", "Dokumentasi 4 Elemen Context Engineering", "notes/02_context_engineering_roadmap.md"),
    ("N3", "Dokumentasi Model Selection & Hosting", "notes/03_model_selection_roadmap.md"),
    ("N4", "Matriks Sintesis Prompt vs Context", "notes/04_prompt_vs_context_synthesis.md")
]

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print_banner()
        print(color("--- FOLDER 1: 01_PROMPT_ENGINEERING (8 SUBMODUL) ---", "1;33"))
        for m in MODULES[:8]:
            print(f"  [{m['id']:>2}] {m['title']}")

        print(color("\n--- FOLDER 2: 02_CONTEXT_ENGINEERING (4 SUBMODUL) ---", "1;33"))
        for m in MODULES[8:12]:
            print(f"  [{m['id']:>2}] {m['title']}")

        print(color("\n--- FOLDER 3: 03_MODEL_SELECTION_AND_HOSTING (3 SUBMODUL) ---", "1;33"))
        for m in MODULES[12:15]:
            print(f"  [{m['id']:>2}] {m['title']}")

        print(color("\n--- FOLDER 4: 04_PROMPT_VS_CONTEXT_ENGINEERING (3 SUBMODUL) ---", "1;33"))
        for m in MODULES[15:]:
            print(f"  [{m['id']:>2}] {m['title']}")

        print(color("\n--- DOKUMENTASI & ROADMAP NOTES ---", "1;35"))
        for nid, title, path in NOTES:
            print(f"  [{nid}] {title}")

        print(color("\n  [0] Keluar / Exit", "1;31"))

        choice = input(color("\nPilih nomor modul/catatan untuk dijalankan [0-18, N1-N4]: ", "1;32")).strip()

        if choice == "0":
            print(color("Terima kasih & selamat belajar AI Engineering!", "1;32"))
            sys.exit(0)

        selected_mod = next((m for m in MODULES if m["id"] == choice), None)
        if selected_mod:
            script_path = os.path.join(base_dir, selected_mod["script"])
            print(color(f"\n>>> Menjalankan: {selected_mod['title']} ...\n", "1;34"))
            if os.path.exists(script_path):
                subprocess.run([sys.executable, script_path])
            else:
                print(color(f"File {script_path} belum tersedia.", "31"))
            input(color("\nTekan ENTER untuk kembali ke menu utama...", "1;30"))
            continue

        selected_note = next((n for n in NOTES if n[0].upper() == choice.upper()), None)
        if selected_note:
            note_path = os.path.join(base_dir, selected_note[2])
            print(color(f"\n>>> Menampilkan Catatan: {selected_note[1]} ...\n", "1;35"))
            if os.path.exists(note_path):
                with open(note_path, "r", encoding="utf-8") as f:
                    print(f.read())
            else:
                print(color(f"File {note_path} tidak ditemukan.", "31"))
            input(color("\nTekan ENTER me-return ke menu utama...", "1;30"))
            continue

        print(color("\nPilihan tidak valid. Silakan coba lagi.", "31"))
        time.sleep(1)

if __name__ == "__main__":
    main()
