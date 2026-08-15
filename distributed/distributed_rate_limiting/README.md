# Distributed Rate Limiter (Token Bucket dengan Redis Lua Script)

Proyek ini mendemonstrasikan implementasi **Distributed Rate Limiting** menggunakan algoritma **Token Bucket** yang dieksekusi secara atomic menggunakan **Redis Lua Script**.

## 🛡️ Mengapa menggunakan Lua Script?
Jika kita menggunakan kode Go biasa untuk mengambil isi token (GET), mengecek sisa, memotong token (SET), maka jika ada 2 request datang bersamaan (*Race Condition*), keduanya bisa sama-sama membaca sisa token = 1, dan sama-sama mengizinkan request tersebut lewat (melebihi limit).

Dengan **Lua Script**, Redis menjamin bahwa skrip dieksekusi secara **atomic** (sebagai satu kesatuan tunggal). Selama skrip dieksekusi, tidak ada operasi lain yang bisa memotong prosesnya. Ini memastikan kalkulasi *rate limiter* akurat 100% di arsitektur multi-server.

## 🪣 Token Bucket
Algoritma ini menggunakan konsep "ember" (bucket) berisi token:
- **Capacity**: Batas maksimal token di dalam ember (memungkinkan adanya *burst* request instan).
- **Refill Rate**: Kecepatan ember diisi kembali (misal 1 token per detik).

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Script akan menembakkan 10 request bersamaan ke sistem yang memiliki *Capacity = 5*. Anda akan melihat sebagian request lolos (200 OK) dan sisanya akan langsung dicegat (429 Too Many Requests).
