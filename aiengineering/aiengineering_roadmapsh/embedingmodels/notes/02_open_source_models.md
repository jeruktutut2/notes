# Catatan Pembelajaran: Open Source Embedding Models

**Open Source Embedding Models** memberikan kontrol penuh kepada AI Engineer atas privasi data, latensi eksekusi lokal, dan kustomisasi fine-tuning tanpa ketergantungan pada vendor pihak ketiga (API lock-in).

---

## 🔑 Key Concepts & Value Proposition

### Keunggulan Utama Open Source Models:
- **Data Privacy & Compliance**: Teks tidak pernah meninggalkan infrastruktur lokal / VPC perusahaan (GDPR & HIPAA compliant).
- **Zero API Cost**: Bebas biaya per-token API, sangat ekonomis untuk skenario batch embedding jutaan dokumen.
- **Offline / Edge Capability**: Dapat dijalankan di server lokal tanpa koneksi internet.
- **Fine-Tuning Flexibility**: Dapat di-finetune menggunakan domain-specific data (hukum, medis, finansial) dengan contrastive loss (e.g. MultipleNegativesRankingLoss).

---

## 1. Sentence Transformers

Library `sentence-transformers` (diciptakan oleh UKPLab dan dikembangkan bersama Hugging Face) adalah fondasi standar industri untuk komputasi embeddings lokal di Python.

### Karakteristik & Workflow:
- Dibangun di atas PyTorch dan Hugging Face Transformers.
- Menyediakan arsitektur **Bi-Encoder** untuk mengompresi kalimat menjadi satu representasi dense vector secara efisien.
- Mendukung pemprosesan batch (*batch processing*), kalkulasi similarity bawaan, dan serialisasi model.

### Model Populer:
1. **`all-MiniLM-L6-v2`**:
   - **Dimensi**: 384
   - **Ukuran Model**: ~90 MB (sangat ringan & cepat di CPU).
   - **Context Window**: 256 token.
2. **`BAAI/bge-small-en-v1.5`**:
   - **Dimensi**: 384
   - **Ukuran Model**: ~130 MB.
   - **MTEB Score**: Sangat tinggi untuk kelas model kecil.
3. **`all-mpnet-base-v2`**:
   - **Dimensi**: 768
   - **Penggunaan**: Kualitas tinggi saat sumber daya compute mencukupi.

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(["Kalimat A", "Kalimat B"], convert_to_tensor=True)
cosine_sim = util.cos_sim(embeddings[0], embeddings[1])
```

---

## 2. Models on Hugging Face Hub

Hugging Face Hub menampung ribuan model embedding open source yang dapat diekstraksi secara manual menggunakan library `transformers` bawaan (`AutoTokenizer` & `AutoModel`).

### Memahami Pooling Strategies:
Ketika model Transformer memproses kalimat, ia menghasilkan matriks output `(batch_size, sequence_length, hidden_size)`. Untuk mengubahnya menjadi satu vektor tunggal (1D embedding), kita harus melakukan **Pooling**:

1. **Mean Pooling (Rata-rata)**: Mengambil rata-rata nilai token representation dengan mempertimbangkan `attention_mask`. Ini adalah pendekatan paling umum & akurat.
2. **CLS Pooling**: Mengambil representasi khusus token pertama (`[CLS]`).
3. **Max Pooling**: Mengambil nilai maksimum di sepanjang dimensi sequence.

```python
import torch
from transformers import AutoTokenizer, AutoModel

# Load model dan tokenizer
tokenizer = AutoTokenizer.from_pretrained('BAAI/bge-small-en-v1.5')
model = AutoModel.from_pretrained('BAAI/bge-small-en-v1.5')

def mean_pooling(model_output, attention_mask):
    token_embeddings = model_output[0] # First element of model_output contains all token embeddings
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    return torch.sum(token_embeddings * input_mask_expanded, 1) / torch.clamp(input_mask_expanded.sum(1), min=1e-9)
```

---

## 3. Jina AI Embeddings

Jina AI menawarkan keluarga model embedding open-source & komersial mutakhir yang memecahkan masalah keterbatasan *context length*.

### Fitur Unggulan Jina Embeddings:
1. **Long-Context Window (8,192 Tokens)**:
   - Kebanyakan model standar (seperti MiniLM atau BERT) terbatas pada 512 token.
   - Jina Embeddings (`jina-embeddings-v2-base-en` atau `jina-embeddings-v3`) mendukung hingga **8,192 token** (setara dengan 10+ halaman dokumen PDF).
2. **Late Chunking Architecture**:
   - Pendekatan inovatif di mana seluruh dokumen dimasukkan ke Transformer encoder terlebih dahulu sebelum dilakukan chunking. Hal ini mencegah hilangnya konteks global antar paragraf.
3. **Multilingual & Task Adapters**:
   - `jina-embeddings-v3` mendukung LoRA task adapters bawaan untuk switching antara retrieval, classification, dan separation task.

---

## 💡 Perbandingan Ringkas Open Source Models

| Model Name | Provider / Creator | Dimensi | Context Window | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| `all-MiniLM-L6-v2` | Sentence Transformers | 384 | 256 tokens | CPU Ultra-Fast Local Inference |
| `bge-small-en-v1.5` | BAAI (Hugging Face) | 384 | 512 tokens | RAG & Semantic Search Akurasi Tinggi |
| `jina-embeddings-v2/v3` | Jina AI | 768 | 8,192 tokens | Dokumen Panjang (Long-Context PDF RAG) |
