# AI Engineering - Regression Testing Workspace 🧪⚡

Selamat datang di ruang belajar **Regression Testing untuk AI Engineering**! Modul ini dirancang berdasarkan kurikulum **[roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer)** untuk membantu Anda memahami, mengukur, dan mencegah penurunan kualitas (*regression*) pada aplikasi berbasis Large Language Model (LLM), RAG, dan AI Agents.

---

## 🎯 Mengapa Regression Testing Penting di AI Engineering?

Dalam pengujian perangkat lunak tradisional, *regression test* memastikan perubahan kode baru tidak merusak fitur lama. 
Dalam **AI Engineering**, *regression testing* menjadi jauh lebih penting dan menantang karena:
1. **Output LLM Bersifat Non-Deterministik**: Output bervariasi meskipun input sama (kecuali temperature=0, namun variasi versi model tetap ada).
2. **Prompt Tweaks Terkadang Merusak Kasus Lain**: Mengubah system prompt untuk memperbaiki Case A seringkali secara tidak sengaja menurunkan akurasi pada Case B (*Prompt Regression*).
3. **Pembaruan Versi Model (Model Drift / Version Upgrades)**: Mengganti model (misal `gpt-4o` ke `gpt-4o-mini` atau update versi model) dapat merubah format JSON, panjang jawaban, atau penalaran.
4. **Perubahan Pipeline RAG**: Mengubah ukuran chunk, top-k retrieval, atau model embedding dapat menyebabkan *hallucination* atau kehilangan informasi krusial.

---

## 📚 Struktur Pembelajaran

### 📖 Dokumentasi Konsep (`docs/`)
- **[`01_concept_overview.md`](docs/01_concept_overview.md)**: Konsep dasar, perbedaan Deterministic Testing vs Non-Deterministic Testing, serta metrik regresi AI.
- **[`02_types_of_ai_regression.md`](docs/02_types_of_ai_regression.md)**: Jenis-jenis regresi: Quality, Guardrail/Safety, Schema/JSON, RAG Retrieval, & Cost/Latency.
- **[`03_testing_methodologies.md`](docs/03_testing_methodologies.md)**: Metodologi pengujian: Golden Datasets, Pairwise LLM-as-a-Judge, Embedding Cosine Similarity, dan Pytest CI/CD Integration.
- **[`04_tools_and_frameworks.md`](docs/04_tools_and_frameworks.md)**: Alat & Framework terpopuler: DeepEval, Promptfoo, Ragas, & Custom Harness.

---

### 💻 Executable Python Code (`examples/`)
- **[`requirements.txt`](examples/requirements.txt)**: Dependensi Python (`pytest`, `numpy`, `tabulate`, `pydantic`).
- **[`01_golden_dataset_eval.py`](examples/01_golden_dataset_eval.py)**: Pengujian baseline dataset emas menggunakan pengujian deterministik & aturan logika.
- **[`02_semantic_embedding_regression.py`](examples/02_semantic_embedding_regression.py)**: Pengujian regresi makna kalimat (*Semantic Cosine Similarity*) antar iterasi prompt/model.
- **[`03_llm_as_a_judge_pairwise.py`](examples/03_llm_as_a_judge_pairwise.py)**: Evaluasi komparatif berpasangan (*Pairwise Regression Evaluation*) antara Prompt v1 vs Prompt v2 menggunakan LLM-as-a-Judge.
- **[`04_rag_regression_test.py`](examples/04_rag_regression_test.py)**: Pengujian regresi sistem RAG (Faithfulness, Context Relevance, Answer Relevance).
- **[`test_ai_regression.py`](examples/test_ai_regression.py)**: Test suite Pytest otomatis yang siap dijalankan dalam CI/CD pipeline.

---

### 🌐 Interactive Web Visualizer (`index.html`)
Buka file [`index.html`](index.html) di browser Anda untuk menggunakan **AI Regression Testing Simulator**:
- **Golden Dataset Manager**: Pilih/Kelola dataset pengujian.
- **Regression Simulator**: Uji perbedaan Prompt v1 vs v2, Model A vs Model B, atau RAG configuration.
- **Diff & Score Visualizer**: Analisis skor regresi, radar chart, visual diff teks, serta latensi & biaya.
- **Knowledge Quiz**: Uji pemahaman Anda tentang pengujian regresi AI.

---

## 🚀 Cara Menjalankan Contoh Kode

```bash
# 1. Masuk ke direktori contoh
cd examples

# 2. Install dependensi
pip install -r requirements.txt

# 3. Jalankan contoh pengujian
python3 01_golden_dataset_eval.py
python3 02_semantic_embedding_regression.py
python3 03_llm_as_a_judge_pairwise.py
python3 04_rag_regression_test.py

# 4. Jalankan Pytest Suite
pytest test_ai_regression.py -v
```
