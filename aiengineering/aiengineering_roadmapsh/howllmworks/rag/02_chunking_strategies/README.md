# Modul 02: Chunking Strategies

Chunking adalah proses memotong dokumen panjang menjadi potongan-potongan teks (*chunks*) yang lebih kecil agar muat ke dalam *context window* LLM dan mempermudah pencarian vektor yang presisi.

## Materi Pembelajaran

1. **`1_fixed_size_and_overlap.py`**
   - Pemotongan ukuran tetap (*fixed size*) berbasis jumlah karakter/token.
   - Menggunakan *sliding window overlap* untuk menjaga konteks batas antar chunk.

2. **`2_recursive_character_chunking.py`**
   - Strategi pembagian bertingkat menggunakan hierarki pembatas: `["\n\n", "\n", " ", ""]`.
   - Menjaga paragraf dan kalimat tetap utuh sebelum terpaksa memotong di batas spasi/karakter.

3. **`3_semantic_and_structure_chunking.py`**
   - Structural Chunking: Memotong teks berdasarkan tag/header Markdown (`#`, `##`).
   - Semantic Chunking concept: Memotong teks ketika terjadi perubahan tema/topik semantik.

## Cara Menjalankan

```bash
python3 02_chunking_strategies/1_fixed_size_and_overlap.py
python3 02_chunking_strategies/2_recursive_character_chunking.py
python3 02_chunking_strategies/3_semantic_and_structure_chunking.py
```
