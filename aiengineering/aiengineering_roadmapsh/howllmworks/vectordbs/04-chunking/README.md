# 04 - Chunking Strategies

## Apa itu Chunking?

Chunking adalah proses **memecah dokumen besar** menjadi potongan-potongan kecil (chunks) sebelum dikonversi menjadi embedding dan disimpan ke vector database.

### Mengapa Chunking Penting?

1. **Batas token model**: Model embedding memiliki batas input (misal 512 token), dokumen besar harus dipecah
2. **Akurasi pencarian**: Chunk yang lebih kecil dan fokus menghasilkan hasil pencarian yang lebih relevan
3. **Konteks LLM**: Chunk yang tepat memberikan konteks yang presisi ke LLM dalam pipeline RAG
4. **Efisiensi memori**: Embedding chunk kecil lebih hemat memori

```
Dokumen Besar (10.000 kata)
        ↓ chunking
[Chunk 1] [Chunk 2] [Chunk 3] ... [Chunk N]
        ↓ embedding
[Vector 1] [Vector 2] [Vector 3] ... [Vector N]
        ↓ simpan
     Vector Database
```

---

## Strategi Chunking

### 1. Fixed-Size Chunking

Memotong teks setiap **N karakter** atau **N token**.

**Kelebihan:** Sederhana, konsisten
**Kekurangan:** Bisa memotong di tengah kalimat/paragraf

```python
def fixed_size_chunk(text, chunk_size=500, overlap=50):
    """Memotong teks setiap chunk_size karakter dengan overlap."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap dengan chunk sebelumnya
    return chunks

# Contoh
text = """
Python adalah bahasa pemrograman tingkat tinggi yang diciptakan oleh 
Guido van Rossum. Python dirilis pertama kali pada tahun 1991. 
Python memiliki filosofi desain yang menekankan keterbacaan kode.
Machine learning adalah cabang dari kecerdasan buatan. ML menggunakan
algoritma untuk belajar dari data. Contoh algoritma ML termasuk
decision tree, random forest, dan neural network.
"""

chunks = fixed_size_chunk(text, chunk_size=150, overlap=30)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1} ({len(chunk)} chars): {chunk.strip()[:60]}...")
```

### 2. Sentence-Based Chunking

Memotong berdasarkan **kalimat**, mengelompokkan beberapa kalimat per chunk.

**Kelebihan:** Tidak memotong di tengah kalimat
**Kekurangan:** Ukuran chunk bisa bervariasi

```python
import re

def sentence_chunk(text, sentences_per_chunk=3, overlap_sentences=1):
    """Memotong teks berdasarkan kalimat."""
    # Split berdasarkan titik, tanda tanya, tanda seru
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    start = 0
    while start < len(sentences):
        end = min(start + sentences_per_chunk, len(sentences))
        chunk = ' '.join(sentences[start:end])
        chunks.append(chunk)
        start = end - overlap_sentences
    return chunks

chunks = sentence_chunk(text, sentences_per_chunk=2, overlap_sentences=1)
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk[:80]}...")
```

### 3. Paragraph-Based Chunking

Memotong berdasarkan **paragraf** (baris kosong sebagai pemisah).

**Kelebihan:** Menjaga konteks per topik
**Kekurangan:** Paragraf bisa terlalu panjang atau terlalu pendek

```python
def paragraph_chunk(text, min_length=100):
    """Memotong teks berdasarkan paragraf."""
    paragraphs = text.split('\n\n')
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    
    # Gabungkan paragraf yang terlalu pendek
    chunks = []
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) < min_length:
            current_chunk += "\n\n" + para if current_chunk else para
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks
```

### 4. Recursive Character Splitting

Memotong secara **bertingkat**: coba paragraph dulu, kalau masih terlalu besar, coba kalimat, lalu kata. Ini strategi default di LangChain.

**Kelebihan:** Balance antara ukuran konsisten dan konteks yang terjaga
**Kekurangan:** Lebih kompleks

```python
def recursive_chunk(text, chunk_size=500, overlap=50):
    """Recursive character text splitter (mirip LangChain)."""
    separators = ["\n\n", "\n", ". ", " ", ""]
    
    def _split(text, separators):
        # Pilih separator yang cocok
        separator = separators[-1]
        for sep in separators:
            if sep in text:
                separator = sep
                break
        
        # Split
        parts = text.split(separator)
        
        chunks = []
        current = ""
        for part in parts:
            candidate = current + separator + part if current else part
            if len(candidate) <= chunk_size:
                current = candidate
            else:
                if current:
                    chunks.append(current)
                if len(part) > chunk_size and len(separators) > 1:
                    # Recursive: coba separator berikutnya
                    sub_chunks = _split(part, separators[1:])
                    chunks.extend(sub_chunks)
                else:
                    current = part
        if current:
            chunks.append(current)
        
        return chunks
    
    return _split(text, separators)
```

### 5. Semantic Chunking

Memotong berdasarkan **perubahan topik** menggunakan embedding. Chunk baru dimulai ketika similarity antara kalimat berturut-turut turun di bawah threshold.

**Kelebihan:** Chunk paling koheren secara semantik
**Kekurangan:** Lebih lambat (harus menghitung embedding per kalimat)

```python
from sentence_transformers import SentenceTransformer
import numpy as np
import re

def semantic_chunk(text, threshold=0.5, model_name='all-MiniLM-L6-v2'):
    """Memotong teks berdasarkan perubahan topik (semantic)."""
    model = SentenceTransformer(model_name)
    
    # Split jadi kalimat
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if len(sentences) <= 1:
        return sentences
    
    # Embedding setiap kalimat
    embeddings = model.encode(sentences)
    
    # Hitung similarity antar kalimat berturut-turut
    chunks = []
    current_chunk = [sentences[0]]
    
    for i in range(1, len(sentences)):
        # Cosine similarity antara kalimat ini dan sebelumnya
        sim = np.dot(embeddings[i], embeddings[i-1]) / (
            np.linalg.norm(embeddings[i]) * np.linalg.norm(embeddings[i-1])
        )
        
        if sim < threshold:
            # Topik berubah → mulai chunk baru
            chunks.append(' '.join(current_chunk))
            current_chunk = [sentences[i]]
        else:
            current_chunk.append(sentences[i])
    
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks
```

---

## Menggunakan LangChain Text Splitters

LangChain menyediakan text splitter yang sudah jadi:

```bash
pip install langchain langchain-text-splitters
```

```python
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter,
    MarkdownHeaderTextSplitter,
)

# 1. Recursive Character (paling umum)
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ". ", " ", ""]
)
chunks = splitter.split_text(text)

# 2. Berdasarkan Token (lebih akurat untuk LLM)
splitter = TokenTextSplitter(
    chunk_size=100,      # 100 token per chunk
    chunk_overlap=20     # overlap 20 token
)
chunks = splitter.split_text(text)

# 3. Markdown Header Splitter (untuk file markdown)
headers_to_split = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    ("###", "Header 3"),
]
splitter = MarkdownHeaderTextSplitter(headers_to_split)
docs = splitter.split_text(markdown_text)
```

---

## Perbandingan Strategi

| Strategi | Konsistensi Ukuran | Kualitas Konteks | Kecepatan | Kompleksitas |
|----------|-------------------|------------------|-----------|-------------|
| **Fixed-size** | ✅ Tinggi | ❌ Rendah | ✅ Cepat | Mudah |
| **Sentence** | ⚠️ Sedang | ⚠️ Sedang | ✅ Cepat | Mudah |
| **Paragraph** | ❌ Rendah | ✅ Tinggi | ✅ Cepat | Mudah |
| **Recursive** | ✅ Tinggi | ✅ Tinggi | ✅ Cepat | Sedang |
| **Semantic** | ⚠️ Sedang | ✅ Sangat Tinggi | ❌ Lambat | Sulit |

---

## Tips Chunking yang Baik

### Ukuran Chunk
| Ukuran | Token | Cocok Untuk |
|--------|-------|-------------|
| Kecil | 100-200 | Pertanyaan spesifik, FAQ |
| Sedang | 200-500 | Dokumen umum (recommended) |
| Besar | 500-1000 | Dokumen teknis, konteks panjang |

### Best Practices
1. **Selalu gunakan overlap** (10-20% dari chunk size) agar konteks antar chunk tidak hilang
2. **Recursive splitter** adalah default yang aman untuk kebanyakan kasus
3. **Sesuaikan chunk size** dengan model embedding (cek max token length)
4. **Test dan evaluasi** — tidak ada "satu strategi untuk semua"
5. **Pertahankan metadata** — simpan sumber, halaman, section bersama chunk
6. **Jangan terlalu kecil** — chunk yang terlalu kecil kehilangan konteks
7. **Jangan terlalu besar** — chunk yang terlalu besar mengurangi presisi pencarian

---

## Referensi
- [LangChain Text Splitters](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
- [Chunking Strategies - Pinecone](https://www.pinecone.io/learn/chunking-strategies/)
- [5 Levels of Text Splitting - Greg Kamradt](https://github.com/FullStackRetrieval-com/RetrievalTutorials)
