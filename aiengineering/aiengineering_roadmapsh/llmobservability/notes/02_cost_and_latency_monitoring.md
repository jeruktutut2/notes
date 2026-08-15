# 02 - Cost & Latency Monitoring dalam LLM Observability

## Overview
Penggunaan LLM dalam skala produksi membutuhkan pemantauan ketat terhadap **Biaya (Cost)** dan **Latensi (Latency)**. Tidak seperti API tradisional yang memiliki biaya konstan per HTTP request, API LLM ditagih berdasarkan jumlah token input (prompt) dan token output (completion), serta memiliki variasi latensi yang signifikan tergantung pada panjang respons.

---

## 1. Perhitungan Biaya LLM (Cost Model)

Biaya API LLM dihitung dengan rumus:

$$\text{Total Cost} = (\text{Input Tokens} \times \text{Rate}_{\text{input}}) + (\text{Output Tokens} \times \text{Rate}_{\text{output}})$$

### Contoh Tarif Model (per 1 Million Tokens):

| Model | Input Rate ($ / 1M) | Output Rate ($ / 1M) | Catatan |
|-------|---------------------|----------------------|---------|
| **GPT-4o** | $2.50 | $10.00 | High reasoning capability |
| **GPT-4o-mini** | $0.15 | $0.60 | Cost-effective for simple tasks |
| **Claude 3.5 Sonnet** | $3.00 | $15.00 | Excellent coding & instruction following |
| **Gemini 1.5 Flash** | $0.075 | $0.30 | Ultra-fast & low cost |

### Strategi Monitoring Biaya:
- **Per-User / Per-Tenant Tracking**: Menandai setiap request dengan `user_id` atau `org_id` untuk menghindari penggelembungan biaya oleh satu pengguna.
- **Budget Threshold Alerts**: Mengirimkan notifikasi Webhook/Email saat konsumsi harian atau bulanan mendekati ambang batas (misal: 80% dari $500 budget).
- **Prompt Token Caching**: Mengidentifikasi sistem prompt atau konteks berulang yang dapat dimanfaatkan untuk *Prompt Caching* (diskon hingga 50-80% pada input token).

---

## 2. Profiling Latensi (Latency Metrics)

Latensi LLM dibagi menjadi beberapa komponen penting:

```
Request Sent ────────────────────────────────────────────────────────► Response Complete
 │                                                                            │
 ├── Network & Retrieval ──► Time to First Token (TTFT) ──► Generation Phase ──┤
 │   (Vector DB / Tools)    (Pekerjaan prefill model)     (Tokens / Second)   │
```

### Metrik Latensi Kunci:
1. **TTFT (Time-to-First-Token)**:
   - Durasi dari awal request dikirim hingga karakter/token pertama diterima dari API streaming.
   - Dipengaruhi oleh latensi jaringan, antrean API, dan panjang prompt (prefill time).
   - Target UX ideal: `< 500ms`.

2. **TPS (Tokens per Second) / Generation Throughput**:
   - Kecepatan model dalam menghasilkan token output setelah token pertama muncul.
   - $\text{TPS} = \frac{\text{Completion Tokens}}{\text{Total Generation Time (detik)}}$.
   - Target ideal: `> 30 tokens/sec` untuk membaca dengan nyaman.

3. **Total Latency / E2E Duration**:
   - Total durasi eksekusi dari input pengguna sampai selesainya seluruh respons.
   - $\text{Total Latency} = \text{Latensi Preprocessing} + \text{TTFT} + \left(\frac{\text{Completion Tokens}}{\text{TPS}}\right)$.

---

## 3. Identifikasi Bottleneck Latensi

Saat aplikasi LLM terasa lambat, observability membantu mengidentifikasi akar masalahnya:

- **Bottleneck di Retrieval (Vector DB)**: Jika `Span: Vector Search` memakan waktu 1.5s dari total 2s.
- **Bottleneck di Prompt Length**: Prompt yang sangat besar (30,000+ token) meningkatkan prefill time pada model (TTFT membengkak).
- **Bottleneck di Model Speed**: Mengganti model besar ke model distilasi/kecil (misal: gpt-4o -> gpt-4o-mini) dapat meningkatkan TPS secara drastis.
