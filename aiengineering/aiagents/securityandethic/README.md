# AI AGENT SECURITY & ETHICS WORKSPACE

Proyek pembelajaran **AI Agent Security & Ethics** berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan diagram visual komponen keamanan AI Agent.

Proyek ini mencakup simulasi murni (*self-contained*) dari 5 pilar utama keamanan & etika Agent:
1. **Prompt Injection / Jailbreaks**:
   - Simulasi Direct Injection (System Override) & Indirect Injection (via dokumen RAG/web scraping).
   - Teknik pertahanan XML Delimiters (`<system_context>`, `<user_query>`), Instruction Isolation, dan Dual-LLM Guardrail Filter.
2. **Tool Sandboxing / Permissioning**:
   - Role-Based Access Control (RBAC) & Human-in-the-Loop (HITL) Approval Gate untuk tindakan sensitif.
   - Sandbox eksekusi kode berbasis AST (Abstract Syntax Tree) & Directory Traversal Jail Check.
3. **Data Privacy + PII Redaction**:
   - Deteksi & Masking PII (Email, Nomor HP, KTP/NIK, Kartu Kredit, API Key).
   - Privacy-Preserving Memory Store (TTL Data Retention & GDPR Right to be Forgotten).
4. **Bias & Toxicity Guardrails**:
   - Input & Output Guardrail Pipeline (Llama Guard Taxonomy).
   - Bias Mitigation pada rekomendasi agent melalui System Steering Prompting & Self-Correction Loop.
5. **Safety + Red Team Testing**:
   - Automated Red Teaming Harness (Adversarial Testing Suite).
   - Evaluasi kuantitatif keselamatan agent: Attack Success Rate (ASR), Precision, Recall, dan Laporan Audit Keselamatan.

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`json`, `re`, `time`, `ast`, `dataclasses`, `enum`, `typing`) tanpa memerlukan dependensi external atau API Key eksternal.

```bash
# Menggunakan Python 3.9+
python3 -m venv .venv
source .venv/bin/activate
```

---

## 🚀 Cara Menjalankan CLI Interaktif

Jalankan menu interaktif CLI untuk memilih dan mengeksekusi modul simulasi secara visual:

```bash
python3 main.py
```

---

## 📚 Daftar Modul Pembelajaran

| No | Modul | Topik & Materi Utama | Skrip Python |
|----|-------|----------------------|--------------|
| **01** | **Prompt Injection / Jailbreaks** | • Direct & Indirect Prompt Injection<br>• XML Delimiters & Dual-LLM Guardrail | [`01_prompt_injection_jailbreaks/`](file:///Users/bsa/Documents/por/aiagents/securityandethic/01_prompt_injection_jailbreaks/) |
| **02** | **Tool Sandboxing / Permissioning** | • Tool RBAC & Human-in-the-Loop (HITL)<br>• AST Code Sandbox & Directory Jail | [`02_tool_sandboxing_permissioning/`](file:///Users/bsa/Documents/por/aiagents/securityandethic/02_tool_sandboxing_permissioning/) |
| **03** | **Data Privacy + PII Redaction** | • PII Masking (Email, NIK, Phone, CC, Key)<br>• Privacy Memory Store (TTL & GDPR Delete) | [`03_data_privacy_pii_redaction/`](file:///Users/bsa/Documents/por/aiagents/securityandethic/03_data_privacy_pii_redaction/) |
| **04** | **Bias & Toxicity Guardrails** | • Input & Output Guardrails Pipeline<br>• Bias Mitigation & Steering | [`04_bias_toxicity_guardrails/`](file:///Users/bsa/Documents/por/aiagents/securityandethic/04_bias_toxicity_guardrails/) |
| **05** | **Safety + Red Team Testing** | • Automated Red Teaming Harness<br>• Safety Benchmark & Audit Report | [`05_safety_red_team_testing/`](file:///Users/bsa/Documents/por/aiagents/securityandethic/05_safety_red_team_testing/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep teori lengkap dalam Bahasa Indonesia dapat dibaca di folder:
👉 [notes/security_and_ethic_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/securityandethic/notes/security_and_ethic_roadmap_notes.md)
