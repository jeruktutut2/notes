# Distributed Database (Sharding & Consistent Hashing)

Proyek ini mendemonstrasikan bagaimana database skala raksasa (seperti Cassandra, DynamoDB, Redis Cluster) mendistribusikan triliunan datanya ke ribuan server tanpa menyebabkan satu server pun kepenuhan (*Overload*). Proses memecah data ini disebut **Sharding**.

## 🧠 Masalah dengan Hashing Biasa (Modulo)
Bayangkan Anda punya 3 server (Node 0, 1, 2) dan menggunakan rumus `hash(kunci) % 3` untuk menentukan data masuk ke server mana. 
- Data A masuk ke Node 0
- Data B masuk ke Node 1
- Data C masuk ke Node 2

Tiba-tiba Node 2 rusak terbakar. Sekarang jumlah server tinggal 2. Rumusnya berubah jadi `hash(kunci) % 2`.
Akibatnya, Data A yang sebelumnya ada di Node 0 bisa saja kini dicari di Node 1. **SEMUA pemetaan data menjadi berantakan (Cache Invalidation total)!** 

## 💡 Solusi: Consistent Hashing
Alih-alih menggunakan modulo sederhana, kita membayangkan rentang nilai hash (0 sampai 4 miliar) sebagai sebuah **Cincin (Ring)**.
1. Kita meletakkan 3 Server di titik-titik tertentu di cincin tersebut berdasarkan *hash* nama servernya.
2. Saat ada Data masuk, kita cari *hash* dari kunci data tersebut, lalu berjalan **searah jarum jam** di cincin sampai menemukan Server pertama.
3. Server itulah yang menyimpan datanya.

Jika Node 2 mati, *hanya data yang dimiliki Node 2* yang dialihkan ke Node tetangganya. Data di Node 0 dan Node 1 **TIDAK TERPENGARUH SAMA SEKALI**. Inilah kehebatan algoritma ini!

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menjalankan 3 server (Node A, B, C) secara paralel. Lalu klien akan melempar 5 data secara acak. Anda bisa membuktikan bahwa data tersebut terbagi rata ke ketiga Node, dan klien bisa mengambilnya kembali dengan sangat akurat berkat algoritma *Consistent Hashing*.
