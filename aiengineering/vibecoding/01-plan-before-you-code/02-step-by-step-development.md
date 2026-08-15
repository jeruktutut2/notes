# 02 - Work Step-by-Step (Incremental Building)

## 🎯 Definisi & Konsep
**Work Step by Step** adalah metodologi eksekusi di mana pengembang menginstruksikan AI untuk membangun aplikasi satu langkah kecil demi satu langkah, menguji hasilnya di setiap tahap, sebelum berlanjut ke langkah berikutnya.

---

## 🛠️ Mengapa Langkah Ini Penting?
- **Mengurangi Bug**: Jika ada masalah pada suatu tahap, Anda langsung tahu penyebabnya adalah perubahan kecil baru tersebut.
- **Mudah Di-rollback**: Jika AI salah arah pada langkah ke-3, Anda cukup melakukan revert ke commit langkah ke-2 tanpa kehilangan seluruh pekerjaan.
- **Menghemat Token & Waktu**: AI tidak perlu membaca/menulis ulang seluruh codebase setiap kali ada perubahan.

---

## 💬 Contoh Skenario & Prompt

### Skenario: Membangun Sistem E-Commerce Sederhana

❌ **Pendekatan Salah (All-in-One Prompt)**:
> "Buatkan e-commerce dengan katalog produk, keranjang belanja, checkout Stripe, dan dashboard admin."

✅ **Pendekatan Vibe Coding (Step-by-Step)**:

**Langkah 1 (Katalog Produk Sederhana)**:
```text
Berdasarkan rencana di plan.md, mari kita kerjakan Fase 1 - Langkah 1.
Buatkan UI komponen katalog produk yang menampilkan list produk statis dari file JSON mock.
Belum perlu fungsi keranjang atau backend.
```

*(Uji & Verifikasi Komponen di Browser/Terminal)*

**Langkah 2 (State Keranjang Belanja)**:
```text
Langkah 1 sudah selesai dan berjalan baik. Sekarang mari kita tambahkan fitur state management untuk Keranjang Belanja. 
Pengunjung bisa menekan tombol "Add to Cart" dan jumlah item di header berakumulasi.
```
