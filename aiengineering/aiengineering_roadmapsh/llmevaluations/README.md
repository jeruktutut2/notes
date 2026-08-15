# LLM Evaluations Learning Workspace

Selamat datang di modul pembelajaran interaktif **LLM Evaluations**! Modul ini dirancang berdasarkan kurikulum [roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer) dan taksonomi evaluasi Model Bahasa Besar (LLM).

---

## 🎯 Pembahasan Utama & Arsitektur Roadmap

Modul ini terbagi menjadi 2 area utama sesuai diagram roadmap: **Evaluation Types** (Jenis Evaluasi) dan **Evaluation Tools** (Kerangka Kerja & Perkakas Evaluasi).

```
+-----------------------------------------------------------------------------------+
|                              LLM EVALUATIONS ROADMAP                              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Evaluation Types]                                                               |
|   ├── 01. Deterministic Evals                                                     |
|   │    ├── Exact String Match, Regex Extraction, Levenshtein Distance             |
|   │    ├── JSON / Schema Validation (Pydantic), AST Parsing & Code Execution      |
|   │    └── BLEU-4, ROUGE-1/2/L, & METEOR Calculators                              |
|   ├── 02. Model-Based Evals (LLM-as-a-Judge)                                      |
|   │    ├── Single Grading vs Pairwise Ranking (Elo Ratings)                       |
|   │    ├── G-Eval Framework (Chain-of-Thought Evaluation & Weighted Criteria)     |
|   │    └── Mitigasi Bias Judge (Position Bias, Verbosity, Self-Enhancement)       |
|   ├── 03. Human Evals                                                             |
|   │    ├── Human-in-the-loop (HITL) Annotation & Likert Scale Scoring             |
|   │    ├── Inter-Annotator Agreement (Cohen's Kappa & Fleiss' Kappa)              |
|   │    └── Chatbot Arena Style ELO Benchmark Simulator                            |
|   └── 04. Evaluation Metrics                                                      |
|        ├── Standard Classification & NLP Metrics (Accuracy, F1, Perplexity)      |
|        └── RAG Triad Metrics (Faithfulness, Answer Relevance, Context Precision/Recall)|
|                                                                                   |
|  [Evaluation Tools]                                                               |
|   └── 05. Frameworks & Tools                                                      |
|        ├── DeepEval: LLM Unit Testing, G-Eval, Custom Metrics, PyTest Integration |
|        └── RAGAS: RAG Assessment, Faithfulness, Context Recall/Precision          |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 📁 Struktur Direktori Repository

```
llmevaluations/
├── README.md                           # Dokumentasi & indeks modul
├── requirements.txt                    # Dependensi Python
├── main.py                             # Master CLI runner untuk lab interaktif
├── notes/                              # Catatan teori & konsep teknis komprehensif
│   ├── 01_deterministic_evals.md
│   ├── 02_model_based_evals.md
│   ├── 03_human_evals.md
│   ├── 04_evaluation_metrics.md
│   └── 05_evaluation_tools.md
├── 01_deterministic_evals/
│   ├── 01_string_and_regex_evals.py     # Exact Match, Regex, Levenshtein Distance
│   ├── 02_schema_and_code_asserts.py   # Validasi JSON Pydantic & AST Python Code
│   └── 03_nlp_deterministic_metrics.py # Kalkulator BLEU, ROUGE-1/2/L & METEOR
├── 02_model_based_evals/
│   ├── 01_llm_judge_single_and_pairwise.py # Single grading vs Pairwise comparison
│   ├── 02_geval_chain_of_thought.py    # Framework G-Eval dengan CoT & Weighting
│   └── 03_judge_bias_mitigation.py     # Swapping position & score normalization
├── 03_human_evals/
│   ├── 01_human_annotation_lab.py      # Simulator annotator & Likert collector
│   ├── 02_inter_annotator_agreement.py # Cohen's & Fleiss' Kappa scorer
│   └── 03_chatbot_arena_elo.py         # ELO rating benchmark simulator
├── 04_evaluation_metrics/
│   ├── 01_classification_and_nlp_metrics.py # Precision, Recall, F1, Perplexity
│   └── 02_rag_triad_evaluator.py       # Math & logic RAG Triad Evaluator
├── 05_evaluation_tools/
│   ├── 01_deepeval_framework_demo.py   # DeepEval metrics, G-Eval & test suites
│   └── 02_ragas_framework_demo.py      # RAGAS metrics & dataset evaluation
└── web_visualizer/                     # Visualizer Web Interaktif SPA
    ├── index.html
    ├── styles.css
    ├── app.js
    └── server.py                       # Python HTTP server visualizer
```

---

## 🚀 Cara Menjalankan

### 1. Menginstall Dependensi
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Master CLI Runner
```bash
python main.py
```

### 3. Menjalankan Interactive Web Visualizer
```bash
python main.py --web
# atau
python web_visualizer/server.py
```
Akses di browser pada URL `http://localhost:5000`.

---

## 📚 Detail Topik Evaluasi

### 1. Deterministic Evals
Evaluasi otomatis tanpa LLM menggunakan aturan matematis, perbandingan karakter, skema JSON, atau regex. Sangat cepat, hemat biaya, dan 100% konsisten.

### 2. Model-Based Evals (LLM-as-a-Judge)
Penggunaan LLM canggih (seperti GPT-4o atau Claude 3.5 Sonnet) untuk mengevaluasi luaran LLM lain berdasarkan kriteria tertentu (G-Eval, CoT evaluation) serta teknik mitigasi bias judge.

### 3. Human Evals
Gold standard evaluasi LLM melibatkan manusia melalui annotation interface, skala Likert, dan pengukuran konsistensi antar-evaluator (Cohen's & Fleiss' Kappa) serta sistem ELO Chatbot Arena.

### 4. Evaluation Metrics
Metrik tradisional (Precision, Recall, F1, BLEU, ROUGE) dan metrik khusus LLM seperti **RAG Triad** (*Faithfulness*, *Answer Relevance*, *Context Precision*, *Context Recall*).

### 5. Evaluation Tools
- **DeepEval**: Framework open-source untuk LLM unit testing berbasis PyTest.
- **RAGAS**: Framework evaluasi terpopuler khusus pipeline Retrieval Augmented Generation (RAG).
