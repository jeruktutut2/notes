# Algoritma Feed Sosial Media

Catatan tentang bagaimana platform sosial media (Twitter/X, Instagram, Facebook, LinkedIn, dll.) menentukan post/thread mana yang muncul di beranda (timeline/feed) pengguna.

---

## 1. Evolusi: Chronological → Algorithmic Feed

### Era Awal — Chronological Feed

Awalnya semua platform menggunakan **urutan kronologis murni**:

```
Timeline = semua post dari akun yang kamu follow
            diurutkan berdasarkan waktu posting (terbaru di atas)
```

Masalah:
- User melewatkan post penting jika tidak online saat itu
- Akun yang posting terlalu sering mendominasi timeline
- Engagement rate rendah karena banyak post tidak relevan

### Era Sekarang — Algorithmic Feed

Semua platform besar beralih ke **ranked feed**:

```
Timeline = post yang dipilih dan diurutkan oleh algoritma
            berdasarkan prediksi relevansi untuk user tersebut
```

> **Catatan**: Twitter/X masih menyediakan opsi "Following" (kronologis) dan "For You" (algoritmik). Tapi default-nya adalah algoritmik.

---

## 2. Perbedaan dengan Rekomendasi Video

Meskipun fondasi teknisnya mirip, ada perbedaan penting:

| Aspek | Rekomendasi Video | Feed Sosial Media |
|-------|-------------------|-------------------|
| **Sumber konten** | Semua video di platform | Mayoritas dari akun yang di-follow + sebagian dari luar |
| **Social graph** | Kurang penting | **Sangat penting** — siapa yang kamu follow, interaksi sosial |
| **Timeliness** | Video bisa relevan berbulan-bulan | Post cepat basi — **freshness sangat kritis** |
| **Tipe konten** | Relatif homogen (video) | Beragam: teks, gambar, video, link, poll, repost |
| **Engagement model** | Watch time dominan | Like, reply, repost, bookmark, dwell time |
| **Network effect** | Lemah | **Kuat** — viralitas melalui repost/share chain |
| **Real-time events** | Kurang penting | **Sangat penting** — breaking news, trending topics |

---

## 3. Sinyal yang Digunakan

### 3.1 Sinyal dari Post Itu Sendiri

| Sinyal | Penjelasan |
|--------|------------|
| **Engagement rate** | Rasio interaksi terhadap impresi (like, reply, repost, bookmark) |
| **Velocity** | Seberapa cepat post mendapat engagement setelah dipublish |
| **Konten** | Teks, gambar, video — dianalisis dengan NLP dan computer vision |
| **Freshness** | Umur post — post baru biasanya mendapat boost |
| **Media type** | Apakah ada gambar/video (biasanya mendapat boost) |
| **Post length** | Panjang teks dan thread |
| **Language** | Bahasa post vs bahasa user |

### 3.2 Sinyal dari Author (Pembuat Post)

| Sinyal | Penjelasan |
|--------|------------|
| **Relationship strength** | Seberapa sering kamu berinteraksi dengan author ini |
| **Author credibility** | Verified status, follower count, akun umur |
| **Posting frequency** | Seberapa sering author posting (spam detection) |
| **Author category** | Teman dekat vs selebriti vs brand vs news outlet |
| **Mutual connections** | Berapa banyak teman/following yang sama |

### 3.3 Sinyal dari User (Kamu sebagai Viewer)

| Sinyal | Penjelasan |
|--------|------------|
| **Interest profile** | Topik yang sering kamu engage |
| **Interaction history** | Post tipe apa yang biasa kamu like/reply/repost |
| **Session context** | Berapa lama kamu sudah scrolling, waktu hari ini |
| **Negative signals** | Post yang kamu hide, akun yang kamu mute/block |
| **Network** | Siapa yang kamu follow dan bagaimana kamu berinteraksi |

### 3.4 Sinyal dari Social Graph

| Sinyal | Penjelasan |
|--------|------------|
| **In-network vs Out-of-network** | Apakah post dari akun yang di-follow atau bukan |
| **Social proof** | Apakah orang yang kamu follow menyukai post ini |
| **Community clusters** | Grup/komunitas apa yang kamu dan author termasuk |
| **Virality chain** | Bagaimana post menyebar melalui jaringan |

---

## 4. Arsitektur Algoritma Feed

### Pipeline Umum

```
┌──────────────────────────────────────────────────────┐
│                                                      │
│  STEP 1: CANDIDATE SOURCING                          │
│  ═══════════════════════════                          │
│  Kumpulkan post potensial dari berbagai sumber:      │
│                                                      │
│  ┌─────────────────────┐  ┌──────────────────────┐   │
│  │   In-Network        │  │   Out-of-Network     │   │
│  │   ───────────       │  │   ──────────────     │   │
│  │   Post dari akun    │  │   Post yang di-like  │   │
│  │   yang kamu follow  │  │   oleh followingmu   │   │
│  │                     │  │   Trending topics    │   │
│  │                     │  │   Suggested content  │   │
│  └─────────────────────┘  └──────────────────────┘   │
│                                                      │
│  Output: ~1,500 kandidat post                        │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  STEP 2: FEATURE EXTRACTION                          │
│  ══════════════════════════                           │
│  Untuk setiap kandidat, ekstrak fitur:               │
│                                                      │
│  • User features (interest embedding, history)       │
│  • Author features (credibility, relationship)       │
│  • Post features (content, media, engagement)        │
│  • Context features (time, device, session)          │
│  • Graph features (social proof, community)          │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  STEP 3: PREDICTION / SCORING                        │
│  ════════════════════════════                         │
│  Model memprediksi probabilitas user akan:           │
│                                                      │
│  P(like)     = 0.12                                  │
│  P(reply)    = 0.05                                  │
│  P(repost)   = 0.03                                  │
│  P(click)    = 0.20                                  │
│  P(dwell>30s)= 0.35                                  │
│  P(hide)     = 0.01   ← sinyal negatif               │
│  P(report)   = 0.001  ← sinyal negatif               │
│                                                      │
│  Final Score = weighted combination of predictions   │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  STEP 4: RANKING                                     │
│  ═══════════════                                     │
│  Urutkan post berdasarkan final score                │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  STEP 5: POST-RANKING RULES                          │
│  ══════════════════════════                           │
│  • Diversifikasi (jangan 5 post berturut-turut       │
│    dari author yang sama)                            │
│  • Mix in-network dan out-of-network                 │
│  • Sisipkan ads pada posisi tertentu                 │
│  • Filter konten sensitif                            │
│  • Author diversity (variasi topik)                  │
│  • Anti-spam dan anti-manipulation rules             │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  STEP 6: SERVE TO CLIENT                             │
│  ═══════════════════════                              │
│  Kirim batch pertama (~20-50 post) ke client         │
│  Saat user scroll, fetch batch berikutnya            │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 5. Cara Kerja per Platform

### 5.1 Twitter / X — "For You" Timeline

Twitter membuka sebagian algoritmanya secara open source (Maret 2023).

#### Arsitektur

```
Candidate Sources (1,500 post)
├── 50% In-Network (dari akun yang di-follow)
│     └── Real Graph: model yang memprediksi
│         engagement berdasarkan relationship strength
│
└── 50% Out-of-Network (dari luar following)
      ├── Social Graph: "Orang yang kamu follow
      │   menyukai post ini"
      └── Embedding Spaces: SimClusters & TwHIN
          (cluster topik + heterogeneous graph embeddings)
         │
         ▼
Ranking Model (~48 juta parameter neural network)
         │
    Prediksi probabilitas untuk setiap engagement type:
    P(favorite), P(retweet), P(reply), P(click),
    P(negative_feedback)
         │
         ▼
    Final Score = Σ (weight_i × P(action_i))
         │
         ▼
    Heuristics & Filters
    ├── Author diversity filter
    ├── Content balance filter  
    ├── Out-of-network budget (max ~50%)
    ├── Feedback fatigue (jangan terlalu banyak post serupa)
    └── Visibility filtering (safety, spam)
         │
         ▼
    Served to user timeline
```

#### Bobot Engagement Twitter/X (yang diketahui dari open source)

| Action | Bobot Relatif |
|--------|---------------|
| **Like (Favorite)** | 0.5x |
| **Retweet** | 1x |
| **Reply** | 13.5x |
| **Membuka profil author dari post** | 12x |
| **Reply yang di-engage balik (conversation)** | 75x |
| **Spend >2 menit membaca thread** | 22x |
| **Meng-like reply dari post** | 16x |
| **Bookmark** | Tidak diketahui pasti, tapi tinggi |
| **Report / Block / Mute** | Penalti berat (negatif) |

> **Insight**: Reply dan conversation bernilai jauh lebih tinggi dari like. Ini menjelaskan kenapa post yang memicu diskusi lebih sering muncul di "For You".

#### SimClusters (Twitter/X)

Sistem clustering yang mengelompokkan user dan konten ke "komunitas" berdasarkan pola follow:

```
User A ──┐
User B ──┼── Cluster "Tech Indonesia"
User C ──┘

Tweet tentang coding → cocok dengan Cluster "Tech Indonesia"
→ ditampilkan ke User A, B, C meskipun mereka tidak follow author
```

---

### 5.2 Instagram Feed & Explore

#### Feed (dari akun yang di-follow)

Instagram menggunakan **machine learning model** yang memprediksi 5 interaksi utama:

1. **Time spent** — berapa lama melihat post
2. **Like** — probabilitas menekan like
3. **Comment** — probabilitas berkomentar
4. **Save** — probabilitas menyimpan
5. **Tap on profile** — probabilitas mengunjungi profil

Sinyal terpenting menurut Instagram (publik):

```
Ranking Signals (urutan prioritas):
1. Information about the post
   └── Engagement rate, waktu posting, lokasi, durasi (jika video)

2. Information about the author
   └── Seberapa menarik author bagi user (interaction history)

3. Your activity
   └── Post apa yang biasanya kamu like dan tipe konten preferensi

4. Your interaction history with the author
   └── Apakah kamu sering komentar/like post author ini
```

#### Explore Page (konten di luar following)

Explore menggunakan pipeline yang berbeda:

```
Seed Accounts
├── Akun yang baru kamu engage
├── Topik yang sering kamu explore
│
└──→ Find Similar Accounts (graph expansion)
      │
      └──→ Candidate Posts dari akun-akun serupa
            │
            └──→ Ranking Model (3 fase)
                  ├── Phase 1: Neural network ringan (filter ribuan → ratusan)
                  ├── Phase 2: Model lebih berat (ratusan → puluhan)
                  └── Phase 3: Final ranking + integrity filter
```

---

### 5.3 Facebook News Feed

Facebook menggunakan sistem yang mereka sebut **"Meaningful Social Interactions" (MSI)** sejak 2018.

#### Prinsip Utama

Post dari **teman dan keluarga** diprioritaskan di atas post dari **halaman (pages) dan brand**.

#### Ranking Formula (Simplified)

```
Score = P(engagement) × Value(engagement_type) × Recency_Decay

Di mana:
- P(engagement)       = probabilitas user akan berinteraksi
- Value(engagement)   = bobot jenis interaksi
- Recency_Decay       = faktor penurunan berdasarkan umur post
```

#### Hierarki Engagement Facebook

```
Interaksi bernilai TINGGI:
├── Komentar panjang dan bermakna
├── Share dengan komentar personal
├── Reactions (Love, Haha, Wow > Like biasa)
└── Messenger share (share post via DM)

Interaksi bernilai RENDAH:
├── Like tanpa komentar
├── Click tanpa engagement lanjutan
└── Passive scrolling (dwell time pendek)

Sinyal NEGATIF:
├── Hide post
├── Snooze author
├── Unfollow
└── Report
```

#### Integrity Systems

Facebook memiliki layer khusus untuk filter konten:

```
Post lolos ranking
      │
      ▼
Integrity Checks:
├── Misinformation classifier (cek fakta)
├── Violence & hate speech detector
├── Clickbait classifier (turunkan ranking)
├── Engagement bait detector ("tag 3 teman!")
├── Borderline content demotion
└── Repeat content reducer
      │
      ▼
Final feed
```

---

### 5.4 LinkedIn Feed

LinkedIn memiliki pendekatan yang unik karena konteksnya profesional.

#### Pipeline

```
Post masuk
    │
    ▼
Content Classification:
├── Spam → BLOCK
├── Low Quality → DEMOTE
└── High Quality → BOOST
    │
    ▼
Subset of connections see the post (small test audience)
    │
    ▼
Measure engagement rate dari test audience
    │
    ├── High engagement → Expand ke lebih banyak connections
    ├── Medium → Tetap di level ini
    └── Low → Stop distribusi
    │
    ▼
Jika viral → expand ke 2nd and 3rd degree connections
```

#### Sinyal Penting LinkedIn

- **Dwell time** — LinkedIn sangat menghargai post yang dibaca lama
- **Niche expertise** — Post dari orang dengan keahlian di topik tertentu mendapat boost
- **Comment quality** — Komentar substantif bernilai lebih dari like
- **Creator mode** — Akun dengan creator mode aktif mendapat distribusi lebih luas

---

### 5.5 TikTok — "For You Page"

Meskipun TikTok adalah platform video, FYP-nya beroperasi lebih mirip **social feed** daripada rekomendasi video tradisional.

#### Keunikan TikTok

1. **Tidak bergantung pada social graph** — Kamu tidak perlu follow siapapun
2. **Content-first** — Algoritma menilai konten, bukan creator
3. **Extremely fast learning** — Bisa memahami preferensi user dalam ~30 menit

#### Arsitektur

```
Video baru diupload
        │
        ▼
Initial Distribution: tunjukkan ke ~300-500 user random
        │
        ▼
Ukur engagement:
├── Completion rate (paling penting!)
├── Replay rate
├── Like/comment/share ratio
├── Follow-through (follow creator setelah nonton)
        │
        ├── Engagement tinggi → expand ke ~5,000 user
        │   ├── Masih tinggi → expand ke ~50,000
        │   │   └── Masih tinggi → expand ke ~500,000+
        │   └── Turun → stop expansion
        └── Engagement rendah → stop distribution
```

---

## 6. Konsep Teknis Penting

### 6.1 Social Graph dan Graph Neural Networks

Berbeda dari rekomendasi video, feed sosial media sangat bergantung pada **social graph**:

```
     ┌─── User A ───┐
     │     │         │
  follow  like    reply
     │     │         │
     ▼     ▼         ▼
  User B  Post X   User C
     │               │
  follow           follow
     │               │
     ▼               ▼
  User D           User E

Graph Neural Network membaca pola relasi ini
untuk memprediksi koneksi dan preferensi
```

**Graph Neural Networks (GNN)** memungkinkan model untuk:
- Memahami community structure
- Menemukan konten relevan dari 2nd/3rd degree connections
- Mendeteksi pola viralitas

### 6.2 Real-Time Ranking vs Batch Processing

| Aspek | Real-Time | Batch |
|-------|-----------|-------|
| **Kapan** | Saat user buka app / scroll | Secara periodik (setiap jam/hari) |
| **Apa** | Ranking final berdasarkan konteks terkini | Pre-compute embeddings, aggregate engagement |
| **Latency** | Harus < 100-200ms | Bisa menit sampai jam |
| **Contoh** | Scoring model saat request | Training model, update user profiles |

```
Batch Processing (offline):
├── Train ranking model (setiap beberapa jam)
├── Update user interest embeddings
├── Compute social graph features
└── Aggregate post engagement statistics

Real-Time (saat user request):
├── Fetch candidates dari cache
├── Apply real-time features (session context, recency)
├── Run ranking model inference
├── Apply business rules
└── Serve response (< 200ms total)
```

### 6.3 Engagement Prediction: Multi-Task Learning

Model modern memprediksi **banyak jenis engagement sekaligus** dalam satu model:

```
                    ┌─── P(like)     = 0.15
Shared              ├─── P(comment)  = 0.04
Hidden     ────────►├─── P(share)    = 0.02
Layers              ├─── P(save)     = 0.08
                    ├─── P(click)    = 0.22
                    ├─── P(dwell>5s) = 0.45
                    └─── P(hide)     = 0.01

Final Score = w1×P(like) + w2×P(comment) + w3×P(share)
            + w4×P(save) + w5×P(click) + w6×P(dwell)
            - w7×P(hide) - w8×P(report)

Bobot (w1...w8) menentukan "apa yang platform ingin optimize"
→ Ini keputusan bisnis, bukan teknis
```

### 6.4 Freshness dan Time Decay

Post di sosial media punya **decay function** — semakin tua, semakin turun skornya:

```
Relevance Score = Base_Score × Decay(age)

Contoh decay functions:
├── Linear:      Decay = max(0, 1 - age/max_age)
├── Exponential: Decay = e^(-λ × age)
└── Logarithmic: Decay = 1 / (1 + log(1 + age))

Platform berbeda punya decay rate berbeda:
├── Twitter/X:  decay sangat cepat (post relevan ~jam)
├── Instagram:  decay medium (post relevan ~1-2 hari)
├── Facebook:   decay medium (post relevan ~1-2 hari)
└── LinkedIn:   decay lambat (post bisa relevan ~minggu)
```

---

## 7. Manipulasi Algoritma & Countermeasures

### Taktik Manipulasi yang Umum

| Taktik | Penjelasan |
|--------|------------|
| **Engagement bait** | "Like jika setuju!" — memancing interaksi artifisial |
| **Follow/unfollow** | Follow massal lalu unfollow untuk menarik attention |
| **Pod groups** | Grup yang saling like/comment untuk boost engagement |
| **Clickbait** | Judul menyesatkan untuk memancing klik |
| **Rage bait** | Konten kontroversial yang sengaja memancing emosi |
| **Bot networks** | Akun palsu untuk inflate engagement |

### Countermeasures

```
Platform melawan dengan:
├── Engagement quality scoring
│   └── Like dari akun bot bernilai 0, dari akun aktif bernilai penuh
│
├── Behavioral pattern detection
│   └── Pod groups terdeteksi dari pola interaksi yang terlalu teratur
│
├── Content classifiers
│   └── NLP model mendeteksi clickbait dan engagement bait
│
├── Velocity anomaly detection
│   └── Spike engagement yang tidak natural → flagged
│
└── Network analysis
    └── Cluster akun bot yang saling berinteraksi
```

---

## 8. Perbandingan Ringkas Semua Platform

| Platform | Sumber Utama | Sinyal Terpenting | Decay Rate | Keunikan |
|----------|-------------|-------------------|------------|----------|
| **Twitter/X** | 50% following + 50% discovery | Reply, conversation, dwell time | Sangat cepat (~jam) | Open source sebagian, real-time events |
| **Instagram** | Mayoritas following | Time spent, save, comment | Medium (~1-2 hari) | Visual-first, personalized thumbnails |
| **Facebook** | Teman & keluarga prioritas | Meaningful interactions (komentar panjang, share) | Medium (~1-2 hari) | MSI framework, integrity heavy |
| **LinkedIn** | Connections + staged expansion | Dwell time, comment quality | Lambat (~minggu) | Professional context, niche expertise boost |
| **TikTok** | 100% algoritmik (content-first) | Completion rate, replay | Cepat | Tidak bergantung social graph |

---

## 9. Flow End-to-End: Apa yang Terjadi Saat Kamu Buka Twitter/X

```
1. Kamu buka app Twitter/X
          │
          ▼
2. Client mengirim request ke server
   Header: user_id, device, timestamp, session_info
          │
          ▼
3. Candidate Sourcing Service
   ├── Query "In-Network" service
   │   └── Ambil post terbaru dari 500 akun yang kamu follow
   │       yang belum kamu lihat (dari cache/database)
   │
   ├── Query "Out-of-Network" service  
   │   └── SimClusters: post populer di cluster topik yang cocok
   │   └── Social proof: post yang di-like oleh followingmu
   │   └── Trending: post dari trending topics
   │
   └── Merge: ~1,500 kandidat post
          │
          ▼
4. Feature Extraction Service
   Untuk setiap 1,500 post, hitung:
   ├── User-Author affinity score
   ├── Post engagement velocity
   ├── Content embedding similarity
   ├── Time decay factor
   └── Social proof strength
          │
          ▼
5. Ranking Service (ML Model Inference)
   ├── Input: feature vector per post
   ├── Model: neural network ~48M parameters
   ├── Output per post:
   │   ├── P(like) = 0.12
   │   ├── P(retweet) = 0.03
   │   ├── P(reply) = 0.05
   │   ├── P(click_profile) = 0.02
   │   └── P(negative_feedback) = 0.005
   │
   └── Score = weighted_sum(predictions)
   
   Latency budget: < 50ms
          │
          ▼
6. Post-Ranking Heuristics
   ├── Jangan > 3 post berturut-turut dari author yang sama
   ├── Mix ratio in-network : out-of-network
   ├── Sisipkan ad di posisi 3, 8, 15, ...
   ├── Boost "blue check" content (configurable)
   ├── Anti-spam filter
   └── Content safety filter
          │
          ▼
7. Response ke client
   ├── Batch 1: 20 post teratas
   ├── Cursor token untuk pagination
   └── Metadata: tracking IDs untuk logging
          │
          ▼
8. Client menampilkan feed
          │
          ▼
9. User berinteraksi (scroll, like, reply, skip)
          │
          ▼
10. Client mengirim engagement events ke server
    ├── Impression log (post mana yang terlihat)
    ├── Engagement log (post mana yang di-interact)
    └── Dwell time log (berapa lama di setiap post)
          │
          ▼
11. Data masuk ke training pipeline
    └── Model di-retrain secara berkala dengan data baru
          │
          ▼
12. Loop: model yang lebih baik → feed yang lebih relevan
         → engagement lebih tinggi → lebih banyak data
         → model lebih baik lagi...
```

---

## 10. Kesimpulan

### Mirip dengan Rekomendasi Video

- Sama-sama menggunakan **deep learning** dan **multi-task prediction**
- Sama-sama punya pipeline **candidate generation → ranking → re-ranking**
- Sama-sama menggunakan **embeddings** untuk merepresentasikan user dan konten
- Sama-sama punya **feedback loop** untuk terus belajar

### Berbeda dari Rekomendasi Video

- **Social graph sangat dominan** — siapa yang kamu follow dan bagaimana kamu berinteraksi menentukan sebagian besar feed
- **Freshness/timeliness jauh lebih penting** — post basi dalam hitungan jam, bukan hari/minggu
- **Real-time events** — breaking news dan trending topics harus langsung muncul
- **Tipe engagement lebih beragam** — bukan hanya watch time, tapi like, reply, repost, save, share, dwell time
- **Network virality** — konten bisa viral melalui rantai repost, bukan hanya dari algoritma
- **Integrity/safety lebih kompleks** — misinformation, hate speech, dan manipulasi lebih menonjol di sosial media teks

### Prinsip Universal

Pada dasarnya, semua algoritma feed sosial media menjawab satu pertanyaan:

> **"Dari ribuan post yang tersedia saat ini, mana yang paling mungkin membuat user ini berinteraksi dan tetap menggunakan platform?"**

Jawabannya dihitung melalui model machine learning yang menggabungkan sinyal dari konten, author, user, social graph, dan konteks — semuanya dalam waktu kurang dari 200 milidetik.

---

## 11. Referensi

1. **Twitter/X Algorithm** (Open Source): [github.com/twitter/the-algorithm](https://github.com/twitter/the-algorithm) — Maret 2023
2. **Instagram Ranking Explained**: Blog resmi Instagram — "Shedding More Light on How Instagram Works" (2021, 2023)
3. **Facebook News Feed Ranking**: Meta Engineering Blog — "How Does News Feed Work?" (various years)
4. **LinkedIn Feed Algorithm**: LinkedIn Engineering Blog — "A Look Behind the AI that Powers LinkedIn Feed" (2023)
5. **TikTok Recommendation**: WSJ Investigation + TikTok Newsroom — "How TikTok Recommends Videos #ForYou" (2020)
6. **Graph Neural Networks for Social**: Ying et al. *"Graph Convolutional Neural Networks for Web-Scale Recommender Systems"* (PinSage, KDD 2018)
