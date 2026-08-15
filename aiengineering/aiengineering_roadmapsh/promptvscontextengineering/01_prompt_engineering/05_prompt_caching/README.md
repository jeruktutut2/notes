# 05. Prompt Caching

Modul ini mempelajari teknik *Prompt Caching* (KV Cache Optimization) untuk memotong biaya API hingga 80-90% dan menurunkan latensi *Time-To-First-Token (TTFT)*.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Konsep Prompt Caching
- **Definisi**: Menyimpan hasil pengolahan tensor *Key-Value (KV) Attention State* dari potongan prompt statis (seperti System Instruction, Dokumentasi RAG, atau Few-Shot Examples) di GPU memory penyedia LLM.
- **Provider Support**: Anthropic Claude (`cache_control: {"type": "ephemeral"}`), OpenAI (Automatic Prompt Caching untuk prompt > 1024 token), vLLM / SGLang.

### 2. Aturan & Structure Prompt Caching
- **Static Prefix Rule**: Elemen yang akan di-cache **WAJIB** berada di posisi paling awal (*prefix*) prompt. Jika ada 1 karakter yang berubah di awal, seluruh cache selanjutnya akan hangus (*cache miss*).
- **Minimum Token Threshold**: Umumnya membutuhkan minimal 1.024 token (OpenAI) atau 2.048 token (Anthropic) untuk dapat di-cache.
- **Cache TTL (Time-To-Live)**: Cache bertahan 5 menit (ephemeral) dan diperpanjang otomatis setiap ada request baru yang cocok (*cache hit*).

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi perbedaan latensi dan biaya antara Cold Start (Cache Miss) vs Warm Request (Cache Hit).
