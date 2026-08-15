# 🤖 AI Agents Learning Workspace (roadmap.sh AI Engineer)

Modul pembelajaran komprehensif, praktis, dan interaktif untuk topik **AI Agents** sesuai dengan panduan kurikulum [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer) dan arsitektur visual resmi:

```
+-----------------------------------------------------------------------+
|                              AI AGENTS                                |
+-----------------------------------------------------------------------+
|  1. Agents Usecases                                                   |
|  2. ReAct Prompting                                                   |
|  3. Tools & Function Calling                                          |
|  4. Multi-agents                                                      |
|  5. Building AI Agents                                                |
|     ├── Manual Implementation                                         |
|     ├── OpenAI AgentKit & Agent SDK                                   |
|     ├── Claude Agent SDK                                              |
|     ├── Vertex AI Agent Builder                                       |
|     └── Google ADK                                                    |
+-----------------------------------------------------------------------+
```

---

## 🗂️ Struktur Direktori Project

```
/Users/bsa/Documents/por/aiengineering/aiagents/
├── README.md                           # Dokumentasi & Panduan Utama
├── requirements.txt                    # Dependensi Python
├── main.py                             # Interactive CLI Runner
├── notes/                              # Catatan Konseptual Mendalam (Markdown)
│   ├── 01_agents_usecases.md
│   ├── 02_react_prompting.md
│   ├── 03_tools_and_function_calling.md
│   ├── 04_multi_agents.md
│   └── 05_building_ai_agents.md
├── 01_agents_usecases/
│   └── demo_usecases.py                # Script Demo Usecases Agent
├── 02_react_prompting/
│   └── react_engine.py                 # Engine ReAct Reasoning Loop
├── 03_tools_and_function_calling/
│   └── tool_calling_demo.py            # Schema JSON & Function Dispatcher
├── 04_multi_agents/
│   └── multi_agent_orchestrator.py     # Topologi Multi-Agent Systems
├── 05_building_ai_agents/
│   ├── 01_manual_implementation.py     # Pure Python Zero-Framework Agent
│   ├── 02_openai_agent_sdk.py          # OpenAI Agents SDK & Swarm Handoff
│   ├── 03_claude_agent_sdk.py          # Claude Agent SDK & Tool Use API
│   ├── 04_vertex_ai_agent_builder.py   # Vertex AI Enterprise Grounding
│   └── 05_google_adk.py                # Google Agent Dev Kit & Gemini
└── web_visualizer/                     # Interactive Glassmorphism Web App
    ├── index.html
    ├── styles.css
    └── app.js
```

---

## 🚀 Cara Menjalankan Project

### 1. Jalankan Script CLI Runner Interaktif (Python)

Di dalam terminal workspace:
```bash
python main.py
```
Anda dapat memilih modul mana saja (1 - 9) untuk dijalankan secara langsung dengan output visual terformat rapi dari pustaka `rich`.

### 2. Jalankan Script Spesifik Secara Mandiri

```bash
python 01_agents_usecases/demo_usecases.py
python 02_react_prompting/react_engine.py
python 03_tools_and_function_calling/tool_calling_demo.py
python 04_multi_agents/multi_agent_orchestrator.py
python 05_building_ai_agents/01_manual_implementation.py
```

### 3. Buka Interactive Web Visualizer

Buka file [web_visualizer/index.html](file:///Users/bsa/Documents/por/aiengineering/aiagents/web_visualizer/index.html) di browser Anda untuk menikmati simulasi ReAct interaktif step-by-step, peta topologi Multi-Agent, Tool Call Inspector, dan Matrix Perbandingan Frameworks.

---

## 📚 Ringkasan Topik Pembelajaran

1. **Agents Usecases**: Memahami penggunaan agentic automation di Support Desk, Coding Assistants, Enterprise Workflows, dan Decision Support.
2. **ReAct Prompting**: Memahami siklus Thought -> Action -> Observation -> Final Answer untuk pemecahan masalah bertahap.
3. **Tools & Function Calling**: Membuat JSON Schema, validasi tipe data Pydantic, serta mekanisme dispatcher & context injection.
4. **Multi-agents**: Menguasai arsitektur Orchestrator-Worker, Sequential Pipeline, dan Router Agent.
5. **Building AI Agents**: Membandingkan pendekatan Manual (Pure Python), OpenAI AgentKit/SDK, Claude Agent SDK, Vertex AI Agent Builder, dan Google ADK.
