# 03 - When You Find a Bug, Ask AI to Write a Breaking Test and Then Fix

## 🎯 Definisi & Konsep
**Write a Breaking Test for Bugs** adalah praktik di mana setiap kali pengembang menemukan bug di produksi atau aplikasi lokal, langkah pertama **bukanlah** langsung memperbaiki kodenya, melainkan menginstruksikan AI untuk mereproduksi bug tersebut ke dalam sebuah pengujian yang sengaja dibuat **gagal (breaking test)**.

---

## 🛠️ Mengapa Metode Ini Sangat Efektif?
1. **Mencegah Regresi**: Pengujian ini akan selamanya menjadi bagian dari test suite repositori. Bug yang sama tidak akan pernah muncul kembali tanpa tertangkap CI/CD.
2. **Klarifikasi Masalah untuk AI**: Membuat test yang membuktikan bug memaksa AI untuk memahami ekspektasi output vs kenyataan yang salah secara eksplisit.

---

## 💬 Contoh Prompt Breaking Test

```text
Pengguna melaporkan bug: Saat mereka memasukkan nama dengan tanda petik (misal: "O'Connor"), sistem melempar error HTTP 500.

Langkah pengerjaan:
1. Buatkan test case baru di `tests/userRegistration.test.ts` yang mencoba meregistrasi user bernama "O'Connor".
2. Jalankan test tersebut dan tunjukkan bahwa test tersebut FAIL (Breaking Test).
3. Setelah terbukti FAIL, perbaiki kode di `src/services/userService.ts` hingga test tersebut PASS.
```
