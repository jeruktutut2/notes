# Implementasi Point 3: Tools & Function Calling

Modul ini berisi implementasi bagaimana LLM bisa memanggil "tools" (fungsi eksternal)
untuk berinteraksi dengan dunia luar — ini adalah fondasi utama AI Agent.

## Daftar File
1. `1_function_calling_basic.py`: Mendefinisikan tool schema dan memahami alur function calling.
2. `2_tool_execution.py`: Mengeksekusi fungsi berdasarkan respons LLM dan mengembalikan hasilnya.
3. `3_multi_tool_agent.py`: Agent sederhana dengan multiple tools (kalkulator, cuaca, waktu).

## Urutan Eksekusi

```bash
python 1_function_calling_basic.py
python 2_tool_execution.py
python 3_multi_tool_agent.py
```

### Cara Instalasi Library
```bash
pip install openai
```
