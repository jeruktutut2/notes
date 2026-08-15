# FINE-TUNING AI ENGINEERING - Belajar dari Roadmap.sh

Proyek pembelajaran **Fine-Tuning LLM & AI Engineering** berdasarkan [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).
Setiap modul berisi skrip Python runnable yang dapat langsung dijalankan beserta penjelasan teori, formula matematika, dan demonstrasi praktis dalam Bahasa Indonesia.

## Persiapan Environment & Install

```bash
# Menggunakan venv Python 3.9+
pyenv versions
pyenv local 3.9.18
python --version
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install torch transformers datasets peft trl numpy pandas scikit-learn
deactivate
python3 main.py
```

> **Catatan Hardware:** Seluruh modul dirancang dapat berjalan ringan di **CPU / Macbook / Apple Silicon** menggunakan dataset sintetis dan model miniatur (seperti `distilgpt2` atau PyTorch custom layers). Jika Anda memiliki GPU Nvidia (CUDA), skrip akan secara otomatis mendeteksi dan menggunakan CUDA.

## Cara Menjalankan

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul:

```bash
source .venv/bin/activate
python3 main.py
```

---

## Daftar Modul Pembelajaran

| No | Modul | Topik & Materi | Skrip Python |
|----|-------|----------------|--------------|
| **01** | Persiapan Dataset & Formatting | Format Alpaca vs ShareGPT, Cleaning & Deduplication, Tokenization & Chat Templates (ChatML, Llama-3) | `01_persiapan_dataset_dan_formatting/` |
| **02** | PEFT & LoRA Architecture | Custom LoRA Linear layer dari scratch ($W + \frac{\alpha}{r} BA$), Hugging Face `peft`, Quantization NF4/QLoRA | `02_peft_dan_lora_architecture/` |
| **03** | Supervised Fine-Tuning (SFT) | Custom SFT Training Loop (Cross-Entropy Target Loss), HF `trl` SFTTrainer, Memory Efficiency (Grad Accum, Mixed Precision) | `03_supervised_fine_tuning_sft/` |
| **04** | Preference Alignment (DPO & RLHF) | Direct Preference Optimization (Chosen vs Rejected Loss), Reward Model & ORPO Alignment | `04_preference_alignment_dpo_rlhf/` |
| **05** | Evaluasi & Hyperparameters | Perplexity & BLEU/ROUGE Evaluation, Hyperparameter Tuning (Learning Rate Warmup, LoRA Rank $r$, Alpha, Dropout) | `05_evaluasi_dan_hyperparameters/` |
| **06** | Merging, Export & Inference | Merging LoRA Weights into Base Model, Safetensors & GGUF Export, Fine-Tuned Model Inference (Greedy vs Sampling) | `06_merging_export_dan_inference/` |

---

## Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap tahap fine-tuning (mulai dari matematika LoRA hingga DPO) dapat dibaca di folder [notes/fine_tuning_roadmap_notes.md](notes/fine_tuning_roadmap_notes.md).
