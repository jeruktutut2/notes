"""
01_openai_vision_api.py
Modul Task & SDK: OpenAI Vision API (GPT-4o Multi-Image Analysis & Detail Modes)
"""

import json

def construct_openai_vision_payload(image_url: str, prompt: str, detail_mode: str = "high") -> dict:
    """Mengonstruksi payload REST API OpenAI Chat Completions dengan Vision (GPT-4o)."""
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                            "detail": detail_mode
                        }
                    }
                ]
            }
        ],
        "max_tokens": 500
    }
    return payload

def simulate_openai_vision_api_call(payload: dict) -> dict:
    """Simulasi eksekusi panggil API GPT-4o Vision dan pengembalian respons terstruktur."""
    print(f"📡 [OpenAI API Request] Sending request to https://api.openai.com/v1/chat/completions")
    print(f"⚙️ Model: {payload['model']} | Image Detail: {payload['messages'][0]['content'][1]['image_url']['detail']}")
    
    response = {
        "id": "chatcmpl-vision-9921",
        "object": "chat.completion",
        "model": "gpt-4o-2024-05-13",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": (
                        "Gambar ini menunjukkan diagram arsitektur sistem multimodal. "
                        "Di bagian atas terdapat komponen Usecases, dan di bagian bawah terdapat API Tasks."
                    )
                },
                "finish_reason": "stop"
            }
        ],
        "usage": {
            "prompt_tokens": 1105,
            "completion_tokens": 42,
            "total_tokens": 1147
        }
    }
    return response

def main():
    print("=" * 70)
    print("👁️ MODUL SDK 01: OPENAI VISION API (GPT-4o)")
    print("=" * 70)

    # 1. Single Image Request
    image_link = "https://roadmap.sh/assets/roadmaps/ai-engineer.png"
    prompt_text = "Jelaskan struktur utama dari arsitektur multimodal pada gambar ini!"
    
    payload = construct_openai_vision_payload(image_link, prompt_text, detail_mode="high")
    print("\n1. JSON Payload Request:")
    print(json.dumps(payload, indent=2))

    # 2. Execute Request Simulation
    print("\n2. Simulasi Panggilan API:")
    api_result = simulate_openai_vision_api_call(payload)
    print(f"\n💡 Hasil Respons GPT-4o Vision:\n   \"{api_result['choices'][0]['message']['content']}\"")
    print(f"📊 Token Usage: {api_result['usage']['total_tokens']} total tokens")

    print("\n✅ Modul OpenAI Vision API Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
