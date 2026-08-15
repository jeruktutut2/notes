# Distributed Computing (MapReduce Pattern)

Proyek ini mendemonstrasikan bagaimana menyelesaikan komputasi super besar (misal: menghitung jumlah kata dari ratusan buku berukuran Terabyte) dengan cara memecah pekerjaannya ke banyak komputer (Distributed Computing) menggunakan algoritma **MapReduce** (dipopulerkan oleh Google).

## 🧠 Konsep MapReduce
1. **Master Node**: Bos yang bertugas membagikan pekerjaan. Dia tahu ada berapa file yang harus diproses.
2. **Worker Nodes**: Para pekerja. Jika ada 100 pekerja, pekerjaan akan selesai 100x lebih cepat.
3. **Fase MAP**: Master memberikan 1 file ke 1 pekerja. Pekerja menghitung kata di file tersebut, lalu melaporkan hasilnya.
4. **Fase REDUCE**: Setelah *semua* fase Map selesai, Master menyuruh pekerja untuk menjumlahkan semua hasil dari fase Map tadi menjadi 1 hasil akhir.

## 🔌 RPC (Remote Procedure Call)
Dalam proyek ini, Master dan Worker tidak berkomunikasi lewat HTTP REST (karena HTTP lambat dan ada overhead). Mereka berkomunikasi lewat koneksi TCP menggunakan **RPC**. RPC memungkinkan program Go di komputer Worker untuk mengeksekusi fungsi Go di komputer Master seolah-olah fungsi itu berada di komputer yang sama.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menyalakan 1 Master dan 3 Worker (A, B, C).
Anda akan melihat Master membagi-bagikan 3 `Map Task` secara adil kepada Worker A, B, dan C. Begitu ketiganya selesai melapor, Master akan menunjuk salah satu Worker yang nganggur untuk mengerjakan `Reduce Task`. Setelah Reduce selesai, Master akan membubarkan semua Worker.
