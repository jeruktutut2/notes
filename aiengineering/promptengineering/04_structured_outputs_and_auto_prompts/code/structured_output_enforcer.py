#!/usr/bin/env python3
"""
Modul 04: Structured Output Enforcer
Validasi dan ekstraksi respons JSON berstruktur dari LLM dengan schema Pydantic.
"""

import json
from typing import List
from pydantic import BaseModel, Field

class SentimentItem(BaseModel):
    aspect: str = Field(description="Fitur atau aspek produk")
    sentiment: str = Field(description="Positif, Netral, atau Negatif")
    confidence: float = Field(description="Skor keyakinan 0.0 - 1.0")

class ReviewAnalysisSchema(BaseModel):
    product_name: str = Field(description="Nama produk")
    overall_score: int = Field(description="Skor keseluruhan 1 - 5")
    aspects: List[SentimentItem]

def generate_json_schema_prompt(raw_text: str) -> str:
    schema_str = json.dumps(ReviewAnalysisSchema.model_json_schema(), indent=2)
    
    prompt = f"""
[SYSTEM INSTRUCTION]
Ekstrak ulasan produk berikut dan kembalikan HANYA berupa objek JSON valid yang mematuhi JSON Schema berikut:

{schema_str}

[INPUT TEXT]
"{raw_text}"

[OUTPUT]
```json
"""
    return prompt

def main():
    print("📋 STRUCTURED OUTPUT SCHEMA ENFORCER DEMO")
    print("=" * 60)
    
    sample_review = "Laptop Asus Zenbook ini layarnya luar biasa jernih (skor 5/5), tapi bodinya mudah meninggalkan sidik jari dan harganya agak mahal."
    
    prompt = generate_json_schema_prompt(sample_review)
    print("--- [GENERATED SCHEMA PROMPT] ---")
    print(prompt)
    print("=" * 60)

if __name__ == "__main__":
    main()
