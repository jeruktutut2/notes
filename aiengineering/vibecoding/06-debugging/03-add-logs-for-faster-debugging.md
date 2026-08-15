# 03 - Tell AI to Add Logs to Find the Bug Faster

## 🎯 Definisi & Konsep
**Tell AI to Add Logs** adalah taktik menambahkan pernyataan logging temporal (seperti `console.log`, `logger.debug`, atau print statement) pada titik-titik krusial aliran data untuk melihat nilai variabel secara nyata di konsol saat alur program berjalan.

Logging memberikan bukti empiris alih-alih asumsi tebakan.

---

## 🛠️ Alur Debugging Berbasis Log
1. Minta AI menambahkan log pernyataan pada input, pertengahan alur, dan output fungsi.
2. Jalankan ulang aplikasi dan reproduksi bug.
3. Salin konsol log yang muncul ke AI.
4. Minta AI mendiagnosis lokasi tepat di mana data menjadi invalid.
5. Hapus log sementara setelah bug terbukti teratasi.

---

## 💬 Contoh Prompt Log Injection
```text
Sistem pembayaran kita gagal tanpa mengeluarkan error di konsol.
Tolong tambahkan log `console.log` di file `paymentProcessor.ts` di:
1. Sebelum memanggil API Stripe (tampilkan payload request).
2. Di dalam catch block (tampilkan error object utuh).
3. Setelah menerima response (tampilkan status code).

Berikan kodenya sehingga saya bisa menjalankannya di terminal dan melihat hasilnya.
```
