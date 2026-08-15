# Distributed File System (Object Storage dengan MinIO)

Proyek ini menunjukkan pergeseran paradigma dari *Block Storage* (Harddisk tradisional) menjadi **Object Storage** (Skala cloud, seperti AWS S3 atau Google Cloud Storage).

## 💽 Masalah Harddisk Biasa
Jika Anda membangun aplikasi YouTube, di mana Anda menyimpan video MP4 yang diupload *user*?
Menyimpannya di harddisk lokal (misal `/var/www/uploads/`) sangat buruk:
1. Harddisk bisa penuh.
2. Jika server aplikasi ditambah (dari 1 menjadi 5 server), server ke-2 tidak bisa mengakses file video yang diupload ke server ke-1.
3. *File system* tradisional sangat lambat jika ada jutaan file dalam satu folder.

## ☁️ Solusi: Object Storage (MinIO / S3)
Penyimpanan dipisahkan sepenuhnya dari server aplikasi. Aplikasi mengakses file bukan lewat *path* folder, melainkan lewat **HTTP API**.
1. **Tidak ada hierarki folder sejati**, hanya *Bucket* dan *Object Key*.
2. **Skalabilitas Tak Terbatas**: Di *background*, sistem terdistribusi memecah video 10 GB menjadi "chunk" (potongan) kecil berukuran 5MB (Multipart Upload) lalu menyebarnya ke ratusan harddisk di berbagai *rack server* (*Erasure Coding*) sehingga tahan terhadap kerusakan *hardware*.
3. **Stateless**: Aplikasi Go kita tidak perlu peduli di mana file disimpan secara fisik.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menjalankan MinIO lokal, lalu mengeksekusi aplikasi Go kita yang menggunakan library resmi `minio-go`. Aplikasi akan otomatis membuat bucket, mengunggah sebuah file, dan mengunduhnya kembali melalui jaringan HTTP menggunakan kredensial S3 statis.
