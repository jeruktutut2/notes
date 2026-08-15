# Implementasi Point 1: Dasar Inference

Memahami konsep fundamental inference dalam AI/ML — apa itu inference, bagaimana perbedaannya dengan training, dan bagaimana menjalankan pipeline inference menggunakan Hugging Face.

## Daftar File

1. `1_apa_itu_inference.py`: Pengenalan konsep inference — definisi, perbedaan dengan training, dan demo sederhana inference menggunakan model pre-trained.
2. `2_pipeline_inference.py`: Menggunakan Hugging Face `pipeline()` untuk berbagai task inference (text classification, NER, summarization, translation, Q&A).

## Urutan Eksekusi

```bash
python 1_apa_itu_inference.py
python 2_pipeline_inference.py
```

## Konsep Kunci

- **Training**: Proses melatih model dari data → menghasilkan bobot (weights)
- **Inference**: Proses menggunakan model yang sudah dilatih → menghasilkan prediksi/output
- **Pipeline**: Abstraksi Hugging Face yang mempermudah inference tanpa setup manual
- **Latency**: Waktu yang dibutuhkan model untuk menghasilkan output (penting di production)
- **Throughput**: Jumlah request yang bisa diproses per satuan waktu
