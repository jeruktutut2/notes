# CATATAN TEORI LENGKAP: AGENT ARCHITECTURE UNTUK AI AGENTS

Dokumentasi teori komprehensif **Agent Architecture** berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan diagram visual komponen arsitektur AI Agent.

---

## DAFTAR ISI
1. [Pengantar Arsitektur AI Agent](#1-pengantar-arsitektur-ai-agent)
2. [Common Architectures (Pola Arsitektur Utama)](#2-common-architectures-pola-arsitektur-utama)
   - [2.1 RAG Agent (Retrieval-Augmented Generation)](#21-rag-agent-retrieval-augmented-generation)
   - [2.2 ReAct (Reason + Act) Agent](#22-react-reason--act-agent)
   - [2.3 Planner-Executor Agent](#23-planner-executor-agent)
   - [2.4 DAG Agents (Directed Acyclic Graph)](#24-dag-agents-directed-acyclic-graph)
   - [2.5 Multi-Agent Systems](#25-multi-agent-systems)
   - [2.6 Self-Critique / Reflection Agents](#26-self-critique--reflection-agents)
3. [Building Agents (Membangun Agent)](#3-building-agents-membangun-agent)
   - [3.1 Manual (From Scratch)](#31-manual-from-scratch)
   - [3.2 LLM Native Function Calling](#32-llm-native-function-calling)
4. [Building Using Frameworks (Kerangka Kerja Ekosistem)](#4-building-using-frameworks-kerangka-kerja-ekosistem)
   - [4.1 LangChain & LangGraph](#41-langchain--langgraph)
   - [4.2 Haystack & LlamaIndex](#42-haystack--llamaindex)
   - [4.3 CrewAI & AutoGen](#43-crewai--autogen)
   - [4.4 Smolagents (Smol Depot) & Agno](#44-smolagents-smol-depot--agno)
5. [Evaluation & Testing (Evaluasi dan Pengujian)](#5-evaluation--testing-evaluasi-dan-pengujian)
   - [5.1 Metrik Evaluasi Agent](#51-metrik-evaluasi-agent)
   - [5.2 Testing Strategy (Unit, Integration, HITL)](#52-testing-strategy-unit-integration-hitl)
   - [5.3 Framework Evaluasi (LangSmith, DeepEval, Ragas)](#53-framework-evaluasi-langsmith-deepeval-ragas)
6. [Debugging & Monitoring (Debug dan Observabilitas)](#6-debugging--monitoring-debug-dan-observabilitas)
   - [6.1 Structured Logging & Tracing](#61-structured-logging--tracing)
   - [6.2 Observability Tools (LangSmith, Helicone, LangFuse, OpenLLMetry)](#62-observability-tools-langsmith-helicone-langfuse-openllmetry)

---

## 1. Pengantar Arsitektur AI Agent

Arsitektur AI Agent menentukan bagaimana sebuah **Large Language Model (LLM)** berinteraksi dengan lingkungan (*environment*), mengeksekusi alat (*tools*), menyimpan konteks memori (*memory*), serta merencanakan langkah (*planning*) untuk menyelesaikan tugas kompleks secara otonom.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                           AI AGENT ARCHITECTURE                           │
│                                                                           │
│  ┌───────────────┐        ┌──────────────────┐       ┌─────────────────┐  │
│  │   PERCEPTION  │ ───►   │  REASON & PLAN   │ ───►  │     ACTION      │  │
│  │ User / Sensors│        │ LLM Core Brain   │       │ Tools / APIs    │  │
│  └───────────────┘        └──────────────────┘       └─────────────────┘  │
│          ▲                         │                          │           │
│          │                         ▼                          │           │
│          │                ┌──────────────────┐                │           │
│          └─────────────── │    OBSERVATION   │ ◄──────────────┘           │
│                           │ Feedback / Memory│                            │
│                           └──────────────────┘                            │
└───────────────────────────────────────────────────────────────────────────┘
```

Perbedaan utama antara LLM standar dan AI Agent terletak pada **Loop Otonom** dan kemampuan eksekusi tindakan (*tool invocation*).

---

## 2. Common Architectures (Pola Arsitektur Utama)

### 2.1 RAG Agent (Retrieval-Augmented Generation)

RAG Agent menggabungkan kemampuan pencarian basis pengetahuan eksternal (*Vector Database* / *Hybrid Search*) dengan penalaran LLM untuk menjawab pertanyaan berdasarkan konteks tepercaya tanpa perlu melakukan retraining.

```
User Query ──► [ Embedding Model ] ──► Vector DB Search ──► Top-K Context
                                                                │
User Query + Top-K Context ──────────────► [ LLM Generator ] ──► Final Response
```

- **Elemen Utama**: Document Chunking, Embedding Model (misal: Text-Embedding-3), Vector Database (Pinecone, ChromaDB, Qdrant), Dynamic Context Injection.
- **Kasus Penggunaan**: Q&A Dokumen Internal Enterprise, Knowledge Base Customer Support.

### 2.2 ReAct (Reason + Act) Agent

Diusulkan oleh Yao et al. (2022), ReAct secara bergantian melakukan penalaran eksplisit (*Thought*), eksekusi tindakan (*Action*), dan pengamatan hasil (*Observation*).

```
Loop ReAct:
  THOUGHT     : LLM menganalisis state saat ini dan menentukan langkah selanjutnya.
  ACTION      : LLM memilih fungsi/alat beserta argumen JSON.
  OBSERVATION : Hasil eksekusi alat dikembalikan ke context window LLM.
```

- **Formulasi Formal Iterasi**:
  $$S_t = (T_1, A_1, O_1, T_2, A_2, O_2, \dots, T_t)$$
  $$A_t \sim P_{\text{LLM}}(A_t \mid S_t)$$
- **Kelebihan**: Transparansi penalaran tinggi, meminimalkan ilusi (*hallucination*) dengan memverifikasi data via aksi.

### 2.3 Planner-Executor Agent

Memisahkan tahap **Perencanaan (*Planning*)** dari tahap **Eksekusi (*Execution*)**.

```
User Task ──► [ Planner Agent ] ──► Plan Steps [Step 1, Step 2, Step 3]
                                          │
                                          ▼
                               [ Execution Engine / Worker ]
                                          │ (Execute Step by Step)
                                          ▼
                               [ Replanner / Evaluator ] ──► (Update Plan jika ada error)
```

- **Modus Kerja**:
  1. **Static Planning**: Membuat daftar langkah di awal dan mengeksekusi secara linier.
  2. **Dynamic Replanning**: Setelah tiap langkah dieksekusi, Planner menilai apakah rencana perlu disesuaikan berdasarkan `Observation`.

### 2.4 DAG Agents (Directed Acyclic Graph)

Pengorganisasian alur kerja agent dalam bentuk **Graf Terarah Tanpa Siklus (DAG)**. Setiap node merepresentasikan tugas/agent, dan edge merepresentasikan dependensi data.

```
        ┌──────────────┐
        │  Fetch Data  │
        └──────┬───────┘
               │
       ┌───────┴───────┐
       ▼               ▼
┌──────────────┐┌──────────────┐
│ Analyze Sentiment│ │ Extract Keywords│
└──────┬───────┘└──────┬───────┘
       │               │
       └───────┬───────┘
               ▼
        ┌──────────────┐
        │ Generate Report│
        └──────────────┘
```

- **Karakteristik**:
  - Node tanpa dependensi silang dapat dieksekusi secara **paralel** ($O(\log N)$ latency).
  - Eksekusi deterministik dan mudah diprediksi dibanding loop ReAct murni.

### 2.5 Multi-Agent Systems

Menggunakan beberapa agent terdesentralisasi atau terhierarki yang saling berkomunikasi dan berkolaborasi untuk menyelesaikan masalah kompleks.

| Topologi | Deskripsi | Kasus Penggunaan |
| :--- | :--- | :--- |
| **Hierarchical (Manager-Worker)** | Manager Agent membagi tugas dan mengawasi Worker Agents. | Enterprise Workflow, Software Engineering Teams |
| **Sequential (Pipeline)** | Output Agent A menjadi input Agent B. | Content Generation & Editing |
| **Swarm / Peer-to-Peer** | Agent-agent sejajar berkomunikasi via message bus/board. | Market Simulation, Negotiation |

### 2.6 Self-Critique / Reflection Agents

Agent yang dilengkapi dengan loop evaluasi internal untuk menguji, mengkritik, dan memperbaiki outputnya sendiri secara berulang (*Iterative Self-Refinement*).

```
Initial Prompt ──► [ Generator ] ──► Draft Output
                                          │
                                          ▼
                                   [ Evaluator / Critic ]
                                          │
                        Is Output Valid? ─┼──► YES ──► Final Result
                                          │
                                          NO (Critique Feedback)
                                          │
                                          ▼
                                   [ Refinement Step ]
```

- **Metode Pendukung**: Reflexion (Shinn et al.), Self-Discover, Chain-of-Verification (CoVe).

---

## 3. Building Agents (Membangun Agent)

### 3.1 Manual (From Scratch)

Membangun agent tanpa framework eksternal untuk pemahaman tingkat rendah (*low-level control*).

- **Komponen Kunci**:
  1. **Direct LLM API Calls**: Mengirim payload HTTP POST ke API endpoint (e.g., OpenAI REST API `/v1/chat/completions`).
  2. **Implementing Agent Loop**: Loop `while` dengan pembatas `max_iterations`, guardrails token, dan kondisi henti.
  3. **Parsing Model Output**: Ekstraksi struktur JSON/XML dari teks respons LLM menggunakan RegEx atau parser aman.
  4. **Error & Rate-Limit Handling**: Mekanisme Exponential Backoff dengan Jitter, fallback model, serta truncation prompt otomatis ketika batas konteks terlampaui.

Formula Exponential Backoff dengan Jitter:
$$t_{\text{wait}} = \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{retry}}) + \text{uniform}(0, \text{jitter})$$

### 3.2 LLM Native Function Calling

Integrasi alat bawaan tingkat protokol (*API-level tool calling*) yang didukung langsung oleh penyedia LLM.

- **OpenAI Function Calling**: Menyuplai skema `tools` berbasis JSON Schema (`type: "function"`). Model mengembalikan `tool_calls` terstruktur alih-alih teks biasa.
- **OpenAI Assistant API**: Layanan stateful bawaan yang mengelola `Threads`, `Runs`, `Messages`, serta built-in tools (Code Interpreter, Vector Search).
- **Gemini Function Calling**: Menggunakan `function_declarations` pada payload SDK Google GenAI.
- **Anthropic Tool Use**: Menggunakan skema `input_schema` pada Anthropic Messages API.

---

## 4. Building Using Frameworks (Kerangka Kerja Ekosistem)

```
┌───────────────────────────────────────────────────────────────────────────┐
│                         AGENT FRAMEWORKS ECOSYSTEM                        │
├──────────────────┬───────────────────┬──────────────────┬─────────────────┤
│    LANGCHAIN     │     LANGGRAPH     │     HAYSTACK     │   LLAMAINDEX    │
│  (LCEL / Chains) │ (Stateful Graph)  │(NLP Pipelines)   │(Data-Centric RAG│
├──────────────────┼───────────────────┼──────────────────┼─────────────────┤
│     CREWAI       │      AUTOGEN      │   SMOLAGENTS     │      AGNO       │
│  (Role Crews)    │ (Microsoft P2P)   │(Code as Action)  │(Fast Pydantic)  │
└──────────────────┴───────────────────┴──────────────────┴─────────────────┘
```

### 4.1 LangChain & LangGraph
- **LangChain**: Perintis ekosistem agent. Menyediakan komponen modular (PromptTemplates, OutputParsers, Memory, Tools). Menggunakan LangChain Expression Language (LCEL).
- **LangGraph**: Framework berbasis graph state machine. Mengatasi keterbatasan linier LangChain dengan mendukung siklus (*cycles*), cabang kondisi (*conditional branches*), persisten state, dan persetujuan manusia (*Human-in-the-loop breakpoints*).

### 4.2 Haystack & LlamaIndex
- **Haystack**: Framework buatan Deepset untuk membangun pipeline NLP & RAG skala produksi berbasis komponen modular.
- **LlamaIndex**: Framework berorientasi data (*data-centric*). Menyediakan abstraksi indexing data heterogen (SQL, PDF, Unstructured) dan Agentic RAG dengan router & query engine.

### 4.3 CrewAI & AutoGen
- **CrewAI**: Framework berbasis peran (*role-playing agents*). Pengembang mendefinisikan Agent (Role, Goal, Backstory), Task, dan Crew (Sequential/Hierarchical process).
- **AutoGen**: Framework buatan Microsoft untuk sistem multi-agent yang berkomunikasi secara percakapan (*ConversableAgent*), mendukung koordinasi otomatis via GroupChatManager.

### 4.4 Smolagents (Smol Depot) & Agno
- **Smolagents (HuggingFace)**: Framework ultra-ringan yang mengeksekusi tindakan dalam bentuk **Kode Python murni** (*Code Agents*) alih-alih JSON Tool Calling.
- **Agno (sebelumnya Phidata)**: Framework cepat dan efisien berbasis Pydantic untuk agent berkinerja tinggi dengan overhead minimal.

---

## 5. Evaluation & Testing (Evaluasi dan Pengujian)

### 5.1 Metrik Evaluasi Agent

Metrik kuantitatif untuk mengukur kualitas dan keandalan agent:

1. **Tool Call Accuracy ($A_{\text{tool}}$)**:
   $$A_{\text{tool}} = \frac{\text{Jumlah Alat & Argumen Benar}}{\text{Total Tool Invocations}}$$
2. **Task Completion Rate ($CR$)**: Persentase skenario di mana agent mencapai goal akhir tanpa error.
3. **Step Efficiency Index**: Rata-rata jumlah langkah iterasi yang dibutuhkan versus jalur optimal.
4. **Hallucination Score & Faithfulness**: Tingkat kesesuaian jawaban terhadap grounding context.

### 5.2 Testing Strategy (Unit, Integration, HITL)

```
               ┌─────────────────────────────┐
               │    Human-in-the-Loop (HITL)  │  ◄── User Feedback & Approval
               ├─────────────────────────────┤
               │   Integration Test (Flows)  │  ◄── End-to-End Trajectories
               ├─────────────────────────────┤
               │   Unit Test (Tools & APIs)  │  ◄── Deterministic Tool Inputs
               └─────────────────────────────┘
```

- **Unit Testing for Individual Tools**: Pengujian terisolasi fungsi alat menggunakan mock data dan JSON schema validation.
- **Integration Testing for Flows**: Pengujian alur percakapan/rekam jejak (*trajectories*) lengkap dari perception hingga final answer.
- **Human-in-the-Loop (HITL) Evaluation**: Gerbang persetujuan manusia untuk tindakan berisiko tinggi (misal: transaksi keuangan, hapus data) serta feedback RLAIF.

### 5.3 Framework Evaluasi (LangSmith, DeepEval, Ragas)
- **LangSmith**: Platform pengujian & dataset buatan LangChain untuk melacak eksekusi prompt dan evaluasi otomatis.
- **DeepEval**: Framework open-source unit testing berbasis Pytest untuk LLM & Agent.
- **Ragas**: Framework khusus untuk mengukur performa RAG (Faithfulness, Answer Relevancy, Context Precision/Recall).

---

## 6. Debugging & Monitoring (Debug dan Observabilitas)

### 6.1 Structured Logging & Tracing

Merekam setiap langkah iterasi agent ke dalam format terstruktur (JSON / OpenTelemetry Spans) yang mencakup:
- `trace_id` & `span_id`
- Input Prompt & System Instructions
- Tool Call Payload & Execution Output
- Usage Metrics (Prompt Tokens, Completion Tokens, Latency ms, Cost USD)

### 6.2 Observability Tools
- **LangSmith**: Visualisasi pohon eksekusi (*call tree*), prompt playground, dan pemantauan latensi latency/token.
- **Helicone**: Proxy observabilitas transparan untuk memantau biaya API LLM, caching, dan rate limiting.
- **LangFuse**: Platform observabilitas open-source berbasis web dengan tracing mendalam untuk LLM dan Agent.
- **OpenLLMetry**: Standardisasi telemetry untuk LLM berdasarkan spesifikasi **OpenTelemetry**.

---
*Catatan disesuaikan dengan roadmap.sh/ai-agents & arsitektur visual Agent Architecture.*
