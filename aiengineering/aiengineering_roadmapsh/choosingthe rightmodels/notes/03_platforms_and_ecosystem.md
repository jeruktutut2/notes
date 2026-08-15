# 03 - Platforms & Ecosystem

 Ekosistem modern AI Engineering tidak hanya berpusat pada model itu sendiri, melainkan pada **platform penyedia, hub repositori model, runtime lokal, dan gateway API** yang menghubungkan model dengan aplikasi akhir.

---

## 🛠️ Komponen Platform & Ekosistem Utama

### 1. Hugging Face Ecosystem
Hugging Face adalah pusat gravitasi (*GitHub of AI*) untuk komunitas open-source AI.

* **Hugging Face Hub**:
  * Tempat menyimpan & mengunduh jutaan model weights, datasets, dan demo (Spaces).
  * Menyediakan kalkulator kebutuhan GPU/VRAM dan metadata lisensi komprehensif.
* **Hugging Face Tasks**:
  * Taksonomi standar industri untuk mengkategorikan tugas AI: `text-generation`, `summarization`, `translation`, `text-to-image`, `feature-extraction` (embeddings), `zero-shot-classification`, dll.
* **Transformers.js**:
  * Library JS/TS untuk menjalankan model ML secara langsung di browser Web atau Node.js menggunakan ONNX Runtime dan WebGPU tanpa server backend.

---

### 2. Local & Managed Hosting Platforms

#### A. Ollama
* **Deskripsi**: Runtime lokal paling populer untuk menjalankan model open-source (Llama 3, DeepSeek R1, Qwen 2.5, Gemma 2) di macOS, Linux, dan Windows.
* **Fitur Utama**:
  * Mengemas bobot model ke dalam file tunggal yang efisien (Modelfile / GGUF).
  * Menyediakan REST API lokal yang kompatibel dengan format OpenAI (`/v1/chat/completions`).
  * Manajemen VRAM GPU & RAM otomatis (KV cache offloading, quantization FP16/Q4_K_M).

#### B. LM Studio
* **Deskripsi**: Aplikasi GUI desktop intuitif untuk menjelajahi, mengunduh, dan menjalankan model GGUF secara lokal di laptop atau komputer server.
* **Fitur Utama**:
  * Chat UI bawaan dengan kontrol hiperparameter lengkap (Temperature, Top_P, Context Size, GPU Offload layers).
  * Local Inference Server 1-click yang kompatibel dengan SDK OpenAI.

#### C. OpenRouter
* **Deskripsi**: Aggregator & Unified Gateway API yang memberikan akses ke ratusan model (Closed & Open Source) melalui satu kredensial API key tunggal.
* **Fitur Utama**:
  * **Unified Endpoint**: Memanggil Claude 3.5 Sonnet, GPT-4o, Llama 3.1 405B, atau DeepSeek R1 dengan format API yang sama.
  * **Automatic Fallback & Load Balancing**: Pengalihan otomatis jika provider utama mengalami outage atau rate-limit.
  * **Cost Transparency**: Pembayaran pay-per-token seragam tanpa komitmen langganan bulanan di banyak vendor terpisah.

---

## 🔄 Diagram Ekosistem Workflow

```text
[ Developer Application ]
           │
           ├─── OpenRouter API Gateway ───► Access 100+ Models (Closed + Open)
           │
           ├─── Hugging Face Hub ────────► Download Weights / Fine-tune Datasets
           │
           ├─── Ollama / LM Studio ──────► Run Locally (Offline / Edge / Privacy)
           │
           └─── Transformers.js ────────► Direct In-Browser AI Inference
```

---

## 🎯 Ringkasan Ekosistem
* Gunakan **Hugging Face Hub** saat mencari model spesifik, mengecek arsitektur, atau mengambil dataset.
* Gunakan **Ollama** untuk proyek lokal, scripting dev, atau aplikasi desktop privacy-first.
* Gunakan **OpenRouter** saat ingin melakukan pengujian komparatif (*A/B testing*) antar model closed vs open weights tanpa setup akun di 10 provider berbeda.
* Gunakan **Transformers.js** jika aplikasi web Anda membutuhkan inferensi gratis langsung di perangkat user tanpa server biaya tinggi.
