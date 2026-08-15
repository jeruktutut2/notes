# 02. Automatic Prompt Engineering (APE)

## Overview
**Automatic Prompt Engineering (APE)** adalah metodologi menggunakan LLM itu sendiri (seperti GPT-4o atau Claude 3.5 Sonnet) untuk merancang, mengkritisi, memperhalus, dan mengoptimalkan prompt manusia secara otomatis.

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Draft Prompt    │ ────> │ Meta-Prompt LLM │ ────> │ Optimized       │
│ (Manusia)       │       │ (Prompt Doctor) │       │ Production      │
└─────────────────┘       └─────────────────┘       │ Prompt          │
                                                    └─────────────────┘
```

---

## 1. Konsep Meta-Prompting
Meta-prompt adalah prompt yang digunakan untuk **menghasilkan prompt lain**.
LLM memiliki pemahaman mendalam mengenai arsitektur internalnya sendiri, sehingga LLM sangat handal dalam menyusun instruksi yang jelas, tidak ambigu, dan menambahkan guardrails yang sering terlewat oleh manusia.

---

## 2. Struktur Meta-Prompt "Prompt Engineer Generator"

```markdown
[SYSTEM INSTRUCTION]
Anda adalah seorang Master Prompt Engineer. Tugas Anda adalah mengambil prompt draft yang kasar dari pengguna dan mengubahnya menjadi Prompt Produksi berkualitas tinggi.

[ATURAN PENULISAN PROMPT PRODUKSI]
1. Tentukan Role/Persona spesifik.
2. Pisahkan Konteks, Instruksi Utama, Batasan (Constraints), dan Format Output menggunakan tag XML (<context>, <instruction>, <constraints>, <format>).
3. Tambahkan 2 contoh Few-Shot jika relevan.
4. Gunakan variabel placeholder {{variable_name}}.
5. Berikan instruksi pembatas agar model tidak berhalusinasi.

[DRAFT PROMPT PENGGUNA]
"Buatkan deskripsi barang buat jualan sepatu di toko online biar menarik"

[PROMPT PRODUKSI HASIL GENERASI]
```

---

## 3. Workflow Iteratif Automatic Optimization (APE Loop)
1. **Candidate Generation**: LLM menghasilkan 5 variasi prompt berbeda.
2. **Execution & Evaluation**: Kelima prompt diuji pada dataset pengujian (benchmark dataset).
3. **Scoring**: Evaluator LLM memberi nilai pada setiap output.
4. **Refinement**: Model memilih prompt dengan skor tertinggi dan melakukan tuning tambahan.
