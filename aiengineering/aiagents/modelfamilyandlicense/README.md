# MODEL FAMILIES, LICENSES & GENERATION CONTROLS - AI AGENTS LEARNING WORKSPACE

Proyek pembelajaran **Model Families, Licenses & Generation Controls** untuk AI Agents berdasarkan roadmap resmi di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan dua diagram referensi pendukung.

Proyek ini mencakup simulasi murni (*self-contained*) dari pilar utama **Model Families and Licences** (*Open Weight Models*, *Closed Weight Models*, *Licensing & Legal Compliance*) serta **Generation Controls** (*Temperature*, *Top-p*, *Frequency Penalty*, *Presence Penalty*, *Stopping Criteria*, dan *Max Length*).

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`math`, `json`, `random`, `re`, `dataclasses`, `typing`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

```bash
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

---

## 📚 Daftar Modul Pembelajaran

| No | Modul | Topik & Materi Utama | Skrip Python |
|----|-------|----------------------|--------------|
| **01** | **Open Weight Models & Lisensi** | • Katalog Llama 3, Mistral, Qwen, DeepSeek, Gemma, Phi<br>• Kalkulasi VRAM & Throughput Dense vs MoE<br>• Analisis Lisensi Apache 2.0, MIT vs Llama 3 & Gemma Terms | [`01_open_weight_models/`](file:///Users/bsa/Documents/por/aiagents/modelfamilyandlicense/01_open_weight_models/) |
| **02** | **Closed Weight Models & Matrix** | • Katalog API GPT-4o, Claude 3.5, Gemini 1.5/2.0, DeepSeek API<br>• Enterprise Privacy (Zero Data Retention / ZDR), Batch API & Caching<br>• Matrix Keputusan Tradeoff Multi-Kriteria Open vs Closed | [`02_closed_weight_models/`](file:///Users/bsa/Documents/por/aiagents/modelfamilyandlicense/02_closed_weight_models/) |
| **03** | **Generation Controls (Gambar 1)** | • Visualisator Softmax Scaling (Temperature) & Nucleus (Top-P)<br>• Logit Adjustment & Penanganan Looping (Freq & Presence Penalty)<br>• Stop Sequences (ReAct `Observation:`) & Truncated JSON Repair Parser | [`03_generation_controls/`](file:///Users/bsa/Documents/por/aiagents/modelfamilyandlicense/03_generation_controls/) |
| **04** | **License Audit & Architecture** | • Interactive Legal Compliance Audit Tool & EU AI Act Risk Tier<br>• Rekomendasi Topology Multi-Agent & Hybrid Model Routing | [`04_license_and_commercial_rights/`](file:///Users/bsa/Documents/por/aiagents/modelfamilyandlicense/04_license_and_commercial_rights/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari matematika Softmax Temperature hingga formulasi Logit Penalties, Lisensi Open Weight, dan Arsitektur Hybrid Model Agent) dapat dibaca di folder:
👉 [`notes/model_family_and_licence_roadmap_notes.md`](file:///Users/bsa/Documents/por/aiagents/modelfamilyandlicense/notes/model_family_and_licence_roadmap_notes.md)
