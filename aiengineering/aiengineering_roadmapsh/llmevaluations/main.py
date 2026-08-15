"""
main.py
-------
Master CLI Runner untuk modul pembelajaran LLM Evaluations.
Menyediakan antarmuka terminal interaktif untuk menjalankan skrip pengujian
serta meluncurkan Interactive Web Visualizer.
"""

import sys
import subprocess
import os

LABS = {
    "1": ("01_deterministic_evals/01_string_and_regex_evals.py", "Deterministic Evals: String Match & Regex"),
    "2": ("01_deterministic_evals/02_schema_and_code_asserts.py", "Deterministic Evals: Schema & Code Asserts"),
    "3": ("01_deterministic_evals/03_nlp_deterministic_metrics.py", "Deterministic Evals: BLEU & ROUGE Metrics"),
    "4": ("02_model_based_evals/01_llm_judge_single_and_pairwise.py", "Model-Based Evals: LLM-as-a-Judge Single & Pairwise"),
    "5": ("02_model_based_evals/02_geval_chain_of_thought.py", "Model-Based Evals: G-Eval Chain-of-Thought Framework"),
    "6": ("02_model_based_evals/03_judge_bias_mitigation.py", "Model-Based Evals: Mitigating Judge Biases"),
    "7": ("03_human_evals/01_human_annotation_lab.py", "Human Evals: HITL Annotation & Likert Collector"),
    "8": ("03_human_evals/02_inter_annotator_agreement.py", "Human Evals: Cohen's & Fleiss' Kappa IAA"),
    "9": ("03_human_evals/03_chatbot_arena_elo.py", "Human Evals: Chatbot Arena Elo Benchmark"),
    "10": ("04_evaluation_metrics/01_classification_and_nlp_metrics.py", "Evaluation Metrics: Precision/Recall/F1 & Perplexity"),
    "11": ("04_evaluation_metrics/02_rag_triad_evaluator.py", "Evaluation Metrics: RAG Triad Evaluator"),
    "12": ("05_evaluation_tools/01_deepeval_framework_demo.py", "Evaluation Tools: DeepEval Unit Testing"),
    "13": ("05_evaluation_tools/02_ragas_framework_demo.py", "Evaluation Tools: RAGAS Batch Assessment"),
}

def print_menu():
    print("\n" + "=" * 65)
    print(" 🤖 LLM EVALUATIONS LEARNING WORKSPACE (ROADMAP.SH AI ENGINEER)")
    print("=" * 65)
    print("  [Evaluation Types]")
    print("   1. String, Exact Match & Regex Evals")
    print("   2. Pydantic Schema & Code Assertions Evals")
    print("   3. BLEU, ROUGE-1/2/L & METEOR N-Gram Metrics")
    print("   4. LLM-as-a-Judge (Single Grading & Pairwise Ranking)")
    print("   5. G-Eval Framework (Chain-of-Thought Rubrics)")
    print("   6. Mitigating Judge Biases (Position Swapping & Normalization)")
    print("   7. Human-in-the-Loop (HITL) Annotation & Likert Collector")
    print("   8. Inter-Annotator Agreement (Cohen's Kappa Scorer)")
    print("   9. Chatbot Arena ELO Rating Simulator")
    print("  10. Classification Metrics (Accuracy, Precision, F1) & Perplexity")
    print("  11. RAG Triad Evaluator (Faithfulness, Relevancy, Precision)")
    print("\n  [Evaluation Tools]")
    print("  12. DeepEval Framework (Unit Testing for LLMs)")
    print("  13. RAGAS Framework (End-to-End RAG Assessment)")
    print("\n  [Interactive Web Visualizer]")
    print("   W. Launch Interactive Web Visualizer Dashboard (HTTP Port 5000)")
    print("   Q. Exit")
    print("=" * 65)

def run_lab(script_path: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, script_path)
    if not os.path.exists(full_path):
        print(f"❌ Error: File '{script_path}' tidak ditemukan.")
        return
    print(f"\n🚀 Menjalankan: {script_path}...\n")
    subprocess.run([sys.executable, full_path])

def launch_web_visualizer():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    server_path = os.path.join(base_dir, "web_visualizer", "server.py")
    print("\n🌐 Meluncurkan Interactive Web Visualizer Dashboard...")
    print("Akses melalui browser di: http://localhost:5000\n")
    subprocess.run([sys.executable, server_path])

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["--web", "-w", "web"]:
        launch_web_visualizer()
        return

    while True:
        print_menu()
        choice = input("Pilih nomor menu (1-13, W, Q): ").strip().lower()
        
        if choice in ["q", "exit", "quit"]:
            print("\nTerima kasih telah belajar LLM Evaluations! 👋")
            break
        elif choice in ["w", "web"]:
            launch_web_visualizer()
        elif choice in LABS:
            script, desc = LABS[choice]
            print(f"\n--- {desc} ---")
            run_lab(script)
            input("\nTekan Enter untuk kembali ke menu utama...")
        else:
            print("❌ Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()
