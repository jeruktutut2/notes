# PROMPT ENGINEERING AI ENGINEERING - Belajar dari Roadmap.sh

Proyek pembelajaran **Prompt Engineering & AI Engineering** berdasarkan [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).
Setiap modul berisi skrip Python runnable yang dapat langsung dijalankan beserta simulasi mekanisme prompt, teknik perancangan, keamanan red teaming, dan catatan teori lengkap dalam Bahasa Indonesia.

## Persiapan Environment & Install

```bash
# Menggunakan Python 3.9+
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

> **Catatan Dependensi:** Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal.

## Cara Menjalankan

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul:

```bash
python3 main.py
```

---

## Daftar Modul Pembelajaran

| No | Modul | Topik & Materi | Skrip Python |
|----|-------|----------------|--------------|
| **01** | Dasar Prompt & Anatomi | Membedah 4 Komponen Prompt (Instruction, Context, Input, Output), Persona & System Role Framing, Pembatas Tag XML | `01_dasar_prompt_dan_anatomi/` |
| **02** | Teknik Prompting Dasar | Zero-Shot vs Few-Shot Learning, Chain-of-Thought (CoT), Self-Consistency Voting & Tree-of-Thought (ToT) | `02_teknik_prompting_dasar/` |
| **03** | Teknik Prompting Lanjutan | ReAct Framework (Thought->Action->Obs), Directional Stimulus, Least-to-Most Decomposition, Prompt Chaining | `03_teknik_prompting_lanjutan/` |
| **04** | Output Structuring & Constraints | JSON Schema Enforcement & Repair Loop, Negative Constraints & Algorithmic Guardrails Validation | `04_output_structuring_dan_constraints/` |
| **05** | Keamanan Prompt & Red Teaming | Direct & Indirect Injection Detection, Jailbreak Patterns (DAN, Base64), Defensive Prompting (Sandwich & Tag Isolation) | `05_keamanan_prompt_dan_red_teaming/` |
| **06** | Evaluasi & Optimasi Prompt | Automated Evaluation & LLM-as-a-Judge Benchmarking, Prompt Compression & Cost Optimization, Meta-Prompting & APE | `06_evaluasi_dan_optimasi_prompt/` |

---

## Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik prompt engineering (mulai dari matematika Self-Consistency hingga arsitektur pertahanan prompt) dapat dibaca di folder [notes/prompt_engineering_roadmap_notes.md](notes/prompt_engineering_roadmap_notes.md).
