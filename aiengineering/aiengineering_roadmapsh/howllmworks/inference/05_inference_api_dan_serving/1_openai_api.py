"""
=================================================================
1. OPENAI API
=================================================================
OpenAI API adalah salah satu API AI paling populer dan menjadi
"standar de facto" yang banyak diikuti provider lain.

Endpoint utama:
- /v1/chat/completions  → Chat (GPT-4, GPT-3.5)
- /v1/embeddings        → Text embedding
- /v1/images/generations → Image generation (DALL-E)
- /v1/audio/transcriptions → Speech to text (Whisper)
- /v1/moderations       → Content moderation

CATATAN: Untuk menjalankan demo yang memanggil API,
         Anda perlu OPENAI_API_KEY yang valid.
         Jika tidak ada, skrip ini menunjukkan pola/format saja.
=================================================================
"""

import os
import json


def demo_format_request():
    """Menjelaskan format request OpenAI API."""
    print("=" * 60)
    print("DEMO 1: Format Request OpenAI Chat API")
    print("=" * 60)

    request_body = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "system",
                "content": "Kamu adalah asisten coding yang membantu."
            },
            {
                "role": "user",
                "content": "Jelaskan perbedaan list dan tuple di Python."
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "top_p": 1.0,
        "frequency_penalty": 0.0,
        "presence_penalty": 0.0,
    }

    print(f"\n📝 Request Body:")
    print(json.dumps(request_body, indent=2, ensure_ascii=False))

    print("""
    📋 Penjelasan Parameter:
    
    ┌─────────────────────┬──────────────────────────────────────┐
    │ Parameter           │ Fungsi                               │
    ├─────────────────────┼──────────────────────────────────────┤
    │ model               │ Model yang digunakan (gpt-4o, dll)   │
    │ messages            │ Array pesan (system, user, assistant) │
    │ temperature         │ Kreativitas (0=fokus, 2=kreatif)     │
    │ max_tokens          │ Batas token output                   │
    │ top_p               │ Nucleus sampling (alternatif temp)   │
    │ frequency_penalty   │ Penalti pengulangan kata (0-2)       │
    │ presence_penalty    │ Penalti topik yang sudah dibahas     │
    │ stream              │ true = streaming response            │
    │ response_format     │ Format output (text/json_object)     │
    └─────────────────────┴──────────────────────────────────────┘
    """)


def demo_format_response():
    """Menjelaskan format response OpenAI API."""
    print("=" * 60)
    print("DEMO 2: Format Response OpenAI API")
    print("=" * 60)

    # Contoh response dari API
    response_example = {
        "id": "chatcmpl-abc123",
        "object": "chat.completion",
        "created": 1719456789,
        "model": "gpt-4o-2024-05-13",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "List dan tuple di Python memiliki beberapa perbedaan utama:\n\n1. **Mutability**: List bersifat mutable (bisa diubah), tuple bersifat immutable (tidak bisa diubah setelah dibuat).\n2. **Syntax**: List menggunakan [], tuple menggunakan ().\n3. **Performa**: Tuple lebih cepat karena immutable."
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 35,
            "completion_tokens": 82,
            "total_tokens": 117
        }
    }

    print(f"\n📨 Response Body:")
    print(json.dumps(response_example, indent=2, ensure_ascii=False))

    print("""
    📋 Bagian Penting Response:
    
    1. choices[0].message.content → Jawaban model
    2. choices[0].finish_reason   → Alasan berhenti:
       - "stop"        = selesai normal
       - "length"      = max_tokens tercapai
       - "content_filter" = diblokir content filter
    3. usage → Info pemakaian token:
       - prompt_tokens     = token input (kita bayar ini)
       - completion_tokens = token output (kita bayar ini juga)
       - total_tokens      = total
    """)


def demo_kode_penggunaan():
    """Contoh kode untuk menggunakan OpenAI API."""
    print("=" * 60)
    print("DEMO 3: Contoh Kode Penggunaan OpenAI API")
    print("=" * 60)

    print("""
    📝 CONTOH 1: Chat Completion Dasar
    
    ```python
    from openai import OpenAI
    
    client = OpenAI()  # Otomatis baca OPENAI_API_KEY dari env
    
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Kamu asisten yang membantu."},
            {"role": "user", "content": "Apa itu machine learning?"}
        ]
    )
    
    print(response.choices[0].message.content)
    print(f"Token terpakai: {response.usage.total_tokens}")
    ```

    📝 CONTOH 2: Streaming Response
    
    ```python
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Ceritakan tentang AI"}],
        stream=True  # <-- Aktifkan streaming
    )
    
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
    ```

    📝 CONTOH 3: JSON Mode (Structured Output)
    
    ```python
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Balas dalam format JSON."},
            {"role": "user", "content": "Analisis sentimen: 'Produk ini bagus!'"}
        ],
        response_format={"type": "json_object"}
    )
    
    import json
    data = json.loads(response.choices[0].message.content)
    # data = {"sentiment": "positive", "confidence": 0.95}
    ```

    📝 CONTOH 4: Text Embedding
    
    ```python
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input="Machine learning is fascinating"
    )
    
    embedding = response.data[0].embedding  # Vector 1536-dimensi
    print(f"Dimensi: {len(embedding)}")
    ```
    """)


def demo_best_practices():
    """Best practices menggunakan OpenAI API."""
    print("=" * 60)
    print("DEMO 4: Best Practices OpenAI API")
    print("=" * 60)

    print("""
    ✅ BEST PRACTICES:

    1. 🔑 API KEY MANAGEMENT
       - Jangan hardcode API key di kode
       - Gunakan environment variable: OPENAI_API_KEY
       - Gunakan .env file + python-dotenv untuk development
       - Gunakan secret manager untuk production (AWS SSM, GCP SM)

    2. 💰 COST MANAGEMENT
       - Set max_tokens untuk membatasi output
       - Gunakan model yang tepat (gpt-4o-mini lebih murah)
       - Cache response untuk query yang sama
       - Monitor usage di dashboard OpenAI

    3. 🔄 ERROR HANDLING & RETRY
       - Implement retry dengan exponential backoff
       - Handle rate limit errors (429)
       - Handle timeout errors
       - Set timeout yang reasonable

       ```python
       from openai import OpenAI
       import tenacity
       
       @tenacity.retry(
           wait=tenacity.wait_exponential(min=1, max=60),
           stop=tenacity.stop_after_attempt(3),
           retry=tenacity.retry_if_exception_type(Exception)
       )
       def call_api(prompt):
           return client.chat.completions.create(
               model="gpt-4o",
               messages=[{"role": "user", "content": prompt}],
               timeout=30
           )
       ```

    4. 📊 MONITORING
       - Log setiap request: model, tokens, latency, cost
       - Track error rate dan response quality
       - Set alerts untuk usage anomali
    """)


def main():
    demo_format_request()
    print()
    demo_format_response()
    print()
    demo_kode_penggunaan()
    print()
    demo_best_practices()

    print("\n✅ Selesai! Lanjut ke: 2_huggingface_inference_api.py")

if __name__ == "__main__":
    main()
