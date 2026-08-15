# 05. ANOMALY DETECTION (DETEKSI ANOMALI)

Modul ini mempelajari penerapan **Embeddings** untuk deteksi anomali transaksi, Out-of-Distribution (OOD) Guardrails LLM, dan outlier log event.

## 📄 Berkas Pembelajaran
1. `01_centroid_distance_detector.py`: Deteksi transaksi anomali berbasis jarak ke Centroid normal.
2. `02_ood_query_guardrail.py`: Guardrail keamanan LLM untuk memblokir prompt injection dan query di luar domain.
3. `03_log_event_outlier_scorer.py`: Skoring outlier log sistem real-time menggunakan jarak KNN.

## 🚀 Cara Menjalankan
```bash
python3 05_anomaly_detection/01_centroid_distance_detector.py
python3 05_anomaly_detection/02_ood_query_guardrail.py
python3 05_anomaly_detection/03_log_event_outlier_scorer.py
```
