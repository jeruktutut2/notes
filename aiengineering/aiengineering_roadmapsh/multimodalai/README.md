# 🎨 MULTIMODAL AI - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **Multimodal AI** berdasarkan peta kurikulum resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)** dan diagram arsitektur Multimodal AI.

---

## 🎯 Peta Kurikulum & Diagram Topik

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                          Multimodal AI Usecases                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  • Image Understanding (VQA, OCR, Object Detection, Visual Reasoning)       │
│  • Image Generation (Text-to-Image, Diffusion Models, Inpainting)           │
│  • Video Understanding (Keyframe Sampling, Temporal QA, Action Detection)   │
│  • Audio Processing (Spectrogram Analysis, Feature Extraction, Classification)│
│  • Text-to-Speech (TTS Vocoder Pipeline, Voice Cloning, Prosody Control)   │
│  • Speech-to-Text (STT/ASR Whisper Encoder-Decoder, Timestamping)           │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│...                       Implementing Multimodal AI                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                           Multimodal AI Tasks                               │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ OpenAI Vision API (GPT-4o Multi-Image Analysis & Structured Output)     │ │
│ │ DALL-E API (Image Synthesis & Prompt Revisions)                        │ │
│ │ NanoBanana API (Specialized & Custom Multimodal REST Endpoints)         │ │
│ │ Whisper API (Audio Transcription, Translation & Subtitles)              │ │
│ │ Hugging Face Models (CLIP Embeddings, BLIP Captioning, Florence-2)      │ │
│ │ LangChain for Multimodal Apps (Multimodal Prompt Templates & Chains)    │ │
│ │ LlamaIndex for Multimodal Apps (MultiModalVectorStoreIndex & Engines)   │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Struktur Direktori Workspace

```text
multimodalai/
├── README.md                                    # Panduan utama workspace & kurikulum
├── main.py                                      # Master Interactive CLI Runner & Test Suite
├── requirements.txt                             # Dependencies Python (Pillow, NumPy, Requests, etc.)
│
├── notes/                                       # Catatan Teori Komprehensif (Bahasa Indonesia)
│   ├── 01_multimodal_usecases_notes.md          # Analisis Teori 6 Multimodal Usecases
│   ├── 02_multimodal_tasks_notes.md             # Analisis Teori 7 Multimodal Tasks & Frameworks
│   └── multimodal_ai_roadmap_notes.md           # Rangkuman Panduan Roadmap Multimodal AI
│
├── 01_multimodal_usecases/                      # Modul 01: Multimodal AI Usecases
│   ├── 01_image_understanding.py                # Visual QA, OCR, Object Detection & Base64 Payload
│   ├── 02_image_generation.py                   # Latent Diffusion Simulation, Prompt Parsing & ControlNet
│   ├── 03_video_understanding.py                # Keyframe Sampling, Temporal Video QA & Action Analysis
│   ├── 04_audio_processing.py                   # Spectrogram Waveform Feature Extraction & Audio Classification
│   ├── 05_text_to_speech.py                     # TTS Vocoder Pipeline, Voice Cloning & SSML Prosody
│   ├── 06_speech_to_text.py                     # STT/ASR Whisper Mel-Spectrogram & Timestamp Decoding
│   └── README.md                                # Submodul README
│
├── 02_multimodal_tasks_and_sdks/                # Modul 02: Multimodal AI Tasks & SDKs
│   ├── 01_openai_vision_api.py                  # GPT-4o / GPT-4 Vision SDK & Multi-Image Comparison
│   ├── 02_dalle_api.py                          # DALL-E 3 API Generator & Prompt Revision Inspector
│   ├── 03_nanobanana_api.py                     # Specialized/Gemini Multimodal REST Endpoint Integration
│   ├── 04_whisper_api.py                        # Whisper API Transcription & SRT/VTT Alignment
│   ├── 05_huggingface_models.py                 # HF Transformers Pipeline (CLIP, BLIP, Florence-2)
│   ├── 06_langchain_multimodal.py               # LangChain Multimodal Prompt Templates & Chains
│   ├── 07_llamaindex_multimodal.py              # LlamaIndex MultiModalVectorStoreIndex & Image Indexing
│   └── README.md                                # Submodul README
│
└── web_visualizer/                              # Interactive Web Dashboard Visualizer
    ├── index.html                               # Modern UI Dashboard (Dark Mode Amber/Gold Glassmorphism)
    ├── styles.css                               # Design System & Styling
    └── app.js                                   # Interactive Simulator & Multimodal Playground
```

---

## 🚀 Cara Menjalankan Workspace

### 1. Menjalankan Master Interactive CLI Runner
Jalankan file `main.py` untuk memilih dan menguji modul secara interaktif dari terminal:

```bash
python3 main.py
```

Untuk menjalankan seluruh modul test suite secara otomatis:
```bash
python3 main.py --all
```

### 2. Menjalankan Standalone Python Script
Masing-masing modul Python dibuat *self-contained* sehingga dapat dijalankan secara terpisah tanpa API Key wajib:

```bash
# 1. Image Understanding Demo
python3 01_multimodal_usecases/01_image_understanding.py

# 2. Audio Processing Demo
python3 01_multimodal_usecases/04_audio_processing.py

# 3. OpenAI Vision API Demo
python3 02_multimodal_tasks_and_sdks/01_openai_vision_api.py

# 4. LangChain Multimodal Apps
python3 02_multimodal_tasks_and_sdks/06_langchain_multimodal.py
```

### 3. Membuka Interactive Web Visualizer
Buka file `web_visualizer/index.html` di browser favorit Anda atau jalankan HTTP server lokal:

```bash
python3 -m http.server 8080 --directory web_visualizer
```
Akses di browser: `http://localhost:8080`
