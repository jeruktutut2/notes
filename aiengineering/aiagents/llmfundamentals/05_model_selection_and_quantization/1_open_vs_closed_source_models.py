#!/usr/bin/env python3
"""
Modul 5.1: Open Weight vs Closed API Model Selection Matrix
Matriks evaluasi pemilihan model (Closed API vs Local Open Weight) untuk arsitektur AI Agent.
"""

def demonstrate_model_selection_matrix():
    print("\n" + "="*70)
    print(" 1. MATRIKS EVALUASI: CLOSED SOURCE API VS OPEN WEIGHT LOCAL MODEL")
    print("="*70)
    
    matrix = [
        ("Kriteria", "Closed Source API (GPT-4o, Claude 3.5)", "Open Weight Local (LLaMA-3, Qwen-2)"),
        ("Kemampuan Penalaran", "Sangat Tinggi (State-of-the-Art)", "Tinggi (Mendekati pada model 70B+)"),
        ("Kerahasiaan Data / Privacy", "Data terkirim ke server vendor", "\033[92m100% Private (On-Premise / Local)\033[0m"),
        ("Latensi & Throughput", "Tergantung traffic & rate limit API", "\033[92mDeterministik (VLLM / Ollama local)\033[0m"),
        ("Kustomisasi & Fine-Tuning", "Terbatas pada prompt / fine-tune API", "\033[92mBebas (Full Weight / LoRA Fine-Tune)\033[0m"),
        ("Biaya Awal (CapEx)", "$0 (Pay-per-use token API)", "Membutuhkan Hardware GPU (NVIDIA H100/A100)"),
        ("Biaya Operasional (OpEx)", "Bertambah seiring volume request", "Biaya listrik & server konstan (TCO Hemat)")
    ]
    
    for row in matrix:
        print(f"{row[0]:<25} | {row[1]:<38} | {row[2]:<38}")
        print("-" * 105)
    print()


def recommend_model_for_usecase():
    print("="*70)
    print(" 2. PANDUAN PEMILIHAN MODEL BERDASARKAN SKENARIO AGENT")
    print("="*70)
    
    usecases = [
        ("Complex Reasoning & Code Agent", "Claude 3.5 Sonnet / GPT-4o", "Penalaran kompleks, perencanaan multi-step & refactoring kode."),
        ("High-Throughput Routing / Triage", "GPT-4o-mini / DeepSeek R1 / LLaMA-3-8B", "Memilah intent user dan mengarahkan ke sub-agent secara cepat & murah."),
        ("Air-gapped & Offline Enterprise", "LLaMA-3-70B (Quantized INT4 / GGUF)", "Industri perbankan/medis yang melarang transfer data ke cloud."),
        ("Edge Device / Mobile Agent", "Phi-3 / Qwen-2.5-3B", "Eksekusi cepat langsung di perangkat HP/Laptop lokal.")
    ]
    
    for title, model, rationale in usecases:
        print(f" • \033[93m{title:<32}\033[0m -> Model: \033[96m{model:<35}\033[0m")
        print(f"   Rasional: {rationale}")
        print("-" * 75)
    print()


def main():
    print("\n" + "█"*70)
    print("  MODUL 5.1: OPEN WEIGHT VS CLOSED API MODEL SELECTION")
    print("█"*70)
    
    demonstrate_model_selection_matrix()
    recommend_model_for_usecase()
    
    print("="*70)
    print(" Rekomendasi Arsitektur Agent Hibrida:")
    print(" 1. Gunakan Open Weight (LLaMA 8B) lokal untuk Router, Classifier, dan Simple Tool Extractor.")
    print(" 2. Escalation ke Closed API (GPT-4o / Claude 3.5) HANYA untuk kasus penalaran kompleks.")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
