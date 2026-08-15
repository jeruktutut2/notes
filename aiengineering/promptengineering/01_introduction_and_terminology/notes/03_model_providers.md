# 03. Major LLM Providers & Model Comparison

## Overview
Node **"Models offered by ___"** pada roadmap.sh menyoroti 5 penyedia model kecerdasan buatan terdepan saat ini. Setiap provider memiliki keunggulan arsitektur, ukuran context window, biaya, dan kekuatan penalaran yang berbeda.

---

## 1. OpenAI
Pionir dalam komersialisasi LLM melalui seri GPT.

- **Flagship Models**:
  - **GPT-4o (Omni)**: Model multimodal multimodal terdepan untuk teks, audio, dan visi. Context window: 128k token.
  - **GPT-4o-mini**: Model efisien berkecepatan tinggi dengan biaya sangat murah untuk task standar.
  - **o1 & o3-mini (Reasoning Models)**: Model berpenalaran tinggi yang menggunakan *Chain of Thought internal* untuk memecahkan masalah matematika kompleks, pemrogramam kompetitif, dan sains murni.

---

## 2. Google (Google DeepMind)
Pemimpin riset kecerdasan buatan modern (pencipta arsitektur Transformer pada tahun 2017).

- **Flagship Models**:
  - **Gemini 1.5 Pro**: Memiliki context window industri terbesar hingga **2.000.000 (2 Juta) token**. Mampu memproses 1 jam video, 11 jam audio, atau 30.000 baris kode sekaligus dalam satu prompt.
  - **Gemini 1.5 / 2.0 Flash**: Model ultra-fast dengan latensi sub-detik untuk aplikasi real-time.

---

## 3. Anthropic
Didirikan oleh mantan peneliti OpenAI dengan fokus utama pada **Constitutional AI** dan kecerdasan berkeselamatan tinggi.

- **Flagship Models**:
  - **Claude 3.5 Sonnet**: Standar emas industri untuk pemrograman (*coding*), pemahaman konteks rumit, dan nuansa bahasa. Context window: 200k token.
  - **Claude 3.5 Haiku**: Model cepat dan sangat efisien.
  - **Claude 3 Opus**: Model penalaran mendalam untuk analisis dokumen dan karya tulis kompleks.

---

## 4. Meta (Open Source / Open Weights)
Pelopor gerakan AI Sumber Terbuka (*Open Weights AI*).

- **Flagship Models**:
  - **Llama 3.1 / 3.3 (8B, 70B, 405B)**: Family model open-weights berkinerja tinggi yang dapat di-host sendiri (*self-hosted*) secara privat di infrastruktur cloud maupun server lokal tanpa biaya lisensi per-token.

---

## 5. xAI
Perusahaan AI yang didirikan oleh Elon Musk dengan fokus pada pencarian kebenaran maksimum dan integrasi data real-time dari platform X (Twitter).

- **Flagship Models**:
  - **Grok 2 & Grok 3**: Model berkinerja tinggi dengan kemampuan penalaran kuat, akses data real-time, dan kemampuan pemrosesan multimodal & visual.

---

## Ringkasan Matriks Perbandingan Model

| Provider | Model Utama | Context Window | Keunggulan Utama | Akses Kode / Weights |
| :--- | :--- | :--- | :--- | :--- |
| **OpenAI** | GPT-4o / o3-mini | 128k | Ecosystem, Function Calling, Reasoning | Closed API |
| **Google** | Gemini 1.5 Pro | 2,000k (2M) | Context window raksasa, Multimodal | Closed API |
| **Anthropic** | Claude 3.5 Sonnet | 200k | Coding & Complex Instructions | Closed API |
| **Meta** | Llama 3.3 70B/405B | 128k | Open Weights, Self-Hosted Privacy | Open Weights |
| **xAI** | Grok 2 / 3 | 128k | Real-time data synthesis, Reasoning | Closed / Partial Open |
