# TYPE OF MODELS - AI ENGINEER ROADMAP

Selamat datang di workspace pembelajaran **Type of Models** berdasarkan roadmap resmi **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)**.

Workspace ini dirancang khusus untuk menguasai klasifikasi, arsitektur, metode deployment, dan pemilihan model dalam dunia AI Engineering.

---

## 🎯 Peta Materi Pembelajaran

```text
typeofmodels/
├── README.md                            # Dokumentasi utama workspace
├── main.py                              # Master CLI Interactive Runner & Test Suite
├── requirements.txt                      # Dependencies Python
│
├── notes/                               # Catatan Pembelajaran Komprehensif (Bahasa Indonesia)
│   ├── 01_pretrained_models.md          # Pre-trained, Base vs Instruct, Quantization, VRAM
│   ├── 02_closed_vs_open_source.md      # Closed APIs vs Open Weights, Trade-off Matrix, Licensing
│   ├── 03_self_hosted_models.md          # Self-Hosting (Ollama, vLLM, Hardware Sizing, FastAPI)
│   └── 04_type_of_models_synthesis.md   # Panduan Strategis Pemilihan Model & Matrix Keputusan
│
├── 01_pretrained_models/                # Subtopik 1: Pre-trained Models
│   ├── 01_base_vs_instruct_models.py    # Simulasi Base Completion vs Instruction/Chat Model
│   ├── 02_model_architectures.py        # Encoder-Only, Decoder-Only, Encoder-Decoder Mechanics
│   ├── 03_quantization_and_formats.py    # Simulasi Presisi (FP32/FP16/INT8/INT4 & GGUF/AWQ/GPTQ)
│   ├── 04_model_size_and_vram_calculator.py # Kalkulator Interaktif VRAM, Parameter & KV Cache
│   └── README.md
│
├── 02_closed_vs_open_source/            # Subtopik 2: Closed vs Open Source Models
│   ├── 01_closed_api_clients.py        # Unified API Client (OpenAI, Claude, Gemini)
│   ├── 02_open_weights_huggingface.py   # Hugging Face Hub Client & Model Metadata Inspector
│   ├── 03_tradeoff_matrix_and_benchmark.py # Simulator Benchmark Biaya, Latensi, Privasi & Performa
│   ├── 04_licensing_and_compliance_checker.py # Analyzer Lisensi Open Source (Apache 2.0, Llama, MIT)
│   └── README.md
│
├── 03_self_hosted_models/               # Subtopik 3: Self-Hosted Models
│   ├── 01_ollama_local_serving.py       # Interaksi REST API Ollama lokal (Pull, Generate, Stream)
│   ├── 02_vllm_continuous_batching.py   # Simulasi PagedAttention & Continuous Batching
│   ├── 03_vram_and_gpu_sizing.py        # Assistant Rekomendasi Hardware GPU & Apple Silicon
│   ├── 04_self_hosted_fastapi_server.py # Server Production-Ready OpenAI-Compatible FastAPI
│   └── README.md
│
└── web_visualizer/                      # Visualizer & Interactive Web Dashboard
    ├── index.html                       # Web Playground Interaktif UI
    ├── styles.css                       # Modern Dark-Mode Glassmorphism Design
    └── app.js                           # Logic & Interactive Calculators
```

---

## 🚀 Cara Menggunakan Workspace

### 1. Menjalankan Master CLI Runner
Anda dapat menjalankan file master CLI untuk mengakses seluruh modul pembelajaran secara interaktif:

```bash
python3 main.py
```

### 2. Menjalankan Modul Spesifik secara Langsung
Setiap script Python bersifat *standalone* dan dapat dijalankan langsung dari terminal:

```bash
# Contoh 1: Kalkulator VRAM & Model Parameters
python3 01_pretrained_models/04_model_size_and_vram_calculator.py

# Contoh 2: Benchmark Closed API vs Open Source
python3 02_closed_vs_open_source/03_tradeoff_matrix_and_benchmark.py

# Contoh 3: Serving Model Lokal via Ollama API
python3 03_self_hosted_models/01_ollama_local_serving.py
```

### 3. Membuka Interactive Web Visualizer
Buka file `web_visualizer/index.html` langsung di browser Anda atau gunakan local server:

```bash
python3 -m http.server 8080 --directory web_visualizer
# Buka http://localhost:8080 di browser
```

---

## 📚 Ringkasan Subtopik

### 1. Pre-trained Models
* **Base Models vs Instruct Models**: Perbedaan model murni completion (pretrained on raw web text) dengan model yang diselaraskan menggunakan SFT (Supervised Fine-Tuning) dan RLHF/DPO.
* **Arsitektur Transformer**: Breakdown mekanik Encoder-Only (BERT/RoBERTa), Decoder-Only (GPT/Llama/Mistral), dan Encoder-Decoder (T5/BART).
* **Quantization & Formats**: Memahami FP32, FP16/BF16, INT8, INT4, serta format file model seperti GGUF, AWQ, GPTQ, dan Safetensors.
* **VRAM Calculation**: Formula matematis menghitung kebutuhan memory GPU berdasarkan jumlah parameter, presisi bit, KV Cache, batch size, dan context length.

### 2. Closed vs Open Source Models
* **Proprietary Closed APIs**: Penggunaan OpenAI GPT-4o, Anthropic Claude 3.5 Sonnet, dan Google Gemini via API.
* **Open Weights Models**: Pemanfaatan Llama 3.1, Mistral/Mixtral, Qwen 2.5, dan DeepSeek dari Hugging Face Hub.
* **Matriks Trade-Off**: Evaluasi komprehensif antara Biaya (Cost per 1M tokens), Latensi (TTFT & TPS), Data Privacy/Sovereignty, dan Control/Customizability.
* **Open Source Licensing**: Analisis lisensi Apache 2.0, MIT, Llama 3 Community License, Rai License, dan pembatasan komersial (MAU limit).

### 3. Self-Hosted Models
* **Local Runners**: Penggunaan Ollama, llama.cpp, dan LM Studio untuk iterasi cepat & pengembangan lokal.
* **Production Engine**: vLLM dan TGI dengan PagedAttention, KV Cache Offloading, dan Continuous Batching untuk throughput maksimum.
* **Hardware Sizing**: Pemilihan GPU (NVIDIA RTX 4090, A100, H100) vs Apple Silicon Unified Memory (M2/M3/M4 Max/Ultra).
* **OpenAI-Compatible FastAPI Server**: Membangun custom API wrapper yang kompatibel dengan SDK OpenAI standar.

---

## 📝 Referensi & Dokumentasi Tambahan
Baca catatan mendalam di folder [notes/](file:///Users/bsa/Documents/por/aiengineering/typeofmodels/notes):
* [01_pretrained_models.md](file:///Users/bsa/Documents/por/aiengineering/typeofmodels/notes/01_pretrained_models.md)
* [02_closed_vs_open_source.md](file:///Users/bsa/Documents/por/aiengineering/typeofmodels/notes/02_closed_vs_open_source.md)
* [03_self_hosted_models.md](file:///Users/bsa/Documents/por/aiengineering/typeofmodels/notes/03_self_hosted_models.md)
* [04_type_of_models_synthesis.md](file:///Users/bsa/Documents/por/aiengineering/typeofmodels/notes/04_type_of_models_synthesis.md)
