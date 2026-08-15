import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n{'='*60}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*60}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"{'='*60}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*60)
        print("=== AI Engineering Fine-Tuning Learning Project ===")
        print("#"*60)
        print("Pilih modul / topik pembelajaran yang ingin Anda jalankan:\n")
        
        print("[ Modul 1: Persiapan Dataset & Formatting ]")
        print("  11. Format Alpaca vs ShareGPT / ChatML Conversion")
        print("  12. Data Cleaning, Deduplication & Quality Filtering")
        print("  13. Tokenization & Chat Templates (Target Loss Masking)")
        
        print("\n[ Modul 2: PEFT & LoRA Architecture ]")
        print("  21. Custom LoRA Layer dari Scratch (PyTorch W + BA)")
        print("  22. Hugging Face PEFT (LoraConfig & Target Modules)")
        print("  23. QLoRA & 4-bit NF4 Quantization Concepts")

        print("\n[ Modul 3: Supervised Fine-Tuning (SFT) ]")
        print("  31. Manual PyTorch SFT Training Loop")
        print("  32. Hugging Face TRL SFTTrainer Integration")
        print("  33. Memory Efficient Training (Grad Accum & Precision)")

        print("\n[ Modul 4: Preference Alignment (DPO & RLHF) ]")
        print("  41. Direct Preference Optimization (DPO) Loss & Pairs")
        print("  42. Reward Modeling & ORPO Concept")

        print("\n[ Modul 5: Evaluasi & Hyperparameter Tuning ]")
        print("  51. Metrik Evaluasi Model (Perplexity, BLEU/ROUGE, LLM-as-a-Judge)")
        print("  52. Hyperparameter Tuning & Learning Rate Schedule")

        print("\n[ Modul 6: Model Merging, Export & Inference ]")
        print("  61. Model Merging (LoRA Weights -> Base Model) & Export")
        print("  62. Fine-Tuned Model Inference (Temperature & Top-P Sampling)")

        print("\n  0. Keluar")
        
        pilihan = input("\nMasukkan angka pilihan Anda (misal: 11, 21, 31): ").strip()
        
        # Mapping pilihan angka ke path file skrip
        scripts_map = {
            '11': "01_persiapan_dataset_dan_formatting/1_dataset_formats.py",
            '12': "01_persiapan_dataset_dan_formatting/2_data_cleaning_filtering.py",
            '13': "01_persiapan_dataset_dan_formatting/3_tokenization_and_chat_templates.py",
            '21': "02_peft_dan_lora_architecture/1_custom_lora_from_scratch.py",
            '22': "02_peft_dan_lora_architecture/2_peft_huggingface_lora.py",
            '23': "02_peft_dan_lora_architecture/3_qlora_quantization.py",
            '31': "03_supervised_fine_tuning_sft/1_custom_sft_training_loop.py",
            '32': "03_supervised_fine_tuning_sft/2_hf_trl_sft_trainer.py",
            '33': "03_supervised_fine_tuning_sft/3_memory_efficient_training.py",
            '41': "04_preference_alignment_dpo_rlhf/1_dpo_preference_tuning.py",
            '42': "04_preference_alignment_dpo_rlhf/2_reward_modeling_and_orpo.py",
            '51': "05_evaluasi_dan_hyperparameters/1_evaluasi_model_metrics.py",
            '52': "05_evaluasi_dan_hyperparameters/2_hyperparameter_tuning.py",
            '61': "06_merging_export_dan_inference/1_model_merging_and_export.py",
            '62': "06_merging_export_dan_inference/2_fine_tuned_inference.py"
        }
        
        if pilihan == '0':
            print("Keluar dari program. Selamat belajar Fine-Tuning!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia.")

if __name__ == "__main__":
    main()
