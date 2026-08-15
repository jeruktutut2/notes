# 05 - RAG Pipeline (Retrieval-Augmented Generation)

## Apa itu RAG?

RAG (Retrieval-Augmented Generation) adalah arsitektur yang **menggabungkan LLM dengan sistem retrieval** untuk menjawab pertanyaan berdasarkan data spesifik/privat. Alih-alih mengandalkan pengetahuan yang sudah "dihafal" oleh LLM, RAG mengambil informasi relevan dari database terlebih dahulu, lalu memberikannya sebagai konteks ke LLM.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  User Query  │────→│  Retrieval   │────→│    LLM      │
│              │     │  (Vector DB) │     │  + Context  │
└─────────────┘     └──────────────┘     └─────┬───────┘
                           │                     │
                    Ambil dokumen           Generate jawaban
                    yang relevan           berdasarkan konteks
                           │                     │
                    ┌──────┴──────┐        ┌─────┴───────┐
                    │ Vector DB   │        │   Response   │
                    │ (Embeddings)│        │  ke User     │
                    └─────────────┘        └─────────────┘
```

---

## Mengapa RAG?

### RAG vs Fine-Tuning

| Aspek | RAG | Fine-Tuning |
|-------|-----|-------------|
| **Data terbaru** | ✅ Mudah diupdate | ❌ Harus retrain |
| **Biaya** | Rendah | Tinggi |
| **Transparansi** | ✅ Bisa tampilkan sumber | ❌ Black box |
| **Halusinasi** | Lebih sedikit | Masih bisa terjadi |
| **Setup** | Mudah | Butuh dataset & GPU |
| **Cocok untuk** | Q&A, dokumen, knowledge base | Mengubah gaya/perilaku model |

### Use Cases RAG
- **Customer Support Bot**: Menjawab pertanyaan berdasarkan dokumentasi produk
- **Internal Knowledge Base**: Cari informasi dari dokumen perusahaan
- **Legal Document Search**: Mencari pasal/klausul yang relevan
- **Medical Q&A**: Menjawab pertanyaan berdasarkan jurnal medis
- **Code Documentation**: Tanya jawab tentang codebase

---

## RAG Pipeline: Step by Step

### Pipeline Overview
```
INGESTION (Offline):
  Load Documents → Split/Chunk → Embed → Store in Vector DB

RETRIEVAL (Online):
  User Query → Embed Query → Search Vector DB → Get Relevant Chunks

GENERATION (Online):
  Relevant Chunks + Query → LLM Prompt → Generate Answer
```

---

### Phase 1: Ingestion (Menyiapkan Data)

```python
# Langkah 1: Load dokumen
# Langkah 2: Chunk dokumen
# Langkah 3: Buat embedding
# Langkah 4: Simpan ke vector database

import os
from sentence_transformers import SentenceTransformer
import chromadb

# --- 1. Load Dokumen ---
def load_documents(directory):
    """Load semua file .txt dari directory."""
    documents = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            documents.append({
                "content": content,
                "source": filename
            })
    return documents

# --- 2. Chunk Dokumen ---
def chunk_document(doc, chunk_size=500, overlap=50):
    """Split dokumen menjadi chunks."""
    text = doc["content"]
    chunks = []
    start = 0
    chunk_idx = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk_text = text[start:end]
        chunks.append({
            "text": chunk_text,
            "source": doc["source"],
            "chunk_index": chunk_idx
        })
        start = end - overlap
        chunk_idx += 1
    
    return chunks

# --- 3 & 4. Embed dan Simpan ---
def ingest_documents(doc_directory):
    """Pipeline ingestion: load → chunk → embed → store."""
    
    # Load
    documents = load_documents(doc_directory)
    print(f"Loaded {len(documents)} documents")
    
    # Chunk
    all_chunks = []
    for doc in documents:
        chunks = chunk_document(doc)
        all_chunks.extend(chunks)
    print(f"Created {len(all_chunks)} chunks")
    
    # Setup ChromaDB
    client = chromadb.PersistentClient(path="./rag_db")
    
    # Hapus collection lama jika ada
    try:
        client.delete_collection("knowledge_base")
    except:
        pass
    
    collection = client.create_collection(
        name="knowledge_base",
        metadata={"hnsw:space": "cosine"}
    )
    
    # Embed dan simpan (batch)
    batch_size = 100
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        
        collection.add(
            documents=[c["text"] for c in batch],
            metadatas=[{"source": c["source"], "chunk_index": c["chunk_index"]} 
                      for c in batch],
            ids=[f"chunk_{i+j}" for j in range(len(batch))]
        )
    
    print(f"Stored {collection.count()} chunks in vector database")
    return collection

# Jalankan ingestion
# collection = ingest_documents("./documents")
```

---

### Phase 2: Retrieval (Mencari Dokumen Relevan)

```python
def retrieve(query, collection, n_results=5):
    """Cari chunk yang relevan berdasarkan query."""
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    
    retrieved_chunks = []
    for doc, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        retrieved_chunks.append({
            "text": doc,
            "source": metadata["source"],
            "similarity": 1 - distance  # convert distance ke similarity
        })
    
    return retrieved_chunks

# Contoh
# chunks = retrieve("Apa itu machine learning?", collection)
# for chunk in chunks:
#     print(f"[{chunk['similarity']:.4f}] {chunk['source']}: {chunk['text'][:100]}...")
```

---

### Phase 3: Generation (Menghasilkan Jawaban)

```python
from openai import OpenAI

def generate_answer(query, retrieved_chunks, model="gpt-4o-mini"):
    """Generate jawaban menggunakan LLM dengan konteks dari retrieval."""
    
    # Gabungkan konteks
    context = "\n\n---\n\n".join([
        f"[Sumber: {chunk['source']}]\n{chunk['text']}" 
        for chunk in retrieved_chunks
    ])
    
    # Buat prompt
    prompt = f"""Kamu adalah asisten yang membantu menjawab pertanyaan berdasarkan 
konteks yang diberikan. Jawab pertanyaan dengan akurat berdasarkan konteks.
Jika jawabannya tidak ada dalam konteks, katakan "Maaf, saya tidak menemukan 
informasi tersebut dalam dokumen yang tersedia."

KONTEKS:
{context}

PERTANYAAN: {query}

JAWABAN:"""
    
    # Panggil LLM
    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Kamu adalah asisten yang menjawab pertanyaan berdasarkan konteks dokumen."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,  # rendah agar lebih faktual
        max_tokens=1000
    )
    
    return response.choices[0].message.content

# Contoh penggunaan
# answer = generate_answer("Apa itu machine learning?", chunks)
# print(answer)
```

---

### Full RAG Pipeline

```python
def rag_pipeline(query, collection, n_results=5, model="gpt-4o-mini"):
    """Pipeline RAG lengkap: query → retrieve → generate."""
    
    print(f"📝 Query: {query}\n")
    
    # 1. Retrieve
    print("🔍 Mencari dokumen relevan...")
    chunks = retrieve(query, collection, n_results)
    
    print(f"   Ditemukan {len(chunks)} chunk relevan:")
    for i, chunk in enumerate(chunks):
        print(f"   {i+1}. [{chunk['similarity']:.4f}] {chunk['source']}")
    print()
    
    # 2. Generate
    print("🤖 Generating jawaban...")
    answer = generate_answer(query, chunks, model)
    
    print(f"\n💡 Jawaban:\n{answer}")
    
    # 3. Return jawaban + sumber
    return {
        "query": query,
        "answer": answer,
        "sources": [c["source"] for c in chunks],
        "chunks": chunks
    }

# Penggunaan
# result = rag_pipeline("Apa itu machine learning?", collection)
```

---

## RAG dengan LangChain

LangChain menyederhanakan implementasi RAG:

```bash
pip install langchain langchain-openai langchain-chroma langchain-community
```

```python
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 1. Load dokumen
loader = DirectoryLoader("./documents", glob="**/*.txt", loader_cls=TextLoader)
documents = loader.load()

# 2. Chunk
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)

# 3. Buat vector store
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./langchain_db"
)

# 4. Buat retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# 5. Buat prompt template
prompt = ChatPromptTemplate.from_template("""
Jawab pertanyaan berdasarkan konteks berikut:

Konteks:
{context}

Pertanyaan: {question}

Jawaban:
""")

# 6. Buat RAG chain
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 7. Tanya!
answer = rag_chain.invoke("Apa itu machine learning?")
print(answer)
```

---

## Evaluasi RAG

### Metrics

| Metric | Mengukur Apa | Tool |
|--------|-------------|------|
| **Faithfulness** | Apakah jawaban sesuai dengan konteks yang diberikan? | RAGAS |
| **Answer Relevancy** | Apakah jawaban relevan dengan pertanyaan? | RAGAS |
| **Context Precision** | Apakah konteks yang diambil relevan? | RAGAS |
| **Context Recall** | Apakah semua informasi yang dibutuhkan berhasil diambil? | RAGAS |

### Evaluasi Sederhana
```python
def evaluate_retrieval(query, expected_source, collection, k=5):
    """Evaluasi apakah sumber yang benar berhasil di-retrieve."""
    chunks = retrieve(query, collection, n_results=k)
    retrieved_sources = [c["source"] for c in chunks]
    
    hit = expected_source in retrieved_sources
    rank = retrieved_sources.index(expected_source) + 1 if hit else -1
    
    return {
        "query": query,
        "hit": hit,
        "rank": rank,
        "top_similarity": chunks[0]["similarity"] if chunks else 0
    }
```

---

## Tips Membangun RAG yang Baik

1. **Chunk size matters** — Eksperimen dengan berbagai ukuran chunk
2. **Overlap penting** — 10-20% overlap menjaga konteks antar chunk
3. **Metadata filtering** — Gunakan metadata untuk mempersempit pencarian
4. **Reranking** — Gunakan reranker (Cohere, cross-encoder) untuk meningkatkan kualitas
5. **Hybrid search** — Kombinasikan vector search + keyword search
6. **Prompt engineering** — Instruksi yang jelas ke LLM menghasilkan jawaban yang lebih baik
7. **Evaluasi rutin** — Buat test set dan ukur performa secara berkala

---

## Referensi
- [LangChain RAG Tutorial](https://python.langchain.com/docs/tutorials/rag/)
- [RAG from Scratch - LangChain](https://github.com/langchain-ai/rag-from-scratch)
- [RAGAS - RAG Evaluation](https://docs.ragas.io/)
- [Building RAG Applications - OpenAI Cookbook](https://cookbook.openai.com/)
