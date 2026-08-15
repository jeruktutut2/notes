# Panduan Teknis: Debugging & Logging di Google Apps Script

Dokumen ini mencatat panduan lengkap mengenai teknik **Logging**, **Debugging**, dan **Peninjauan Eksekusi Kode** pada aplikasi Google Apps Script (baik sisi backend `Code.gs` maupun frontend `Index.html`).

---

## 1. Logging di Backend (`Code.gs`)

Di dalam file skrip backend `Code.gs`, Anda dapat menggunakan fungsi logging berikut:

```javascript
// 1. console.log() - Sangat Direkomendasikan (V8 Engine Modern)
console.log('User terautentikasi:', username);
console.warn('Stok barang menipis untuk ID:', itemId);
console.error('Terjadi kesalahan database:', err.toString());

// 2. Logger.log() - Fungsi Logging Legacy Bawaan Apps Script
Logger.log('Stok berhasil diperbarui');
```

### 📍 Lokasi Meninjau Log Backend:
1. Buka Editor Apps Script di browser (`script.google.com`).
2. Di panel navigasi sebelah kiri, pilih ikon 📜 **Executions (Eksekusi)**.
3. Seluruh riwayat pemanggilan fungsi backend akan tercatat secara *real-time* beserta baris `console.log()` dan `Logger.log()`.
4. Jika proyek terhubung ke Google Cloud Platform, `console.log()` otomatis terintegrasi dengan **Google Cloud Logging (Stackdriver Logs)**.

---

## 2. Logging di Frontend (`Index.html`)

Di dalam file HTML client-side `Index.html`, fungsi `console.log()` berjalan di lingkungan JavaScript browser pengguna:

```javascript
console.log('Token sesi tersimpan:', sessionToken);
console.error('Error koneksi server:', err);
```

### 📍 Lokasi Meninjau Log Frontend:
1. Buka halaman Web App di browser.
2. Tekan tombol **F12** (atau Klik Kanan ➔ *Inspect*).
3. Buka tab **Console** di Developer Tools browser.

---

## 3. Fitur Interactive Debugger (Breakpoints) 🐞

Editor Apps Script di `script.google.com` menyediakan fitur debugger interaktif berbasis breakpoint:

1. **Memasang Breakpoint**: Klik pada nomor baris kode di `Code.gs` hingga muncul titik merah 🔴.
2. **Jalankan Mode Debug**:
   - Pilih fungsi yang ingin diuji dari dropdown menu di bagian atas editor.
   - Klik tombol **Debug** (Ikon Kutu 🐞 di sebelah tombol Run).
3. **Inspeksi Variabel**: Eksekusi skrip akan berhenti di titik breakpoint. Anda dapat mengecek isi nilai variabel pada panel **Variables** & **Call Stack**.

---

## 4. Matriks Ringkasan Logging

| Jenis Logging | Lokasi Eksekusi | Lokasi Peninjauan Log |
| :--- | :--- | :--- |
| `console.log()` di `Code.gs` | Server Cloud Google | Apps Script Editor (Executions Menu) / Google Cloud Logs |
| `Logger.log()` di `Code.gs` | Server Cloud Google | Apps Script Editor (Executions Menu) |
| `console.log()` di `Index.html` | Browser Client Pengguna | Browser Developer Tools (F12) ➔ Tab Console |
| Interactive Breakpoints 🔴 | Server Cloud Google | Apps Script Editor ➔ Panel Variables & Call Stack |
