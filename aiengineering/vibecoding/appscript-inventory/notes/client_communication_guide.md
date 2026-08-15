# Panduan Komunikasi Klien: Menyampaikan Batasan & Kapasitas Aplikasi Google Apps Script

Dokumen ini berisi panduan praktis, strategi framing, analogi, serta **template komunikasi siap pakai** untuk menjelaskan batasan teknis Google Apps Script (GAS) kepada klien non-teknis secara profesional dan transparan.

---

## 1. Strategi & Mindset Komunikasi

Saat menjelaskan batasan teknis ke klien, gunakan prinsip **Value-Driven Positioning**:
- **Jangan sebut sebagai "Kelemahan" atau "Keterbatasan Sistem"**.
- **Bahasakan sebagai "Kapasitas Maksimal Solusi Efisien & Hemat Biaya"**.

### Poin Nilai Tambah yang Harus Ditekankan:
1. **Nol Biaya Server Bulanan**: Klien tidak perlu membayar sewa server cloud (AWS/DigitalOcean $20–$100/bulan).
2. **Nol Perawatan (Zero Maintenance)**: Tidak perlu biaya maintenance server, perpanjangan SSL, atau backup database manual.
3. **Kepemilikan Data Penuh**: Data tersimpan langsung di Google Drive / Google Sheets akun perusahaan klien sendiri.

---

## 2. Analogi Sederhana untuk Klien Non-Teknis

Gunakan analogi kendaraan untuk memberikan pemahaman intuitif tanpa istilah teknis rumit:

> 🚗 **Analogi Mobil MPV vs Bus Pariwisata**:
> *"Sistem berbasis Google Apps Script ini ibarat **Mobil MPV Keluarga (seperti Avanza)**. Sangat efisien, hemat biaya (tidak ada sewa bensin/server bulanan), dan sangat pas untuk operasional harian tim 5–50 orang. Namun, mobil ini tentu bukan dirancang untuk mengangkut beban berat sekelas **Truk Tronton atau Bus Pariwisata 1.000 penumpang**."*

---

## 3. Template Komunikasi Siap Pakai

### 3.1. Opsi A: Format Bahasa Profesional (Proposal / Proposal Kontrak)

```markdown
### Lingkup Kapasitas & Spesifikasi Solusi

Aplikasi ini dibangun menggunakan arsitektur **Google Apps Script (Serverless Enterprise)** yang terintegrasi langsung dengan ekosistem Google Workspace perusahaan Anda.

#### Keunggulan Solusi:
- **Zero Server Cost**: Aplikasi berjalan 100% bebas biaya sewa server bulanan.
- **Data Transparency**: Data transaksi tersimpan aman dan transparan di Google Sheets perusahaan Anda.

#### Spesifikasi Kapasitas Operasional:
- **Pengguna Simultan**: Dirancang optimal untuk penggunaan tim internal (hingga 30 pengguna aktif bersamaan di detik yang sama).
- **Volume Data**: Berjalan sangat cepat dan stabil untuk skala data hingga 500.000 transaksi.

*Catatan: Apabila di masa depan operasional bisnis berkembang pesat hingga membutuhkan ribuan pengguna umum secara bersamaan, sistem ini dirancang modular sehingga dapat di-upgrade (migrasi) ke arsitektur Dedicated Cloud Server.*
```

---

### 3.2. Opsi B: Format Bahasa Diskusi / Chat Santai

> *"Pak/Bu, untuk tahap ini kita gunakan teknologi **Google Apps Script**. Kelebihan utamanya adalah **bapak/ibu tidak perlu mengeluarkan biaya bulanan untuk sewa server**, dan datanya langsung masuk ke Google Sheet kantor.*
>
> *Secara kapasitas, sistem ini sangat aman dan cepat untuk dipakai operasional tim harian kita (sampai puluhan user bersamaan dan ratusan ribu data).*
> 
> *Namun perlu dicatat, sistem ini memang didesain untuk kebutuhan internal kantor, bukan untuk aplikasi publik skala raksasa yang dipakai ribuan orang bersamaan di detik yang sama. Jadi solusinya sangat pas dan efisien untuk kebutuhan operasional saat ini."*

---

## 4. Draft Klausul Perjanjian Kontrak / PRD

Untuk melindungi pengembang dari potensi komplain di kemudian hari akibat beban trafik melebihi kapasitas standar, sertakan klausul ini dalam Perjanjian Kerja / PRD:

```text
Klausul Kapasitas & Batasan Operasional Sistem:
Sistem dikembangkan menggunakan arsitektur Google Apps Script dengan batas kapasitas rekomendasi:
1. Maksimal 30 eksekusi request simultan di detik yang sama.
2. Maksimal 1.000.000 sel data per tabel Google Sheets.
3. Maksimal waktu pemrosesan skrip 6 menit per eksekusi tunggal.

Penambahan kapasitas yang melebihi batas standar Google Apps Script memerlukan pengembangan tahap lanjut (System Upgrade / Migrasi) ke Dedicated Cloud Server & SQL Database yang akan disepakati dalam Addendum terpisah.
```
