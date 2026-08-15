# AGENT MEMORY - AI AGENTS WORKSPACE

Proyek pembelajaran **Agent Memory** untuk AI Agents berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents) dan arsitektur komponen memori (Short-Term Memory vs Long-Term Memory, Episodic vs Semantic Memory, serta Maintaining Memory).

Proyek ini mencakup simulasi murni (*self-contained*) dari 3 pilar utama arsitektur Agent Memory:
- **What is Agent Memory?**:
  - **Short Term Memory**: In-prompt working memory, scratchpad CoT, conversation context window, dan sliding window budgeting.
  - **Long Term Memory**: External storage (Vector DB, Persistent SQL Store, Custom JSON Database) melintasi sesi berberbeda.
- **Episodic vs Semantic Memory**:
  - **Episodic Memory**: Log urutan kejadian (*Event Sequence*) & jejak tindakan (*trajectories*) dengan timestamp dan catatan refleksi.
  - **Semantic Memory**: Pengetahuan faktual terstruktur (*Entity-Attribute-Value triples* / *Knowledge Graph*) yang bebas dari konteks waktu.
- **Maintaining Memory**:
  - **RAG & Vector Databases**: Text embedding, perhitungan Cosine Similarity \( \frac{A \cdot B}{\|A\| \|B\|} \), retrieval Top-K, dan dynamic context injection.
  - **User Profile Storage**: Pengelolaan profil & preferensi pengguna terstruktur, ekstraksi fakta otomatis, dan penanganan konflik (*conflict resolution*).
  - **Summarization / Compression**: Summary Buffer Memory, kompresi bertahap (*progressive condensation*), dan metrik efisiensi token.
  - **Forgetting / Aging Strategies**: Kurva peluruhan memori Ebbinghaus \( S(t) = S_0 \cdot e^{-\lambda t} + \alpha \cdot \text{AccessCount} \), importance score, dan *threshold eviction policy*.

---

## 🛠️ Persiapan Environment & Instalasi

Seluruh skrip dibuat mandiri (*self-contained*) menggunakan pustaka standar Python (`sqlite3`, `json`, `math`, `time`, `dataclasses`, `typing`, `re`, `subprocess`) sehingga dapat langsung dijalankan tanpa memerlukan API Key eksternal atau dependensi tambahan.

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
| **01** | **What is Agent Memory?** | • Short-Term Memory (Within Prompt & Context Window)<br>• Long-Term Memory (Persistent SQL / External Storage) | [`01_what_is_agent_memory/`](file:///Users/bsa/Documents/por/aiagents/agentmemory/01_what_is_agent_memory/) |
| **02** | **Episodic vs Semantic Memory** | • Episodic Memory (Event Sequence & Trajectory Logs)<br>• Semantic Memory (Factual Knowledge & Entity Stores) | [`02_episodic_vs_semantic_memory/`](file:///Users/bsa/Documents/por/aiagents/agentmemory/02_episodic_vs_semantic_memory/) |
| **03** | **Maintaining Memory** | • RAG and Vector Databases (Cosine Similarity Search)<br>• User Profile Storage (Structured Preferences)<br>• Summarization / Compression (Summary Buffer Memory)<br>• Forgetting / Aging Strategies (Decay Curve & Eviction) | [`03_maintaining_memory/`](file:///Users/bsa/Documents/por/aiagents/agentmemory/03_maintaining_memory/) |

---

## 📖 Catatan Teori Lengkap

Catatan konsep komprehensif dari setiap topik (mulai dari *Context Window Dynamics*, RAG pipeline, taksonomi Episodic vs Semantic, hingga formula peluruhan memori Ebbinghaus) dapat dibaca di folder:
👉 [notes/agent_memory_roadmap_notes.md](file:///Users/bsa/Documents/por/aiagents/agentmemory/notes/agent_memory_roadmap_notes.md)
