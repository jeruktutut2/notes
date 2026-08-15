# Implementasi Point 1: LLM Fundamentals (Fondasi - "Otak" Agent)

Modul ini berisi implementasi dasar penggunaan Large Language Model (LLM) via API,
yang merupakan fondasi utama sebelum membangun AI Agent.

## Daftar File
1. `1_api_call_openai_compatible.py`: Cara memanggil LLM via API menggunakan library `openai` (compatible dengan berbagai provider).
2. `2_generation_controls.py`: Eksperimen dengan parameter generasi (Temperature, Top-P, Max Tokens).
3. `3_tokenization_dan_context.py`: Memahami tokenization, menghitung jumlah token, dan context window.

## Urutan Eksekusi

```bash
# Pastikan env vars sudah diset
export OPENAI_API_KEY="sk-xxx"
export OPENAI_BASE_URL="https://api.groq.com/openai/v1"
export OPENAI_MODEL="llama-3.1-8b-instant"

# Jalankan masing-masing
python 1_api_call_openai_compatible.py
python 2_generation_controls.py
python 3_tokenization_dan_context.py  # Tidak butuh API key
```

### Cara Instalasi Library
```bash
pip install openai tiktoken
```
