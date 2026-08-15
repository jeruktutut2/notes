# Implementasi Point 7: Safety dan Guardrails

Teknik keamanan dan pembatasan untuk memastikan output model AI aman, tepat, dan sesuai kebijakan.

## Daftar File

1. `1_content_moderation.py`: Cara memoderasi konten — memfilter output yang berbahaya, tidak pantas, atau melanggar kebijakan.
2. `2_prompt_injection_defense.py`: Pertahanan terhadap prompt injection — serangan dimana user mencoba memanipulasi instruksi model.
3. `3_output_validation.py`: Validasi dan constraining output model agar sesuai format/schema yang diharapkan.

## Konsep Kunci

| Ancaman | Solusi | Prioritas |
|---------|--------|-----------|
| Konten berbahaya/NSFW | Content moderation API | 🔴 Tinggi |
| Prompt injection | Input sanitization, detection | 🔴 Tinggi |
| Hallucination | RAG, grounding, fact-checking | 🟡 Medium |
| Output tidak valid | Schema validation, guardrails | 🟡 Medium |
| Data leakage | PII detection, output filtering | 🔴 Tinggi |
| Bias | Evaluation, diverse training data | 🟡 Medium |
