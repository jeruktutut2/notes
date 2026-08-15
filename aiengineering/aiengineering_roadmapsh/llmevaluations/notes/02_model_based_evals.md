# 02. Model-Based Evals (LLM-as-a-Judge)

**Model-Based Evals** adalah metode evaluasi di mana LLM yang lebih kuat (seperti GPT-4o, Claude 3.5 Sonnet, atau Llama-3 70B) digunakan sebagai "Hakim" (*Judge*) untuk menilai respons dari model target berdasarkan instruksi atau rubrik khusus.

---

## 🧠 Metode Utama LLM-as-a-Judge

### 1. Single Grading (Absolut Scoring)
- Judge membaca Prompt User, Ground Truth (opsional), dan Respons LLM Target.
- Judge memberikan skor numerik (misal 1-5 atau 1-10) beserta penjelasan rasional (*Chain-of-Thought*).
- **Kelebihan**: Cepat dan mudah dihitung rata-rata skornya.
- **Kelemahan**: Rawan terhadap *score drift* dan tidak konsisten antar run jika prompt judge tidak ketat.

### 2. Pairwise Ranking (Relative Comparison)
- Judge menerima dua respons sekaligus: Model A vs Model B.
- Judge memutuskan opsi mana yang lebih unggul: **Model A menang**, **Model B menang**, atau **Seri (Tie)**.
- **Kelebihan**: Lebih presisi dibanding skor absolut karena LLM lebih handal membandingkan dua opsi.
- **Hasil**: Digunakan untuk membangun pemeringkatan skala Elo (*Elo Rating System*).

### 3. Framework G-Eval (Zheng et al., 2023)
- Menggunakan LLM dengan *Chain-of-Thought* (CoT) & *Formulated Rubrics*.
- Langkah G-Eval:
  1. Buat kriteria evaluasi (misal *Coherence*, *Relevance*, *Fluency*).
  2. Minta LLM mendefinisikan langkah-langkah evaluasi (*Evaluation Steps*).
  3. Minta LLM memberikan skor berbobot (*Weighted Probability Scoring* dari logprobs).

---

## ⚠️ Jenis-jenis Bias LLM-as-a-Judge & Solusinya

| Jenis Bias | Deskripsi | Teknik Mitigasi |
| :--- | :--- | :--- |
| **Position Bias** | Judge cenderung memilih opsi pertama (Model A) dalam Pairwise evaluation. | **Position Swapping**: Jalankan dua evaluasi dengan meretas posisi A & B, lalu gabungkan hasilnya. |
| **Verbosity Bias** | Judge menyukai jawaban yang lebih panjang meskipun spans penjelasan bertele-tele. | Sertakan batasan panjang kata atau instruksikan judge untuk mengabaikan panjang teks. |
| **Self-Enhancement Bias** | Model judge cenderung memenangkan respons yang dibuat oleh keluarganya sendiri. | Gunakan judge netral atau evaluasi secara agregat dengan multi-model judges. |
| **Egocentric Bias** | Judge menyukai gaya penulisan tertentu. | Sediakan rubrik penilain tertulis yang sangat detail dengan contoh konkret (*few-shot examples*). |
