# Catatan Pembelajaran: Self-Hosted Models

## 1. Mengapa Menjalankan Model Secara Self-Hosted?

Self-Hosting adalah praktik menginstal, mengoptimasi, dan menyajikan model LLM di infrastruktur milik sendiri (Lokal PC, Server Bare-Metal, atau Private Cloud GPU).

### Keuntungan Utama:
1. **Keamanan & Data Sovereignty**: Data sensitif tidak pernah meninggalkan network internal perusahaan.
2. **Kustomisasi Lengkap**: Bebas mengatur quantisation, context window size, sampling temperature, hingga custom CUDA kernels.
3. **Throughput Tinggi & Latensi Rendah**: Menghilangkan latency jaringan internet ke API publik vendor.
4. **Efisiensi Biaya pada Volume Tinggi**: Untuk juta token per detik, biaya sewa server GPU jauh lebih rendah daripada pay-per-token API.

---

## 2. Tools & Framework Self-Hosting

Ekosistem Self-Hosting dibagi menjadi 2 kategori utama:

```text
+-------------------------------------------------------------------------+
|                       SELF-HOSTING ENGINE ECOSYSTEM                     |
+-------------------------------------------------------------------------+
|                                   |                                     |
|    Local & Edge Execution         |     Production Inference Servers    |
|    (Ollama, llama.cpp, LM Studio) |     (vLLM, TGI, Triton)             |
|                                   |                                     |
|  • Single User / Desktop          |  • High Concurrency & Multi-Tenant   |
|  • Easy Setup & Zero Config       |  • PagedAttention & Continuous Batch|
|  • CPU + GGUF / Apple Silicon     |  • Scale out to Multiple GPUs       |
+-------------------------------------------------------------------------+
```

### A. Local & Desktop Runners:
1. **Ollama**: Tool paling populer untuk mengeksekusi LLM secara lokal via terminal & REST API (`ollama run llama3.1`).
2. **llama.cpp**: Engine C/C++ ultra-efisien tanpa dependensi berat yang mendasari Ollama dan LM Studio.
3. **LM Studio**: GUI desktop ramah pengguna untuk mencari, mengunduh, dan mencoba model GGUF dari Hugging Face.

### B. Production Serving Frameworks:
1. **vLLM**: Engine inferensi LLM produksi paling populer. Menggunakan algoritma **PagedAttention** untuk mengelola memory KV Cache dengan efisiency hingga 96%, meningkatkan throughput 2x-4x lipat dibanding Hugging Face Transformers murni.
2. **TGI (Text Generation Inference)**: Framework produksi dari Hugging Face dengan dukungan Tensor Parallelism, Continuous Batching, dan Token Streaming.

---

## 3. Fitur Kunci Engine Produksi (vLLM & TGI)

1. **PagedAttention**: Mengatasi fragmentasi memori KV Cache dengan membaginya ke dalam block-block virtual (mirip Paging pada OS Memory Management).
2. **Continuous Batching (Iteration-level Batching)**: Tidak menunggu seluruh sequence dalam satu batch selesai. Request baru yang tiba dapat langsung disisipkan ke dalam slot batch yang sudah selesai generate token.
3. **Tensor Parallelism**: Membagi layer model ke beberapa GPU (misal 8x A100) secara horisontal agar model raksasa (70B/405B) dapat dimuat ke VRAM.

---

## 4. Arsitektur Production Deployment (OpenAI-Compatible FastAPI Server)

Dalam arsitektur enterprise, model self-hosted disajikan dalam bentuk REST API yang **OpenAI Compatible** (`/v1/chat/completions`) sehingga dapat langsung menggantikan API OpenAI tanpa mengubah kode aplikasi front-end/backend.

```text
 Client Apps / Front-End
         │
         ▼
 ┌───────────────┐
 │ API Gateway   │  (Authentication, Rate Limiting, Logging)
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ Load Balancer │  (Nginx / Traefik)
 └───────┬───────┘
         ├────────────────────────┐
         ▼                        ▼
 ┌───────────────┐        ┌───────────────┐
 │ vLLM Worker 1 │        │ vLLM Worker 2 │
 │ (GPU Server 1)│        │ (GPU Server 2)│
 └───────────────┘        └───────────────┘
```
