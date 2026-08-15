"""
=================================================================
2. HUGGING FACE INFERENCE API
=================================================================
Hugging Face menyediakan beberapa cara untuk inference:

1. Inference API (Serverless) → Gratis/murah, rate-limited
2. Inference Endpoints → Dedicated server, fully managed
3. Local inference → Download model, jalankan sendiri

Keunggulan:
✅ Akses ke 500K+ model
✅ Tidak perlu manage GPU/server
✅ API format sederhana
✅ Bisa pakai model open-source terbaik
=================================================================
"""

import requests
import json


def demo_inference_api_format():
    """Format request ke Hugging Face Inference API."""
    print("=" * 60)
    print("DEMO 1: Format Hugging Face Inference API")
    print("=" * 60)

    print("""
    📋 HUGGING FACE INFERENCE API:

    Base URL: https://api-inference.huggingface.co/models/{model_id}

    Headers:
    - Authorization: Bearer {HF_TOKEN}
    - Content-Type: application/json

    📝 Contoh Request — Text Classification:
    """)

    request_example = {
        "url": "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english",
        "headers": {
            "Authorization": "Bearer hf_xxxxxxxxxxxxx"
        },
        "body": {
            "inputs": "I love this movie!"
        }
    }

    print(f"   URL    : {request_example['url']}")
    print(f"   Headers: {json.dumps(request_example['headers'], indent=2)}")
    print(f"   Body   : {json.dumps(request_example['body'], indent=2)}")

    response_example = [
        [
            {"label": "POSITIVE", "score": 0.9998},
            {"label": "NEGATIVE", "score": 0.0002}
        ]
    ]
    print(f"\n   Response: {json.dumps(response_example, indent=2)}")


def demo_berbagai_task():
    """Contoh penggunaan berbagai task di Inference API."""
    print("\n" + "=" * 60)
    print("DEMO 2: Berbagai Task di Inference API")
    print("=" * 60)

    tasks = [
        {
            "nama": "Text Classification",
            "model": "distilbert-base-uncased-finetuned-sst-2-english",
            "input": {"inputs": "This product is amazing!"},
            "output": [[{"label": "POSITIVE", "score": 0.9998}]]
        },
        {
            "nama": "Text Generation",
            "model": "gpt2",
            "input": {"inputs": "The future of AI is", "parameters": {"max_new_tokens": 50}},
            "output": [{"generated_text": "The future of AI is..."}]
        },
        {
            "nama": "Summarization",
            "model": "facebook/bart-large-cnn",
            "input": {"inputs": "Long article text here...", "parameters": {"max_length": 100}},
            "output": [{"summary_text": "Summary of the article..."}]
        },
        {
            "nama": "Translation",
            "model": "Helsinki-NLP/opus-mt-en-id",
            "input": {"inputs": "Hello, how are you?"},
            "output": [{"translation_text": "Halo, apa kabar?"}]
        },
        {
            "nama": "Sentence Similarity",
            "model": "sentence-transformers/all-MiniLM-L6-v2",
            "input": {
                "inputs": {
                    "source_sentence": "Machine learning is great",
                    "sentences": ["AI is wonderful", "I like pizza"]
                }
            },
            "output": [0.89, 0.12]
        },
        {
            "nama": "Question Answering",
            "model": "deepset/roberta-base-squad2",
            "input": {
                "inputs": {
                    "question": "Who invented Python?",
                    "context": "Python was created by Guido van Rossum."
                }
            },
            "output": {"answer": "Guido van Rossum", "score": 0.98}
        },
    ]

    for task in tasks:
        print(f"\n   📌 {task['nama']}")
        print(f"      Model  : {task['model']}")
        print(f"      Input  : {json.dumps(task['input'], ensure_ascii=False)[:80]}...")
        print(f"      Output : {json.dumps(task['output'], ensure_ascii=False)[:80]}...")


def demo_kode_python():
    """Contoh kode Python untuk memanggil HF Inference API."""
    print("\n" + "=" * 60)
    print("DEMO 3: Kode Python untuk HF Inference API")
    print("=" * 60)

    print("""
    📝 CONTOH 1: Menggunakan requests library
    
    ```python
    import requests
    import os
    
    API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
    headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}
    
    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    output = query({"inputs": "I love machine learning!"})
    print(output)
    # [[{'label': 'POSITIVE', 'score': 0.9998}]]
    ```

    📝 CONTOH 2: Menggunakan huggingface_hub library
    
    ```python
    from huggingface_hub import InferenceClient
    
    client = InferenceClient(token=os.getenv("HF_TOKEN"))
    
    # Text Classification
    result = client.text_classification("I love this!")
    print(result)
    
    # Text Generation
    result = client.text_generation(
        "The key to success is",
        model="mistralai/Mistral-7B-Instruct-v0.3",
        max_new_tokens=100
    )
    print(result)
    
    # Chat Completion (OpenAI-compatible format!)
    result = client.chat_completion(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {"role": "user", "content": "Apa itu inference?"}
        ],
        max_tokens=200
    )
    print(result.choices[0].message.content)
    ```

    📝 CONTOH 3: Inference Endpoints (Dedicated)
    
    ```python
    from huggingface_hub import InferenceClient
    
    # Endpoint yang sudah di-deploy
    client = InferenceClient(
        model="https://xyz123.us-east-1.aws.endpoints.huggingface.cloud"
    )
    
    result = client.text_generation("Hello, world!")
    ```
    """)


def demo_inference_endpoints():
    """Penjelasan Hugging Face Inference Endpoints."""
    print("=" * 60)
    print("DEMO 4: HF Inference Endpoints vs Serverless")
    print("=" * 60)

    print("""
    ┌───────────────────┬─────────────────────┬──────────────────────┐
    │ Fitur             │ Serverless API      │ Inference Endpoints  │
    ├───────────────────┼─────────────────────┼──────────────────────┤
    │ Setup             │ Langsung pakai      │ Deploy via UI/API    │
    │ Biaya             │ Gratis (rate-limit) │ ~$0.06-$4.50/jam     │
    │ Hardware          │ Shared              │ Dedicated GPU        │
    │ Latensi           │ Bervariasi          │ Konsisten            │
    │ Autoscaling       │ ❌                  │ ✅                   │
    │ Custom Model      │ ❌                  │ ✅                   │
    │ SLA               │ ❌                  │ ✅ (paid plan)       │
    │ Cocok untuk       │ Prototyping/testing │ Production           │
    └───────────────────┴─────────────────────┴──────────────────────┘

    🚀 Deploy Inference Endpoint:
    1. Buka https://ui.endpoints.huggingface.co
    2. Pilih model dari Hub
    3. Pilih cloud provider & GPU
    4. Deploy → Dapatkan URL endpoint
    5. Panggil endpoint via HTTP/SDK
    """)


def main():
    demo_inference_api_format()
    demo_berbagai_task()
    demo_kode_python()
    demo_inference_endpoints()

    print("\n✅ Selesai! Lanjut ke: 3_fastapi_model_serving.py")

if __name__ == "__main__":
    main()
