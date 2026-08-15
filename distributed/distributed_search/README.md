# Distributed Search (Elasticsearch)

Proyek ini mendemonstrasikan bagaimana situs web berskala besar seperti Tokopedia, Netflix, atau StackOverflow mengimplementasikan kolom pencarian (Search Bar) mereka.

## 🐌 Masalah dengan SQL Biasa (`LIKE %...%`)
Jika Anda punya tabel berisi 1 juta baris artikel, dan Anda menjalankan *query* MySQL: 
`SELECT * FROM artikel WHERE konten LIKE '%golang%'`
Maka MySQL harus membaca teks tersebut baris per baris. Ini sangat lambat (bisa bermenit-menit). Apalagi jika user salah ketik (*typo*) "golng", MySQL tidak akan menemukan apapun.

## 🚀 Solusi: Inverted Index (Elasticsearch)
Alih-alih mencari kata dalam dokumen, Elasticsearch (ES) membedah seluruh dokumen ke dalam daftar kata tunggal (Tokenization), mirip dengan **Daftar Indeks di halaman paling belakang buku cetak**.
Misal: Dokumen 1 ("Saya suka Golang"). ES mencatat:
- Saya -> Dokumen 1
- Suka -> Dokumen 1
- Golang -> Dokumen 1

Ketika Anda mencari "Golang", ES langsung melihat daftarnya dan seketika tahu bahwa kata itu ada di Dokumen 1 dalam hitungan milidetik.
Selain itu, ES juga menangani penilaian (*Scoring/Relevancy*), *typo tolerance* (Fuzzy Search), dan mencari kombinasi kata (*Multi-Match*).

## 🗄️ Terdistribusi (Distributed)
Elasticsearch secara native berarsitektur *Distributed*. Artinya, 1 juta dokumen tidak perlu disimpan di 1 server. Dokumen bisa dipecah (*Sharding*) ke 10 server Elasticsearch yang saling bekerja sama, sehingga pencarian semakin cepat karena ke-10 server tersebut akan mencari data masing-masing secara serentak (paralel) saat Anda mengirim 1 kata kunci.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menjalankan Elasticsearch, meng- *index* 4 dokumen dummy berbahasa Indonesia, lalu melakukan *query* pencarian untuk kalimat `go backend`. Anda akan melihat bagaimana Elasticsearch mampu menemukan artikel yang relevan dan memberikan "Skor Relevansi", di mana artikel yang paling cocok berada di urutan teratas.
