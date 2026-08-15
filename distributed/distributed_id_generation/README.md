# Distributed ID Generation (Algoritma Snowflake)

Proyek ini mendemonstrasikan bagaimana menyelesaikan masalah pembuatan ID unik (`Primary Key`) di arsitektur Terdistribusi menggunakan algoritma **Twitter Snowflake**.

## 🛑 Kenapa Tidak Menggunakan `AUTO_INCREMENT` MySQL?
Di sistem *monolith* dengan 1 database, kita bisa menggunakan tipe data `SERIAL` atau `AUTO_INCREMENT`. Namun di sistem terdistribusi skala besar (Microservices):
1. Database seringkali di-**Sharding** (dibelah) ke beberapa server.
2. Jika ada 2 database terpisah, keduanya bisa menghasilkan ID `1001` secara bersamaan, sehingga terjadi tabrakan (Collision).
3. Melakukan sinkronisasi antar-database untuk mendapatkan ID secara sekuensial akan sangat lambat (Bottleneck).

## ❄️ Apa itu Snowflake ID?
Snowflake ID adalah sebuah integer 64-bit yang terdiri dari:
- **Timestamp (41 bits)**: Akurasi milidetik (bisa diurutkan secara waktu/chronological).
- **Machine/Node ID (10 bits)**: Identitas unik dari server (bisa mendukung 1024 server berbeda).
- **Sequence (12 bits)**: Angka urut lokal di server tersebut (bisa menghasilkan 4096 ID dalam milidetik yang sama).

**Kelebihan**:
1. Menghasilkan angka integer biasa (bukan string panjang seperti UUID), sehingga *query Index* di Database (B-Tree) tetap sangat cepat.
2. Sama sekali tidak butuh kordinasi antar server saat eksekusi.
3. Kinerja sangaaaaaat cepat (jutaan ID per detik tanpa *central server*).

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menjalankan 2 *Node* (Server) yang berbeda. Tiap Node akan mencoba men-generate **50.000 ID** secara bersamaan menggunakan seratus goroutine paralel. Skrip akan memverifikasi bahwa kecepatan pembuatannya sangat instan dan membuktikan **0 Duplikat**.
