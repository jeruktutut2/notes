# AGENT LOOP ARCHITECTURE & EXAMPLE USECASES - AI AGENTS LEARNING WORKSPACE

Proyek pembelajaran **Agent Loop** untuk AI Agents berdasarkan roadmap resmi di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan diagram arsitektur siklus agent.

Proyek ini mencakup simulasi murni (*self-contained*) dari **4 Pilar Utama Agent Loop**:
1. **Perception / User Input**
2. **Reason and Plan**
3. **Acting / Tool Invocation**
4. **Observation & Reflection**

Serta **5 Example Usecases** nyata yang saling terhubung:
- Personal Assistant
- Code Generation
- Data Analysis
- Web Scraping / Crawling
- NPC / Game AI

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python 3.9+ (`math`, `json`, `re`, `dataclasses`, `time`, `typing`, `random`, `subprocess`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

```bash
# Pindah ke direktori agentloop
cd /Users/bsa/Documents/por/aiagents/agentloop

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
| **01** | **Perception / User Input** | • User Input Parsing & Intent Extraction<br>• Input Sanitization, Prompt Injection & Guardrails | [`01_perception_user_input/`](file:///Users/bsa/Documents/por/aiagents/agentloop/01_perception_user_input/) |
| **02** | **Reason and Plan** | • ReAct Framework (Thought-Action-Obs) & CoT<br>• Task Decomposition & DAG Planning | [`02_reason_and_plan/`](file:///Users/bsa/Documents/por/aiagents/agentloop/02_reason_and_plan/) |
| **03** | **Acting / Tool Invocation** | • JSON Schema Tool Registry & Function Calling<br>• Resilient Action Execution, Retries & Fallbacks | [`03_acting_tool_invocation/`](file:///Users/bsa/Documents/por/aiagents/agentloop/03_acting_tool_invocation/) |
| **04** | **Observation & Reflection** | • Observation Processing & Working Memory (Sliding Window)<br>• Reflection, Self-Correction & Termination Criteria | [`04_observation_reflection/`](file:///Users/bsa/Documents/por/aiagents/agentloop/04_observation_reflection/) |
| **05** | **Agent Loop Architecture Engine** | • End-to-End Autonomous Agent Loop Engine | [`05_agent_loop_architecture/`](file:///Users/bsa/Documents/por/aiagents/agentloop/05_agent_loop_architecture/) |
| **06** | **Example Usecases (Sesuai Diagram)** | • Personal Assistant (Calendar & Agenda Manager)<br>• Code Generation Agent (Write, Test & Auto-Debug Loop)<br>• Data Analysis Agent (Tabular Aggregation & Insights)<br>• Web Scraping / Crawling Agent (URL & Link Extraction)<br>• NPC / Game AI Agent (World Perception & Tactics) | [`06_example_usecases/`](file:///Users/bsa/Documents/por/aiagents/agentloop/06_example_usecases/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari teori ReAct, alur kerja sequence, pencegahan infinite loop, hingga analisis 5 Usecase) dapat dibaca di folder:
👉 [notes/agent_loop_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/agentloop/notes/agent_loop_roadmap_notes.md)
