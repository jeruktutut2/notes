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
        print("=== AI Engineering Trainings Project ===")
        print("#"*50)
        print("Pilih modul / point yang ingin Anda jalankan:\n")
        
        print("[ Point 1: Persiapan Data & Preprocessing ]")
        print("  11. Data Loading & Cleaning (Tabular / Pandas)")
        print("  12. NLP Text Preprocessing (Hugging Face Transformers)")
        print("  13. CV Image Augmentation (PyTorch / Torchvision)")
        print("  14. End-to-End Pipeline (Cleaning -> Tokenization Tensor)")
        
        print("\n[ Point 2: Mendefinisikan Model & Arsitektur ]")
        print("  21. Custom Architecture (PyTorch)")
        print("  22. Pre-trained Model (Hugging Face)")

        print("\n[ Point 3: Proses Pelatihan / Training Loop ]")
        print("  31. Manual Training Loop (PyTorch)")

        print("\n[ Point 4: Evaluasi & Metrik ]")
        print("  41. Classification Metrics (Scikit-Learn)")

        print("\n[ Point 5: Hyperparameter Tuning ]")
        print("  51. Optuna Tuning")

        print("\n[ Point 6: Menyimpan & Ekspor Model ]")
        print("  61. Save & Load (PyTorch state_dict)")

        print("\n  0. Keluar")
        
        pilihan = input("\nMasukkan angka pilihan Anda: ").strip()
        
        # Mapping input ke path file
        scripts_map = {
            '11': "01_persiapan_data_dan_preprocessing/1_data_loading_and_cleaning.py",
            '12': "01_persiapan_data_dan_preprocessing/2_nlp_text_preprocessing.py",
            '13': "01_persiapan_data_dan_preprocessing/3_cv_image_augmentation.py",
            '14': "01_persiapan_data_dan_preprocessing/4_end_to_end_nlp_pipeline.py",
            '21': "02_definisi_model_arsitektur/1_custom_architecture_pytorch.py",
            '22': "02_definisi_model_arsitektur/2_pretrained_model_hf.py",
            '31': "03_proses_pelatihan/1_manual_training_loop.py",
            '41': "04_evaluasi_metrik/1_classification_metrics.py",
            '51': "05_hyperparameter_tuning/1_optuna_tuning.py",
            '61': "06_simpan_ekspor_model/1_save_load_pytorch.py"
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
