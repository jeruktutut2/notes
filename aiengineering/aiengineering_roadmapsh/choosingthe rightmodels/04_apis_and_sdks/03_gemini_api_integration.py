#!/usr/bin/env python3
"""
03_gemini_api_integration.py
Modul eksplorasi Google Gemini API Integration:
- Google GenAI SDK Standard
- Safety Settings configuration (`BLOCK_NONE`, `BLOCK_MEDIUM_AND_ABOVE`)
- Generation Config (Temperature, TopP, TopK, MaxOutputTokens)
"""

import json
from typing import Dict, Any

def build_gemini_api_payload() -> Dict[str, Any]:
    """Membangun payload konfigurasional Google Gemini API."""
    return {
        "contents": [
            {
                "parts": [
                    {"text": "Analisis dampak perubahan iklim terhadap ketahanan pangan nasional."}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95,
            "topK": 40,
            "maxOutputTokens": 2048,
            "responseMimeType": "application/json"
        },
        "safetySettings": [
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_LOW_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]
    }

def main():
    print("=" * 65)
    print(" ♊ GOOGLE GEMNI API & SAFETY SETTINGS CONFIGURATION")
    print("=" * 65)
    
    payload = build_gemini_api_payload()
    print("\n📋 Google Gemini API Config Payload Structure:")
    print(json.dumps(payload, indent=2))
    
    print("\n✅ Perbedaan Utama Gemini SDK vs OpenAI SDK:")
    print(" 1. Menggunakan struktur `contents` -> `parts` (bukan `messages` -> `content`).")
    print(" 2. Pengaturan `safetySettings` yang sangat terperinci untuk 4 kategori bahaya utama.")
    print(" 3. Dukungan native `responseMimeType: application/json` langsung di generationConfig.")

if __name__ == "__main__":
    main()
