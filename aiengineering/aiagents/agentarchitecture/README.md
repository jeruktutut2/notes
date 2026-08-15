# AGENT ARCHITECTURE - AI AGENTS WORKSPACE

Proyek pembelajaran **Agent Architecture** untuk AI Agents berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan diagram visual komponen arsitektur AI Agent (Common Architectures, Building Agents, Building Using Frameworks, serta Evaluation & Monitoring).

Proyek ini mencakup simulasi murni (*self-contained*) dari 4 pilar utama arsitektur Agent:
- **Common Architectures**:
  - **RAG Agent**: Retrieval-Augmented Generation dengan Cosine Similarity Search & Prompt Context Injection.
  - **ReAct Agent**: Loop penalaran dan eksekusi bergantian (*Thought -> Action -> Observation*).
  - **Planner-Executor**: Pemisahan tahap perencanaan dan eksekusi berurutan dengan *Dynamic Replanning*.
  - **DAG Agents**: Eksekusi paralel berbasis Graf Terarah Tanpa Siklus (*Directed Acyclic Graph*).
  - **Multi-Agents**: Kolaborasi agent terhierarki (*Manager, Researcher, Coder, QA Reviewer*).
  - **Self-Critique Agents**: Loop refleksi dan perbaikan mandiri berulang (*Iterative Refinement*).
- **Building Agents**:
  - **Manual (From Scratch)**: Panggilan API tingkat rendah, Agent Loop murni, Parsing JSON/RegEx, dan Exponential Backoff + Jitter.
  - **LLM Native Function Calling**: Skema integrasi bawaan OpenAI, Gemini, Anthropic, dan pattern OpenAI Assistant API.
- **Building Using Frameworks**:
  - Tinjauan ekosistem framework utama: LangChain, LangGraph, Haystack, LlamaIndex, CrewAI, AutoGen, Smolagents (Smol Depot), dan Agno.
- **Evaluation, Testing, Debugging & Monitoring**:
  - **Evaluation & Testing**: Metrik kuantitatif (*Completion Rate, Tool Accuracy, Faithfulness*), Tool Unit Testing, Integration Trajectory Flow, dan *Human-in-the-Loop* (HITL).
  - **Debugging & Monitoring**: *Structured Logging*, OpenTelemetry Spans, serta format muatan (*telemetry payloads*) untuk LangSmith, Helicone, LangFuse, dan OpenLLMetry.

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`json`, `re`, `math`, `time`, `uuid`, `collections`, `subprocess`, `dataclasses`, `typing`) sehingga dapat langsung dijalankan tanpa memerlukan API Key eksternal atau dependensi tambahan.

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
| **01** | **Common Architectures** | • RAG Agent & ReAct (Reason + Act) Loop<br>• Planner-Executor & DAG Engine<br>• Multi-Agent Systems & Self-Critique | [`01_common_architectures/`](file:///Users/bsa/Documents/por/aiagents/agentarchitecture/01_common_architectures/) |
| **02** | **Building Agents** | • Manual Agent Construction (From Scratch)<br>• LLM Native Function Calling (OpenAI, Gemini, Anthropic, Assistant API) | [`02_building_agents/`](file:///Users/bsa/Documents/por/aiagents/agentarchitecture/02_building_agents/) |
| **03** | **Building Using Frameworks** | • Overview Ekosistem Frameworks (LangChain, LangGraph, Haystack, LlamaIndex, CrewAI, AutoGen, Smolagents, Agno) | [`03_building_using_frameworks/`](file:///Users/bsa/Documents/por/aiagents/agentarchitecture/03_building_using_frameworks/) |
| **04** | **Evaluation & Monitoring** | • Metrik Evaluasi, Tool Unit Testing, Integration Flows & HITL<br>• Structured Logging, Tracing & Observability Tools (LangSmith, LangFuse, Helicone, OpenLLMetry) | [`04_eval_testing_debugging_monitoring/`](file:///Users/bsa/Documents/por/aiagents/agentarchitecture/04_eval_testing_debugging_monitoring/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari ReAct loop formulation, topological DAG sort, perbandingan framework, metrik evaluasi kuantitatif, hingga OpenTelemetry tracing) dapat dibaca di folder:
👉 [notes/agent_architecture_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/agentarchitecture/notes/agent_architecture_roadmap_notes.md)
