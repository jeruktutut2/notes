# Distributed Messaging (Pub/Sub Pattern)

Proyek ini mendemonstrasikan komunikasi *asynchronous* antar microservices menggunakan pola **Publish/Subscribe (Pub/Sub)** dengan Message Broker **RabbitMQ**.

## 📨 Queue vs Pub/Sub
- **Task Queue** (Proyek sebelumnya): 1 pesan (tugas) hanya boleh dieksekusi oleh **1 Worker** saja. (Pekerjaan yang dibagi-bagi).
- **Pub/Sub** (Proyek ini): 1 pesan (pengumuman) di- *broadcast* dan harus didengar oleh **SEMUA** service yang berkepentingan.

## 🎯 Studi Kasus
Bayangkan sebuah sistem *E-Commerce*. Saat ada "Pesanan Baru Dibayar":
1. *Service* Pemesanan (Publisher) berteriak (*publish*) ke **Exchange**: `"Pesanan #100 dibayar!"`.
2. *Service* **Notifikasi** (Subscriber 1) mendengarnya, lalu mengirim email ke pembeli.
3. *Service* **Gudang** (Subscriber 2) mendengarnya, lalu memerintahkan staf mengepak barang.
4. *Service* **Loyalty** (Subscriber 3) mendengarnya, lalu menambah poin untuk pembeli.

Satu aksi memicu banyak reaksi secara instan tanpa Publisher (Service Pemesanan) perlu tahu siapa saja yang bereaksi. Ini menciptakan arsitektur yang **Sangat Terpisah (Loosely Coupled)**.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menyalakan 1 Publisher dan 2 Subscriber berbeda (`Notifikasi-Service` & `Audit-Service`). Anda akan melihat bagaimana 1 pesan teks yang dikirimkan oleh Publisher langsung menggandakan dirinya dan diterima oleh kedua Subscriber secara bersamaan!
