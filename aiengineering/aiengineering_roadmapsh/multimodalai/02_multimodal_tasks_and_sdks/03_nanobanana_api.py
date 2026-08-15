"""
03_nanobanana_api.py
Modul Task & SDK: NanoBanana API & Specialized Multimodal REST Integration Wrapper
"""

import json

class NanoBananaClient:
    """SDK Wrapper untuk NanoBanana API & Specialized Multimodal Endpoints."""
    def __init__(self, api_key: str = "nb-mock-key-12345", base_url: str = "https://api.nanobanana.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url

    def analyze_multimodal(self, text_prompt: str, media_url: str, media_type: str = "image") -> dict:
        """Mengirim request multimodal ke NanoBanana API endpoint."""
        print(f"🍌 [NanoBanana SDK] Connecting to {self.base_url}/multimodal/analyze...")
        print(f"   Media Type: {media_type} | Target: {media_url}")
        
        request_body = {
            "api_key": f"***{self.api_key[-4:]}",
            "task": "MULTIMODAL_REASONING",
            "prompt": text_prompt,
            "inputs": [
                {
                    "type": media_type,
                    "url": media_url
                }
            ]
        }
        
        # Simulated server response
        response = {
            "status": 200,
            "message": "SUCCESS",
            "inference_time_ms": 184,
            "data": {
                "prediction": "Analisis NanoBanana: Deteksi visual mengonfirmasi 3 komponen utama sistem AI.",
                "confidence_score": 0.967,
                "embedding_id": "emb_nanobanana_99182"
            }
        }
        return {"request": request_body, "response": response}

def main():
    print("=" * 70)
    print("🍌 MODUL SDK 03: NANOBANANA MULTIMODAL API SDK")
    print("=" * 70)

    # Initialize client
    client = NanoBananaClient(api_key="nanobanana_sec_881923")
    
    # Execute analysis
    res = client.analyze_multimodal(
        text_prompt="Deteksi anomali pada gambar sensor berikut",
        media_url="https://nanobanana.ai/samples/sensor_dashboard.png",
        media_type="image"
    )
    
    print("\n1. Client Request Structure:")
    print(json.dumps(res["request"], indent=2))
    
    print("\n2. Server Response Payload:")
    print(json.dumps(res["response"], indent=2, ensure_ascii=False))

    print("\n✅ Modul NanoBanana API Berhasil Dijalankan!")

if __name__ == "__main__":
    main()
