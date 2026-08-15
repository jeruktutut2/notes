"""
MODUL 4.1: JSON & Schema Enforcement Techniques
===============================================
Penjelasan:
Mengunci format output LLM ke skema JSON yang valid sangat penting saat membangun integrasi API/aplikasi.
Teknik ini menggabungkan:
1. System Instruction eksplisit & contoh JSON Schema.
2. Validasi Parser (Regex / json.loads).
3. Retry/Repair Mechanism jika JSON pertama cacat sintaks.
"""

import json
import re

def build_schema_prompt(user_text: str) -> str:
    schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "nama_perusahaan": {"type": "string"},
            "tahun_didirikan": {"type": "integer"},
            "sektor_industri": {"type": "string"},
            "layanan_utama": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["nama_perusahaan", "sektor_industri", "layanan_utama"]
    }
    
    return f"""Tugas: Ekstrak informasi dari teks berikut ke dalam format JSON murni tanpa markdown triple backticks atau teks pengantar lainnya.

Skema JSON yang Wajib Dipatuhi:
{json.dumps(schema, indent=2)}

Teks Input:
"{user_text}"

JSON Output:"""


def simulate_llm_json_generation(attempt: int) -> str:
    if attempt == 1:
        # Cacat sintaks (ada trailing comma dan markdown block)
        return """```json
{
  "nama_perusahaan": "PT Solusi Digital",
  "tahun_didirikan": 2018,
  "sektor_industri": "Teknologi Informasi",
  "layanan_utama": ["Cloud Computing", "AI Development",],
}
```"""
    else:
        # JSON Valid setelah dimurnikan
        return """{
  "nama_perusahaan": "PT Solusi Digital",
  "tahun_didirikan": 2018,
  "sektor_industri": "Teknologi Informasi",
  "layanan_utama": ["Cloud Computing", "AI Development"]
}"""


def clean_and_parse_json(raw_response: str) -> dict:
    """Membersihkan markdown backticks dan memvalidasi JSON."""
    cleaned = re.sub(r'```(?:json)?\s*([\s\S]*?)\s*```', r'\1', raw_response).strip()
    # Bersihkan trailing commas jika ada
    cleaned = re.sub(r',\s*([\]}])', r'\1', cleaned)
    return json.loads(cleaned)


def main():
    print("==========================================================")
    print(" DEMO 4.1: Structural Schema Enforcement & Repair Loop")
    print("==========================================================\n")

    input_text = "PT Solusi Digital adalah perusahaan IT yang berdiri sejak 2018. Kami menyediakan layanan Cloud Computing dan AI Development."
    prompt = build_schema_prompt(input_text)

    print("[1] PROMPT SKEMA EKSPLISIT:")
    print(prompt)
    print("\n" + "="*60 + "\n")

    # Simulasi percobaan 1
    print("[2] ATTEMPT 1: Mengubah Output LLM Cacat ke Valid Struct...")
    raw_1 = simulate_llm_json_generation(attempt=1)
    print("Raw Response 1:")
    print(raw_1)
    
    try:
        data = clean_and_parse_json(raw_1)
        print("\nHasil Parsing JSON Sukses:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"\nParsing Gagal: {e}. Menjalankan Retry Repair Loop...")
        raw_2 = simulate_llm_json_generation(attempt=2)
        data = clean_and_parse_json(raw_2)
        print("\nHasil Repaired JSON:")
        print(json.dumps(data, indent=2, ensure_ascii=False))

    print("==========================================================")

if __name__ == "__main__":
    main()
