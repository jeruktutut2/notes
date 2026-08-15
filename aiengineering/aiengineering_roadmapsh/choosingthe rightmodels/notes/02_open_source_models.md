# 02 - Open Source & Open Weights Models

 Open Source Models (atau secara presisi disebut **Open Weights Models**) adalah model AI di mana parameter/bobot (*weights*) dipublikasikan ke publik sehingga dapat diunduh, dijalankan secara lokal, di-*fine-tune*, atau di-host di infrastruktur pribadi tanpa ketergantungan pada vendor pihak ketiga.

---

## 🌐 Lanskap Open Source Models Utama

### 1. Meta Llama (Llama 3.1 & 3.2)
* **Model Unggulan**: Llama 3.1 (8B, 70B, 405B), Llama 3.2 (1B, 3B, 11B Vision, 90B Vision).
* **Kekuatan Utama**:
  * **Standar Industri Open Source**: Ekosistem pendukung paling luas (Ollama, vLLM, llama.cpp, Unsloth, Hugging Face).
  * **Pilihan Parameter Luas**: Dari 1B/3B untuk *edge devices* (HP/IoT), 8B untuk laptop/server kecil, hingga 405B yang menyaingi model closed-source top-tier.
  * **Context Window 128K**: Mendukung konteks panjang dengan kualitas retrieval tinggi.
* **Kasus Penggunaan Terbaik**: Self-hosted LLM enterprise, fine-tuning khusus industri, agen lokal offline.

### 2. DeepSeek (DeepSeek V3 & R1)
* **Model Unggulan**: DeepSeek V3 (671B MoE), DeepSeek R1 (Reasoning MoE & Distilled Models).
* **Kekuatan Utama**:
  * **Arsitektur Mixture-of-Experts (MoE) Efisien**: Mengaktifkan hanya 37B parameter per token dari total 671B, menghasilkan throughput sangat tinggi dengan biaya komputasi jauh lebih hemat.
  * **Reasoning Capabilities (DeepSeek R1)**: Menggunakan RL (*Reinforcement Learning*) murni untuk kemampuan penalaran matematika dan coding yang menandingi OpenAI o1 dengan efisiensi harga fantastis.
  * **Distillation Models**: Tersedia varian *distilled* berbasis Llama & Qwen (1.5B, 7B, 8B, 14B, 32B, 70B) yang membawa logika R1 ke hardware konsumen.
* **Kasus Penggunaan Terbaik**: Penalaran tingkat lanjut berbiaya rendah, self-hosting high-throughput enterprise, aplikasi riset/coding.

### 3. Qwen (Alibaba Cloud)
* **Model Unggulan**: Qwen 2.5 (0.5B - 72B), Qwen 2.5-Coder, Qwen 2.5-Math, Qwen 2-VL (Vision-Language).
* **Kekuatan Utama**:
  * **Kemampuan Multilingual & Coding Luar Biasa**: Mengungguli sebagian besar model open source dalam performa bahasa non-Inggris (termasuk Bahasa Indonesia) dan pemrograman.
  * **Penguasaan Matematika & Spesialisasi**: Varian Qwen-Coder dan Qwen-Math sering memenangkan benchmark open-weights di kategorinya.
* **Kasus Penggunaan Terbaik**: Aplikasi aplikasi multibahasa, local code completion, pemrosesan matematika & finansial.

### 4. Google Gemma (Gemma 2)
* **Model Unggulan**: Gemma 2 (2.7B, 9B, 27B).
* **Kekuatan Utama**:
  * **Arsitektur Ringan & Presisi Tinggi**: Dibangun menggunakan riset arsitektur yang sama dengan Gemini, dioptimalkan untuk inferensi cepat pada 1 GPU konsumen atau laptop.
  * **Lisensi Aman**: Bebas digunakan untuk aplikasi komersial dengan aturan keselamatan Google.
* **Kasus Penggunaan Terbaik**: On-device AI, microservice berlatensi rendah, deployment hemat biaya.

---

## 📈 Perbandingan Model Open Source

| Model | Parameter Available | Context Window | Arsitektur | Keunggulan Utama |
| :--- | :--- | :--- | :--- | :--- |
| **Meta Llama 3.1** | 8B, 70B, 405B | 128K | Dense Transformer | Standard industri, ekosistem fine-tuning & tooling terluas |
| **DeepSeek R1 / V3** | 671B (MoE 37B active) | 64K - 128K | MoE + Multi-head Latent Attention | Reasoning setara o1, biaya inferensi teramat murah |
| **Alibaba Qwen 2.5** | 0.5B s/d 72B | 128K | Dense / MoE Varian | Multilingual terbaik, Qwen-Coder sangat responsif |
| **Google Gemma 2** | 2.7B, 9B, 27B | 8K | Dense (Interleaved Attention) | Efisiensi VRAM tinggi, performa luar biasa di kelas 9B & 27B |

---

## 🔒 Lisensi & Compliance Open Source
1. **Apache 2.0 / MIT**: Bebas digunakan untuk komersial, modifikasi, dan redistribusi tanpa batasan pengguna (e.g., Qwen 2.5, Mistral 7B).
2. **Llama 3 Community License**: Bebas untuk komersial kecuali aplikasi Anda memiliki lebih dari 700 juta Pengguna Aktif Bulanan (MAU), yang memerlukan lisensi khusus dari Meta.
3. **Gemma Terms of Use**: Bebas komersial dengan batasan penggunaan bertanggung jawab (Responsible AI guidelines).
