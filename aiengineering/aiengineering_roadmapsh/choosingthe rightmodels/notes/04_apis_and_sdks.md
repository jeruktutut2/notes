# 04 - APIs & SDKs

 Integrasi LLM dalam aplikasi modern berpusat pada konsumsi API dan SDK yang fleksibel, aman, serta terstruktur.

---

## 📡 Lanskap API & SDK Utama

### 1. OpenAI Response API & SDK
* **Format**: Standard JSON payload via POST request atau Python/JS SDK (`openai`).
* **Fitur Kunci**:
  * **Structured Outputs**: Menggunakan `response_format={"type": "json_schema", "json_schema": ...}` dengan jaminan 100% kepatuhan struktur JSON tanpa sintaks rusak.
  * **Tool Calling / Function Calling**: Meneruskan definisi fungsi JSON Schema sehingga model memilih fungsi yang akan dieksekusi oleh sistem backend.
  * **Streaming**: Server-Sent Events (SSE) untuk memberikan *typewriter effect* respons secara real-time.

### 2. Claude Messages API (Anthropic SDK)
* **Format**: Endpoints `/v1/messages` menggunakan Anthropic Python/JS SDK (`anthropic`).
* **Fitur Kunci**:
  * **System Prompt Separat**: Memisahkan instruksi karakter/aturan sistem dari daftar histori percakapan `messages`.
  * **Prompt Caching**: Menyimpan instruksi konteks panjang (misal 50.000 token dokumen) di cache server Anthropic selama 5 menit, memangkas latency hingga 85% dan cost hingga 90%.
  * **Content Blocks**: Respons mendukung blok teks murni, pemanggilan alat (*tool_use*), dan artefak secara visual terpisah.

### 3. Google Gemini API (Google GenAI SDK)
* **Format**: Google Generative AI SDK (`google-generativeai` / `google-genai`).
* **Fitur Kunci**:
  * **Multimodal Payloads**: Meneruskan objek Byte/Media (Gambar, Video MP4, Audio WAV, PDF) langsung ke dalam prompt bersama instruksi teks.
  * **System Instructions & Safety Settings**: Pengaturan tingkat keamanan (*Hate Speech*, *Harassment*, *Dangerous Content*) yang dapat disesuaikan per permintaan.

### 4. Hugging Face Inference SDK
* **Format**: `huggingface_hub` Python Client (`InferenceClient`).
* **Fitur Kunci**:
  * Mengakses Serverless Inference API milik Hugging Face secara gratis/berbayar untuk ribuan model terbuka tanpa menginstal PyTorch/GPU lokal.

### 5. OpenAI-Compatible APIs Standard
* **Format**: `/v1/chat/completions`, `/v1/embeddings`, `/v1/models`.
* **Deskripsi**: Standardisasi de-facto industri! Banyak provider & framework hosting lokal (Ollama, LM Studio, vLLM, OpenRouter, Together AI, Groq, Anyscale) mengimplementasikan skema API yang identik dengan OpenAI.
* **Keuntungan**: Aplikasi Anda cukup mengganti `base_url` dan `api_key` tanpa perlu mengubah kode integrasi bisnis utama!

---

## 💻 Contoh Perbandingan Format Klien Code

### OpenAI Standard API
```python
from openai import OpenAI
client = OpenAI(base_url="https://api.openai.com/v1", api_key="sk-...")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Halo!"}]
)
```

### OpenAI-Compatible (Ollama Lokal)
```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
response = client.chat.completions.create(
    model="llama3.1",
    messages=[{"role": "user", "content": "Halo dari Ollama!"}]
)
```

### Anthropic Claude Messages API
```python
import anthropic
client = anthropic.Anthropic(api_key="sk-ant-...")
response = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    system="Anda adalah asisten medis terpercaya.",
    messages=[{"role": "user", "content": "Apa itu hipertensi?"}]
)
```
