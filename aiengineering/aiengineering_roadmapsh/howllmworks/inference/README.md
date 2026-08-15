# INFERENCE

Bagian ini mencakup seluruh materi pembelajaran tentang **Inference** dalam AI Engineering — yaitu proses menjalankan model yang sudah dilatih (pre-trained) untuk menghasilkan prediksi/output dari data input baru.

> **Inference ≠ Training**
> Training = melatih bobot model dari data. Inference = menggunakan model yang sudah jadi untuk memproduksi output.

## Struktur Pembelajaran

```
inference/
├── 01_dasar_inference/                  # Konsep dasar inference
│   ├── 1_apa_itu_inference.py           # Definisi & perbedaan training vs inference
│   ├── 2_pipeline_inference.py          # Pipeline inference dengan Hugging Face
│   └── README.md
│
├── 02_model_selection/                  # Memilih model yang tepat
│   ├── 1_open_vs_closed_model.py        # Perbandingan model open-source vs closed API
│   ├── 2_huggingface_model_hub.py       # Menggunakan Hugging Face Model Hub
│   ├── 3_ollama_local_inference.py      # Menjalankan model secara lokal dengan Ollama
│   └── README.md
│
├── 03_prompt_engineering/               # Teknik prompt engineering
│   ├── 1_zero_shot_prompting.py         # Prompting tanpa contoh
│   ├── 2_few_shot_prompting.py          # Prompting dengan beberapa contoh
│   ├── 3_chain_of_thought.py            # Chain-of-Thought prompting
│   ├── 4_system_prompt_design.py        # Merancang system prompt yang efektif
│   └── README.md
│
├── 04_optimasi_inference/               # Teknik optimasi performa
│   ├── 1_quantization.py                # Mengurangi ukuran model (INT8/INT4)
│   ├── 2_batching_strategies.py         # Strategi batching untuk throughput tinggi
│   ├── 3_caching_kv_cache.py            # KV-Cache dan teknik caching
│   ├── 4_streaming_output.py            # Streaming response secara real-time
│   └── README.md
│
├── 05_inference_api_dan_serving/        # Menyajikan model sebagai API
│   ├── 1_openai_api.py                  # Menggunakan OpenAI API
│   ├── 2_huggingface_inference_api.py   # Hugging Face Inference Endpoints
│   ├── 3_fastapi_model_serving.py       # Membuat API sendiri dengan FastAPI
│   └── README.md
│
├── 06_evaluasi_dan_observability/       # Evaluasi output & monitoring
│   ├── 1_evaluasi_output_model.py       # Metrik evaluasi (BLEU, ROUGE, dsb.)
│   ├── 2_cost_latency_tracking.py       # Monitoring biaya & latensi
│   ├── 3_logging_tracing.py             # Logging dan tracing inference
│   └── README.md
│
├── 07_safety_dan_guardrails/            # Keamanan & pembatasan
│   ├── 1_content_moderation.py          # Moderasi konten output model
│   ├── 2_prompt_injection_defense.py    # Pertahanan terhadap prompt injection
│   ├── 3_output_validation.py           # Validasi & constraining output
│   └── README.md
│
├── main.py                              # Interactive CLI runner untuk semua modul
└── README.md                            # File ini
```

## Install & Cara Menjalankan

```bash
pyenv versions
pyenv local 3.9.18
python --version
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install numpy pandas transformers torch huggingface_hub openai fastapi uvicorn requests rouge-score nltk
python3 main.py
deactivate
```

## Urutan Belajar

| No | Topik | Deskripsi |
|----|-------|-----------|
| 01 | Dasar Inference | Memahami apa itu inference, pipeline, dan perbedaannya dengan training |
| 02 | Model Selection | Cara memilih model (open-source vs API), Hugging Face Hub, Ollama |
| 03 | Prompt Engineering | Zero-Shot, Few-Shot, Chain-of-Thought, dan system prompt design |
| 04 | Optimasi Inference | Quantization, batching, KV-cache, dan streaming output |
| 05 | Inference API & Serving | Menggunakan API (OpenAI, HF) dan membuat API sendiri (FastAPI) |
| 06 | Evaluasi & Observability | Metrik evaluasi output, monitoring biaya/latensi, logging |
| 07 | Safety & Guardrails | Content moderation, prompt injection defense, output validation |
