# Subtopik 02: Closed vs Open Source Models

Modul ini mempelajari perbandingan mendasar antara **Proprietary Closed APIs** (OpenAI, Anthropic Claude, Google Gemini) dan **Open Weights Models** (Llama 3, Mistral, Qwen, DeepSeek), matriks biaya, serta lisensi open source.

## Daftar Hands-on Script Python:

1. **`01_closed_api_clients.py`**:
   * Unified interface client untuk melakukan request ke OpenAI, Claude, dan Gemini (dengan fallback simulation).

2. **`02_open_weights_huggingface.py`**:
   * Penggunaan Hugging Face Model Hub client untuk menginspeksi metadata model open-weights, config, dan file weights.

3. **`03_tradeoff_matrix_and_benchmark.py`**:
   * Simulator benchmark perbandingan Biaya (Cost per 1M tokens), Latensi, Privasi Data, dan Kontrol.

4. **`04_licensing_and_compliance_checker.py`**:
   * Tool analyzer lisensi open source (Apache 2.0, MIT, Llama 3 Community License, RAIL).

## Cara Menjalankan Script:
```bash
python3 02_closed_vs_open_source/01_closed_api_clients.py
python3 02_closed_vs_open_source/02_open_weights_huggingface.py
python3 02_closed_vs_open_source/03_tradeoff_matrix_and_benchmark.py
python3 02_closed_vs_open_source/04_licensing_and_compliance_checker.py
```
