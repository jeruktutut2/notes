# Implementasi Point 5: Memory (Memori Agent)

Modul ini berisi implementasi berbagai jenis memori untuk AI Agent agar bisa mengingat
percakapan sebelumnya dan informasi jangka panjang.

## Daftar File
1. `1_conversation_memory.py`: Short-term memory — mengelola riwayat percakapan dalam prompt.
2. `2_summary_memory.py`: Meringkas percakapan panjang agar muat di context window.
3. `3_vector_memory.py`: Long-term memory — menyimpan dan mencari informasi di vector store.

## Urutan Eksekusi

```bash
python 1_conversation_memory.py
python 2_summary_memory.py
python 3_vector_memory.py
```

### Cara Instalasi Library
```bash
pip install openai chromadb numpy
```
