# 04 - Once Tests are in Place, Refactor Regularly

## 🎯 Definisi & Konsep
**Refactor Safely with Tests** adalah melakukan pembersihan, penyederhanaan, dan pengoptimalan kode secara agresif dengan percaya diri penuh karena ada jaring pengaman berupa *test suite* otomatis.

Jika pengujian sudah 100% PASS sebelum refactor, dan tetap 100% PASS setelah refactor, Anda yakin 100% bahwa perubahan arsitektur tersebut tidak merusak fungsionalitas produk.

---

## 💬 Contoh Prompt Refactoring Berbasis Test

```text
Seluruh unit test dan E2E test di folder `tests/` saat ini berstatus PASS (100% hijau).

Tolong lakukan refactoring pada modul `src/services/paymentService.ts`:
1. Sederhanakan blok nested `if-else` menjadi pola Guard Clauses / Early Returns.
2. Optimalkan performa eksekusi kueri data.

Setelah refactoring selesai, jalankan `npm test` kembali. 
Refactoring hanya dianggap sukses jika seluruh test tetap berstatus PASS tanpa ada satu pun yang pecah.
```
