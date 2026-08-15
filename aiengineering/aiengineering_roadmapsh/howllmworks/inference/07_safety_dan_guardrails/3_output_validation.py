"""
=================================================================
3. OUTPUT VALIDATION
=================================================================
Output validation = memastikan output model sesuai dengan
format, aturan, dan batasan yang diharapkan SEBELUM dikirim
ke user atau sistem downstream.

Mengapa penting:
- LLM bisa menghasilkan output yang tidak sesuai format (JSON rusak)
- Model bisa hallucinate (mengada-ada informasi)
- Output bisa mengandung konten yang tidak diinginkan
- Downstream systems butuh format yang strict

Strategi:
1. Schema Validation → Cek format output (JSON schema)
2. Content Guardrails → Cek isi output (topik, tone)
3. Factual Validation → Cek kebenaran informasi
4. Retry on Failure → Coba ulang jika output tidak valid
=================================================================
"""

import json
import re
from dataclasses import dataclass


# ─────────────────────────────────────────────────────
# 1. JSON SCHEMA VALIDATION
# ─────────────────────────────────────────────────────

def validate_json_output(output: str, required_fields: list = None) -> dict:
    """
    Validasi apakah output model adalah JSON yang valid
    dan mengandung field yang dibutuhkan.
    """
    result = {"valid": False, "data": None, "errors": []}

    # Step 1: Coba parse JSON
    # LLM kadang menambahkan text sebelum/sesudah JSON
    json_match = re.search(r'\{.*\}', output, re.DOTALL)
    if not json_match:
        result["errors"].append("Tidak ditemukan JSON object dalam output")
        return result

    try:
        data = json.loads(json_match.group())
        result["data"] = data
    except json.JSONDecodeError as e:
        result["errors"].append(f"JSON parse error: {str(e)}")
        return result

    # Step 2: Cek required fields
    if required_fields:
        missing = [f for f in required_fields if f not in data]
        if missing:
            result["errors"].append(f"Field yang hilang: {missing}")
            return result

    result["valid"] = True
    return result


def demo_json_validation():
    """Demo validasi JSON output."""
    print("=" * 60)
    print("DEMO 1: JSON Output Validation")
    print("=" * 60)

    required_fields = ["sentiment", "confidence", "summary"]

    test_outputs = [
        ("Valid", '{"sentiment": "positive", "confidence": 0.95, "summary": "Great product"}'),
        ("Dengan teks tambahan", 'Here is the analysis:\n{"sentiment": "negative", "confidence": 0.87, "summary": "Poor quality"}\nDone.'),
        ("JSON rusak", '{"sentiment": "positive", "confidence": 0.95, "summary": }'),
        ("Field hilang", '{"sentiment": "neutral"}'),
        ("Bukan JSON", "The sentiment is positive with 95% confidence."),
    ]

    print(f"\n📋 Required fields: {required_fields}")
    print(f"\n📊 Hasil Validasi:")

    for label, output in test_outputs:
        result = validate_json_output(output, required_fields)
        status = "✅ Valid" if result["valid"] else "❌ Invalid"
        print(f"\n   [{label}]")
        print(f"   Output : {output[:60]}...")
        print(f"   Status : {status}")
        if result["errors"]:
            print(f"   Errors : {result['errors']}")
        if result["data"]:
            print(f"   Data   : {result['data']}")


# ─────────────────────────────────────────────────────
# 2. CONTENT GUARDRAILS
# ─────────────────────────────────────────────────────

class OutputGuardrails:
    """Guardrails untuk memvalidasi konten output model."""

    def __init__(self):
        self.rules = []

    def add_rule(self, name: str, check_fn, error_msg: str):
        """Tambahkan aturan validasi."""
        self.rules.append({"name": name, "check": check_fn, "error": error_msg})

    def validate(self, output: str) -> dict:
        """Jalankan semua aturan validasi."""
        results = {"passed": True, "violations": []}

        for rule in self.rules:
            if not rule["check"](output):
                results["passed"] = False
                results["violations"].append({
                    "rule": rule["name"],
                    "error": rule["error"]
                })

        return results


def demo_content_guardrails():
    """Demo content guardrails."""
    print("\n" + "=" * 60)
    print("DEMO 2: Content Guardrails")
    print("=" * 60)

    # Setup guardrails
    guards = OutputGuardrails()

    # Rule 1: Output tidak boleh terlalu pendek
    guards.add_rule(
        "minimum_length",
        lambda text: len(text) >= 20,
        "Output terlalu pendek (min 20 karakter)"
    )

    # Rule 2: Output tidak boleh terlalu panjang
    guards.add_rule(
        "maximum_length",
        lambda text: len(text) <= 5000,
        "Output terlalu panjang (max 5000 karakter)"
    )

    # Rule 3: Tidak boleh mengandung disclaimer tertentu
    guards.add_rule(
        "no_ai_disclaimer",
        lambda text: "as an ai" not in text.lower() and "as a language model" not in text.lower(),
        "Output mengandung AI disclaimer (tidak natural)"
    )

    # Rule 4: Tidak boleh mengandung URL eksternal
    guards.add_rule(
        "no_external_urls",
        lambda text: not re.search(r'https?://(?!api\.yourcompany\.com)', text),
        "Output mengandung URL eksternal"
    )

    # Rule 5: Harus dalam bahasa yang diminta
    guards.add_rule(
        "language_check",
        lambda text: not bool(re.search(r'[\u4e00-\u9fff]', text)),  # No Chinese chars
        "Output mengandung karakter non-Latin yang tidak diharapkan"
    )

    test_outputs = [
        ("Bagus", "Produk ini memiliki kualitas premium dengan bahan katun organik yang lembut dan nyaman dipakai."),
        ("Terlalu pendek", "OK."),
        ("AI Disclaimer", "As an AI language model, I think this product is good. The quality is nice."),
        ("URL Eksternal", "Untuk info lebih lanjut, kunjungi https://malicious-site.com/steal-data"),
    ]

    print(f"\n📋 Aturan aktif: {len(guards.rules)}")
    print(f"\n📊 Hasil Validasi:")

    for label, output in test_outputs:
        result = guards.validate(output)
        status = "✅ PASS" if result["passed"] else "❌ FAIL"
        print(f"\n   [{label}] {status}")
        print(f"   Output: {output[:60]}...")
        if result["violations"]:
            for v in result["violations"]:
                print(f"   ⚠️ Rule '{v['rule']}': {v['error']}")


# ─────────────────────────────────────────────────────
# 3. RETRY ON FAILURE
# ─────────────────────────────────────────────────────

def demo_retry_pattern():
    """Pola retry ketika output tidak valid."""
    print("\n" + "=" * 60)
    print("DEMO 3: Retry Pattern untuk Output Invalid")
    print("=" * 60)

    print("""
    📋 POLA RETRY SAAT OUTPUT TIDAK VALID:

    ```python
    import json
    from openai import OpenAI
    
    client = OpenAI()

    def get_structured_output(prompt, max_retries=3):
        \"\"\"Dapatkan output JSON yang valid, dengan retry.\"\"\"
        
        for attempt in range(max_retries):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": \"\"\"
                            Selalu jawab dalam format JSON valid.
                            Schema: {"sentiment": str, "confidence": float, "summary": str}
                        \"\"\"},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},  # Force JSON
                    temperature=0.3,  # Lebih deterministik
                )
                
                output = response.choices[0].message.content
                
                # Validasi
                data = json.loads(output)
                required = ["sentiment", "confidence", "summary"]
                missing = [f for f in required if f not in data]
                
                if missing:
                    raise ValueError(f"Missing fields: {missing}")
                
                if not isinstance(data["confidence"], (int, float)):
                    raise ValueError("confidence harus angka")
                
                return data  # ✅ Valid!
                
            except (json.JSONDecodeError, ValueError) as e:
                print(f"⚠️ Attempt {attempt + 1} gagal: {e}")
                
                if attempt < max_retries - 1:
                    # Tambahkan hint di retry
                    prompt += f"\\n\\n[PENTING: Output sebelumnya tidak valid. Error: {e}. Pastikan JSON valid.]"
                else:
                    raise RuntimeError(f"Gagal setelah {max_retries} percobaan")
    
    # Penggunaan
    result = get_structured_output("Analisis sentimen: 'Produk bagus!'")
    print(result)  # {"sentiment": "positive", "confidence": 0.95, ...}
    ```

    💡 TIPS RETRY:
    1. Batasi jumlah retry (3-5x max)
    2. Tambahkan error info di retry prompt
    3. Gunakan temperature rendah untuk konsistensi
    4. Gunakan response_format={"type": "json_object"} (OpenAI)
    5. Log setiap retry untuk monitoring
    6. Fallback ke default value jika semua retry gagal
    """)


def demo_best_practices():
    """Best practices output validation."""
    print("=" * 60)
    print("DEMO 4: Best Practices Output Validation")
    print("=" * 60)

    print("""
    ✅ CHECKLIST OUTPUT VALIDATION:

    1. 📋 FORMAT VALIDATION
       □ JSON valid (jika mengharapkan JSON)
       □ Required fields lengkap
       □ Tipe data benar (string, number, boolean)
       □ Value dalam range yang valid

    2. 📏 LENGTH VALIDATION
       □ Tidak terlalu pendek (output kosong/singkat)
       □ Tidak terlalu panjang (cost & relevance)
       □ Sesuai batasan yang ditentukan

    3. 🔍 CONTENT VALIDATION
       □ Tidak mengandung konten berbahaya
       □ Tidak mengandung PII
       □ Tidak ada AI disclaimer yang tidak natural
       □ Dalam bahasa yang benar
       □ Tidak mengandung hallucinated URLs

    4. 🔄 FALLBACK STRATEGY
       □ Retry dengan prompt yang lebih jelas
       □ Fallback ke model lain
       □ Fallback ke default response
       □ Return error yang user-friendly

    5. 📊 MONITORING
       □ Log validation failure rate
       □ Track retry rate per model
       □ Alert jika failure rate tinggi
       □ Analisis pattern kegagalan

    🛠️ TOOLS UNTUK OUTPUT VALIDATION:
    ┌──────────────────────┬────────────────────────────────┐
    │ Tool                 │ Kegunaan                       │
    ├──────────────────────┼────────────────────────────────┤
    │ Pydantic             │ Python data validation         │
    │ Guardrails AI        │ LLM output validation lib      │
    │ Instructor           │ Structured LLM output (Python) │
    │ JSON Schema          │ Standard JSON validation       │
    │ NeMo Guardrails      │ NVIDIA's guardrails framework  │
    │ LangChain OutputParser│ Parsing & validation         │
    └──────────────────────┴────────────────────────────────┘
    """)


def main():
    demo_json_validation()
    demo_content_guardrails()
    demo_retry_pattern()
    demo_best_practices()

    print("\n" + "=" * 60)
    print("🎉 SELESAI! Anda telah menyelesaikan seluruh materi Inference!")
    print("=" * 60)
    print("""
    📚 Ringkasan Materi:
    01. Dasar Inference       → Apa itu inference, pipeline HF
    02. Model Selection       → Open vs Closed, HF Hub, Ollama
    03. Prompt Engineering    → Zero-Shot, Few-Shot, CoT, System Prompt
    04. Optimasi Inference    → Quantization, Batching, KV-Cache, Streaming
    05. API & Serving         → OpenAI API, HF API, FastAPI
    06. Evaluasi & Observability → Metrik, Cost Tracking, Logging
    07. Safety & Guardrails   → Moderation, Injection Defense, Validation
    """)

if __name__ == "__main__":
    main()
