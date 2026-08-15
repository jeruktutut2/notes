# 05. Building AI Agents (Pendekatan & Framework)

Sesuai dengan roadmap [roadmap.sh/ai-engineer](https://roadmap.sh/ai-engineer), terdapat beberapa pendekatan dan SDK utama yang digunakan oleh industri saat ini untuk membangun AI Agent:

```
+-----------------------------------------------------------------------+
|                         BUILDING AI AGENTS                            |
+-----------------------------------------------------------------------+
|  1. Manual Implementation (Pure Code / Zero-Framework Loop)           |
|  2. OpenAI AgentKit & Agent SDK (Assistant API & Swarm Patterns)      |
|  3. Claude Agent SDK (Anthropic Tool Use & Agentic Loop)              |
|  4. Vertex AI Agent Builder (Google Cloud Enterprise Grounding)       |
|  5. Google ADK (Agent Development Kit & Gemini Multi-Tool)            |
+-----------------------------------------------------------------------+
```

---

## 1. Manual Implementation (Pengembangan Mandiri Tanpa Framework)

### Konsep:
Membangun loop agen secara langsung menggunakan bahasa pemograman (Python/TypeScript) dan HTTP Client / SDK dasar dari LLM Provider.

### Komponen Utama:
- **State Machine**: Dictionary/Object untuk menyimpan riwayat percakapan (`messages = []`).
- **While Loop**: `while iteration < max_iterations:` untuk menjaga siklus ReAct.
- **Function Dispatcher**: Pemetaan nama tool (`string`) ke fungsi Python lokal (`Callable`).

### Keuntungan & Kerugian:
- **(+) Kontrol Penuh**: Tanpa abstraksi tersembunyi (*magic black box*), mudah didebug dan disesuaikan.
- **(+) Ringan**: Tanpa dependency berat.
- **(-) Boilderplate Code**: Harus menulis sendiri penanganan retries, memory pruning, dan parsing error.

---

## 2. OpenAI AgentKit & Agent SDK (OpenAI Swarm & Assistant API)

### Konsep:
OpenAI menyediakan ekosistem untuk agentic workflows:
1. **OpenAI Agents SDK / Swarm Pattern**: Kerangka kerja berbobot ringan (*lightweight*) yang berfokus pada dua abstraksi utama: `Agent` dan `Handoff`.
2. **Assistants API**: Managed agent service dengan built-in Code Interpreter, File Search (RAG), dan Persistent Threads.

### Contoh Karakteristik (OpenAI Agents SDK):
- Menggunakan `Agent(name="...", instructions="...", tools=[...])`.
- Handoff dilakukan dengan mengembalikan instansi `Agent` lain dari dalam sebuah tool.

---

## 3. Claude Agent SDK (Anthropic Tool Use & Agentic Loop)

### Konsep:
Anthropic menyediakan mekanisme Tool Use yang sangat presisi pada model Claude 3.5 Sonnet / Claude 3 Opus.

### Fitur Kunci:
- **`tool_use` & `tool_result` content blocks**: Anthropic memisahkan jawaban teks biasa dan perintah eksekusi tool secara eksplisit di tingkat API.
- **Computer Use**: Kemampuan agen Claude untuk mengendalikan mouse, keyboard, dan melihat screenshot layar desktop secara otomatis.
- **Strict Structured Outputs**: Menjamin argumen fungsi sesuai skema JSON tanpa halusinasi.

---

## 4. Vertex AI Agent Builder (Google Cloud Enterprise)

### Konsep:
Platform managed (*no-code / low-code / SDK*) dari Google Cloud untuk membuat agen AI skala enterprise yang siap pakai.

### Komponen Utama:
- **Data Stores**: Integrasi otomatis RAG dengan Google Search, BigQuery, Google Drive, dan Unstructured Data.
- **Extensions**: Menghubungkan agent ke API enterprise (Salesforce, ServiceNow, Custom REST APIs).
- **Grounding & Citation**: Verifikasi jawaban agen berdasarkan dokumen internal untuk mencegah halusinasi.

---

## 5. Google ADK (Agent Development Kit) & Gemini Multi-Tool

### Konsep:
Google ADK (Agent Development Kit) adalah toolkit dan pola arsitektur resmi dari Google untuk membangun agen AI multimodal dengan model Gemini.

### Fitur Utama:
- **Native Multimodal Agents**: Menerima input teks, gambar, video, dan audio secara simultan dalam siklus ReAct.
- **Code Execution Sandbox**: Kemampuan agen Gemini menjalankan kode Python di lingkungan terisolasi untuk analisis data instan.
- **Structured Function Declarations**: Integrasi ketat dengan OpenAPI Spec / Protocol Buffers.

---

## Ringkasan Perbandingan Framework Agent

| Framework / Pendekatan | Tingkat Kontrol | Kurva Pembelajaran | Best Use Case |
| :--- | :--- | :--- | :--- |
| **Manual Implementation** | Maximum (100%) | Sedang | Custom Enterprise Agents & Production Microservices |
| **OpenAI AgentKit / SDK** | Tinggi | Mudah | Rapid Multi-agent Prototyping (Swarm architecture) |
| **Claude Agent SDK** | Tinggi | Mudah | Complex Reasoning, Coding Agents, Computer Use |
| **Vertex AI Agent Builder**| Rendah-Sedang | Sangat Mudah | Enterprise Internal Search, HR/Policy Bots |
| **Google ADK (Gemini)** | Tinggi | Sedang | Native Multimodal Agents (Audio/Video + Tools) |
