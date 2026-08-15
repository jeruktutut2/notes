# LLM Observability Learning Workspace

Selamat datang di modul pembelajaran interaktif **LLM Observability**! Modul ini dirancang berdasarkan kurikulum [roadmap.sh AI Engineer](https://roadmap.sh/ai-engineer) dan gambar arsitektur observability untuk Generative AI.

---

## 🎯 Pembahasan Utama & Arsitektur Roadmap

Modul ini terbagi menjadi 2 bagian utama: **Core Pillars** (Prinsip Dasar Observability) dan **Observability Tools** (Platform Profesional).

```
+-----------------------------------------------------------------------------------+
|                            LLM OBSERVABILITY ROADMAP                              |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Core Pillars]                                                                   |
|   ├── 01. Tracing & Logging                                                       |
|   │    ├── Step-by-step Trace & Span Hierarchies (Trace -> Span -> Event)          |
|   │    └── Standar metadata OpenInference & OpenTelemetry                         |
|   ├── 02. Cost & Latency Monitoring                                               |
|   │    ├── Token Pricing Engine (Input vs Output rates) & Budget Alerts           |
|   │    └── Profiling Latensi: TTFT (Time-to-First-Token) & TPS (Tokens/Second)    |
|   └── 03. Production Monitoring                                                   |
|        ├── Evaluasi Kualitas LLM-as-a-Judge (Faithfulness & Relevance)             |
|        └── Drift Detection (Embedding/Prompt Drift) & User Feedback Tracking      |
|                                                                                   |
|  [Observability Tools]                                                            |
|   ├── 04. Tools Platform Simulation                                               |
|   │    ├── LangSmith (Run tracing, dataset evals, feedback logging)                |
|   │    ├── Langfuse (Open-source traces, score tracking, prompt management SDK)   |
|   │    ├── Helicone (Proxy gateway, smart caching layer, header cost tracking)   |
|   │    └── Arize AI / Phoenix (Embedding clustering, OpenTelemetry spans, evals)   |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 📁 Struktur Direktori Repository

```
llmobservability/
├── README.md                           # dokumentasi & indeks modul
├── requirements.txt                    # Dependensi Python
├── main.py                             # Master CLI runner untuk lab interaktif
├── notes/                              # Panduan teori & konsep teknis
│   ├── 01_tracing_and_logging.md
│   ├── 02_cost_and_latency_monitoring.md
│   ├── 03_production_monitoring.md
│   └── 04_observability_tools.md
├── 01_tracing_and_logging/
│   ├── 01_span_execution_tracer.py     # Hierarki Trace/Span context manager
│   └── 02_structured_llm_logger.py     # OpenInference JSON log formatter
├── 02_cost_and_latency_monitoring/
│   ├── 01_token_cost_calculator.py     # Token pricing engine & budget alert
│   └── 02_latency_profiler.py          # TTFT, TPS & latency breakdown profiler
├── 03_production_monitoring/
│   ├── 01_evaluators_and_hallucination.py# LLM-as-a-Judge & RAGAS-style scorer
│   └── 02_drift_and_feedback_monitor.py # Embedding drift & CSAT feedback monitor
├── 04_observability_tools/
│   ├── 01_langsmith_simulation.py      # Simulasi LangSmith SDK
│   ├── 02_langfuse_simulation.py       # Simulasi Langfuse SDK
│   ├── 03_helicone_simulation.py       # Simulasi Helicone Proxy Gateway
│   └── 04_arize_phoenix_simulation.py  # Simulasi Arize AI & Phoenix
└── web_visualizer/                      # Web GUI Dashboard (FastAPI + JS)
    ├── index.html                      # Interactive dark-mode dashboard
    ├── styles.css                      # Modern dark theme styles
    ├── app.js                          # Dynamic UI & live simulator logic
    └── server.py                       # HTTP Server backend
```

---

## 🚀 Cara Menggunakan

### 1. Install Dependensi
```bash
pip install -r requirements.txt
```

### 2. Menjalankan Interactive CLI Runner
```bash
python main.py
```

### 3. Menjalankan Web Visualizer Dashboard
```bash
python web_visualizer/server.py
```
Lalu buka browser Anda di `http://localhost:8000`.
