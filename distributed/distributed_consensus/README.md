# Distributed Consensus & Leader Election (etcd)

Proyek ini mendemonstrasikan bagaimana sekumpulan server *Microservices* yang identik/setara (*Peer-to-Peer*) dapat **bersepakat** untuk menunjuk 1 server sebagai **Leader** (Pemimpin), sementara sisanya menjadi pengikut (*Follower/Standby*).

## 🤔 Mengapa Butuh Leader Election?
Misalkan Anda punya sistem yang menagih tagihan kartu kredit (*Billing System*). Sistem ini di-*deploy* ke 5 server untuk berjaga-jaga jika ada server yang mati (*High Availability*).

Namun, jika kelimanya berjalan bersamaan, tagihan nasabah bisa terpotong 5 kali! Kita butuh kepastian bahwa **hanya ada 1 server yang bekerja (Active)**, sementara 4 lainnya hanya diam menonton (*Standby/Passive*).
Jika server yang *Active* mendadak mati/terbakar, keempat server yang *Standby* harus langsung sadar dan **mengadakan pemilu secara otomatis** untuk memilih Leader pengganti dalam hitungan milidetik.

## 🧠 Solusi: Konkurensi dengan `etcd`
`etcd` adalah database kunci-nilai terdistribusi yang sangat kokoh (digunakan sebagai otak dari Kubernetes).
Dengan fitur `concurrency` (Election) bawaan `etcd`, proses pemilihan Leader ini menjadi sangat mudah di Go:
- Semua Node memanggil fungsi `Campaign()`.
- Node yang datang pertama (mendapat *Lock* dari etcd) akan lanjut mengeksekusi baris kode di bawahnya (sebagai Leader).
- Node lainnya akan **terblokir** (menggantung/menunggu di fungsi `Campaign()`).
- Jika sang Leader mati (koneksi terputus/lease *expired*) atau secara sadar memanggil `Resign()`, etcd akan langsung melepaskan blokiran dari Node pengantre nomor urut dua, menobatkannya sebagai Leader baru.

## 🚀 Cara Menjalankan & Menguji
```bash
chmod +x run_all_tests.sh
./run_all_tests.sh
```
Skrip akan menjalankan etcd dan **3 Node**. Anda akan melihat bagaimana ketiga node tersebut berebut. Node pertama akan mendapat status 👑 LEADER dan bekerja selama 10 detik, sementara 2 node lain menahan diri (mengantre). Begitu node pertama selesai (resign), node kedua langsung sadar dan mengambil alih jabatan.
