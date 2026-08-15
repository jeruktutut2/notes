"""
02_dalle_api.py
Modul Task & SDK: DALL-E API (Image Synthesis & Prompt Revision Inspector)
"""

import json

def construct_dalle3_request(prompt: str, size: str = "1024x1024", quality: str = "hd", style: str = "vivid") -> dict:
    """Mengonstruksi payload DALL-E 3 API Request."""
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": size,
        "quality": quality,
        "style": style,
        "response_format": "url"
    }
    return payload

def simulate_dalle3_api_call(payload: dict) -> dict:
    """Simulasi panggilan DALL-E 3 API dan menginspeksi hasil 'revised_prompt' otomatis dari OpenAI."""
    print(f"🎨 [DALL-E 3 Request] Target Size: {payload['size']} | Quality: {payload['quality']} | Style: {payload['style']}")
    print(f"📝 Original Prompt: '{payload['prompt']}'")
    
    revised_prompt = (
        f"A cinematic high-resolution digital painting of {payload['prompt']}. "
        "Intricate details, dramatic lighting, 8k resolution, photorealistic volumetric light rays."
    )
    
    response = {
        "created": 1721990000,
        "data": [
            {
                "revised_prompt": revised_prompt,
                "url": "https://oaidalleapiprodscus.blob.core.windows.net/private/generated_image_dalle3_demo.png"
            }
        ]
    }
    return response

def main():
    print("=" * 70)
    print("🎨 MODUL SDK 02: DALL-E 3 IMAGE GENERATION API")
    print("=" * 70)

    # Construct Payload
    user_prompt = "Kucing astronot membaca buku di stasiun luar angkasa dengan latar belakang planet Bumi."
    request_payload = construct_dalle3_request(user_prompt, size="1024x1024", quality="hd", style="vivid")
    
    print("\n1. DALL-E 3 Request Payload:")
    print(json.dumps(request_payload, indent=2, ensure_ascii=False))

    # Simulate Call
    print("\n2. Executing Generation Request...")
    result = simulate_dalle3_api_call(request_payload)
    
    print("\n💡 Results & Revised Prompt Inspector:")
    print(f"   • Revised Prompt (Optimized by OpenAI GPT-4):")
    print(f"     \"{result['data'][0]['revised_prompt']}\"")
    print(f"   • Generated Image URL: {result['data'][0]['url']}")

    print("\n✅ Modul DALL-E API Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
