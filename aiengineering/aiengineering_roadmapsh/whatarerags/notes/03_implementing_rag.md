# 🛠️ MODUL 03: IMPLEMENTING RAG PIPELINE

Proses pengimplementasian RAG terdiri dari 5 tahapan utama yang berurutan: **Chunking ➔ Embedding ➔ Vector Database ➔ Retrieval Process ➔ Generation**.

```text
┌──────────┐     ┌───────────┐     ┌─────────────┐     ┌───────────┐     ┌────────────┐
│ Chunking │ ──► │ Embedding │ ──► │ Vector DB   │ ──► │ Retrieval │ ──► │ Generation │
└──────────┘     └───────────┘     └─────────────┘     └───────────┘     └────────────┘
```

---

## 1. ✂️ Chunking (Pemotongan Teks)
LLM memiliki batas *context window*. Dokumen besar harus dipotong menjadi pecahan (*chunks*) lebih kecil.

### Strategi Chunking Utama:
- **Fixed-Size Chunking**: Memotong berdasarkan jumlah karakter/token tetap (misal 500 karakter) dengan overlap (misal 50 karakter).
- **Sentence-Based Chunking**: Memotong berdasarkan batas kalimat (`.`, `!`, `?`).
- **Recursive Character Chunking**: Memotong hierarkis berdasarkan separator berurutan (`\n\n`, `\n`, spasi, `""`).
- **Semantic Chunking**: Pemotongan dinamis berdasarkan perubahan makna semantik antar kalimat.

---

## 2. 🔢 Embedding (Vektorisasi Teks)
*Text Chunks* diubah menjadi vector numerik berdimensi tinggi menggunakan *Embedding Model* (misal OpenAI `text-embedding-3-small` atau HuggingFace `all-MiniLM-L6-v2`).

---

## 3. 🗄️ Vector Database (Penyimpanan Index & Metadata)
Vector embedding disimpan ke dalam **Vector Database** (misal FAISS, ChromaDB, Pinecone, Qdrant).
- **Index**: Menggunakan struktur data ANN seperti HNSW (Hierarchical Navigable Small World) atau IVF (Inverted File Index) untuk pencarian cepat.
- **Payload/Metadata**: Menyimpan teks asli, judul dokumen, nomor halaman, dan tanggal update.

---

## 4. 🔎 Retrieval Process (Pencarian Context)
Saat user mengajukan pertanyaan (*query*):
1. Query di-embed menjadi vector pencarian.
2. Vector DB melakukan pencarian kemiripan (*similarity search*) dengan Cosine Similarity atau Dot Product.
3. **Hybrid Search**: Menggabungkan Dense Retrieval (Vector) + Sparse Retrieval (BM25 Keyword Search).
4. **Re-ranking**: Menggunakan model *Cross-Encoder* untuk menyaring dan mengurutkan ulang Top-K chunks paling relevan.

---

## 5. 🤖 Generation (Sintesis Jawaban LLM)
Konteks dokumen yang berhasil diambil dimasukkan ke dalam *system prompt* LLM:

```text
SYSTEM PROMPT:
Anda adalah asisten AI yang jujur. Jawablah pertanyaan pengguna HANYA berdasarkan konteks berikut.
Jika informasi tidak ada dalam konteks, katakan "Maaf, data tidak ditemukan".

KONTEKS:
[Top Chunk 1 dari Vector DB]
[Top Chunk 2 dari Vector DB]

PERTANYAAN PENGGUNA:
[Query Pengguna]
```
