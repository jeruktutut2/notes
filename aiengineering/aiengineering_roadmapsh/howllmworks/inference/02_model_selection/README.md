# Implementasi Point 2: Model Selection

Memahami cara memilih model AI yang tepat untuk kebutuhan inference — mulai dari perbandingan model open-source vs closed API, menggunakan Hugging Face Model Hub, hingga menjalankan model secara lokal.

## Daftar File

1. `1_open_vs_closed_model.py`: Perbandingan lengkap antara model open-source (Hugging Face, Ollama) vs closed API (OpenAI, Anthropic) — kapan pakai yang mana.
2. `2_huggingface_model_hub.py`: Cara mencari, memilih, dan mengunduh model dari Hugging Face Hub berdasarkan task, ukuran, dan performa.
3. `3_ollama_local_inference.py`: Menjalankan LLM secara lokal menggunakan Ollama — tanpa perlu GPU cloud atau API key.

## Konsep Kunci

| Aspek | Open-Source | Closed API |
|-------|------------|------------|
| Biaya | Gratis (tapi butuh hardware) | Bayar per token/request |
| Privasi | Data tetap di lokal | Data dikirim ke server vendor |
| Kustomisasi | Bisa fine-tune | Terbatas (prompt engineering) |
| Performa | Bervariasi | Umumnya state-of-the-art |
| Setup | Perlu infrastruktur | Cukup API key |
| Contoh | Llama, Mistral, Gemma | GPT-4, Claude, Gemini |
