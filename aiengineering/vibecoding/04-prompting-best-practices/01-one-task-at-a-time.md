# 01 - Ask for One Task at a Time Rather Than Five Items

## 🎯 Definisi & Konsep
**One Task at a Time** adalah aturan membagi permintaan menjadi instruksi tunggal yang berfokus pada satu item pekerjaan spesifik, daripada menumpuk 5 instruksi atau fitur berbeda dalam satu kali pengiriman prompt.

---

## 🛠️ Perbandingan Efektivitas

❌ **BURUK (Multi-tasking Prompt)**:
```text
Tolong buatkan form registrasi user, sekalian hubungkan ke database PostgreSQL, buatkan validation schema dengan Zod, kirim email konfirmasi pakai Resend, dan tambahkan animasi toaster di UI saat sukses.
```
*Risiko: AI akan kehilangan fokus pada detail keamanan auth, lupa memasukkan error handling email, atau membuat kode setengah jadi.*

✅ **BENAR (Single Tasking Iteratif)**:

**Prompt 1**:
```text
Mari buat skema validasi Zod untuk form registrasi user di `src/schemas/authSchema.ts`. 
Form membutuhkan email, password (min 8 karakter + 1 angka), dan nama lengkap.
```
*(Cek & Verifikasi Schema)*

**Prompt 2**:
```text
Sekarang gunakan `authSchema.ts` tersebut di komponen `src/components/RegisterForm.tsx` untuk menangani submit form.
```
