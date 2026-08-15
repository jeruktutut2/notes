# 01 - Embeddings

## Apa itu Embeddings?

Embedding adalah **representasi numerik** (vektor) dari data — seperti teks, gambar, atau audio — dalam ruang berdimensi tinggi. Tujuannya adalah mengubah data yang tidak terstruktur menjadi angka-angka yang bisa dipahami dan diproses oleh komputer.

**Analogi sederhana:** Bayangkan setiap kata/kalimat memiliki "koordinat" di sebuah peta. Kata-kata yang maknanya mirip akan berada di lokasi yang berdekatan di peta tersebut.

```
Contoh embedding (disederhanakan):
"kucing"  → [0.2, 0.8, 0.1, 0.5]
"anjing"  → [0.3, 0.7, 0.2, 0.4]   ← dekat dengan "kucing"
"mobil"   → [0.9, 0.1, 0.8, 0.2]   ← jauh dari "kucing"
```

---

## Mengapa Embeddings Penting?

1. **Semantic Search**: Mencari berdasarkan makna, bukan hanya kata kunci exact
2. **Recommendation System**: Merekomendasikan item yang mirip
3. **RAG (Retrieval-Augmented Generation)**: Menemukan dokumen relevan untuk konteks LLM
4. **Clustering & Classification**: Mengelompokkan data berdasarkan kemiripan
5. **Anomaly Detection**: Mendeteksi data yang "berbeda" dari pola umum

---

## Jenis-Jenis Embeddings

### 1. Word Embeddings
Merepresentasikan **satu kata** sebagai vektor.

| Model | Deskripsi |
|-------|-----------|
| **Word2Vec** | Model klasik dari Google, menggunakan CBOW atau Skip-gram |
| **GloVe** | Global Vectors, menangkap statistik global dari corpus |
| **FastText** | Dari Facebook, mendukung subword (bagian kata) |

### 2. Sentence/Document Embeddings
Merepresentasikan **kalimat atau dokumen utuh** sebagai satu vektor.

| Model | Deskripsi |
|-------|-----------|
| **Sentence Transformers** | Model open-source berbasis BERT untuk sentence embedding |
| **OpenAI Embeddings** | API `text-embedding-ada-002`, `text-embedding-3-small/large` |
| **Cohere Embed** | API embedding dari Cohere |
| **Google Gemini Embedding** | API embedding dari Google |
| **BGE** | Model open-source performa tinggi dari BAAI |

### 3. Multimodal Embeddings
Merepresentasikan **berbagai tipe data** (teks + gambar) dalam ruang vektor yang sama.

| Model | Deskripsi |
|-------|-----------|
| **CLIP** | Dari OpenAI, menghubungkan teks dan gambar |
| **ImageBind** | Dari Meta, menghubungkan 6 modalitas |

---

## Embedding Models Populer

### A. API-Based (Mudah, Berbayar)

#### OpenAI Embeddings
```python
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    input="Kucing adalah hewan peliharaan yang populer",
    model="text-embedding-3-small"  # 1536 dimensi
)

embedding = response.data[0].embedding
print(f"Dimensi: {len(embedding)}")
print(f"Vektor: {embedding[:5]}...")  # 5 nilai pertama
```

**Model tersedia:**
| Model | Dimensi | Catatan |
|-------|---------|---------|
| `text-embedding-3-small` | 1536 | Lebih murah, cukup baik |
| `text-embedding-3-large` | 3072 | Lebih akurat, lebih mahal |
| `text-embedding-ada-002` | 1536 | Model lama, masih banyak dipakai |

#### Google Gemini Embeddings
```python
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")

result = genai.embed_content(
    model="models/text-embedding-004",
    content="Kucing adalah hewan peliharaan yang populer"
)

print(f"Dimensi: {len(result['embedding'])}")
```

#### Cohere Embeddings
```python
import cohere

co = cohere.Client("YOUR_API_KEY")

response = co.embed(
    texts=["Kucing adalah hewan peliharaan yang populer"],
    model="embed-english-v3.0",
    input_type="search_document"
)

print(f"Dimensi: {len(response.embeddings[0])}")
```

### B. Open-Source (Gratis, Self-Hosted)

#### Sentence Transformers
```python
from sentence_transformers import SentenceTransformer

# Load model
model = SentenceTransformer('all-MiniLM-L6-v2')  # 384 dimensi

# Buat embedding
sentences = [
    "Kucing adalah hewan peliharaan yang populer",
    "Anjing adalah sahabat manusia",
    "Python adalah bahasa pemrograman"
]

embeddings = model.encode(sentences)
print(f"Shape: {embeddings.shape}")  # (3, 384)
```

**Model populer:**
| Model | Dimensi | Ukuran | Catatan |
|-------|---------|--------|---------|
| `all-MiniLM-L6-v2` | 384 | 80 MB | Cepat, ringan, bagus untuk awal |
| `all-mpnet-base-v2` | 768 | 420 MB | Lebih akurat |
| `BAAI/bge-small-en-v1.5` | 384 | 130 MB | Performa tinggi |
| `BAAI/bge-large-en-v1.5` | 1024 | 1.34 GB | Sangat akurat |

#### HuggingFace Transformers
```python
from transformers import AutoTokenizer, AutoModel
import torch

# Load model
tokenizer = AutoTokenizer.from_pretrained("BAAI/bge-small-en-v1.5")
model = AutoModel.from_pretrained("BAAI/bge-small-en-v1.5")

# Tokenize
inputs = tokenizer(
    "Kucing adalah hewan peliharaan",
    return_tensors="pt",
    padding=True,
    truncation=True
)

# Generate embedding
with torch.no_grad():
    outputs = model(**inputs)
    # Ambil [CLS] token embedding
    embedding = outputs.last_hidden_state[:, 0, :]

print(f"Shape: {embedding.shape}")  # (1, 384)
```

---

## Dimensi Embedding

Dimensi embedding menentukan seberapa "detail" representasi vektor:

| Aspek | Dimensi Rendah (128-384) | Dimensi Tinggi (768-3072) |
|-------|--------------------------|---------------------------|
| **Kecepatan** | Lebih cepat | Lebih lambat |
| **Memori** | Lebih hemat | Lebih boros |
| **Akurasi** | Cukup baik | Lebih akurat |
| **Use case** | Prototyping, real-time | Produksi, akurasi tinggi |

---

## Praktik: Membandingkan Embeddings

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Buat embedding untuk beberapa kalimat
kalimat = [
    "Saya suka kucing",           # [0]
    "Kucing adalah hewan favorit saya", # [1] - mirip dengan [0]
    "Saya ingin membeli mobil baru",   # [2] - berbeda
]

embeddings = model.encode(kalimat)

# Hitung cosine similarity
from sklearn.metrics.pairwise import cosine_similarity

similarity_matrix = cosine_similarity(embeddings)

print("Similarity Matrix:")
for i, k1 in enumerate(kalimat):
    for j, k2 in enumerate(kalimat):
        if i < j:
            print(f"  '{k1}' vs '{k2}'")
            print(f"  → Similarity: {similarity_matrix[i][j]:.4f}")
            print()
```

**Output yang diharapkan:**
```
"Saya suka kucing" vs "Kucing adalah hewan favorit saya"
→ Similarity: ~0.75 (tinggi, karena topik sama)

"Saya suka kucing" vs "Saya ingin membeli mobil baru"
→ Similarity: ~0.20 (rendah, topik berbeda)
```

---

## Hal Penting yang Perlu Diingat

1. **Model yang sama**: Pastikan menggunakan model embedding yang sama saat menyimpan dan melakukan query
2. **Normalisasi**: Beberapa model sudah menormalisasi output, beberapa belum
3. **Max token length**: Setiap model memiliki batas panjang input (misal 512 token)
4. **Bahasa**: Pilih model yang mendukung bahasa target (multilingual vs English-only)
5. **Biaya**: API berbayar dihitung per token, open-source gratis tapi butuh GPU

---

## Referensi
- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [Sentence Transformers Documentation](https://www.sbert.net/)
- [HuggingFace MTEB Leaderboard](https://huggingface.co/spaces/mteb/leaderboard)
- [What are Embeddings? - Vicki Boykis](https://vickiboykis.com/what_are_embeddings/)
