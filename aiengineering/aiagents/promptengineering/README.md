# PROMPT ENGINEERING & WRITING GOOD PROMPTS - AI AGENTS LEARNING WORKSPACE

Proyek pembelajaran **Prompt Engineering** untuk AI Agents berdasarkan roadmap resmi di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan diagram visual **Writing Good Prompts**.

Proyek ini mencakup simulasi murni (*self-contained*) dari **6 Pilar Utama Writing Good Prompts**:
1. **Be Specific in What You Want**
2. **Provide Additional Context**
3. **Use Relevant Technical Terms**
4. **Use Examples in Your Prompt**
5. **Iterate and Test Your Prompts**
6. **Specify Length, Format Etc.**

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python 3.9+ (`json`, `re`, `dataclasses`, `time`, `typing`, `subprocess`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

```bash
# Pindah ke direktori promptengineering
cd /Users/bsa/Documents/por/aiagents/promptengineering

# Menggunakan Python 3.9+
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

---

## 🚀 Cara Menjalankan CLI Interaktif

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul simulasi secara visual:

```bash
python3 main.py
```

Atau jalankan seluruh simulasi modul sekaligus secara non-interaktif:

```bash
python3 main.py --all
```

---

## 📚 Daftar Modul Pembelajaran

| No | Modul | Topik & Materi Utama | Skrip Python |
|----|-------|----------------------|--------------|
| **01** | **Be Specific in What You Want** | • Perbandingan Prompt Ambigu vs Spesifik<br>• Persona & Role Prompting (Action Verbs & Task Boundary)<br>• Refaktoring Engine Prompt Otomatis | [`01_be_specific_and_role_prompting/`](file:///Users/bsa/Documents/por/aiagents/promptengineering/01_be_specific_and_role_prompting/) |
| **02** | **Provide Additional Context** | • Injeksi Konteks Data (Grounding Data & RAG)<br>• XML Tag Delimiters (<context>, <document>)<br>• Mitigasi Halusinasi Data & Isolasi Konteks Sistem | [`02_provide_additional_context/`](file:///Users/bsa/Documents/por/aiagents/promptengineering/02_provide_additional_context/) |
| **03** | **Use Relevant Technical Terms** | • Attention Steering Mechanism pada Transformer<br>• Kosakata Domain Spesifik (ACID, MVCC, WAL, Cosine Annealing)<br>• Mengarahkan Vektor Perhatian LLM ke Pakar Domain | [`03_technical_terms_and_domain_jargon/`](file:///Users/bsa/Documents/por/aiagents/promptengineering/03_technical_terms_and_domain_jargon/) |
| **04** | **Use Examples in Your Prompt** | • In-Context Learning (ICL) & Few-Shot Exemplars<br>• Zero-Shot vs Few-Shot Comparison<br>• Penanganan Edge Cases & Format Style Matching | [`04_use_examples_few_shot/`](file:///Users/bsa/Documents/por/aiagents/promptengineering/04_use_examples_few_shot/) |
| **05** | **Iterate and Test Your Prompts** | • Automated Prompt Evaluation & Benchmarking Suite<br>• A/B Testing (Prompt v1.0 Unoptimized vs v2.0 Optimized)<br>• Format & Keyword Pass Rate Metrics | [`05_iterate_and_test_prompts/`](file:///Users/bsa/Documents/por/aiagents/promptengineering/05_iterate_and_test_prompts/) |
| **06** | **Specify Length, Format Etc.** | • Structured Output Enforcement (JSON Schema & XML Tags)<br>• Batasan Panjang Kata/Token (Length Constraints)<br>• Robust Regex Fallback Cleaner untuk Machine Parsers | [`06_specify_length_and_format/`](file:///Users/bsa/Documents/por/aiagents/promptengineering/06_specify_length_and_format/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari teori Attention Steering, anatomi System Prompt AI Agent, mitigasi Prompt Injection, hingga skema evaluasi otomatis) dapat dibaca di folder:
👉 [notes/prompt_engineering_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/promptengineering/notes/prompt_engineering_roadmap_notes.md)
