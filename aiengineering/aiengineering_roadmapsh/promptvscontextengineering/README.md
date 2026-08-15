# PROMPT VS CONTEXT ENGINEERING - ROADMAP AI ENGINEER

Workspace pembelajaran komprehensif **Prompt Engineering vs Context Engineering** berdasarkan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer).

---

## 📁 Fungsi & Kegunaan Folder Utama Workspace

Folder dalam proyek ini dikelompokkan ke dalam **4 Kategori Utama**:

```
promptvscontextengineering/
├── 📁 01_prompt_engineering/            # Kategori 1: Teknik Rekayasa Prompt LLM
├── 📁 02_context_engineering/           # Kategori 2: Pengelolaan State, Memori & Environment Data
├── 📁 03_model_selection_and_hosting/   # Kategori 3: Pemilihan Model (Pre-trained, Closed/Open Source, Hosting)
├── 📁 04_prompt_vs_context_engineering/ # Kategori 4: Perbandingan Paradigma, Decision Engine & Hybrid Pipeline
├── 📁 notes/                            # Dokumentasi Teori & Syllabi Roadmap.sh
├── 📄 main.py                           # CLI Launcher Utama Interaktif
└── 📄 README.md                         # Dokumen Utama Panduan Proyek
```

---

## 🎯 Penjelasan Fungsi Masing-Masing Folder

### 📌 `01_prompt_engineering/`
**Fungsi**: Mempelajari teknik rekayasa instruksi langsung (*prompting*) untuk mengarahkan perilaku, penalaran, format luaran, dan keamanan LLM tanpa mengubah bobot model.
- **Topik di dalamnya**: `01_zero_shot_and_few_shot`, `02_cot_and_react`, `03_input_format_and_structured_output`, `04_function_calling`, `05_prompt_caching`, `06_streaming_responses`, `07_system_prompting_role_behavior`, `08_context_and_constraints`.

### 📌 `02_context_engineering/`
**Fungsi**: Mempelajari teknik pengelolaan lingkungan (*environment state*), memori percakapan jangka panjang, kompresi token, dan isolasi data sebelum masuk ke *Context Window* LLM.
- **Topik di dalamnya**: `01_external_memory`, `02_rag_and_dynamic_filters`, `03_context_compaction`, `04_context_isolation`.

### 📌 `03_model_selection_and_hosting/`
**Fungsi**: Mempelajari cara memilih model fondasi yang tepat (skala 7B hingga 405B), analisis biaya Proprietary API vs Open-Source, serta kalkulasi infrastruktur VRAM GPU untuk *Self-Hosted Inference Engine* (vLLM / Ollama).
- **Topik di dalamnya**: `01_pretrained_models`, `02_closed_vs_open_source_models`, `03_self_hosted_models`.

### 📌 `04_prompt_vs_context_engineering/`
**Fungsi**: Mempelajari perbandingan langsung antara Prompt Engineering dan Context Engineering, termasuk *Architectural Decision Routing Engine* dan pembuatan *End-to-End Production Hybrid Pipeline*.
- **Topik di dalamnya**: `01_perbandingan_paradigma_dan_tradeoffs.py`, `02_decision_matrix_dan_routing.py`, `03_hybrid_prompt_context_architecture.py`.

---

## 🚀 Cara Menjalankan

Jalankan menu interaktif dari terminal:

```bash
cd /Users/bsa/Documents/por/aiengineering/promptvscontextengineering
python3 main.py
```
