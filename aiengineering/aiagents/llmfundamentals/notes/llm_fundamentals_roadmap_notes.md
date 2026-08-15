# CATATAN TEORI LENGKAP: LLM FUNDAMENTALS & MODEL MECHANISMS UNTUK AI AGENTS

Dokumentasi teori komprehensif **LLM Fundamentals (Transformer Models and LLMs - Model Mechanisms)** berdasarkan roadmap di [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents).

---

## DAFTAR ISI
1. [Transformer Architecture & Attention Mechanism](#1-transformer-architecture--attention-mechanism)
2. [Model Mechanisms: Tokenization](#2-model-mechanisms-tokenization)
3. [Model Mechanisms: Context Windows & KV-Cache](#3-model-mechanisms-context-windows--kv-cache)
4. [Model Mechanisms: Token-Based Pricing & Cost Optimization](#4-model-mechanisms-token-based-pricing--cost-optimization)
5. [Model Selection & Kuantisasi (Local vs Closed API)](#5-model-selection--kuantisasi-local-vs-closed-api)
6. [Evaluasi LLM & Benchmarks](#6-evaluasi-llm--benchmarks)

---

## 1. Transformer Architecture & Attention Mechanism

### 1.1 Scaled Dot-Product Attention
Attention mechanism memungkinkan model memberikan bobot penekanan pada token lain yang relevan dalam suatu kalimat.

$$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$

- **Query ($Q$)**: Vektor representasi apa yang sedang dicari oleh token saat ini.
- **Key ($K$)**: Vektor penanda informasi yang dimiliki oleh token lain.
- **Value ($V$)**: Isi informasi aktual yang akan diambil.
- **Skalar $\sqrt{d_k}$**: Mencegah nilai dot product menjadi terlalu besar pada dimensi tinggi yang dapat membuat gradien softmax menjadi sangat kecil (*vanishing gradient*).

```
   Query (Q)    Key (K)
      │            │
      └──────┬─────┘
             ▼
        Matmul (Q · K^T)
             │
             ▼
       Scale (/ √d_k)
             │
             ▼
        Softmax (Weights)
             │
      ┌──────┴─────┐
      ▼            ▼
 Value (V)    Attention Output
```

### 1.2 MHA vs MQA vs GQA

| Tipe Attention | Query Heads | Key/Value Heads | Penghematan Memori KV-Cache | Kualitas Performa Model |
| :--- | :--- | :--- | :--- | :--- |
| **MHA (Multi-Head)** | $N$ Heads | $N$ Heads | 0% (Baseline) | \033[92mTerbaik (Baseline)\033[0m |
| **MQA (Multi-Query)** | $N$ Heads | 1 Head | ~96% Hemat | Ada penurunan kualitas |
| **GQA (Grouped-Query)**| $N$ Heads | $G$ Groups (e.g. 8:1) | ~85% Hemat | \033[92mMendekati MHA (Ideal Standar)\033[0m |

---

## 2. Model Mechanisms: Tokenization

### 2.1 Algoritma Subword Tokenization
Tokenisasi adalah proses mengubah teks mentah (string) menjadi urutan token ID (integer) yang dapat diproses oleh tensor neural network.

```
Teks Mentah: "Transformers dan AI Agents"
     │
     ▼
[ Tokenizer (Byte-level BPE / Tiktoken) ]
     │
     ▼
Subword Tokens: ["Transform", "ers", " dan", " AI", " Agents"]
Token IDs     : [45102, 381, 1421, 15592, 17821]
```

1. **Byte Pair Encoding (BPE)**: Menggabungkan pasang byte/karakter terkerat yang paling sering muncul secara berulang. Digunakan oleh GPT-4, LLaMA.
2. **WordPiece**: Mirip BPE tetapi memilih penggabungan yang memaksimalkan *likelihood* data pelatihan. Digunakan oleh BERT.
3. **SentencePiece**: Mengapresiasi spasi sebagai karakter normal (`_`), bekerja langsung pada byte mentah tanpa membutuhkan pemisah kata pre-tokenisasi. Digunakan oleh T5, PaLM, LLaMA.

### 2.2 Efisiensi Token Menurut Bahasa & Data

```
┌──────────────────────────────┬───────────────────────────┐
│ Kategori Teks                │ Rata-rata Token/Karakter  │
├──────────────────────────────┼───────────────────────────┤
│ Bahasa Inggris               │ ~0.25 (1 Token ≈ 4 Char)  │
│ Bahasa Indonesia             │ ~0.45 (1 Token ≈ 2.2 Char)│
│ Payload JSON & Kode          │ ~0.50 (Banyak simbol/spasi│
│ Unicode / Emoji / Non-Latin  │ ~1.00 s/d 3.00 per simbol │
└──────────────────────────────┴───────────────────────────┘
```

---

## 3. Model Mechanisms: Context Windows & KV-Cache

### 3.1 Anatomi Context Window AI Agent
Context window adalah total kapasitas memori urutan token yang dapat diproses oleh LLM dalam 1 pasang *forward pass*.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        TOTAL CONTEXT WINDOW LIMIT                      │
├──────────────┬─────────────────┬───────────────────┬───────────────────┤
│ System Prompt│ History Chat    │ RAG / Retrieval   │ Working Memory    │ Max Output
│ & Tools Def  │ Percakapan      │ Knowledge Base    │ Scratchpad        │ (Reserved)
│ (10-15%)     │ (20-30%)        │ (40-50%)          │ (10%)             │ (4096 tok)
└──────────────┴─────────────────┴───────────────────┴───────────────────┴───────────┘
```

### 3.2 Rumus Memori KV-Cache (VRAM)
Memori yang dibutuhkan untuk menyimpan Key dan Value dari seluruh token dalam sequence agar tidak perlu dihitung ulang pada generasi autoregressive berikutnya:

$$\text{KV Cache Size (Bytes)} = 2 \times \text{layers} \times \text{heads} \times \text{head\_dim} \times \text{seq\_len} \times \text{batch\_size} \times \text{bytes\_per\_param}$$

### 3.3 Positional Scaling & Lost-in-the-Middle
- **RoPE (Rotary Position Embedding)**: Mengodekan posisi dengan memutar vektor query/key pada bidang 2D.
- **YaRN (Yet another RoPE NTI Extension)**: Memperluas konteks dari 4K ke 128K+ token tanpa merusak loss perplexity.
- **Lost in the Middle**: Efek di mana LLM mengingat fakta di paling awal dan paling akhir dokumen dengan sangat baik (U-Shape curve), tetapi sering alpa pada fakta yang berada di tengah-tengah context.

---

## 4. Model Mechanisms: Token-Based Pricing & Cost Optimization

### 4.1 Skema Pricing LLM Provider
Model komersial membebankan biaya berdasarkan:
1. **Input Tokens**: Token yang dikirimkan pengguna/agent ke API.
2. **Output Tokens**: Token yang dihasilkan/digenerasikan oleh LLM (umumnya **3x s/d 4x lebih mahal** dari Input).

### 4.2 Multi-Turn Cost Explosion
Pada ReAct loop AI Agent, setiap iterasi menyertakan seluruh histori sebelumnya, sehingga input token tumbuh secara kuadratis:

$$\text{Total Input Tokens} = \sum_{t=1}^{N} \left( \text{SystemPrompt} + t \times \text{TurnContext} \right)$$

### 4.3 Prompt Caching
Prompt Caching menyimpan KV-Cache dari prefix prompt yang konstan di server provider:
- **Diskon Biaya**: Hingga **50% - 90%** lebih murah pada *Cache Hit*.
- **Latensi (TTFT)**: Hingga **80% lebih cepat** (Time-To-First-Token).

---

## 5. Model Selection & Kuantisasi (Local vs Closed API)

### 5.1 Kuantisasi Bobot Model
Kuantisasi mengonversi presisi floating point tinggi (FP16/BF16 - 16 bit) ke presisi lebih rendah (INT8 / INT4):
- **FP16**: 2 Bytes per parameter ($8\text{B model} \approx 16\text{ GB VRAM}$)
- **INT8**: 1 Byte per parameter ($8\text{B model} \approx 8\text{ GB VRAM}$)
- **INT4 (GGUF / AWQ)**: 0.5 Byte per parameter ($8\text{B model} \approx 4.5\text{ GB VRAM}$)

---

## 6. Evaluasi LLM & Benchmarks

1. **Pass@k**: Metrik evaluasi coding yang mengukur probabilitas minimal 1 jawaban benar dari $k$ percobaan sampel.
2. **LLM-as-a-Judge**: Menggunakan LLM kuat (e.g. GPT-4o) untuk menilai kualitas respon model lain.
3. **Mitigasi Bias**: Selalu gunakan *Swap Position Test* (A-B vs B-A) untuk menghilangkan *Position Bias*.
