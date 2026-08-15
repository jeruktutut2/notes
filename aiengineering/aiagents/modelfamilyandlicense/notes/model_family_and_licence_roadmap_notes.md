# MODEL FAMILIES, LICENSES & GENERATION CONTROLS - CATATAN PANDUAN PENGEMBANGAN AI AGENTS

Dokumen ini menyajikan panduan mendalam (*deep-dive reference*) mengenai **Model Families and Licences** serta **Generation Controls** berdasarkan kurikulum resmi [roadmap.sh/ai-agents](https://roadmap.sh/ai-agents). Catatan ini dirancang khusus bagi pengembang AI Agent yang perlu memilih arsitektur LLM, memahami aspek lisensi legal komersial, serta mengontrol perilaku generatif model secara presisi.

---

## 📋 DAFTAR ISI

1. [Bab 1: Model Families - Open Weight vs Closed Weight](#bab-1-model-families---open-weight-vs-closed-weight)
2. [Bab 2: Arsitektur Model - Dense vs Mixture of Experts (MoE)](#bab-2-arsitektur-model---dense-vs-mixture-of-experts-moe)
3. [Bab 3: Generation Controls - Matematika & Sampling Mechanics](#bab-3-generation-controls---matematika--sampling-mechanics)
4. [Bab 4: Modifikasi Logit - Frequency & Presence Penalties](#bab-4-modifikasi-logit---frequency--presence-penalties)
5. [Bab 5: Guardrails Generasi - Stopping Criteria & Max Length](#bab-5-guardrails-generasi---stopping-criteria--max-length)
6. [Bab 6: Lisensi Model & Kepatuhan Legal Komersial](#bab-6-lisensi-model--kepatuhan-legal-komersial)
7. [Bab 7: Arsitektur Model untuk AI Agent Systems](#bab-7-arsitektur-model-untuk-ai-agent-systems)

---

## 🌐 BAB 1: MODEL FAMILIES - OPEN WEIGHT VS CLOSED WEIGHT

Dalam pengembangan AI Agent, pemilihan arsitektur model mendasari performa, biaya, latensi, serta privasi data. Ekosistem LLM modern terbagi menjadi dua ranah utama:

```
                          ┌─────────────────────────────────────┐
                          │   AI Agent Model Selection Decision │
                          └──────────────────┬──────────────────┘
                                             │
                      ┌──────────────────────┴──────────────────────┐
                      ▼                                             ▼
        ┌───────────────────────────┐                 ┌───────────────────────────┐
        │    Open Weight Models     │                 │   Closed Weight Models    │
        │  (Self-Hosted / Local)    │                 │      (Proprietary APIs)   │
        └─────────────┬─────────────┘                 └─────────────┬─────────────┘
                      │                                             │
      ├── Llama 3.1 / 3.3 (Meta)                      ├── GPT-4o / o1 / o3-mini (OpenAI)
      ├── Mistral / Mixtral (Mistral AI)              ├── Claude 3.5 Sonnet / Haiku (Anthropic)
      ├── Qwen 2.5 / Qvq (Alibaba)                    ├── Gemini 1.5 Pro / 2.0 Flash (Google)
      ├── DeepSeek R1 / V3 (DeepSeek)                 └── DeepSeek API (Commercial Cloud)
      ├── Gemma 2 (Google)
      └── Phi-3 / Phi-4 (Microsoft)
```

### 1.1 Open Weight Models
Model yang bobot parameternya (*weights*) dipublikasikan sehingga dapat diunduh, dijalankan lokal (*on-premises*), atau di-deploy di cloud privat.
- **Keunggulan**: Privasi data 100% (tidak ada data meninggalkan jaringan perusahaan), tanpa biaya per-token API, latency konsisten untuk lokal edge, bebas melakukan fine-tuning (*LoRA / Full Fine-Tuning*).
- **Tantangan**: Memerlukan investasi infrastruktur GPU (VRAM), pengelolaan inferensi engine (vLLM, Ollama, TGI), serta tanggung jawab maintenance sistem.

### 1.2 Closed Weight Models (Proprietary APIs)
Model yang hanya dapat diakses melalui layanan cloud API berbayar. Bobot model dan detail arsitektur internal tidak dibuka untuk publik.
- **Keunggulan**: Kinerja *state-of-the-art* (SOTA) untuk reasoning kompleks dan tool calling, zero infrastructure setup, konteks sangat besar (misal: 1M - 2M tokens), dan pembaruan otomatis.
- **Tantangan**: Risiko *vendor lock-in*, biaya variabel bertumbuh seiring skala agent, latensi jaringan external API, dan pembatasan regulasi privasi data.

---

## 🏗️ BAB 2: ARSITEKTUR MODEL - DENSE VS MIXTURE OF EXPERTS (MoE)

```
        Dense Model (e.g. Llama 3 70B)             Mixture of Experts (e.g. Mixtral 8x7B)
     ┌──────────────────────────────────┐        ┌──────────────────────────────────┐
     │ Token -> [All 70B Params Active] │        │ Token -> [Router / Gate Network] │
     │       -> Output Token            │        │           │                      │
     └──────────────────────────────────┘        │           ├──> Expert 1 (Active) │
                                                 │           ├──> Expert 4 (Active) │
                                                 │           └──> (Other 6 Idle)    │
                                                 │       -> Output Token            │
                                                 └──────────────────────────────────┘
```

### 2.1 Dense Architecture
Setiap token yang diproses oleh model akan melewati **seluruh parameter** yang ada dalam jaringan neural.
- **Contoh**: Llama 3.1 8B, Llama 3.1 70B, Qwen 2.5 7B.
- **Matematika VRAM**: VRAM yang dibutuhkan untuk menyimpan bobot dalam skala 16-bit (FP16) diperkirakan dengan rumus:
  $$\text{VRAM}_{\text{weights}} \approx P \times 2 \text{ Bytes}$$
  di mana $P$ adalah jumlah parameter (dalam miliaran).

### 2.2 Mixture of Experts (MoE) Architecture
Model terbagi menjadi beberapa "Expert" independen. Sebuah jaringan kecil (*Router / Gate Network*) menentukan expert mana yang relevan untuk setiap token.
- **Contoh**: Mixtral 8x7B (47B total params, ~13B active params per token), DeepSeek V3 (671B total params, 37B active params per token).
- **Keuntungan**:
  - **Efisiensi Komputasi (FLOPs)**: Hanya mengaktifkan sebagian kecil parameter per token, sehingga inference speed jauh lebih cepat dibanding Dense model dengan ukuran total yang sama.
  - **Kapasitas Pengetahuan**: Total parameter tetap besar sehingga menyimpan pengetahuan luas tanpa mengorbankan kecepatan inferensi.

---

## 🎛️ BAB 3: GENERATION CONTROLS - MATEMATIKA & SAMPLING MECHANICS

Sesuai dengan **Gambar 1 (Generation Controls)**, LLM tidak secara otomatis mengeluarkan teks berturut-turut, melainkan menghitung *distribution of probabilities* untuk token berikutnya melalui lapisan **Logits**.

```
    [LLM Neural Net] ──> Logits (z_1, z_2, ..., z_V) ──> [Temperature Scaling]
                                                                 │
    [Token Selection] <── [Top-P / Top-K Truncation] <── [Softmax Probability P_i]
```

### 3.1 Temperature ($T$)
Temperature mengubah ketajaman kurva probabilitas *Softmax*.
Logits awal disimbolkan sebagai $z_i$ untuk setiap token $i$ dalam kosakata $V$. Formula Softmax dengan Temperature adalah:

$$P(y_i) = \frac{\exp(z_i / T)}{\sum_{j=1}^{V} \exp(z_j / T)}$$

- **$T \to 0$ (Greedy Decoding / Argmax)**:
  Distribusi probabilitas terkonsentrasi 100% pada token dengan logit tertinggi. Menghasilkan respons deterministik dan berulang. Ideal untuk: *Code generation, JSON tool calling, kalkulasi matematika*.
- **$T = 1.0$ (Default Sampling)**:
  Distribusi probabilitas sesuai dengan bobot latihan asli model.
- **$T > 1.0$ (High Creativity / Entropy)**:
  Distribusi probabilitas menjadi lebih rata (*uniform*). Token berprobabilitas rendah mendapatkan kesempatan lebih besar untuk terpilih. Ideal untuk: *Brainstorming, penulisan cerita kreatif*.

### 3.2 Top-P (Nucleus Sampling)
Top-P memilih himpunan terkecil token $V^{(p)}$ sedemikian rupa sehingga akumulasi probabilitasnya mencapai ambang batas $p$:

$$\sum_{i \in V^{(p)}} P(y_i) \ge p$$

- **Mekanisme**: Token diurutkan secara menurun (*descending*). Token di luar akumulasi $p$ dipotong (*truncated*), dan sisa token di-renormalisasi.
- **Nilai Tipikal**: $p = 0.9$ berarti 10% token *tail* yang sangat tidak masuk akal dieeliminasi, sementara fleksibilitas keberagaman jawaban tetap terjaga.

### 3.3 Kombinasi Temperature & Top-P
> [!TIP]
> Praktik terbaik AI Agent: Ubah salah satu antara Temperature atau Top-P, **jangan merubah keduanya secara ekstrem bersamaan**, karena dapat membuat perilaku generasi tidak terprediksi.

---

## 🔂 BAB 4: MODIFIKASI LOGIT - FREQUENCY & PRESENCE PENALTIES

Untuk mencegah AI Agent mengalami ketersendatan (*looping*) atau menggunakan kata-kata yang sama secara berulang-ulang, digunakanlah **Frequency Penalty** dan **Presence Penalty**.

Formula penyesuaian logit ($\text{logit}_i'$):

$$\text{logit}_i' = \text{logit}_i - (c_i \times \text{frequency\_penalty}) - (\mathbb{I}(c_i > 0) \times \text{presence\_penalty})$$

di mana:
- $c_i$: Berapa kali token $i$ telah muncul dalam teks sampel yang dihasilkan sejauh ini (*token count*).
- $\mathbb{I}(c_i > 0)$: Fungsi indikator binary, bernilai $1$ jika $c_i > 0$ dan $0$ jika belum pernah muncul.

### 4.1 Frequency Penalty (Rentang: -2.0 hingga 2.0)
- **Fungsi**: Menghukum token berdasarkan **frekuensi kemunculannya**. Semakin sering token muncul, semakin besar penurunan logit-nya.
- **Dampak AI Agent**: Mencegah pengulangan frasa spesifik yang sama berulang kali dalam satu paragraf.

### 4.2 Presence Penalty (Rentang: -2.0 hingga 2.0)
- **Fungsi**: Menghukum token seketika token tersebut **muncul minimal 1 kali** tanpa memedulikan frekuensi kumulatifnya.
- **Dampak AI Agent**: Mendorong model untuk memperkenalkan topik/kata baru (*topic expansion*), meningkatkan keberagaman kosakata.

---

## 🛑 BAB 5: GUARDRAILS GENERASI - STOPPING CRITERIA & MAX LENGTH

### 5.1 Stopping Criteria (Stop Sequences)
Daftar string atau token khusus yang memerintahkan engine inferensi untuk **segera menghentikan generasi** saat token tersebut terdeteksi.
- **Penggunaan Utama dalam Agent Frameworks**:
  - ReAct Pattern: Stop sequence `Observation:` menghentikan LLM agar Agent Executor dapat menjalankan tool.
  - Chat Template: Stop token `<|im_end|>` atau `<|endoftext|>` menandai akhir dari turn percakapan.

### 5.2 Max Length / Max Tokens
Membatasi jumlah maksimum token baru yang diizinkan untuk dihasilkan oleh model dalam satu panggilan API.
- **Dampak Jika Terpotong**: Respons terpotong di tengah kalimat atau menghasilkan JSON yang tidak valid (*unclosed brace* `}`).
- **Solusi Agent**: Mengimplementasikan *Truncated JSON Repair Parser* untuk merekonstruksi sintaks JSON jika `finish_reason == "length"`.

---

## 📜 BAB 6: LISENSI MODEL & KEPATUHAN LEGAL KOMERSIAL

Memahami lisensi sangat krusial saat mendeploy Open Weight Model untuk produk SaaS atau Enterprise AI Agent.

| Lisensi Model | Jenis | Penggunaan Komersial | Batasan Khusus & Aturan MAU |
|---------------|-------|----------------------|-----------------------------|
| **Apache 2.0** | Permissive OSI | ✅ Bebas Sepenuhnya | Tanpa batasan user, bebas mengubah & menjual |
| **MIT** | Permissive OSI | ✅ Bebas Sepenuhnya | Sertakan atribusi hak cipta asli |
| **Llama 3 Community License** | Custom Open Weight | ⚠️ Komersial Terbatas | Jika MAU bulanan > 700 juta, wajib lisensi khusus dari Meta |
| **Gemma Terms of Use** | Custom Open Weight | ⚠️ Komersial Terbatas | Mematuhi Prohibited Use Policy Google |
| **RAIL (Responsible AI License)** | Ethical License | ⚠️ Bersyarat | Dilarang digunakan untuk skenario bahaya (medis tanpa izin, surveilans massal) |

### 6.1 Batasan Penggunaan Data Hasil Generasi (Synthetic Data Restrictions)
Sebagian besar lisensi model komersial (termasuk Syarat Layanan OpenAI & Llama 3 License) memuat klausul:
> *"Dilarang menggunakan output dari model X untuk melatih model bahasa lain yang secara langsung berkompetisi dengan model X."*

---

## 🏛️ BAB 7: ARSITEKTUR MODEL UNTUK AI AGENT SYSTEMS

Dalam arsitektur AI Agent modern, seringkali digunakan **Hybrid Model Routing**:

```
                              ┌─────────────────────────┐
                              │  User Request / Trigger │
                              └────────────┬────────────┘
                                           │
                                           ▼
                               ┌───────────────────────┐
                               │  Router Agent (Fast)  │
                               │  (Gemini Flash / 8B)  │
                               └───────────┬───────────┘
                                           │
                    ┌──────────────────────┴──────────────────────┐
                    ▼                                             ▼
       [Kompleksitas High / Reasoning]              [Task Spesifik / Privasi]
       ┌─────────────────────────────┐              ┌─────────────────────────┐
       │ Primary Reasoner Agent      │              │ Sub-Task Worker Agent   │
       │ (Claude 3.5 / GPT-4o / R1)  │              │ (Local DeepSeek/Qwen)   │
       └─────────────────────────────┘              └─────────────────────────┘
```

1. **Router Agent**: Model kecil & murah (misal: Gemini 2.0 Flash / Qwen 2.5 7B) untuk mengklasifikasi intent.
2. **Primary Reasoner Agent**: Model closed/open weight raksasa untuk perencanaan (*planning*) dan pemecahan masalah kompleks.
3. **Task Worker Agent**: Model open weight yang ter-finetune untuk mengeksekusi ekstraksi data atau format teks lokal secara aman dan hemat biaya.
