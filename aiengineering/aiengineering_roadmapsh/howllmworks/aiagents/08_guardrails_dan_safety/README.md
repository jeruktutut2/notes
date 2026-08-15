# Implementasi Point 8: Guardrails & Safety (Keamanan Agent)

Modul ini berisi implementasi mekanisme keamanan untuk AI Agent:
memvalidasi input user dan mengecek output agent sebelum dikirimkan.

## Daftar File
1. `1_input_validation.py`: Memfilter input berbahaya (prompt injection, konten tidak pantas).
2. `2_output_guardrails.py`: Mengecek output agent sebelum dikirim ke user (PII, format, safety).

## Urutan Eksekusi

```bash
python 1_input_validation.py
python 2_output_guardrails.py
```

### Cara Instalasi Library
```bash
pip install openai
```
