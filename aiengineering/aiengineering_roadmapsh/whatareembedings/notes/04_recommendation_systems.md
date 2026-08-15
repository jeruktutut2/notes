# 04. RECOMMENDATION SYSTEMS (SISTEM REKOMENDASI)

## 🛍️ Rekomendasi Berbasis Embeddings

Sistem Rekomendasi modern berbasis AI memanfaatkan vektor embedding untuk mencocokkan **preferensi pengguna (User Vector)** dengan **karakteristik item/produk (Item Vector)** dalam ruang vektor bersama (shared vector space).

---

## 🏗️ 2 Pendekatan Utama

### 1. Item-to-Item Content Filtering
Merekomendasikan item yang secara semantik serupa dengan item yang sedang dilihat atau disukai pengguna.

$$\text{Similarity}(I_A, I_B) = \text{CosineSimilarity}(\mathbf{v}_{I_A}, \mathbf{v}_{I_B})$$

- **Contoh**: Jika pengguna membaca artikel tentang *"Pemrograman Python untuk Data Science"*, sistem merekomendasikan artikel dengan embedding terdekat seperti *"Panduan Pandan & NumPy untuk Pemula"*.

### 2. User Profile Vector Aggregation
Membangun satu vektor profil sintetis pengguna ($\mathbf{U}$) dengan menghitung rata-rata terpembobot dari embedding item yang pernah diinteraksi (dibeli/dilihat/disukai) oleh pengguna:

$$\mathbf{U} = \frac{\sum_{k=1}^M w_k \cdot \mathbf{v}_{k}}{\sum_{k=1}^M w_k}$$

Di mana $w_k$ adalah bobot interaksi (misal: Beli = 1.0, Klik = 0.3, Rating 5 bintang = 1.2). Rekomendasi dihasilkan dengan mencari item dengan Cosine Similarity tertinggi terhadap $\mathbf{U}$.

---

## ❄️ Mengatasi Cold-Start Problem
- **Item Baru**: Langsung buat embedding dari metadata/deskripsi teks item baru. Item baru langsung bisa direkomendasikan secara semantik tanpa harus menunggu riwayat interaksi pengguna!
- **User Baru**: Buat embedding awal berdasarkan onboarding preferences atau pencarian pertama pengguna.
