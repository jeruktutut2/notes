# Subtopik 03: Self-Hosted Models

Modul ini mempelajari teknik penyajian model secara mandiri (**Self-Hosted Models**), penggunaan Ollama REST API, engine inferensi produksi vLLM (PagedAttention & Continuous Batching), penentuan hardware GPU/Apple Silicon, serta pembuatan server FastAPI OpenAI-compatible.

## Daftar Hands-on Script Python:

1. **`01_ollama_local_serving.py`**:
   * Interaksi lengkap dengan service Ollama lokal (List models, Pull, Generate, Streaming response via REST API).

2. **`02_vllm_continuous_batching.py`**:
   * Simulasi konsep PagedAttention dan Continuous Batching untuk throughput inferensi 3x-5x lebih tinggi.

3. **`03_vram_and_gpu_sizing.py`**:
   * Assistant pemilihan spesifikasi hardware GPU (NVIDIA RTX 4090, A100, H100) dan Apple Silicon Unified Memory.

4. **`04_self_hosted_fastapi_server.py`**:
   * Kode server production-ready FastAPI yang mendukung endpoint `/v1/chat/completions` dan `/v1/models` yang kompatibel dengan SDK OpenAI.

## Cara Menjalankan Script:
```bash
python3 03_self_hosted_models/01_ollama_local_serving.py
python3 03_self_hosted_models/02_vllm_continuous_batching.py
python3 03_self_hosted_models/03_vram_and_gpu_sizing.py
python3 03_self_hosted_models/04_self_hosted_fastapi_server.py
```
