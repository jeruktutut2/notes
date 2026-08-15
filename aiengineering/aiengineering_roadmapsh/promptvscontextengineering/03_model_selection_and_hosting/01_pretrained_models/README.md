# 01. Pre-trained Foundation Models

Modul ini mempelajari arsitektur dasar model LLM *pre-trained* (Model Fondasi) dan bagaimana skala parameter serta tipe tuning mempengaruhi strategi Prompt vs Context Engineering.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Model Scaling & Capabilities
- **Parameter Sizes**: 7B / 8B (Ringan, cepat, lokal), 70B (Enterprise standar), 405B+ (Model raksasa seperti Llama-3.1-405B / GPT-4o).
- **Base Models vs Instruction-Tuned (IT / Instruct)**:
  - **Base Model**: Melanjutkan kalimat tanpa memahami instruksi percakapan.
  - **Instruct Model**: Dilatih dengan SFT (Supervised Fine-Tuning) + RLHF/DPO untuk mematuhi Prompt & System Instructions.

### 2. Hubungan Pre-trained Models dengan Prompt/Context
- Model dengan kapasitas parameter lebih besar (misal 70B+) memiliki penalaran CoT yang lebih kuat dibanding model 8B.
- Model dengan Context Window panjang (128K - 2M tokens) membutuhkan strategi *Context Compaction* dan *Prefix Caching* agar tetap ekonomis.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi perbandingan kapasitas model dan rekomendasi arsitektur.
