# Subtopik 01: Pre-trained Models

Modul ini mempelajari dasar-dasar **Pre-trained Models** (Foundation Models), arsitektur dasar Transformer, kuantisasi presisi bit, serta kalkulasi VRAM untuk inferensi LLM.

## Daftar Hands-on Script Python:

1. **`01_base_vs_instruct_models.py`**:
   * Membandingkan simulasi perilaku Base Model (raw completion) vs Instruct/Chat Fine-tuned Model.
   * Menjelaskan format ChatML dan Special Prompt Templates (`<|im_start|>`, `[INST]`).

2. **`02_model_architectures.py`**:
   * Simulasi 3 arsitektur Transformer: Encoder-Only (BERT/Embeddings), Decoder-Only (GPT/Generative LLM), dan Encoder-Decoder (T5/Translation).

3. **`03_quantization_and_formats.py`**:
   * Simulasi kompresi bobot dan kuantisasi presisi (FP32, FP16, INT8, INT4).
   * Penjelasan format file model (GGUF, AWQ, GPTQ, Safetensors).

4. **`04_model_size_and_vram_calculator.py`**:
   * Tool kalkulator interaktif untuk menghitung VRAM GPU yang dibutuhkan berdasarkan parameter model (7B, 13B, 70B), presisi bit, batch size, dan KV cache.

## Cara Menjalankan Script:
```bash
python3 01_pretrained_models/01_base_vs_instruct_models.py
python3 01_pretrained_models/02_model_architectures.py
python3 01_pretrained_models/03_quantization_and_formats.py
python3 01_pretrained_models/04_model_size_and_vram_calculator.py
```
