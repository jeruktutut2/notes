# AI AGENTS - Belajar dari Roadmap.sh

Proyek belajar AI Agents berdasarkan [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents).
Setiap modul berisi kode Python yang bisa langsung dijalankan beserta penjelasan dalam Bahasa Indonesia.

## Install

```bash
pyenv versions
pyenv local 3.9.18
python --version
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install openai tiktoken numpy chromadb
deactivate
python3 main.py
```

## Konfigurasi API Key

Sebelum menjalankan script yang memanggil LLM, set environment variable berikut:

```bash
export OPENAI_API_KEY="sk-xxx-your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # atau Groq/Together/OpenRouter
export OPENAI_MODEL="gpt-4o-mini"  # sesuaikan dengan provider
```

**Provider yang didukung (OpenAI-compatible):**
- OpenAI: `https://api.openai.com/v1`
- Groq: `https://api.groq.com/openai/v1`
- Together AI: `https://api.together.xyz/v1`
- OpenRouter: `https://openrouter.ai/api/v1`

## Menjalankan

```bash
source .venv/bin/activate
python3 main.py
```

## Daftar Modul

| No | Modul | Topik |
|----|-------|-------|
| 01 | LLM Fundamentals | API Call, Generation Controls, Tokenization |
| 02 | Prompt Engineering | Roles, Chain-of-Thought, Structured Output |
| 03 | Tools & Function Calling | Definisi Tool, Eksekusi, Multi-Tool |
| 04 | Agent Loop | ReAct Pattern, Perception→Plan→Act→Observe |
| 05 | Memory | Conversation, Summary, Vector Memory |
| 06 | RAG | Embedding, Similarity Search, Chunking |
| 07 | Multi-Agent | Sequential Pipeline, Supervisor Pattern |
| 08 | Guardrails & Safety | Input Validation, Output Guardrails |
| 09 | Evaluasi & Observability | Automated Eval, Logging & Tracing |
