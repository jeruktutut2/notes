import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n{'='*60}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*60}\n")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"\n{'='*60}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*65)
        print("=== AI ENGINEERING: PROMPT ENGINEERING LEARNING WORKSPACE ===")
        print("#"*65)
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print("[ Modul 1: Dasar Prompt & Anatomi ]")
        print("  11. Membedah Anatomi & Komponen Utama Prompt")
        print("  12. Persona & System Role Prompting")
        print("  13. Formatting & XML Delimiters Techniques")
        
        print("\n[ Modul 2: Teknik Prompting Dasar ]")
        print("  21. Zero-Shot vs Few-Shot In-Context Learning")
        print("  22. Chain-of-Thought (CoT) Reasoning Mechanics")
        print("  23. Self-Consistency Voting & Tree-of-Thought (ToT)")

        print("\n[ Modul 3: Teknik Prompting Lanjutan ]")
        print("  31. ReAct (Reason + Act) Agent Framework")
        print("  32. Directional Stimulus Prompting")
        print("  33. Least-to-Most Problem Decomposition")
        print("  34. Prompt Chaining Sequential Pipeline")

        print("\n[ Modul 4: Output Structuring & Constraints ]")
        print("  41. JSON & Schema Enforcement with Repair Loop")
        print("  42. Negative Constraints & Algorithmic Guardrails")

        print("\n[ Modul 5: Keamanan Prompt & Red Teaming ]")
        print("  51. Direct & Indirect Prompt Injection Detection Engine")
        print("  52. Jailbreaking Patterns & Red Teaming Vulnerability Testing")
        print("  53. Defensive Prompting (Sandwich & Tag Isolation)")

        print("\n[ Modul 6: Evaluasi & Optimasi Prompt ]")
        print("  61. Automated Evaluation & LLM-as-a-Judge Benchmarking")
        print("  62. Prompt Compression, Token Estimation & Cost Optimization")
        print("  63. Automatic Prompt Engineering (APE) & Meta-Prompting")

        print("\n  0. Keluar")
        
        pilihan = input("\nMasukkan angka pilihan Anda (misal: 11, 21, 31, 51): ").strip()
        
        scripts_map = {
            '11': "01_dasar_prompt_dan_anatomi/1_prompt_anatomy_and_components.py",
            '12': "01_dasar_prompt_dan_anatomi/2_persona_and_role_prompting.py",
            '13': "01_dasar_prompt_dan_anatomi/3_formatting_and_delimiters.py",
            '21': "02_teknik_prompting_dasar/1_zero_shot_vs_few_shot.py",
            '22': "02_teknik_prompting_dasar/2_chain_of_thought_cot.py",
            '23': "02_teknik_prompting_dasar/3_self_consistency_and_tot.py",
            '31': "03_teknik_prompting_lanjutan/1_react_reason_and_act.py",
            '32': "03_teknik_prompting_lanjutan/2_directional_stimulus_prompting.py",
            '33': "03_teknik_prompting_lanjutan/3_least_to_most_decomposition.py",
            '34': "03_teknik_prompting_lanjutan/4_prompt_chaining.py",
            '41': "04_output_structuring_dan_constraints/1_json_and_schema_enforcement.py",
            '42': "04_output_structuring_dan_constraints/2_negative_constraints_and_guardrails.py",
            '51': "05_keamanan_prompt_dan_red_teaming/1_prompt_injection_detection.py",
            '52': "05_keamanan_prompt_dan_red_teaming/2_jailbreaking_and_bypasses.py",
            '53': "05_keamanan_prompt_dan_red_teaming/3_defensive_prompting.py",
            '61': "06_evaluasi_dan_optimasi_prompt/1_automated_prompt_evaluation.py",
            '62': "06_evaluasi_dan_optimasi_prompt/2_prompt_compression_and_token_cost.py",
            '63': "06_evaluasi_dan_optimasi_prompt/3_automatic_prompt_engineering_ape.py"
        }
        
        if pilihan == '0':
            print("Keluar dari program. Selamat belajar Prompt Engineering!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia.")

if __name__ == "__main__":
    main()
