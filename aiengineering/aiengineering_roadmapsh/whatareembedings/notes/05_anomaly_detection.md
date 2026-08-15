# 05. ANOMALY DETECTION (DETEKSI ANOMALI)

## 🚨 Deteksi Anomali Berbasis Embeddings

Deteksi anomali adalah proses mengidentifikasi data poin atau query yang menyimpang secara signifikan dari pola "normal" yang telah dipelajari.

Dalam ruang vektor embedding, data normal cenderung membentuk satu atau beberapa kluster rapat. Data anomali akan berada **jauh di luar kluster (Out of Distribution / Outlier)**.

---

## 🎯 Kasus Penggunaan Utama dalam AI Engineering

1. **LLM Safety & Out-Of-Distribution (OOD) Guardrails**: Menolak query berbahaya, prompt injection, atau query di luar domain aplikasi sebelum dikirim ke LLM mahal.
2. **Fraud Detection & Log Analysis**: Mendeteksi pola transaksi tidak wajar atau log server bermasalah secara real-time.
3. **Data Quality Monitoring**: Menemukan teks sampah, spam, atau corrupted data pada dataset training.

---

## 📐 Metode Kalkulasi Anomali

### 1. Distance-to-Centroid (Jarak ke Pusat Kluster Normal)
1. Hitung vektor centroid $\mathbf{C}$ dari kumpulan data normal $D_{\text{normal}}$:
   $$\mathbf{C} = \frac{1}{N} \sum_{i=1}^N \mathbf{v}_i$$
2. Hitung jarak Cosine Distance atau L2 Distance data baru $\mathbf{x}$ ke $\mathbf{C}$.
3. Jika $d(\mathbf{x}, \mathbf{C}) > \text{Threshold}$, tandai $\mathbf{x}$ sebagai **Anomali**.

### 2. K-Nearest Neighbors (KNN) Outlier Score
Menghitung rerata jarak dari data baru ke $K$ tetangga terdekatnya dalam dataset normal. Jika nilainya besar, data tersebut berada di area terpencil/anomali.
