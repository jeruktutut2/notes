# MATRIKS SINTESIS & ARCHITECTURAL DECISION (PROMPT VS CONTEXT ENGINEERING)

Dokumen ini menyajikan panduan sintesis mendalam mengenai perbandingan dan integrasi **Prompt Engineering vs Context Engineering**.

---

## 📊 Matriks Tradeoff 6 Dimensi

| Dimensi Evaluasi | Prompt Engineering | Context Engineering |
|------------------|--------------------|---------------------|
| **Fokus Utama** | Formulasi instruksi, persona, CoT, dan format output. | Pengelolaan environment state, memory buffer, pruning, RAG, KV Caching. |
| **Sifat Data** | Statis & Terstruktur di dalam prompt. | Dinamis, Stateful, Multi-Tenant & Real-time Knowledge. |
| **Ukuran Token** | Kecil hingga Menengah ($100 - 4,000$ tokens). | Besar hingga Masif ($8,000 - 128,000+$ tokens). |
| **Latensi (TTFT)** | Latensi rendah / Time-to-first-token cepat. | Membutuhkan Prefix Caching untuk mencegah lonjakan latensi. |
| **Biaya API** | Sangat murah per eksekusi. | Berpotensi mahal tanpa Token Compaction & Caching. |
| **Tantangan Utama**| Direct Prompt Injection, Jailbreak, Instruction Drift. | Lost-in-the-Middle, Context Overflow, Memory Leak, Privacy Leak. |

---

## 🌲 Decision Tree: Kapan Menggunakan Apa?

```
                               Apakah tugas membutuhkan data eksternal / state?
                                                      │
                       ┌──────────────────────────────┴──────────────────────────────┐
                       │ Tidak                                                       │ Ya
                       ▼                                                             ▼
         Prompt Engineering Only                                    Apakah data muat dalam 16K tokens?
  (Persona + CoT + JSON Schema)                                                      │
                                                      ┌──────────────────────────────┴──────────────────────────────┐
                                                      │ Ya                                                          │ Tidak
                                                      ▼                                                             ▼
                                       Context Engineering (In-Context)                             Context Engineering + RAG
                                     (Prefix Caching + Density Pruning)                         (Dynamic Assembler + Vector DB)
```

---

## 🏗️ Production Hybrid Architecture

Dalam arsitektur *production-grade*, Prompt Engineering dan Context Engineering bekerja bersama secara berurutan:

1. **Context Engineering Layer**:
   - Membaca External Memory (Semantic & Episodic).
   - Menjalankan Hybrid Search RAG + Dynamic Metadata Filter.
   - Melakukan PII Masking & Token Compaction.
2. **Prompt Engineering Layer**:
   - Membungkus data terkompresi dengan XML Tag Delimiters.
   - Menetapkan System Persona & Behavioral Negative Constraints.
   - Menjalankan CoT Reasoning & Output JSON Schema Repair Loop.
