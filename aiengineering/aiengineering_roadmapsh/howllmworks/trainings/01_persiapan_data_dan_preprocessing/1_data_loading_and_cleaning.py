import pandas as pd
import numpy as np
import re
import os

def clean_html_and_url(text):
    """Membuang tag HTML, URL, dan merapikan spasi."""
    if not isinstance(text, str):
        return ""
    # Hapus tag HTML
    text = re.sub(r'<[^>]+>', '', text)
    # Hapus URL
    text = re.sub(r'http\S+|www\S+', '', text)
    # Rapikan spasi
    return re.sub(r'\s+', ' ', text).strip()

def main():
    print("=== 1. Data Loading dan Pembersihan (Tabular + Text) ===\n")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, 'dataset.csv')
    output_path = os.path.join(base_dir, 'cleaned_dataset.csv')

    if not os.path.exists(dataset_path):
        print(f"File {dataset_path} tidak ditemukan!")
        return

    # 1. Loading Data dari CSV
    print(f"Memuat data mentah dari '{dataset_path}'...")
    df = pd.read_csv(dataset_path)
    
    print("\nData Asli (Kotor):")
    print(df)
    print("-" * 60)

    # A. Menghapus baris jika data penting (nama atau ulasan) kosong
    df = df.dropna(subset=['nama', 'ulasan'])

    # B. Imputasi Missing Values (Umur & Pendapatan)
    rata_umur = df['umur'].mean()
    df['umur'] = df['umur'].fillna(rata_umur)

    median_pendapatan = df['pendapatan'].median()
    df['pendapatan'] = df['pendapatan'].fillna(median_pendapatan)

    # C. Handling Outliers (Umur di atas 100 tahun tidak wajar)
    df = df[df['umur'] < 100]

    # D. Cleaning Teks Ulasan (Menghapus HTML, URL, & noise)
    df['ulasan_bersih'] = df['ulasan'].apply(clean_html_and_url)
    
    # Buang baris jika ulasan_bersih menjadi kosong (misal awalnya cuma spasi)
    df = df[df['ulasan_bersih'].str.len() > 0]

    print("\nData Setelah Dibersihkan (Cleaned):")
    print(df[['id', 'nama', 'umur', 'pendapatan', 'ulasan_bersih']])
    print("-" * 60)

    # Simpan hasil pembersihan ke file CSV baru
    df.to_csv(output_path, index=False)
    print(f"✅ Data bersih berhasil disimpan ke '{output_path}'.")
    print("Catatan: Data ini sekarang siap digunakan untuk tahap berikutnya (NLP Text Preprocessing / Tensor).")

if __name__ == "__main__":
    main()
