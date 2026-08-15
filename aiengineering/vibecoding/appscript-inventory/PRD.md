# Product Requirement Document (PRD): GAS Inventory & User Management System

**Nama Produk**: VibeInventory (Google Apps Script Inventory & Stock Management System)  
**Platform**: Google Apps Script (GAS) Web App + Google Sheets Database  
**Versi**: 1.0.0  
**Status**: Approved  
**Tanggal**: 26 Juli 2026  
**Penulis**: Vibe Coding Core Team  

---

## 1. Executive Summary & Goals

### 1.1 Problem Statement
Banyak bisnis dan tim operasional membutuhkan sistem manajemen stok barang yang cepat, murah, dan mudah diakses tanpa harus menginstal database server kompleks. **Google Sheets** digemari sebagai basis data, namun mengedit sheet secara langsung rawan kesalahan manusia (data terhapus acak, stok diubah tanpa catat transaksi, tidak ada proteksi autentikasi user).

### 1.2 Product Objectives
- Menyediakan Web App interaktif berbasis **Google Apps Script (GAS)** yang terhubung langsung ke Google Sheets.
- Menyediakan **Manajemen User dengan Password Hashing (SHA-256)** untuk autentikasi aman tanpa menyimpan password teks biasa (*plain text*).
- Menyediakan fitur **Penambahan Stok (Stock In)** dan **Pengurangan Stok (Stock Out)** lengkap dengan pengecekan stok minimal (tidak boleh minus) serta catatan transaksi.
- Menjaga **Audit Log Transaksi** otomatis setiap kali stok berubah.

---

## 2. Target Users & Roles

1. **Admin**:
   - Memiliki akses penuh mengelola inventori (tambah barang, edit stok, hapus barang).
   - Memiliki hak akses khusus **Manajemen User** (membuat akun staf baru, mengubah password user, dan menghapus akun staf).
2. **Staff / Kasir / Petugas Gudang**:
   - Melakukan entri Penambahan Stok (Stock In) barang masuk dari supplier.
   - Melakukan entri Pengurangan Stok (Stock Out) barang keluar untuk penjualan/pemakaian.
   - Membaca daftar stok terkini tanpa akses manajemen akun user.

---

## 3. Detailed Technical & Feature Specifications

### 3.1 Authentication & Security (`Code.gs`)
- **Password Hashing**: Menggunakan `Utilities.computeDigest(Utilities.DigestAlgorithm.SHA_256, password)` untuk mengubah password plaintext menjadi String Hex Hash SHA-256.
- **Sesi Login**: Web App menggunakan token sesi berbasis `PropertiesService.getUserProperties()` atau token enkripsi lokal di `Index.html` (LocalStorage) yang membawa status role user.

### 3.2 Database Schema (Google Sheets Sheets)
Aplikasi secara otomatis membuat 3 tab sheet utama pada Google Sheets terhubung:

#### A. Sheet `Users`
| Column | Type | Description |
|---|---|---|
| `user_id` | String (UUID) | ID Unik Pengguna |
| `username` | String | Username unik (misal: `admin`, `budi_gudang`) |
| `password_hash` | String | SHA-256 Hash Hex |
| `full_name` | String | Nama lengkap pengguna |
| `role` | String | `ADMIN` atau `STAFF` |
| `created_at` | String | Tanggal akun dibuat |

#### B. Sheet `Items`
| Column | Type | Description |
|---|---|---|
| `item_id` | String (BRG-101) | Kode Barang Unik |
| `item_name` | String | Nama Barang |
| `category` | String | Kategori (misal: Elektronik, Alat Tulis) |
| `stock` | Number | Jumlah stok terkini |
| `min_stock` | Number | Batas minimal stok untuk alert warning |
| `unit` | String | Satuan (Pcs, Box, Kg) |
| `updated_at` | String | Waktu pembaruan stok terakhir |

#### C. Sheet `StockTransactions`
| Column | Type | Description |
|---|---|---|
| `trx_id` | String (TRX-xxxx) | ID Unik Transaksi |
| `item_id` | String | Kode Barang |
| `type` | String | `STOCK_IN` atau `STOCK_OUT` |
| `quantity` | Number | Jumlah barang yang ditambah/dikurangi |
| `notes` | String | Catatan transaksi (misal: Penerimaan dari supplier X / Penjualan #102) |
| `actor` | String | Username pelaksana |
| `timestamp` | String | Waktu transaksi |

### 3.3 WhatsApp Integration Specifications
- **Click-to-WhatsApp Sharing**: Fitur berbagi informasi stok barang, order reorder supplier, dan bukti transaksi melalui URL `https://wa.me/` terformat otomatis.
- **Backend WA Helper**: Helper function `sendWhatsAppNotification()` di `Code.gs` untuk mendukung opsi otomatisasi notifikasi via WhatsApp Gateway API.
- **Floating Contact Widget**: Akses cepat kontak bantuan Admin / Helpdesk via WhatsApp di antarmuka Web App (`Index.html`).

---

## 4. Acceptance Criteria (Kriteria Penerimaan)

- [x] Fungsi `doGet()` di `Code.gs` merender antarmuka `Index.html` dengan tepat.
- [x] Login pengguna memverifikasi SHA-256 hash password dan membedakan akses Admin vs Staff.
- [x] Pengurangan stok barang gagal (reject) dengan pesan error jika jumlah yang dikurangi melebihi stok yang tersedia.
- [x] Setiap penambahan atau pengurangan stok dicatat otomatis ke sheet `StockTransactions`.
- [x] Admin dapat menambah staf baru dan mengubah password staf melalui menu Manajemen User.
- [x] Fitur WhatsApp Integration (Share Info Barang, Reorder Supplier, Struk WA, & Floating Widget Support) aktif dan berfungsi di Web App.
