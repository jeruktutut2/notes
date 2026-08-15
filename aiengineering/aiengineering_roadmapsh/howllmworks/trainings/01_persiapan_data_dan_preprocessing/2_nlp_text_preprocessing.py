# Catatan: Skrip ini membutuhkan library `pandas` dan `transformers` dari Hugging Face.
# Bisa diinstal dengan: pip install pandas transformers torch

import os
import pandas as pd
from transformers import AutoTokenizer

def main():
    print("=== 2. Pemrosesan Data Teks untuk NLP (Natural Language Processing) ===\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_path = os.path.join(base_dir, 'cleaned_dataset.csv')
    
    # Memastikan file hasil cleaning dari Tahap 1 ada
    if not os.path.exists(input_path):
        print(f"⚠️ File '{input_path}' tidak ditemukan!")
        print("Harap jalankan '1_data_loading_and_cleaning.py' terlebih dahulu untuk menghasilkan data bersih.")
        return

    print(f"Memuat data teks hasil pembersihan dari '{input_path}'...")
    df = pd.read_csv(input_path)

    # Mengambil kolom ulasan_bersih hasil tahap 1
    sentences = df['ulasan_bersih'].tolist()
    print(f"Total ulasan bersih yang dimuat: {len(sentences)} kalimat\n")
    
    print("Daftar Ulasan Bersih (Input NLP):")
    for idx, (nama, s) in enumerate(zip(df['nama'], sentences), 1):
        print(f"{idx}. [{nama}]: \"{s}\"")

    # 1. Menentukan model Tokenizer Hugging Face
    model_name = "bert-base-uncased"
    print(f"\nMemuat Tokenizer untuk model: {model_name}...")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        print("Harap pastikan library transformers terinstal. (pip install transformers)")
        return

    # 2. Proses Tokenization, Padding, Truncation, & Tensor Conversion
    print("\nMelakukan Tokenization (Padding & Truncation ke PyTorch Tensor)...")
    
    encoded_inputs = tokenizer(
        sentences,
        padding=True,       # Menyamakan panjang token dengan padding (0)
        truncation=True,    # Memotong token jika melebihi panjang maksimal
        max_length=64,      # Batas maksimum token
        return_tensors="pt" # Mengembalikan PyTorch Tensor
    )

    print("\nHasil Preprocessing NLP (Siap masuk ke Model Neural Network):")
    
    # Input IDs: Representasi numerik dari setiap token
    print(f"\n1. Input IDs Shape: {encoded_inputs['input_ids'].shape}")
    print("Input IDs (Matrix Tensor Angka):")
    print(encoded_inputs["input_ids"])

    # Attention Mask: Membedakan mana token asli (1) dan mana padding (0)
    print(f"\n2. Attention Mask Shape: {encoded_inputs['attention_mask'].shape}")
    print("Attention Mask:")
    print(encoded_inputs["attention_mask"])

    print("\n✅ Pemrosesan NLP Selesai! Data teks dari dataset.csv telah sukses dikonversi menjadi Tensor siap latih.")

if __name__ == "__main__":
    main()
