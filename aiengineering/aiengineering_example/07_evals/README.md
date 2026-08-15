# 📘 Modul 7 — Evaluasi AI (AI Evals)

Modul ini membahas metodologi **AI Evals** (Pengujian Otomatis Kualitas AI) untuk memastikan respon Model AI tetap konsisten, akurat, dan mematuhi format seiring berjalannya pembaruan sistem.

---

## 🧪 Metrik & Jenis Pengujian

1. **Exact & Substring Match**: Memastikan kata kunci wajib (seperti POSITIF, NEGATIF, nama entitas) muncul dalam respon.
2. **Structural Validation**: Memastikan string JSON dari LLM dapat diparse oleh **Pydantic** tanpa error.
3. **Latency Benchmarking**: Memastikan waktu tunggu respon memenuhi Service Level Agreement (SLA).
4. **LLM-as-a-Judge**: Menggunakan prompt evaluasi pada LLM sekunder untuk memberikan skor kualitas (1 s/d 5) secara kuantitatif.

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# Jalankan test suite pytest dengan output verbose
pytest 07_evals/test_ai.py -v -s
```
