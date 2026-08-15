# Panduan Deploy VibeInventory (Google Apps Script)

Panduan cara memasang dan menyebarkan (*deploy*) aplikasi **VibeInventory** ke Google Apps Script (GAS) dan Google Sheets secara gratis.

---

## 🛠️ Langkah-Langkah Pemasangan (Setup)

### Langkah 1: Buat Google Sheet Baru
1. Buka [Google Sheets](https://sheets.google.com) dan buat Spreadsheet baru bernama **"VibeInventory Database"**.
2. Pada menu atas, klik **Extensions (Ekstensi)** -> **Apps Script**.

### Langkah 2: Salin Kode Backend (`Code.gs`)
1. Di editor Apps Script, hapus seluruh isi file `Code.gs` bawaan.
2. Buka file [`Code.gs`](./Code.gs) di repositori ini, salin seluruh kodenya, dan tempelkan ke editor Apps Script `Code.gs`.
3. Simpan proyek dengan menekan tombol `Ctrl + S` atau ikon disket.

### Langkah 3: Tambahkan File HTML Frontend (`Index.html`)
1. Di panel kiri Apps Script (sebelah tulisan Files / Berkas), klik tombol **`+`** (Add a file) -> pilih **HTML**.
2. Beri nama file **`Index`** (tanpa ekstensi `.html`).
3. Salin seluruh isi file [`Index.html`](./Index.html) dari repositori ini, lalu tempelkan ke dalam file `Index.html` di Apps Script.
4. Simpan proyek (`Ctrl + S`).

---

## 🚀 Langkah Deploy Web App

1. Di pojok kanan atas editor Apps Script, klik tombol **Deploy** -> **New deployment (Peluncuran baru)**.
2. Klik ikon gerigi (Select type) -> pilih **Web app**.
3. Isi konfigurasi berikut:
   - **Description**: `VibeInventory v1.0.0`
   - **Execute as (Jalankan sebagai)**: `Me (Email Anda)`
   - **Who has access (Siapa yang memiliki akses)**: `Anyone (Siapa saja)` atau `Anyone within organization`.
4. Klik tombol **Deploy**.
5. Otorisasikan izin (Authorize access) dengan akun Google Anda saat diminta.
6. Salin **Web App URL** yang dihasilkan. Buka URL tersebut di tab browser baru!

---

## 🔑 Akun Default Login

Setelah Web App dibuka, gunakan akun demo bawaan:

- **Admin Account**:
  - Username: `admin`
  - Password: `admin123`
  - Hak Akses: Stok In/Out, Tambah Barang, Audit Log, **Manajemen User Staf & Reset Password**.

- **Staff Account**:
  - Username: `staf`
  - Password: `staf123`
  - Hak Akses: Stok In (Tambah Stok), Stok Out (Kurangi Stok), & Audit Log.
