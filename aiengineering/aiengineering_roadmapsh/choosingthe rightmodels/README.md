# CHOOSING THE RIGHT MODELS - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **Choosing the Right Models** berdasarkan roadmap resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)**.

Workspace ini merangkum seluruh lanskap pemilihan model AI, membandingkan **Closed Models**, **Open Source Models**, **Platforms & Ecosystem**, serta **APIs & SDKs**.

---

## 🎯 Peta Struktur Pembelajaran

```text
choosingthe rightmodels/
├── README.md                                    # Dokumentasi utama workspace
├── main.py                                      # Master CLI Interactive Runner & Test Suite
├── requirements.txt                             # Python Dependencies
│
├── notes/                                       # Catatan Pembelajaran Komprehensif (Bahasa Indonesia)
│   ├── 01_closed_models.md                      # Claude 3.5, Gemini 1.5, OpenAI GPT-4o/o1, Cohere, Mistral
│   ├── 02_open_source_models.md                 # Meta Llama 3.1/3.2, DeepSeek V3/R1, Qwen 2.5, Gemma 2
│   ├── 03_platforms_and_ecosystem.md            # Hugging Face Tasks/Hub/Transformers.js, Ollama, LM Studio, OpenRouter
│   ├── 04_apis_and_sdks.md                      # OpenAI Response API, Claude Messages API, Gemini API, HF SDK
│   └── 05_choosing_models_decision_matrix.md    # Selection Framework, Cost/Latency/Privacy Decision Matrix
│
├── 01_closed_models/                            # Subtopik 1: Closed Models
│   ├── 01_openai_models.py                      # GPT-4o, GPT-4o-mini, o1/o3 reasoning & Structured Output
│   ├── 02_anthropic_claude.py                   # Claude 3.5 Sonnet/Haiku, Prompt Caching & 200K Context
│   ├── 03_google_gemini.py                      # Gemini 1.5 Pro/Flash native multimodal & 2M Context
│   ├── 04_cohere_and_mistral.py                 # Cohere Command R+ (RAG Citations) & Mistral Large 2
│   └── README.md
│
├── 02_open_source_models/                       # Subtopik 2: Open Source Models
│   ├── 01_meta_llama.py                         # Meta Llama 3.1/3.2 family (1B s/d 405B) & Hardware VRAM
│   ├── 02_deepseek_models.py                    # DeepSeek V3 & R1 MoE architecture & Distilled models
│   ├── 03_qwen_multilingual.py                  # Qwen 2.5 series (Coder, Math, Multilingual)
│   ├── 04_google_gemma.py                       # Gemma 2 lightweight on-device open weight models
│   └── README.md
│
├── 03_platforms_and_ecosystem/                  # Subtopik 3: Platforms & Ecosystem
│   ├── 01_huggingface_hub_and_tasks.py          # HF Hub model discovery, pipeline tasks, model cards
│   ├── 02_transformers_js_web.py                # Client-side web execution via Transformers.js
│   ├── 03_ollama_and_lmstudio.py                # Local model runtimes (Ollama API, LM Studio endpoints)
│   ├── 04_openrouter_unified_gateway.py         # OpenRouter unified API gateway & auto-fallback
│   └── README.md
│
├── 04_apis_and_sdks/                            # Subtopik 4: APIs & SDKs
│   ├── 01_openai_response_api.py                # OpenAI Response API & Function Calling Tool Schema
│   ├── 02_claude_messages_api.py                # Anthropic Messages API & System instructions
│   ├── 03_gemini_api_integration.py             # Google Gemini SDK & Multimodal payload processing
│   ├── 04_hf_inference_sdk_and_compat.py        # HF Inference SDK & Custom OpenAI-Compatible FastAPI
│   └── README.md
│
└── web_visualizer/                              # Interactive Web Visualizer & Playground
    ├── index.html                               # Modern Glassmorphism Dashboard UI
    ├── styles.css                               # Dark Mode Design System
    └── app.js                                   # Interactive Model Matrix, Cost Calculator & Decision Tree
```

---

## 🚀 Cara Menggunakan Workspace

### 1. Menjalankan Master CLI Runner
Jalankan file master CLI untuk memilih dan mengeksekusi modul pembelajaran secara interaktif:

```bash
python3 main.py
```

Untuk mengeksekusi seluruh pengujian suite secara otomatis:
```bash
python3 main.py --test
```

### 2. Membuka Interactive Web Visualizer
Jalankan local HTTP server untuk membuka visualizer interaktif di browser:

```bash
python3 -m http.server 8080 --directory web_visualizer
# Buka http://localhost:8080 di browser Anda
```

---

## 📚 Ringkasan Subtopik

### 1. Closed Models (Proprietary)
* **Anthropic Claude**: Terkemuka untuk *coding*, *reasoning*, dan hemat biaya via *Prompt Caching* (-90% cost, -85% latency).
* **Google Gemini**: Native *multimodal* (Video, Audio, Teks) dengan context window hingga 2 juta token.
* **OpenAI (GPT & o-series)**: Ekosistem terluas dengan *Structured Outputs* terjamin 100% valid schema & *o1 reasoning*.
* **Cohere & Mistral**: Spesialis enterprise RAG (citations) & kedaulatan data Uni Eropa (GDPR).

### 2. Open Source / Open Weights Models
* **Meta Llama 3.1 & 3.2**: Standar industri open-source (1B s/d 405B), lisensi komersial hingga 700M MAU.
* **DeepSeek V3 & R1**: Arsitektur *Mixture-of-Experts* (MoE) efisien (671B Total / 37B Active) dan *pure RL reasoning*.
* **Qwen 2.5**: Spesialis multibahasa (Bahasa Indonesia) serta varian *Qwen-Coder* dan *Qwen-Math*.
* **Gemma 2**: Model open weights ringan Google (2.7B, 9B, 27B) ideal untuk perangkat lokal/edge.

### 3. Platforms & Ecosystem
* **Hugging Face**: Hub repositori model, taksonomi Tasks, dan in-browser inference via *Transformers.js*.
* **Local Runtimes**: *Ollama* (CLI-first REST API) & *LM Studio* (GUI desktop local server).
* **OpenRouter**: Unified Gateway API yang menghubungkan 100+ model dengan 1 key dan *automatic fallback*.

### 4. APIs & SDKs
* Standardisasi API endpoints, payload JSON Schema, system prompts, serta pembuatan server *OpenAI-Compatible API*.

---

## 📝 Catatan Lengkap Pembelajaran
Baca dokumentasi lengkap di folder [notes/](file:///Users/bsa/Documents/por/aiengineering/choosingthe%20rightmodels/notes):
* [01_closed_models.md](file:///Users/bsa/Documents/por/aiengineering/choosingthe%20rightmodels/notes/01_closed_models.md)
* [02_open_source_models.md](file:///Users/bsa/Documents/por/aiengineering/choosingthe%20rightmodels/notes/02_open_source_models.md)
* [03_platforms_and_ecosystem.md](file:///Users/bsa/Documents/por/aiengineering/choosingthe%20rightmodels/notes/03_platforms_and_ecosystem.md)
* [04_apis_and_sdks.md](file:///Users/bsa/Documents/por/aiengineering/choosingthe%20rightmodels/notes/04_apis_and_sdks.md)
* [05_choosing_models_decision_matrix.md](file:///Users/bsa/Documents/por/aiengineering/choosingthe%20rightmodels/notes/05_choosing_models_decision_matrix.md)
