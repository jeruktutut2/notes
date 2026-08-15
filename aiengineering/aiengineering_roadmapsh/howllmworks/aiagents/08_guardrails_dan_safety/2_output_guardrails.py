import os
import re
import json
from openai import OpenAI

def main():
    print("=== 8.2 Output Guardrails (Mengecek Output Agent) ===\n")

    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    if not api_key:
        print("[ERROR] OPENAI_API_KEY belum diset!")
        return

    client = OpenAI(api_key=api_key, base_url=base_url)

    # ---------------------------------------------------------------
    # OUTPUT GUARDRAILS
    # Setelah LLM menghasilkan jawaban, kita perlu mengecek sebelum
    # mengirimkan ke user:
    # 1. PII Detection: Cek apakah output mengandung data pribadi
    # 2. Content Safety: Cek apakah output mengandung konten berbahaya
    # 3. Format Validation: Cek apakah output sesuai format yang diharapkan
    # 4. Hallucination Check: Cek apakah output sesuai fakta yang diberikan
    # ---------------------------------------------------------------

    # --- GUARDRAIL 1: PII (Personally Identifiable Information) Detection ---
    def detect_pii(text):
        """Deteksi informasi pribadi dalam output."""
        pii_patterns = {
            "NIK": r"\b\d{16}\b",
            "Email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
            "Telepon": r"\b(?:08|\+62)\d{8,12}\b",
            "Kartu Kredit": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
            "NPWP": r"\b\d{2}\.\d{3}\.\d{3}\.\d-\d{3}\.\d{3}\b",
        }

        found = []
        for pii_type, pattern in pii_patterns.items():
            matches = re.findall(pattern, text)
            if matches:
                # Mask PII
                for match in matches:
                    found.append({"type": pii_type, "value": match, "masked": mask_pii(match)})

        return found

    def mask_pii(value):
        """Menyembunyikan sebagian besar karakter PII."""
        if len(value) <= 4:
            return "****"
        return value[:2] + "*" * (len(value) - 4) + value[-2:]

    def remove_pii(text, pii_list):
        """Menghapus PII dari teks dan menggantinya dengan masked version."""
        cleaned = text
        for pii in pii_list:
            cleaned = cleaned.replace(pii["value"], f"[{pii['type']}: {pii['masked']}]")
        return cleaned

    # --- GUARDRAIL 2: Content Safety Check ---
    def check_content_safety(text):
        """Cek apakah output mengandung konten yang tidak aman."""
        unsafe_categories = {
            "konten_kekerasan": [
                r"cara\s+(?:membunuh|menyakiti|melukai)",
                r"instruksi\s+(?:senjata|bom|racun)",
            ],
            "informasi_palsu": [
                r"(?:sudah\s+)?terbukti\s+(?:secara\s+)?ilmiah\s+(?:bahwa|kalau)",
            ]
        }

        issues = []
        for category, patterns in unsafe_categories.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    issues.append({"category": category, "pattern": pattern})

        return issues

    # --- GUARDRAIL 3: LLM-based Output Check ---
    def check_output_quality(output, original_question):
        """Menggunakan LLM untuk mengecek kualitas output."""
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Kamu adalah quality checker untuk output AI. "
                        "Analisis output berikut dan berikan penilaian.\n"
                        "Kembalikan JSON:\n"
                        "{\n"
                        '  "relevant": true/false,\n'
                        '  "contains_harmful": true/false,\n'
                        '  "is_hallucination_likely": true/false,\n'
                        '  "quality_score": 1-10,\n'
                        '  "issues": ["..."] \n'
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": f"Pertanyaan user: {original_question}\n\nOutput AI: {output}"
                }
            ],
            temperature=0.0
        )

        result = response.choices[0].message.content.strip()
        try:
            clean = result
            if clean.startswith("```"):
                clean = clean.split("\n", 1)[1].rsplit("```", 1)[0]
            return json.loads(clean)
        except:
            return {"error": "Gagal parse"}

    # --- PIPELINE OUTPUT GUARDRAILS ---
    def apply_guardrails(output, original_question):
        """Menerapkan semua guardrails pada output."""
        print(f"\n{'─'*50}")
        print(f"📤 Output: \"{output[:100]}{'...' if len(output) > 100 else ''}\"")

        passed = True

        # Guardrail 1: PII Detection
        pii_found = detect_pii(output)
        if pii_found:
            print(f"  ⚠️ PII Detected: {len(pii_found)} item(s)")
            for pii in pii_found:
                print(f"     - {pii['type']}: {pii['value']} → {pii['masked']}")
            output = remove_pii(output, pii_found)
            print(f"  🔒 PII telah di-mask dalam output")
        else:
            print(f"  ✅ PII Check: Bersih")

        # Guardrail 2: Content Safety
        safety_issues = check_content_safety(output)
        if safety_issues:
            print(f"  ❌ Content Safety: {len(safety_issues)} masalah ditemukan")
            for issue in safety_issues:
                print(f"     - Kategori: {issue['category']}")
            passed = False
        else:
            print(f"  ✅ Content Safety: OK")

        # Guardrail 3: LLM Quality Check
        quality = check_output_quality(output, original_question)
        if isinstance(quality, dict) and "error" not in quality:
            score = quality.get("quality_score", 0)
            print(f"  📊 Quality Score: {score}/10")
            if quality.get("contains_harmful"):
                print(f"  ❌ LLM Check: Konten berbahaya terdeteksi")
                passed = False
            elif quality.get("is_hallucination_likely"):
                print(f"  ⚠️ LLM Check: Kemungkinan halusinasi")
            else:
                print(f"  ✅ LLM Check: OK")

            issues = quality.get("issues", [])
            if issues:
                print(f"  📝 Issues: {', '.join(issues)}")

        if passed:
            print(f"  ✅ OUTPUT APPROVED")
        else:
            print(f"  ❌ OUTPUT BLOCKED")

        return output if passed else None

    # --- DEMO ---
    print("=" * 60)
    print("DEMO: Output Guardrails")
    print("=" * 60)

    test_cases = [
        {
            "question": "Siapa PIC untuk project Alpha?",
            "output": "PIC project Alpha adalah Budi Santoso, bisa dihubungi di 081234567890 atau email budi.santoso@company.com. NIK: 3174012345670001."
        },
        {
            "question": "Apa itu machine learning?",
            "output": "Machine learning adalah cabang dari kecerdasan buatan yang memungkinkan komputer belajar dari data tanpa diprogram secara eksplisit."
        },
        {
            "question": "Berapa revenue Q3?",
            "output": "Revenue Q3 2024 mencapai Rp 15.5 miliar, meningkat 23% dari Q2. Pertumbuhan ini didorong oleh peluncuran produk baru."
        },
    ]

    for tc in test_cases:
        result = apply_guardrails(tc["output"], tc["question"])

    print(f"\n{'='*60}")
    print("✅ Selesai! Memahami output guardrails.")
    print("\nLayer Output Guardrails:")
    print("  1. PII Detection: Cari dan mask data pribadi (email, telepon, NIK)")
    print("  2. Content Safety: Cek konten berbahaya dengan regex")
    print("  3. LLM Quality Check: Cek relevansi dan halusinasi dengan LLM")
    print("\nBest Practices:")
    print("  - Selalu mask PII sebelum mengirim output ke user")
    print("  - Log semua output yang diblokir untuk review")
    print("  - Gunakan multiple layers (rule-based + LLM-based)")

if __name__ == "__main__":
    main()
