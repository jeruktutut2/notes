# 02. Closed-Source vs Open-Source Models

Modul ini mempelajari analisis perbandingan antara **Closed-Source Models (API Proprietary)** dan **Open-Source Models (Open Weights)** dalam arsitektur AI Engineering.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Model Proprietary (Closed-Source API)
- **Contoh**: OpenAI (GPT-4o, o1), Anthropic (Claude 3.5 Sonnet), Google (Gemini 1.5 Pro).
- **Keunggulan**: SOTA Accuracy, Zero Infrastructure Management, Dukungan Built-in Caching & JSON Mode terbaik.
- **Kelemahan**: Data privacy risk (dikirim ke server pihak ketiga), Biaya per-token API bertumbuh linier dengan skala trafik, *Vendor Lock-in*.

### 2. Open-Source / Open-Weight Models
- **Contoh**: Meta (Llama 3.3 / 3.1), Mistral AI, Qwen 2.5, DeepSeek R1 / V3.
- **Keunggulan**: Data Privacy 100% (On-premise / VPC lokal), Tidak ada biaya token API per panggilan, Bebas di-fine-tune / diubah bobotnya.
- **Kelemahan**: Membutuhkan pengelolaan server GPU (vLLM / TGI), biaya fixed infrastructure.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat kalkulator TCO (Total Cost of Ownership) Closed-Source vs Open-Source.
