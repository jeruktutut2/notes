# Distributed Queue (Background Jobs)

Proyek ini mendemonstrasikan pola **Distributed Task Queue** atau *Background Processing* menggunakan Go dan Redis (via library `hibiken/asynq`).

## 🤔 Mengapa Membutuhkan Message Queue?
Jika pengguna mendaftar ke aplikasi Anda dan Anda perlu:
1. Memasukkan data ke database (100ms)
2. Membuat thumbnail avatar (3 detik)
3. Mengirim email konfirmasi (2 detik)

Jika semua dilakukan secara sinkron (langsung) di *HTTP Request*, pengguna harus menunggu **5.1 detik** hanya untuk melihat layar "Berhasil Mendaftar". Ini pengalaman pengguna (UX) yang sangat buruk.

## 💡 Solusi: Antrean Pekerjaan (Queue)
Dengan menggunakan *Task Queue*, server API hanya memasukkan data ke DB, lalu membuang "Tugas Resize" dan "Tugas Email" ke dalam **Antrean (Redis List)**, lalu langsung mengembalikan respon "Sukses" ke pengguna dalam waktu total **100ms**.

Di belakang layar (di server lain), beberapa proses **Worker** akan mengawasi antrean tersebut dan mengeksekusi tugas-tugas beratnya secara asinkron (*Background Job*).

## ✨ Fitur-fitur yang Didemonstrasikan:
1. **Immediate Task**: Tugas yang langsung diproses.
2. **Delayed Task (Scheduled)**: Tugas yang dijadwalkan untuk dieksekusi nanti (misal: 5 detik lagi).
3. **Queue Prioritization**: Menugaskan prioritas (*critical* vs *default*) agar tugas penting dikerjakan lebih dulu.
4. **Retry Mechanism**: Jika pengiriman email gagal, Worker otomatis mencoba lagi (*retry*) hingga batas maksimal.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Script akan men-set up Redis, menyalakan 1 Worker di background, dan 1 Client yang akan melempar 3 jenis tugas ke dalam Queue. Anda akan melihat eksekusi log secara riil (*real-time*).
