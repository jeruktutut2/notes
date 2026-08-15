# Sistem Rekomendasi Video

Catatan tentang bagaimana aplikasi/server memilih rekomendasi video untuk pengguna.

---

## 1. Gambaran Umum

Sistem rekomendasi adalah **algoritma yang memprediksi konten apa yang paling mungkin disukai atau ditonton oleh user**, berdasarkan data historis dan kontekstual. Semua platform besar (YouTube, TikTok, Netflix, Spotify) menggunakan sistem ini sebagai inti produk mereka.

### Tujuan Utama

- **Meningkatkan engagement** (watch time, session duration)
- **Meningkatkan retensi** (user kembali lagi)
- **Personalisasi pengalaman** setiap user berbeda

---

## 2. Data / Sinyal yang Dikumpulkan

Sebelum algoritma bekerja, server mengumpulkan berbagai sinyal dari user:

### Sinyal Eksplisit

User memberikan feedback secara sadar:

- Like / Dislike
- Subscribe / Follow
- Rating bintang
- "Not Interested" / "Don't recommend"
- Share video ke orang lain

### Sinyal Implisit

Dikumpulkan otomatis dari perilaku user:

- **Watch time** — berapa lama user menonton (sinyal paling kuat)
- **Completion rate** — apakah video ditonton sampai selesai
- **Click-through rate (CTR)** — rasio klik terhadap impresi thumbnail
- **Scroll behavior** — seberapa cepat user scroll melewati video
- **Search history** — kata kunci yang dicari
- **Replay** — apakah video ditonton ulang

### Sinyal Kontekstual

- Waktu menonton (pagi vs malam)
- Device (mobile vs desktop vs TV)
- Lokasi geografis
- Bahasa user
- Koneksi internet (Wi-Fi vs cellular)

---

## 3. Algoritma Utama

### 3.1 Collaborative Filtering

**Prinsip**: "User yang mirip denganmu menyukai video ini."

Collaborative filtering bekerja dengan menemukan pola kesamaan antar user atau antar item, tanpa perlu memahami konten video itu sendiri.

#### Cara Kerja

```
User A suka: Video 1, Video 2, Video 3
User B suka: Video 1, Video 2, Video 4

User A dan B mirip (sama-sama suka Video 1 & 2)
→ Rekomendasikan Video 4 ke User A
→ Rekomendasikan Video 3 ke User B
```

#### Dua Pendekatan

| Tipe | Penjelasan |
|------|------------|
| **User-Based** | Cari user yang mirip, lalu rekomendasikan apa yang mereka suka |
| **Item-Based** | Cari item yang sering disukai bersamaan, lalu rekomendasikan item serupa |

#### Teknik Implementasi

- **k-Nearest Neighbors (kNN)** — cari k user/item terdekat
- **Matrix Factorization** — dekomposisi matriks user-item menjadi faktor laten
  - Contoh: **SVD (Singular Value Decomposition)**, **ALS (Alternating Least Squares)**

#### Kelebihan dan Kekurangan

| Kelebihan | Kekurangan |
|-----------|------------|
| Tidak perlu memahami konten | **Cold Start Problem** — user/item baru tidak punya data |
| Bisa menemukan rekomendasi yang tidak terduga | **Sparsity** — matriks user-item sangat jarang (sparse) |
| Semakin banyak user, semakin akurat | Sulit scale ke jutaan user/item tanpa optimasi |

---

### 3.2 Content-Based Filtering

**Prinsip**: "Karena kamu suka video tentang X, ini video lain tentang X."

Menganalisis fitur/atribut dari konten itu sendiri dan mencocokkan dengan profil preferensi user.

#### Fitur yang Dianalisis

- Judul dan deskripsi video
- Tag dan kategori
- Thumbnail (image recognition)
- Audio/speech content (transcript)
- Channel/creator
- Durasi video
- Metadata upload (tanggal, resolusi)

#### Teknik Implementasi

- **TF-IDF** — mengukur pentingnya kata dalam deskripsi video relatif terhadap semua video
- **Word Embeddings** (Word2Vec, GloVe) — representasi kata sebagai vektor
- **CNN untuk thumbnail** — analisis visual dari gambar thumbnail
- **Cosine Similarity** — mengukur kemiripan antara vektor fitur

#### Kelebihan dan Kekurangan

| Kelebihan | Kekurangan |
|-----------|------------|
| Tidak butuh data user lain | Rekomendasi cenderung terlalu mirip (**filter bubble**) |
| Bisa bekerja untuk user baru (jika ada preferensi awal) | Sulit menemukan konten di luar preferensi yang sudah ada |
| Transparan — bisa dijelaskan kenapa direkomendasikan | Bergantung pada kualitas metadata |

---

### 3.3 Deep Learning / Neural Networks

**Prinsip**: Gabungkan semua sinyal (user behavior + konten + konteks) dalam satu model neural network yang sangat besar.

Ini adalah pendekatan yang digunakan oleh **YouTube, TikTok, dan Netflix** saat ini.

#### Arsitektur YouTube (Two-Phase System)

Referensi: Paper Google — *"Deep Neural Networks for YouTube Recommendations"* (2016)

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  PHASE 1: CANDIDATE GENERATION                      │
│  ════════════════════════════                        │
│  Input:                                             │
│    - Watch history (daftar video yang ditonton)      │
│    - Search history (query yang dicari)              │
│    - Demographics (usia, gender, lokasi)             │
│    - Context (waktu, device)                         │
│                                                     │
│  Proses:                                            │
│    - Deep Neural Network                            │
│    - Memetakan user ke embedding vector             │
│    - Nearest neighbor search di video embeddings    │
│                                                     │
│  Output:                                            │
│    - ~ratusan kandidat dari jutaan video             │
│    - Tahap ini fokus pada RECALL (jangan lewatkan   │
│      video yang relevan)                            │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  PHASE 2: RANKING                                    │
│  ═══════════════                                     │
│  Input:                                             │
│    - Kandidat dari Phase 1                          │
│    - Fitur detail: video age, channel stats,        │
│      user-video interaction history                  │
│                                                     │
│  Proses:                                            │
│    - Deep Neural Network yang lebih besar           │
│    - Memprediksi expected watch time                │
│    - Weighted logistic regression                   │
│                                                     │
│  Output:                                            │
│    - Skor ranking per video                         │
│    - Tahap ini fokus pada PRECISION (pilih yang     │
│      paling tepat)                                  │
│                                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  PHASE 3: RE-RANKING & BUSINESS RULES               │
│  ════════════════════════════════════                 │
│    - Diversifikasi (jangan semua topik sama)        │
│    - Freshness boost (video baru dapat bonus)       │
│    - Filter konten tidak pantas                     │
│    - Ads insertion                                  │
│    - A/B testing rules                              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

#### Konsep Kunci: Embeddings

```
User  → [0.23, -0.45, 0.78, 0.12, ...]   (user embedding vector)
Video → [0.21, -0.43, 0.80, 0.15, ...]   (video embedding vector)

Similarity = dot_product(user_vector, video_vector)
→ Semakin tinggi similarity, semakin relevan video untuk user
```

Embedding adalah representasi **vektor berdimensi tinggi** yang menangkap "makna" dari user dan video. User dan video dipetakan ke ruang vektor yang sama, sehingga kedekatan bisa dihitung.

---

### 3.4 Reinforcement Learning

**Prinsip**: "Belajar dari feedback real-time untuk mengoptimalkan rekomendasi jangka panjang."

Berbeda dari supervised learning yang belajar dari data historis, reinforcement learning (RL) memperlakukan rekomendasi sebagai **sequential decision problem**.

#### Cara Kerja

```
State:    profil user + konteks saat ini
Action:   memilih video untuk ditampilkan
Reward:   user menonton lama → reward tinggi
          user skip → reward rendah
          user uninstall app → reward sangat negatif

Agent belajar policy optimal untuk memaksimalkan
total reward jangka panjang (bukan hanya klik sesaat)
```

#### Mengapa Penting

- Menghindari **clickbait trap** — video dengan CTR tinggi tapi watch time rendah
- Optimasi untuk **long-term engagement** bukan hanya satu klik
- TikTok sangat kuat menggunakan pendekatan ini

---

## 4. Hybrid Systems (Sistem Gabungan)

Semua platform besar menggunakan **kombinasi** dari algoritma di atas:

```
┌──────────────────────────────────────────────────┐
│              HYBRID RECOMMENDATION               │
│                                                  │
│  ┌──────────────┐  ┌──────────────────────────┐  │
│  │ Collaborative │  │ Content-Based            │  │
│  │ Filtering     │  │ Filtering                │  │
│  └──────┬───────┘  └───────────┬──────────────┘  │
│         │                      │                  │
│         ▼                      ▼                  │
│  ┌─────────────────────────────────────────────┐  │
│  │         Deep Learning Ranking Model         │  │
│  │   (menggabungkan semua sinyal menjadi       │  │
│  │    satu skor prediksi)                      │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │                              │
│                     ▼                              │
│  ┌─────────────────────────────────────────────┐  │
│  │      Reinforcement Learning Layer           │  │
│  │   (optimasi jangka panjang)                 │  │
│  └──────────────────┬──────────────────────────┘  │
│                     │                              │
│                     ▼                              │
│              Final Recommendations                │
└──────────────────────────────────────────────────┘
```

---

## 5. Pendekatan per Platform

### YouTube

- **Arsitektur**: Two-tower deep neural network
- **Objective utama**: Predicted watch time
- **Skala**: Memilih dari ratusan juta video
- **Paper**: "Deep Neural Networks for YouTube Recommendations" (RecSys 2016)
- **Fitur unik**: Sangat mempertimbangkan video age (freshness) dan user history

### TikTok

- **Arsitektur**: Multi-gate Mixture-of-Experts (MMoE)
- **Objective utama**: Completion rate + engagement signals
- **Keunggulan**: Sangat cepat belajar preferensi user baru (~30 menit penggunaan)
- **Fitur unik**: Heavy pada computer vision (analisis konten video secara visual)
- **Feedback loop** sangat pendek — setiap swipe adalah data point

### Netflix

- **Arsitektur**: Hybrid (Collaborative + Content-Based + Deep Learning)
- **Objective utama**: Retensi subscriber (jaga user tetap berlangganan)
- **Fitur unik**: Personalisasi bukan hanya pilihan video, tapi juga **thumbnail** — setiap user melihat thumbnail yang berbeda untuk film yang sama
- **Paper**: "The Netflix Recommender System" (various publications)

### Spotify

- **Arsitektur**: Collaborative Filtering + NLP + Audio Analysis
- **Teknik unik**: 
  - **Audio embeddings** — analisis fitur audio langsung (tempo, beat, spectral features)
  - **NLP pada lirik** — memahami konten lagu melalui teks
  - **Discover Weekly** menggunakan collaborative filtering yang di-enhance dengan deep learning

---

## 6. Tantangan dalam Sistem Rekomendasi

### Cold Start Problem

User baru atau video baru tidak punya data interaksi.

**Solusi**:
- Tanya preferensi saat onboarding
- Gunakan content-based filtering untuk item baru
- Leverage demographic data

### Filter Bubble / Echo Chamber

User hanya melihat konten yang sesuai preferensi, tidak pernah terekspos ke hal baru.

**Solusi**:
- Sengaja memasukkan **exploration** di antara rekomendasi
- Diversity constraints dalam re-ranking
- Serendipity metrics

### Scalability

Miliaran user × jutaan video = komputasi yang sangat masal.

**Solusi**:
- **Approximate Nearest Neighbor (ANN)** search — contoh: FAISS (Facebook), ScaNN (Google)
- Precompute embeddings secara offline
- Two-phase architecture (candidate generation → ranking)
- Distributed computing (MapReduce, Spark)

### Bias dan Fairness

- Popularity bias — video populer makin sering direkomendasikan
- Position bias — video di posisi atas lebih sering diklik
- Creator fairness — creator baru sulit mendapat exposure

---

## 7. Simplified Flow End-to-End

```
User membuka aplikasi
        │
        ▼
Server mengambil user profile & interaction history
        │
        ▼
Candidate Generation
├── Collaborative Filtering → kandidat berdasarkan user serupa
├── Content-Based → kandidat berdasarkan konten serupa  
└── Trending/Popular → kandidat dari video yang sedang viral
        │
        ▼
Merge semua kandidat (~ratusan - ribuan video)
        │
        ▼
Ranking Model (Deep Neural Network)
├── Input: user features + video features + context
├── Predict: expected watch time / engagement score
└── Output: skor per video
        │
        ▼
Re-Ranking & Business Rules
├── Diversifikasi topik
├── Freshness boost
├── Filter konten tidak pantas
├── Ad slot insertion
└── A/B test variant selection
        │
        ▼
Response: 10-20 video teratas → tampilkan ke user
        │
        ▼
User berinteraksi (tonton, skip, like, share)
        │
        ▼
Feedback dikirim ke server → model di-retrain secara berkala
        │
        ▼
Loop kembali ke atas (semakin akurat seiring waktu)
```

---

## 8. Referensi & Paper Penting

1. **YouTube**: Covington, Adams, Sargin. *"Deep Neural Networks for YouTube Recommendations"*. RecSys 2016.
2. **Netflix**: Gomez-Uribe, Hunt. *"The Netflix Recommender System: Algorithms, Business Value, and Innovation"*. ACM TMIS 2015.
3. **TikTok/ByteDance**: Ma et al. *"Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts"*. KDD 2018.
4. **General**: Koren, Bell, Volinsky. *"Matrix Factorization Techniques for Recommender Systems"*. IEEE Computer 2009.
5. **Reinforcement Learning for Rec**: Chen et al. *"Top-K Off-Policy Correction for a REINFORCE Recommender System"*. WSDM 2019.

---

## Kesimpulan

Sistem rekomendasi video modern bukan satu algoritma tunggal, melainkan **pipeline kompleks** yang menggabungkan:

1. **Collaborative Filtering** — belajar dari perilaku kolektif user
2. **Content-Based Filtering** — memahami konten video itu sendiri
3. **Deep Learning** — menggabungkan semua sinyal dalam model neural yang besar
4. **Reinforcement Learning** — optimasi jangka panjang berdasarkan feedback loop

Semakin banyak data yang dikumpulkan, semakin akurat prediksinya — inilah mengapa platform dengan miliaran user memiliki keunggulan kompetitif yang sangat besar di bidang rekomendasi.
