# Distributed Cache (Cache-Aside & Singleflight)

Proyek ini mendemonstrasikan cara menggunakan Redis sebagai **Distributed Cache** dengan pola *Cache-Aside* dan pencegahan bencana **Cache Stampede (Thundering Herd)** menggunakan *Singleflight* di Golang.

## 📚 Apa itu Cache Stampede?
Saat sebuah data yang sangat populer (misalnya flash sale) tiba-tiba *expired* dari cache, ribuan *request* yang datang bersamaan akan mengalami *Cache Miss*. 
Jika sistem tidak dilindungi, ribuan *request* ini akan langsung "menerjang" (stampede) Database secara bersamaan untuk mengambil data yang sama. Ini akan membuat database langsung *down* seketika.

## 🛡️ Solusi: Go `singleflight`
Dengan menggunakan library `golang.org/x/sync/singleflight`, ketika ribuan request masuk secara bersamaan untuk `key` yang sama dan mengalami *Cache Miss*, hanya **SATU request** yang akan diizinkan mengeksekusi query lambat ke database. 

Ribuan request sisanya akan **diblok/menunggu**, dan begitu 1 request pertama berhasil mengambil data dari database, hasilnya akan **dibagikan (shared)** ke ribuan request lainnya yang sedang menunggu.

## 🚀 Cara Menjalankan & Menguji
Kami telah menyediakan skrip otomatis untuk menguji hal ini.

```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```

**Yang akan terjadi saat script berjalan:**
1. Script akan menyalakan Redis dan menjalankan server Go.
2. Script menembakkan 10 request bersamaan (simulasi traffic tinggi).
3. Anda akan melihat di *log server* bahwa `[DB FETCH]` (akses ke DB) hanya terjadi **1 KALI**, sedangkan 9 request lainnya langsung mendapatkan hasil melalui mekanisme `[SINGLEFLIGHT]`.
4. Setelah jeda beberapa detik, request berikutnya akan langsung mendapatkan `[CACHE HIT]`.
