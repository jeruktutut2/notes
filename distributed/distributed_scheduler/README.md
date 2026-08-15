# Distributed Scheduler (Leader Election via Lock)

Proyek ini mendemonstrasikan bagaimana menyelesaikan masalah umum pada *cron jobs* di lingkungan *Microservices* atau *multi-instance*.

## 🚨 Masalah Asli (Double Execution)
Jika Anda memiliki sistem `Generate Laporan Keuangan` yang berjalan setiap jam 00:00 (Cron Job), dan aplikasi Anda di-*deploy* ke 3 kontainer (Node A, B, C) untuk *load balancing*:
Saat jam menunjukkan tepat pukul 00:00, **KETIGA Node tersebut akan mengeksekusi cron tersebut secara bersamaan!** Akibatnya, laporan keuangan ter-generate 3 kali lipat di dalam database (Double Execution/Duplication).

## 💡 Solusi: Distributed Lock (Leader Election)
Di dalam fungsi Cron, kita membungkus logika dengan sebuah **Distributed Lock** menggunakan Redis (dalam proyek ini menggunakan library `bsm/redislock`). 

Pada detik yang sama (00:00):
1. Node A, Node B, dan Node C serentak mencoba membuat kunci (Lock) di Redis.
2. Karena sifat atomik Redis, hanya 1 Node (misal Node B) yang sukses membuat kunci.
3. Node B menjadi "Leader" sementara dan mengeksekusi pekerjaan berat (Generate Laporan).
4. Node A dan C gagal mendapatkan kunci, sehingga mereka mundur dan tidak melakukan apapun (*Skip*).

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menjalankan 3 server Node (A, B, C) secara paralel, di mana ketiganya punya cron setiap 2 detik. 
Anda akan melihat log bahwa salah satu node akan mendapatkan tulisan `👑 MENDAPATKAN LOCK!` dan dua node lainnya akan mengeluarkan pesan gagal (skipped).
