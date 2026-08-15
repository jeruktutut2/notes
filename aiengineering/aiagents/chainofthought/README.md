# CHAIN OF THOUGHT (CoT), TREE OF THOUGHT (ToT) & TOOLS - AI AGENTS WORKSPACE

Proyek pembelajaran **Chain of Thought (CoT), Tree of Thought (ToT), Tool Definition & Examples of Tools** untuk AI Agents berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan arsitektur penalaran terstruktur.

Proyek ini mencakup simulasi murni (*self-contained*) dari pilar utama penalaran agen dan integrasi aksi:
- **Chain of Thought (CoT)**: Zero-shot CoT, Few-shot CoT, Self-Consistency (Majority Voting), dan Thought-Action Tag Parsing.
- **Tree of Thought (ToT)**: Multi-path exploration (BFS vs DFS), State Evaluation, Pruning cabang buruk, dan Backtracking.
- **Tool Definition**: Name & Semantic Description, Input & Output JSON Schema, Error Handling Validation, dan Usage Examples.
- **Examples of Tools**: 6 Pilar contoh tool dasar (Web Search, Code Execution / REPL, Database Queries, API Requests, Email/Slack/SMS Dispatcher, File System Access).

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`sqlite3`, `json`, `re`, `dataclasses`, `time`, `typing`, `math`, `tempfile`) sehingga dapat langsung dijalankan di sistem operasi apapun tanpa memerlukan API Key eksternal atau instalasi pustaka berat.

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
| **01** | **Chain of Thought (CoT)** | • Zero-Shot CoT ("Let's think step by step") vs Few-Shot CoT<br>• Self-Consistency CoT (Majority Voting & Sampling)<br>• Thought Execution & Action Parsing (`<thought>` & `<action>`) | [`01_chain_of_thought/`](file:///Users/bsa/Documents/por/aiagents/chainofthought/01_chain_of_thought/) |
| **02** | **Tree of Thought (ToT)** | • ToT Branching & Search Algorithms (BFS vs DFS)<br>• State Evaluation, Pruning (< threshold) & Backtracking | [`02_tree_of_thought/`](file:///Users/bsa/Documents/por/aiagents/chainofthought/02_tree_of_thought/) |
| **03** | **Tool Definition & Schema** | • Name, Description, Input & Output Schema Standards<br>• Tool Error Handling & Feedback Loop Recovery<br>• Tool Usage Examples & Few-Shot Demonstrations | [`03_tool_definition/`](file:///Users/bsa/Documents/por/aiagents/chainofthought/03_tool_definition/) |
| **04** | **Examples of Tools** | • Web Search & Database Queries (SQL SQLite in-memory)<br>• Code Execution / REPL & File System Sandbox<br>• API Requests & Email / Slack / SMS Dispatcher | [`04_examples_of_tools/`](file:///Users/bsa/Documents/por/aiagents/chainofthought/04_examples_of_tools/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari matematika Self-Consistency hingga arsitektur Tree of Thought, JSON Schema, dan Boundary Security pada Tool Execution) dapat dibaca di folder:
👉 [notes/chain_of_thought_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/chainofthought/notes/chain_of_thought_roadmap_notes.md)
