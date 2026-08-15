# Catatan Pembelajaran: Proprietary Embedding Models

Dalam lanskap AI Engineering, **Proprietary Embedding Models** adalah model embedding komersial yang disediakan melalui API terkelola oleh vendor SaaS AI (seperti OpenAI, Google Gemini, dan Cohere). 

---

## 🔑 Key Concepts & Value Proposition

Proprietary models menawarkan solusi *zero-infrastructure* di mana developer tidak perlu mengelola server GPU, alokasi memori VRAM, atau skrip pembagian batch (batching).

### Keunggulan Utama:
- **Zero Maintenance**: Tidak memerlukan GPU hosting, PyTorch setup, atau model quantization.
- **High Elasticity**: Dapat menangani jutaan request embedding secara bersamaan dengan SLA vendor.
- **State-of-the-Art Performance**: Sering menjadi model *top-tier* pada leaderboard evaluasi MTEB (Massive Text Embedding Benchmark).
- **Advanced Features**: Mendukung Matryoshka representation (pemotongan dimensi tanpa kehilangan performa signifikan), kompresi int8/binary, serta pengkodean berbasis tipe tugas (Task-Aware Embeddings).

---

## 1. OpenAI Embeddings API

OpenAI menyediakan generasi model embedding v3 yang sangat fleksibel dan efisien.

### Family Model:
1. **`text-embedding-3-small`**:
   - **Default Dimensions**: 1,536
   - **Penggunaan**: Efisien untuk sebagian besar aplikasi semantic search & RAG umum.
   - **Harga**: Sangat terjangkau ($0.02 per 1M tokens).
2. **`text-embedding-3-large`**:
   - **Default Dimensions**: 3,072
   - **Penggunaan**: Aplikasi akurasi tinggi, multilingual kompleks, & pencarian dokumen hukum/medis.
   - **Harga**: $0.13 per 1M tokens.
3. **`text-embedding-ada-002`** (Legacy):
   - **Dimensions**: 1,536 (Fixed).

### Fitur Unggulan: Flexible Dimensions (Matryoshka Embeddings)
Model v3 OpenAI menggunakan teknik **Matryoshka Representation Learning**. Fitur ini memungkinkan developer memotong dimensi vektor (misal dari 1,536 menjadi 512 atau 256) menggunakan parameter `dimensions`:

```python
from openai import OpenAI

client = OpenAI()
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="AI Engineering dan Embedding Vector",
    dimensions=512 # Memotong dimensi dari 1536 ke 512 untuk menghemat penyimpanan Vector DB
)
vector = response.data[0].embedding
print(len(vector)) # 512
```

---

## 2. Gemini Embedding (Google GenAI)

Google Gemini menyediakan model embedding mutakhir yang dirancang khusus untuk memproses tugas-tugas NLP dengan penyesuaian tipe tugas (*Task Types*).

### Family Model:
- **`text-embedding-004`**: Model embedding flagship Google dengan default 768 dimensi (dapat dipotong hingga 256/128).

### Fitur Unggulan: Task-Aware Embeddings
Google Gemini memungkinkan penentuan `task_type` saat mengkodekan teks. Model akan menyesuaikan representasi vektor berdasarkan tujuan akhir penggunaan:

| Task Type | Deskripsi |
| :--- | :--- |
| `RETRIEVAL_DOCUMENT` | Untuk dokumen yang disimpan di Vector DB |
| `RETRIEVAL_QUERY` | Untuk query pencarian user saat melakukan RAG |
| `SEMANTIC_SIMILARITY` | Untuk menghitung jarak kemiripan teks pasangan |
| `CLASSIFICATION` | Untuk klasifikasi teks / pemeta preferensi |
| `CLUSTERING` | Untuk pengelompokan topik dokumen |

```python
from google import genai
from google.genai import types

client = genai.Client()
result = client.models.embed_content(
    model="text-embedding-004",
    contents="Dokumen pengetahuan AI Engineering",
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT",
        title="AI Engineering Guide"
    )
)
print(len(result.embedding.values)) # 768
```

---

## 3. Cohere Embed API

Cohere menawarkan model embedding khusus enterprise yang didesain untuk pencarian multibahasa dan efisiensi memori tingkat tinggi.

### Family Model:
- **`embed-english-v3.0`**: Optimized untuk bahasa Inggris (1,024 dimensi).
- **`embed-multilingual-v3.0`**: Mendukung 100+ bahasa termasuk Bahasa Indonesia (1,024 dimensi).

### Fitur Unggulan: Compression Types (Int8 & Binary Embeddings)
Cohere memelopori fitur kompresi vektor langsung pada API level (`input_type` & `embedding_types`):
- `float32`: Presisi penuh (4 byte per float).
- `int8`: Mengurangi konsumsi penyimpanan Vector DB hingga **75%**.
- `ubyte` / `binary`: Mengurangi penyimpanan hingga **96%** dengan pencarian Hamming distance yang ultra-cepat.

```python
import cohere

co = cohere.ClientV2()
response = co.embed(
    texts=["Strategi optimasi RAG enterprise"],
    model="embed-multilingual-v3.0",
    input_type="search_document",
    embedding_types=["float", "int8"]
)
```

---

## 💡 Ringkasan Pertimbangan Pemilihan

| Provider | Model Rekomendasi | Dimensi | Kelebihan Utama |
| :--- | :--- | :--- | :--- |
| **OpenAI** | `text-embedding-3-small` | 1536 / 512 | Integrasi ekosistem luas, Matryoshka scaling murah |
| **Google Gemini** | `text-embedding-004` | 768 / 256 | Aspek Task-Type spesifik (Query vs Document) |
| **Cohere** | `embed-multilingual-v3.0` | 1024 | Multilingual luar biasa, dukungan kompresi int8/binary native |
