"""
main.py
Master Interactive CLI Runner & Test Suite for 'Multimodal AI' Workspace
Berdasarkan Kurikulum Roadmap AI Engineer (roadmap.sh/ai-engineer)
"""

import sys
import subprocess
import os

SCRIPTS = [
    ("01. Image Understanding (VQA, OCR, Base64 Formatting)", "01_multimodal_usecases/01_image_understanding.py"),
    ("02. Image Generation (Latent Diffusion & Prompt Parsing)", "01_multimodal_usecases/02_image_generation.py"),
    ("03. Video Understanding (Frame Sampling & Temporal QA)", "01_multimodal_usecases/03_video_understanding.py"),
    ("04. Audio Processing (Spectrogram & Waveform Classification)", "01_multimodal_usecases/04_audio_processing.py"),
    ("05. Text-to-Speech (TTS Vocoder & Voice Synthesis)", "01_multimodal_usecases/05_text_to_speech.py"),
    ("06. Speech-to-Text (STT Whisper Decoder & Alignment)", "01_multimodal_usecases/06_speech_to_text.py"),
    ("07. OpenAI Vision API (GPT-4o Multi-Image Analysis)", "02_multimodal_tasks_and_sdks/01_openai_vision_api.py"),
    ("08. DALL-E API (Text-to-Image & Revision Inspector)", "02_multimodal_tasks_and_sdks/02_dalle_api.py"),
    ("09. NanoBanana API (Specialized REST Endpoint SDK)", "02_multimodal_tasks_and_sdks/03_nanobanana_api.py"),
    ("10. Whisper API (Audio Transcription & Subtitles)", "02_multimodal_tasks_and_sdks/04_whisper_api.py"),
    ("11. Hugging Face Models (CLIP, BLIP, Florence-2)", "02_multimodal_tasks_and_sdks/05_huggingface_models.py"),
    ("12. LangChain for Multimodal Apps (Templates & Chains)", "02_multimodal_tasks_and_sdks/06_langchain_multimodal.py"),
    ("13. LlamaIndex for Multimodal Apps (MultiModal Index & QA)", "02_multimodal_tasks_and_sdks/07_llamaindex_multimodal.py")
]

def print_header():
    print("=" * 80)
    print("🎨 MULTIMODAL AI - MASTER INTERACTIVE CLI RUNNER")
    print("   Berdasarkan Roadmap AI Engineer (roadmap.sh/ai-engineer)")
    print("=" * 80)

def run_script(script_path: str):
    print(f"\n▶️ Menjalankan: {script_path}\n")
    if not os.path.exists(script_path):
        print(f"❌ File tidak ditemukan: {script_path}")
        return
    try:
        res = subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error saat menjalankan {script_path}: {e}")

def run_all():
    print("\n🧪 MENJALANKAN SELURUH TEST SUITE MODUL MULTIMODAL AI...\n")
    for title, script in SCRIPTS:
        print(f"\n--- {title} ---")
        run_script(script)
    print("\n✅ SELURUH TEST SUITE MULTIMODAL SELESAI MENJALANKAN TANPA ERROR!")

def main_menu():
    while True:
        print_header()
        print("Pilih modul interaktif yang ingin dijalankan:\n")
        for idx, (title, _) in enumerate(SCRIPTS, 1):
            print(f"  [{idx:2d}] {title}")
        print("  [ A] Jalankan Semua Modul (Automated Test Suite)")
        print("  [ Q] Keluar")
        print("-" * 80)
        
        choice = input("Masukkan pilihan Anda [1-13, A, Q]: ").strip().upper()
        if choice == 'Q':
            print("👋 Terima kasih! Selamat belajar Multimodal AI.")
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
