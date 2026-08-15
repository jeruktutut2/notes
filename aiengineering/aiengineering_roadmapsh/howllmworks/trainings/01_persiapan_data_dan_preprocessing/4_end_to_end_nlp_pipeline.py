# Catatan: Skrip ini membaca 'dataset.csv' terpusat dan menjalankan kedua tahap secara langsung
# dari Data Loading & Cleaning hingga ke NLP Text Preprocessing Tensor.

import os
import re
import pandas as pd
from transformers import AutoTokenizer

def clean_text(text):
    """Pembersihan noise teks (HTML, URL, Spasi)."""
    if not isinstance(text, str):
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'http\S+|www\S+', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def main():
    print("=== Pipeline Utuh: Membaca 'dataset.csv' -> Cleaning -> NLP Tensor ===\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'dataset.csv')

    if not os.path.exists(dataset_path):
        print(f"File {dataset_path} tidak ditemukan!")
        return

    # TAHAP 1: DATA LOADING & CLEANING
    print(f"1. Memuat dataset terpusat '{dataset_path}'...")
    df = pd.read_csv(dataset_path)
    
    print(f"Total baris mentah: {len(df)}")
    print("\n[Beberapa Baris Data Mentah]")
    print(df[['id', 'nama', 'umur', 'ulasan']].head(5))
    print("-" * 60)

    print("\nMelakukan Cleaning (Hapus Null, Imputasi, Clean Teks)...")
    df = df.dropna(subset=['nama', 'ulasan'])
    df['umur'] = df['umur'].fillna(df['umur'].mean())
    df['pendapatan'] = df['pendapatan'].fillna(df['pendapatan'].median())
    df = df[df['umur'] < 100]
    df['ulasan_bersih'] = df['ulasan'].apply(clean_text)
    df = df[df['ulasan_bersih'].str.len() > 0]

    print(f"\nTotal baris bersih: {len(df)}")
    print("\n[Beberapa Baris Data Bersih]")
    print(df[['id', 'nama', 'umur', 'ulasan_bersih']].head(5))
    print("-" * 60)

    # TAHAP 2: NLP PREPROCESSING
    print("\n2. Mengonversi Ulasan Bersih ke PyTorch Tensor...")
    sentences = df['ulasan_bersih'].tolist()

    tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    encoded_inputs = tokenizer(
        sentences,
        padding=True,
        truncation=True,
        max_length=64,
        return_tensors="pt"
    )

    print(f"\n- Shapes Input IDs    : {encoded_inputs['input_ids'].shape}")
    print(f"- Shapes Attention Mask: {encoded_inputs['attention_mask'].shape}")

    print("\nContoh Matrix Input IDs (Semua ulasan bersih):")
    print(encoded_inputs["input_ids"])

    print("\n✅ End-to-End Pipeline Sukses!")

if __name__ == "__main__":
    main()
