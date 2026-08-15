# Modul 01: Document Loading & Parsing

Modul ini membahas tahap paling awal dalam pipeline RAG: mengambil dokumen mentah dari berbagai format (`.txt`, `.md`, `.json`, `.pdf`, `.html`) dan mengonversinya menjadi format teks terstruktur yang dilengkapi dengan metadata.

## Materi Pembelajaran

1. **`1_text_and_markdown_loader.py`**
   - Membaca dan mem-parsing dokumen teks mentah dan Markdown.
   - Menarik atribut metadata seperti nama file, ekstensi, timestamp, serta meng-parsing frontmatter YAML (seperti `title`, `author`, `tags`).

2. **`2_pdf_and_html_parsing.py`**
   - Mendemonstrasikan pembuatan parser PDF berbasis struktur halaman.
   - Parsing dokumen HTML untuk membuang tag berisik (`<script>`, `<style>`, `nav`) dan mengambil konten utama secara bersih.

3. **`3_multimodal_data_prep.py`**
   - Mengolah data terstruktur (JSON/CSV) dan tabel ke dalam format deskripsi teks (*serialization*) agar siap di-embed oleh model teks RAG.

## Cara Menjalankan

```bash
python3 01_document_loading_dan_parsing/1_text_and_markdown_loader.py
python3 01_document_loading_dan_parsing/2_pdf_and_html_parsing.py
python3 01_document_loading_dan_parsing/3_multimodal_data_prep.py
```
