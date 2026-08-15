# Catatan Pembelajaran: Closed vs Open Source Models

## 1. Proprietary Closed APIs vs Open Weights Models

Dalam ekosistem AI Engineering, pilihan arsitektur deployment dibagi menjadi dua paradigma utama: **Closed Source Proprietary APIs** dan **Open Source / Open Weights Models**.

```text
+-------------------------------------------------------------------------+
|                         MODEL DEPLOYMENT PARADIGM                        |
+-------------------------------------------------------------------------+
|                                   |                                     |
|  Proprietary Closed Source APIs   |    Open Weights / Open Source      |
|  (OpenAI, Anthropic, Gemini)      |    (Meta Llama, Mistral, Qwen)      |
|                                   |                                     |
|  • Hosted & Managed by Vendor     |    • Downloadable Weights           |
|  • Pay-per-token API Pricing      |    • Self-Hosted / Local Execution  |
|  • Zero Infra Maintenance         |    • Full Data Privacy & Control    |
|  • Black-box Model Weights        |    • Fine-tuning & Modifiable       |
+-------------------------------------------------------------------------+
```

---

## 2. Tabel Perbandingan Komprehensif

| Dimensi Evaluasi | Closed Proprietary APIs (e.g. GPT-4o, Claude 3.5) | Open Weights Models (e.g. Llama 3.1, Qwen 2.5) |
| :--- | :--- | :--- |
| **Akses Bobot Model** | Tidak ada (Black box API) | Akses penuh bobot (`.safetensors`, `.gguf`) |
| **Biaya Skala Kecil** | Sangat Murah (Tanpa Biaya GPU Idle) | Lebih Mahal (Perlu sewa Server GPU) |
| **Biaya Skala Besar** | Mahal (Biaya linier berdasarkan token) | Sangat Murah (Fixed GPU Infra Cost) |
| **Privasi Data** | Ketergantungan pada Kebijakan Vendor (SOC2, Zero Retention) | 100% Data On-Premise / Local Control |
| **Custom fine-tuning** | Terbatas (API Parameter Tuning) | Kustomisasi Penuh (LoRA, Full Fine-Tuning) |
| **Latensi & Throughput** | Tergantung Server Vendor & Rate Limits | Dapat Dioptimasi Bebas (vLLM, Speculative Decoding) |
| **Ketergantungan (Lock-in)**| Risiko API Deprecation & Rate Limits | Independen (Dapat dijalankan selamanya) |

---

## 3. Lisensi Model Open Source & Open Weights

Model yang dapat diunduh bobotnya memiliki jenis lisensi yang membatasi penggunaan komersial:

1. **Permissive Open Source (Perusahaan & Komersial Bebas)**:
   * **Apache 2.0**: Digunakan oleh Mistral 7B, Qwen 2.5. Komersial bebas, modifikasi bebas, patent grant disertakan.
   * **MIT License**: Digunakan oleh beberapa model kecil/komponen utility. Sangat bebas.

2. **Open Weights dengan Pembatasan Komersial (Community Licenses)**:
   * **Llama 3 Community License**: Bebas untuk komersial hingga **700 Juta Monthly Active Users (MAU)**. Lebih dari itu memerlukan lisensi khusus dari Meta. Melarang penggunaan output Llama untuk melatih model kompetitor non-Llama.
   * **RAIL (Responsible AI License)**: Mengizinkan penggunaan bebas namun melarang bidang penggunaan berbahaya tertentu (surveillance, disinformation, medis tanpa pengawasan).

---

## 4. Matriks Matrik Keputusan (Decision Tree)

Gunakan *decision flow* berikut saat menentukan apakah akan menggunakan Closed API atau Open Weights:

```text
Apakah proyek memiliki aturan Privasi / Regulasi Ketat (HIPAA/Banking) 
yang melarang data keluar dari server internal?
  │
  ├── YA  ────────► GUNAKAN OPEN WEIGHTS (Self-Hosted Llama / Qwen)
  │
  └── TIDAK ──────► Apakah throughput token melebihi > 50 Juta token/bulan?
                      │
                      ├── YA  ────────► HITUNG TCO: Self-Hosted GPU biasanya lebih murah
                      │
                      └── TIDAK ──────► GUNAKAN CLOSED API (GPT-4o / Claude / Gemini)
```
