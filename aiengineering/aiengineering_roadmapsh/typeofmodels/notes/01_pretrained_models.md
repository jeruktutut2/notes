# Catatan Pembelajaran: Pre-trained Models

## 1. Apa itu Pre-trained Model (Foundation Model)?

**Pre-trained Model** (sering disebut *Base Model* atau *Foundation Model*) adalah model pembelajaran mesin (terutama berbasis arsitektur Transformer) yang telah dilatih pada sekumpulan data teks yang sangat besar (terabita/petabita teks dari internet, buku, kode program, artikel ilmiah) menggunakan metode **Self-Supervised Learning**.

Tujuan utama tahap pre-training adalah mengajarkan model **pemahaman bahasa umum**, tata bahasa, fakta tentang dunia, penalaran dasar, dan pola penulisan melalui tugas utama **Next Token Prediction** (prediksi kata/token berikutnya).

---

## 2. Base Model vs Instruct/Chat Fine-Tuned Model

| Karakteristik | Base Model (Pre-trained) | Instruct / Chat Model (Fine-Tuned) |
| :--- | :--- | :--- |
| **Metode Pelatihan** | Self-Supervised Learning pada raw text (Web Crawl, Wikipedia, GitHub) | Base Model + SFT (Supervised Fine-Tuning) + RLHF / DPO |
| **Tujuan Utama** | Melanjutkan teks yang diberikan (Next Token Completion) | Mengikuti instruksi manusia & melakukan percakapan multi-turn |
| **Respon terhadap Prompt** | Jika diberi `"Apa ibukota Indonesia?"`, bisa menjawab `"Apa ibukota Malaysia?"` (melanjutkan teks) | Menjawab `"Ibukota Indonesia adalah Nusantara (atau Jakarta)."` |
| **Format Input** | Raw Text / Teks Polos | ChatML / Prompt Template (`<|im_start|>user...`, `[INST]...[/INST]`) |
| **Penggunaan** | Foundation untuk fine-tuning khusus (Domain Adaptation) | Siap pakai untuk Chatbot, Assistant, RAG, dan Task Automation |

---

## 3. Arsitektur Utama Transformer

Arsitektur Transformer (Vaswani et al., 2017) terbagi menjadi 3 varian utama tergantung pada susunan Encoder dan Decoder:

```text
               +----------------------------------+
               |     Transformer Architectures    |
               +----------------------------------+
                 /                |               \
                /                 |                \
    +-------------------+ +---------------+ +--------------------+
    |   Encoder-Only    | | Decoder-Only  | |  Encoder-Decoder   |
    | (BERT, RoBERTa)   | |(GPT, Llama)   | |  (T5, BART)      |
    +-------------------+ +---------------+ +--------------------+
    | Bi-directional    | | Autoregressive| | Cross-Attention    |
    | Embedding & Class | | Text Gen / LLM| | Translation / Summar|
    +-------------------+ +---------------+ +--------------------+
```

1. **Encoder-Only (Bi-directional)**:
   * **Contoh**: BERT, RoBERTa, DeBERTa.
   * **Mekanisme**: Membaca konteks teks dari dua arah (kiri dan kanan bersamaan).
   * **Kegunaan**: Embeddings, Sentiment Analysis, Text Classification, Named Entity Recognition (NER), Semantic Search.

2. **Decoder-Only (Autoregressive)**:
   * **Contoh**: GPT-4, Llama 3, Mistral, Qwen, DeepSeek.
   * **Mekanisme**: Membaca konteks dari kiri ke kanan (causal masking) untuk memprediksi token berikutnya secara berurutan.
   * **Kegunaan**: Large Language Models (LLM), Generasi Teks, Code Generation, Reasoning, Conversational AI.

3. **Encoder-Decoder (Sequence-to-Sequence)**:
   * **Contoh**: T5, BART, Whisper (Audio to Text).
   * **Mekanisme**: Encoder memproses input ke dalam representasi laten, lalu Decoder menghasilkan output berdasarkan representasi tersebut dengan cross-attention.
   * **Kegunaan**: Penerjemahan Bahasa (Translation), Summarization, Audio Transcription.

---

## 4. Quantization (Kuantisasi) & Format Model

Kuantisasi adalah teknik memetakan bobot model (weights) dari presisi tinggi (seperti FP32 atau FP16) ke presisi lebih rendah (seperti INT8 atau INT4) untuk menghemat VRAM dan mempercepat inference tanpa menurunkan kualitas secara drastis.

### Presisi Bit Model:
* **FP32 (Single Precision)**: 32 bit (4 byte per parameter). Presisi asli pelatihan awal.
* **FP16 / BF16 (Half Precision)**: 16 bit (2 byte per parameter). Standar industri untuk inference & fine-tuning.
* **INT8 (Quantized 8-bit)**: 8 bit (1 byte per parameter). Hemat VRAM 50%, penurunan kualitas sangat minimal.
* **INT4 / Q4_K_M (Quantized 4-bit)**: 4 bit (~0.5 - 0.75 byte per parameter). Hemat VRAM hingga 75%, memungkinkan LLM 7B berjalan di laptop RAM 8GB.

### Format File Model Populer:
1. **GGUF (GPT-Generated Unified Format)**: Format standar Ollama & llama.cpp. Menggabungkan arsitektur, kosa kata (tokenizer), dan bobot terkuantisasi dalam 1 file tunggal. Optimal untuk CPU & Metal (Apple Silicon).
2. **AWQ (Activation-aware Weight Quantization)**: Kuantisasi INT4 yang mempertahankan bobot penting berdasarkan aktivasi. Optimal untuk GPU NVIDIA (vLLM, TensorRT-LLM).
3. **GPTQ (Post-Training Quantization for GPT)**: Kuantisasi 4-bit berkecepatan tinggi untuk GPU.
4. **Safetensors**: Format penyimpanan bobot mentah yang aman (anti-arbitrary code execution) dikembangkan oleh Hugging Face.

---

## 5. Rumus Estimasi VRAM (GPU Memory Formula)

VRAM minimum yang dibutuhkan untuk menjalankan model LLM dapat dihitung dengan rumus:

$$VRAM_{total} = VRAM_{weights} + VRAM_{KV\_Cache} + VRAM_{overhead}$$

Di mana:
1. **$VRAM_{weights}$** = $\text{Jumlah Parameter (Miliar)} \times \text{Byte per Parameter} \times 1.2 \text{ (Margin Safety)}$
   * **FP16 (2 Bytes)**: Model 7B $\rightarrow 7 \times 2 \times 1.2 = 16.8 \text{ GB}$ VRAM.
   * **INT4 (0.5 Bytes)**: Model 7B $\rightarrow 7 \times 0.5 \times 1.2 = 4.2 \text{ GB}$ VRAM.
2. **$VRAM_{KV\_Cache}$**: Memori untuk menyimpan Key-Value Cache selama inferensi multi-turn:
   $$\text{KV Cache} \approx 2 \times N_{layers} \times N_{heads} \times d_{head} \times L_{context} \times B_{batch} \times \text{Bytes}$$
3. **Overhead**: ~1-2 GB untuk PyTorch/CUDA runtime buffers.
