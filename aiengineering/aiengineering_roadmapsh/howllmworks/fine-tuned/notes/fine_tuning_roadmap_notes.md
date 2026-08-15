# Catatan Pembelajaran Fine-Tuning LLM & AI Engineering

Dokumen ini berisi rangkuman teori, arsitektur, dan prinsip utama dalam **Fine-Tuning Large Language Models (LLMs)** berdasarkan kurikulum **AI Engineering (roadmap.sh)**.

---

## 1. Persiapan Dataset & Formatting

### 1.1 Format Data Instruction Tuning
Untuk melatih model agar mengikuti instruksi (Instruction Tuning / Alignment), data diproses ke dalam format terstruktur:

- **Format Alpaca (Single-turn):**
  ```json
  {
    "instruction": "Jelaskan apa itu LoRA dalam ML.",
    "input": "",
    "output": "LoRA (Low-Rank Adaptation) adalah teknik fine-tuning efisien..."
  }
  ```

- **Format ShareGPT / ChatML (Multi-turn Conversational):**
  ```json
  {
    "conversations": [
      {"from": "system", "value": "Anda adalah asisten AI yang ahli dalam Machine Learning."},
      {"from": "human", "value": "Berapa rank yang ideal untuk LoRA?"},
      {"from": "gpt", "value": "Rank r yang umum digunakan berkisar antara 8 hingga 64."}
    ]
  }
  ```

### 1.2 Target-Only Loss Masking
Pada Causal Language Modeling, loss default dihitung untuk seluruh token dalam urutan. Namun pada SFT, kita **hanya memprediksi jawaban (assistant response)**, bukan prompt pengguna. Token prompt diberi label `-100` pada PyTorch CrossEntropyLoss agar diabaikan dalam perhitungan gradient.

---

## 2. Parameter-Efficient Fine-Tuning (PEFT) & LoRA

### 2.1 Konsep & Formula Matematika LoRA
Fine-tuning seluruh parameter (Full Fine-Tuning) membutuhkan GPU VRAM berkapasitas besar. **LoRA (Low-Rank Adaptation)** membekukan bobot asli model $W_0 \in \mathbb{R}^{d \times k}$ dan menyisipkan dua matriks rank rendah $A \in \mathbb{R}^{r \times k}$ dan $B \in \mathbb{R}^{d \times r}$ di mana $r \ll \min(d, k)$.

$$h = W_0 x + \Delta W x = W_0 x + \frac{\alpha}{r} (B A) x$$

- **Inisialisasi:** Matriks $A$ diinisialisasi secara acak (Gaussian distribution) dan Matriks $B$ diinisialisasi dengan angka nol $0$. Sehingga saat awal training, $\Delta W = 0$.
- **Scaling Factor $\frac{\alpha}{r}$:** Membantu menstabilkan pembaruan gradien saat merubah rank $r$.

### 2.2 Quantized LoRA (QLoRA)
QLoRA menggabungkan:
1. **NF4 (NormalFloat 4):** Tipe data 4-bit teoretis optimal untuk bobot berdistribusi normal.
2. **Double Quantization (DQ):** Mengkuantisasi statistik kuantisasi untuk menghemat VRAM tambahan.
3. **Paged Optimizers:** Menggunakan memory swapping ke CPU RAM jika VRAM penuh selama puncaknya (gradient checkpointing spike).

---

## 3. Supervised Fine-Tuning (SFT) & Memory Efficiency

### 3.1 VRAM Memory Breakdown
Kebutuhan memori GPU saat training model dengan $P$ milyar parameter:
- **Model Weights (FP16):** $2 \times P$ GB
- **Optimizer States (AdamW 32-bit):** $8 \times P$ GB
- **Gradients (FP16):** $2 \times P$ GB
- **Activations & Temporary Buffers:** Bergantung pada sequence length & batch size.

*Contoh Full FT Model 7B:* Butuh minimal ~80GB VRAM.
*Dengan QLoRA 4-bit:* Memerlukan hanya ~6-10GB VRAM!

### 3.2 Trik Efisiensi Memori
- **Gradient Accumulation:** Menghitung gradien secara mikro-batch lalu memperbarui bobot setelah $N$ akumulasi (simulasi batch size besar tanpa membengkakkan VRAM).
- **Gradient Checkpointing:** Mengorbankan sedikit kecepatan hitung (re-compute activation saat backward pass) demi menghemat VRAM signifikan.
- **Mixed Precision (FP16/BF16):** Mempercepat perkalian matriks menggunakan Tensor Cores.

---

## 4. Preference Alignment (DPO & RLHF)

Setelah Supervised Fine-Tuning (SFT), model mungkin masih menghasilkan respon yang tidak relevan, bias, atau bertele-tele. **Alignment** menyelaraskan model dengan preferensi manusia.

### 4.1 RLHF vs DPO
- **RLHF (PPO):** Membutuhkan pembuatan Reward Model terpisah, Policy Model, Reference Model, dan Value Model. Sangat rumit dan tidak stabil.
- **DPO (Direct Preference Optimization):** Mengeliminasi kebutuhan Reward Model dan PPO. Loss DPO diturunkan secara analitis langsung dari preferensi pasangan $(y_w, y_l)$ di mana $y_w$ adalah respon yang disukai (*winning/chosen*) dan $y_l$ yang ditolak (*losing/rejected*).

Formula Loss DPO:
$$\mathcal{L}_{\text{DPO}} = -\mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)} - \beta \log \frac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)} \right) \right]$$

---

## 5. Evaluasi & Export Model

### 5.1 Metrik Evaluasi
- **Loss & Perplexity (PPL):** $PPL = \exp(\text{CrossEntropyLoss})$. Mengukur seberapa "terkejut" model memprediksi kata berikutnya.
- **ROUGE / BLEU:** Mengukur overlap $n$-gram antara hasil generasi dan jawaban referensi.
- **LLM-as-a-Judge:** Menggunakan model lebih kuat (seperti GPT-4o) untuk menilai aspek keakuratan, kejelasan, dan tata bahasa respon fine-tuned model.

### 5.2 Merging & Export Format
- **Merge LoRA:** $W_{\text{final}} = W_0 + \frac{\alpha}{r} (B A)$. Menggabungkan bobot LoRA kembali ke base model agar inference tidak mengalami tambahan latensi.
- **Safetensors:** Format penyimpanan bobot biner modern yang cepat dan aman dari arbitrary code execution (berbeda dari `pickle` / `.pt`).
- **GGUF:** Format kuantisasi (Q4_K_M, Q8_0) yang dioptimalkan untuk eksekusi CPU / llama.cpp / Ollama.
