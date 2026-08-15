# Implementasi Point 1: Persiapan Data (Data Preparation & Preprocessing)

Proyek ini berisi implementasi kode dari catatan pelatihan AI Engineer, khususnya pada tahap persiapan data sebelum masuk ke proses pelatihan (training).

## Dataset Terpusat
Seluruh skrip data preparation menggunakan dataset terpusat yang sama: **`dataset.csv`**.
Dataset ini berisi gabungan data kotor tabular (missing values, outliers) dan data kotor teks ulasan (HTML tags, URL, noise).

## Daftar File
1. `dataset.csv`: Dataset terpusat (mentah/kotor) yang dipakai bersama oleh skrip 1, 2, dan 4.
2. `1_data_loading_and_cleaning.py`: Membaca `dataset.csv`, melakukan imputasi data tabular & cleaning teks ulasan, lalu menyimpan hasilnya ke `cleaned_dataset.csv`.
3. `2_nlp_text_preprocessing.py`: Membaca `cleaned_dataset.csv` (hasil tahap 1), mengambil kolom ulasan bersih, dan mengonversinya menjadi PyTorch Tensors (Input IDs & Attention Mask).
4. `3_cv_image_augmentation.py`: Memuat folder dataset multi-gambar (`dataset_images/`), melakukan augmentasi & transformasi gambar, lalu mengelompokkannya secara batch menggunakan `ImageFolder` dan `DataLoader` PyTorch.

5. `4_end_to_end_nlp_pipeline.py`: Menggabungkan alur kerja dari `dataset.csv` mentah langsung ke cleaning hingga menghasilkan Tensor NLP dalam 1 eksekusi skrip.

## Urutan Eksekusi Skrip

Untuk melihat keterhubungan antar skrip:

```bash
# Tahap 1: Loading & Cleaning (Menghasilkan cleaned_dataset.csv)
python 1_data_loading_and_cleaning.py

# Tahap 2: NLP Preprocessing (Membaca cleaned_dataset.csv -> PyTorch Tensor)
python 2_nlp_text_preprocessing.py

# Atau jalankan pipeline utuh sekaligus:
python 4_end_to_end_nlp_pipeline.py
```

### Cara Instalasi Library

```bash
pip install pandas datasets transformers torch torchvision Pillow
```
