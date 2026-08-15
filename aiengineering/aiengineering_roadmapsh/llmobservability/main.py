"""
main.py
-------
Master CLI Runner untuk modul interaktif LLM Observability.
Menyediakan menu interaktif untuk menjalankan semua lab Python dan meluncurkan Web Visualizer.
"""

import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("""
====================================================================
 👁️  LLM OBSERVABILITY INTERACTIVE LEARNING WORKSPACE
     Based on roadmap.sh/ai-engineer
====================================================================
""")

def run_script(script_path: str):
    print(f"\n▶️ Running: {script_path}\n" + "-"*60)
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except Exception as e:
        print(f"\n❌ Error executing script: {e}")
    print("-" * 60)
    input("\nTekan Enter untuk kembali ke menu utama...")

def main_menu():
    while True:
        clear_screen()
        print_header()
        print("""
Pilih modul lab yang ingin dijalankan:

--- 1. TRACING & LOGGING ---
 [1] 01_span_execution_tracer.py     (Span Execution Tree & Context)
 [2] 02_structured_llm_logger.py     (OpenInference JSON Logger)

--- 2. COST & LATENCY MONITORING ---
 [3] 01_token_cost_calculator.py     (Token Pricing Engine & Budget Alert)
 [4] 02_latency_profiler.py          (TTFT, TPS & Latency Breakdown)

--- 3. PRODUCTION MONITORING ---
 [5] 01_evaluators_and_hallucination.py (LLM-as-a-Judge & Faithfulness)
 [6] 02_drift_and_feedback_monitor.py (Embedding Drift & CSAT Feedback)

--- 4. OBSERVABILITY TOOLS SIMULATION ---
 [7] 01_langsmith_simulation.py      (LangSmith SDK Runs & Datasets)
 [8] 02_langfuse_simulation.py       (Langfuse Traces & Prompt Management)
 [9] 03_helicone_simulation.py       (Helicone Proxy & Smart Caching)
[10] 04_arize_phoenix_simulation.py  (Arize Phoenix Spans & RAG Evals)

--- 5. WEB VISUALIZER DASHBOARD ---
[11] Launch Web Visualizer Server (FastAPI HTTP Server)

 [0] Keluar (Exit)
""")
        choice = input("Masukkan pilihan Anda (0-11): ").strip()

        if choice == "1":
            run_script("01_tracing_and_logging/01_span_execution_tracer.py")
        elif choice == "2":
            run_script("01_tracing_and_logging/02_structured_llm_logger.py")
        elif choice == "3":
            run_script("02_cost_and_latency_monitoring/01_token_cost_calculator.py")
        elif choice == "4":
            run_script("02_cost_and_latency_monitoring/02_latency_profiler.py")
        elif choice == "5":
            run_script("03_production_monitoring/01_evaluators_and_hallucination.py")
        elif choice == "6":
            run_script("03_production_monitoring/02_drift_and_feedback_monitor.py")
        elif choice == "7":
            run_script("04_observability_tools/01_langsmith_simulation.py")
        elif choice == "8":
            run_script("04_observability_tools/02_langfuse_simulation.py")
        elif choice == "9":
            run_script("04_observability_tools/03_helicone_simulation.py")
        elif choice == "10":
            run_script("04_observability_tools/04_arize_phoenix_simulation.py")
        elif choice == "11":
            print("\n🌐 Memulai Web Visualizer Server pada http://localhost:8000 ...")
            run_script("web_visualizer/server.py")
        elif choice == "0":
            print("\nTerima kasih telah belajar LLM Observability! Selamat tinggal! 👋\n")
            sys.exit(0)
        else:
            input("Pilihan tidak valid. Tekan Enter untuk mencoba lagi...")

if __name__ == "__main__":
    main_menu()
