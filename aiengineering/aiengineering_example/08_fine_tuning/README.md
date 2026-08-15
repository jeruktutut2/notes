# 📘 Modul 8 — Fine-Tuning (Melatih Ulang Model)

Modul ini mempelajari konsep **Fine-Tuning**, yaitu mengambil model AI dasar yang sudah ada lalu melatih ulang sebagian bobot parameternya (*weights*) menggunakan dataset kustom agar lebih ahli di domain spesifik.

---

## ⚖️ Kapan Perlu Fine-Tuning vs RAG?

| Kebutuhan | Solusi Terbaik |
|---|---|
| AI perlu pengetahuan dokumen internal terbaru | ❌ Fine-Tuning -> ✅ **RAG (Modul 4)** |
| AI perlu memformat data JSON secara ketat | ❌ Fine-Tuning -> ✅ **Pydantic (Modul 3)** |
| AI perlu gaya bahasa, persona, atau dialek khusus | ✅ **Fine-Tuning (LoRA / QLoRA)** |
| Mengurangi jumlah token prompt instruction yang panjang | ✅ **Fine-Tuning** |

---

## 🛠️ Alur Langkah Kerja
1. `prepare_data.py`: Mengubah pasangan data mentah QA menjadi format `dataset_finetune.jsonl`.
2. `fine_tune.py`: Membuat file `Modelfile` lokal untuk Ollama dan menyediakan template skrip QLoRA / Unsloth untuk eksekusi GPU gratis di Google Colab.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# 1. Siapkan dataset
python 08_fine_tuning/prepare_data.py

# 2. Buat Modelfile Ollama
python 08_fine_tuning/fine_tune.py

# 3. Rakit model custom baru di Ollama
cd 08_fine_tuning
ollama create cs-serba-jaya -f Modelfile
ollama run cs-serba-jaya
```
