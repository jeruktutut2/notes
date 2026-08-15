# 🧱 MODUL 04: WAYS OF IMPLEMENTING RAG

Terdapat beberapa pendekatan untuk membangun arsitektur RAG, mulai dari pendekatan tingkat rendah (*low-level SDK*) hingga framework orchestration tingkat tinggi (*agentic framework*).

---

## 🗂️ Matriks Komparasi Pendekatan

| Pendekatan | Fleksibilitas | Kurva Pembelajaran | Overhead Framework | Cocok Untuk |
| :--- | :--- | :--- | :--- | :--- |
| **Using SDKs Directly** | ★★★★★ (Maksimal) | Sedang | Nol | Sistem produksi dengan custom pipeline presisi tinggi |
| **LangChain** | ★★★★☆ | Tinggi | Sedang - Tinggi | Ekosistem serbaguna, integrasi ratusan tools & vector DBs |
| **LlamaIndex** | ★★★★☆ | Sedang | Sedang | Aplikasi RAG berfokus data, indexing dokumen kompleks |
| **Haystack** | ★★★★☆ | Sedang | Rendah - Sedang | Production-ready NLP pipelines & enterprise search |
| **RAGFlow** | ★★★☆☆ | Rendah (UI-centric) | Tinggi | Enterprise Agentic RAG dengan Deep Document Parsing |

---

## 1. ⚙️ Using SDKs Directly
Membangun pipeline RAG secara langsung menggunakan SDK resmi (misal `openai`, `chromadb`, `faiss-cpu`, `numpy`).
- **Keuntungan**: Kontrol penuh atas memori, tanpa ketergantungan abstraksi framework lain, performa optimal.
- **Kekurangan**: Harus menulis sendiri modul chunking, formatting, retry logic, dan metadata filter.

---

## 2. 🦜🔗 LangChain
Framework paling populer untuk menyatukan LLM, Vector Store, dan Tool chains.
- Menyediakan class seperti `RecursiveCharacterTextSplitter`, `VectorStoreRetriever`, `RetrievalQA`.

---

## 3. 🦙 LlamaIndex
Framework khusus berorientasi data yang mengoptimalkan pembuatan indeks dokumen, konektor data (*data connectors*), dan mesin kueri (*query engine*).

---

## 4. 🌾 Haystack (by Deepset)
Framework open-source berfokus produksi yang menggunakan konsep **Pipelines** dan **Nodes** eksplisit untuk membangun arsitektur pencarian semantik & RAG.

---

## 5. 🌊 RAGFlow
Framework Agentic RAG modern open-source yang menonjol pada kemampuan **Deep Document Parsing** (dapat mengekstrak tabel, gambar, layout PDF rumit) dan alur kerja visual agentic RAG.
