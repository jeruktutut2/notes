# Implementasi Point 5: Inference API dan Model Serving

Cara menyajikan model AI sebagai layanan API yang bisa diakses oleh aplikasi — mulai dari menggunakan API provider hingga membangun API sendiri.

## Daftar File

1. `1_openai_api.py`: Cara menggunakan OpenAI API (GPT-4, embeddings) — format request, response, dan best practices.
2. `2_huggingface_inference_api.py`: Menggunakan Hugging Face Inference API/Endpoints untuk serving model tanpa manage infrastruktur.
3. `3_fastapi_model_serving.py`: Membuat REST API sendiri untuk serving model ML menggunakan FastAPI.

## Konsep Kunci

- **API Provider**: Menggunakan layanan pihak ketiga (OpenAI, Anthropic, HF) — mudah tapi berbayar
- **Self-Hosted**: Meng-host model sendiri — kontrol penuh tapi perlu manage infrastruktur
- **Model Serving Framework**: Tools khusus untuk serving model (vLLM, TGI, Triton, TorchServe)
