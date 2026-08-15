# 01. Structured Outputs & Schema Enforcement

## Overview
Dalam aplikasi software produksi, output LLM tidak boleh berupa teks bebas yang acak; output harus dapat diparse (*parseable*) secara otomatis oleh program menggunakan format seperti **JSON**, **XML**, **Markdown**, atau **CSV**.

---

## 1. Format-Format Structured Outputs

### A. JSON / JSON Schema
Format paling populer untuk integrasi API dan backend microservices.
- **Pydantic / Structured Outputs API (OpenAI/Gemini)**: Menjamin 100% kepatuhan tata bahasa skema JSON tanpa syntax error (misal: koma terbalik, tanda petik hilang).

### B. XML Tags (`<context>`, `<instructions>`, `<output>`)
Sangat direkomendasikan untuk model Anthropic Claude.
- **Keunggulan XML**: Mencegah ambiguasi antara instruksi sistem, teks dokumen input dari pengguna, dan output yang dihasilkan.

### C. Markdown Tables & CSV
Cocok untuk visualisasi data, pelaporan, atau ekspor data tabel langsung ke spreadsheet.

---

## 2. Teknik Enforcing Structured Outputs
1. **JSON Mode (`response_format={"type": "json_object"}`)**: Mengharuskan LLM menghasilkan sintaks JSON valid.
2. **Strict Schema / Function Calling**: Mempassing JSON Schema Pydantic langsung ke dalam API payload.
3. **Delimiter & Few-Shot Schema**: Memberikan contoh skema JSON persis di dalam prompt.
