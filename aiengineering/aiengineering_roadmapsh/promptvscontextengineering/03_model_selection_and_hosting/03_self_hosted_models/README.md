# 03. Self-Hosted Models & Inference Engines

Modul ini mempelajari teknik *Self-Hosting* LLM secara mandiri menggunakan engine inferensi berperforma tinggi (*vLLM, Ollama, TensorRT-LLM*) dan kuantisasi bobot.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. High-Performance Inference Engines
- **vLLM**: Pipelining PagedAttention yang mengelola memori KV-Cache secara efisien tanpa fragmentasi.
- **Ollama**: Framework lokal ringkas berbasis llama.cpp untuk pengujian di komputer lokal / developer workstation.
- **TensorRT-LLM (NVIDIA)**: Optimasi kernel GPU NVIDIA tingkat terendah untuk throughput maksimal di lingkungan produksi enterprise.

### 2. Quantization Techniques
- **FP16 / BF16**: Akurasi penuh (16-bit precision), membutuhkan 2GB GPU RAM per 1 Milyar parameter.
- **INT8 / INT4 (AWQ, GPTQ, GGUF)**: Menekan penggunaan memori GPU hingga 70% dengan penurunan akurasi penalaran < 1%.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat kalkulator GPU VRAM Requirement untuk Self-Hosted LLM.
