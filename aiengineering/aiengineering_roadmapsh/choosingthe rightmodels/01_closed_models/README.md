# Subtopik 1: Closed Models (Proprietary APIs)

Modul ini mempelajari penggunaan dan karakteristik teknis model komersial closed-source:
1. `01_openai_models.py` - Penggunaan OpenAI GPT-4o, GPT-4o-mini, dan o1/o3 reasoning model dengan Structured Outputs.
2. `02_anthropic_claude.py` - Penggunaan Anthropic Claude 3.5 Sonnet / Haiku, Prompt Caching, dan sistem pesan.
3. `03_google_gemini.py` - Pemanfaatan Google Gemini 1.5 Pro / Flash untuk pemrosesan multimodal & konteks masif.
4. `04_cohere_and_mistral.py` - Penggunaan Cohere Command R+ (Enterprise RAG/Citations) & Mistral Large.

## Cara Menjalankan Script
```bash
python3 01_closed_models/01_openai_models.py
python3 01_closed_models/02_anthropic_claude.py
python3 01_closed_models/03_google_gemini.py
python3 01_closed_models/04_cohere_and_mistral.py
```
*(Catatan: Jika API key tidak diset di `.env`, script akan secara otomatis menjalankan Mode Simulasi Offline untuk pengujian).*
