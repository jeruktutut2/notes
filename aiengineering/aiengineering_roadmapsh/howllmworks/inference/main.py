import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n{'='*50}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*50}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"{'='*50}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*50)
        print("=== AI Engineering Inference Project ===")
        print("#"*50)
        print("Pilih modul / point yang ingin Anda jalankan:\n")
        
        print("[ Point 1: Dasar Inference ]")
        print("  11. Apa Itu Inference (Definisi & Konsep Dasar)")
        print("  12. Pipeline Inference (Hugging Face Pipeline)")

        print("\n[ Point 2: Model Selection ]")
        print("  21. Open vs Closed Model")
        print("  22. Hugging Face Model Hub")
        print("  23. Ollama Local Inference")

        print("\n[ Point 3: Prompt Engineering ]")
        print("  31. Zero-Shot Prompting")
        print("  32. Few-Shot Prompting")
        print("  33. Chain-of-Thought Prompting")
        print("  34. System Prompt Design")

        print("\n[ Point 4: Optimasi Inference ]")
        print("  41. Quantization (INT8/INT4)")
        print("  42. Batching Strategies")
        print("  43. Caching & KV-Cache")
        print("  44. Streaming Output")

        print("\n[ Point 5: Inference API & Serving ]")
        print("  51. OpenAI API Integration")
        print("  52. Hugging Face Inference API")
        print("  53. FastAPI Model Serving")

        print("\n[ Point 6: Evaluasi & Observability ]")
        print("  61. Evaluasi Output Model (BLEU, ROUGE, dsb.)")
        print("  62. Cost & Latency Tracking")
        print("  63. Logging & Tracing Inference")

        print("\n[ Point 7: Safety & Guardrails ]")
        print("  71. Content Moderation")
        print("  72. Prompt Injection Defense")
        print("  73. Output Validation & Structuring")

        print("\n  0. Keluar")
        
        pilihan = input("\nMasukkan angka pilihan Anda: ").strip()
        
        # Mapping input ke path file
        scripts_map = {
            '11': "01_dasar_inference/1_apa_itu_inference.py",
            '12': "01_dasar_inference/2_pipeline_inference.py",
            '21': "02_model_selection/1_open_vs_closed_model.py",
            '22': "02_model_selection/2_huggingface_model_hub.py",
            '23': "02_model_selection/3_ollama_local_inference.py",
            '31': "03_prompt_engineering/1_zero_shot_prompting.py",
            '32': "03_prompt_engineering/2_few_shot_prompting.py",
            '33': "03_prompt_engineering/3_chain_of_thought.py",
            '34': "03_prompt_engineering/4_system_prompt_design.py",
            '41': "04_optimasi_inference/1_quantization.py",
            '42': "04_optimasi_inference/2_batching_strategies.py",
            '43': "04_optimasi_inference/3_caching_kv_cache.py",
            '44': "04_optimasi_inference/4_streaming_output.py",
            '51': "05_inference_api_dan_serving/1_openai_api.py",
            '52': "05_inference_api_dan_serving/2_huggingface_inference_api.py",
            '53': "05_inference_api_dan_serving/3_fastapi_model_serving.py",
            '61': "06_evaluasi_dan_observability/1_evaluasi_output_model.py",
            '62': "06_evaluasi_dan_observability/2_cost_latency_tracking.py",
            '63': "06_evaluasi_dan_observability/3_logging_tracing.py",
            '71': "07_safety_dan_guardrails/1_content_moderation.py",
            '72': "07_safety_dan_guardrails/2_prompt_injection_defense.py",
            '73': "07_safety_dan_guardrails/3_output_validation.py"
        }
        
        if pilihan == '0':
            print("Keluar dari program. Terima kasih!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia (misal: 11, 21, 31).")

if __name__ == "__main__":
    main()
