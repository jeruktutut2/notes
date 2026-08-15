# 04. Multi-Agents System (Sistem Multi-Agent)

Saat sebuah tugas menjadi terlalu kompleks untuk ditangani oleh satu agen tunggal (karena bloat context window, kebingungan instruksi, atau keahlian yang sangat spesifik), kita menggunakan **Sistem Multi-Agent (Multi-Agent Systems)**.

Dalam Multi-Agent System, beberapa agen khusus (*Specialized Agents*) bekerja sama, berkomunikasi, dan saling mentransfer tugas (*handoff*) untuk menyelesaikan goal akhir.

---

## 1. Mengapa Multi-Agent?

- **Specialization (Spesialisasi)**: Setiap agent memiliki system prompt, tools, dan panduan yang fokus pada satu domain saja (contoh: Researcher, Coder, Critic/Reviewer).
- **Context Isolation (Isolasi Konteks)**: Agen pembantu tidak perlu mengetahui seluruh percakapan awal, hanya data spesifik yang dibutuhkannya. Ini menghemat token dan menjaga performaLLM.
- **Modularity & Scalability**: Komponen agent mudah ditambah, diuji, dan diperbaiki secara terpisah.

---

## 2. Pola Arsitektur Multi-Agent (Topologi)

### A. Hierarchical Pattern (Orchestrator - Worker)
Satu **Manager / Orchestrator Agent** menerima tugas utama dari pengguna, memecahnya menjadi beberapa sub-task, menugaskan **Worker Agents**, dan mensintesis hasil akhirnya.

```
                  +-----------------------+
                  |  ORCHESTRATOR AGENT   |
                  +-----------------------+
                     /        |        \
                    /         |         \
                   v          v          v
            +----------+ +----------+ +----------+
            | Worker A | | Worker B | | Worker C |
            |(Research)| | (Coder)  | | (Review) |
            +----------+ +----------+ +----------+
```

### B. Sequential Pipeline (Chain / Assembly Line)
Tugas mengalir secara linier dari Agen 1 ke Agen 2 ke Agen 3, di mana output Agen N menjadi input bagi Agen N+1.

```
+------------+     +------------+     +------------+     +------------+
| Agent A    | --> | Agent B    | --> | Agent C    | --> | Final      |
| (Planner)  |     | (Writer)   |     | (Editor)   |     | Output     |
+------------+     +------------+     +------------+     +------------+
```

### C. Router / Dispatcher Pattern
Satu **Router Agent** menganalisis niat pengguna (*intent classification*) dan mengarahkan pengguna ke agen spesialis yang tepat (misal: Billing Agent vs Technical Support Agent).

```
                            +---------------+
                            | ROUTER AGENT  |
                            +---------------+
                             /             \
                            /               \
                           v                 v
                 +-------------------+  +-------------------+
                 | Billing Agent     |  | Tech Support Agent|
                 +-------------------+  +-------------------+
```

### D. Peer-to-Peer / Collaborative (Debate / Consensus)
Dua agen atau lebih berdiskusi, memberikan penilaian (*critique*), atau berdebat sampai mencapai konsensus akhir (misal: Generator Agent vs Critic Agent).

---

## 3. Mekanisme Agent Handoff & State Sharing

Ada dua metode umum untuk mengomunikasikan antar agent:

1. **Explicit Function Handoff (Swarm / AgentKit Pattern)**:
   Agent memanggil tool spesifik (contoh: `transfer_to_support_agent()`) yang mengembalikan instansiasi agen baru beserta konteks percakapan yang diteruskan.
2. **Shared State Store (LangGraph / CrewAI Pattern)**:
   Sebuah *Global State Object* (misal: dictionary atau database) dibaca dan diperbarui oleh agen-agen yang terlibat secara bergantian.
