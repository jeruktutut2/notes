# 03 - Based on Previous Coding Sessions, Tell AI What NOT to Do

## 🎯 Definisi & Konsep
**Negative Prompting (Batas Larangan)** adalah mengarahkan AI dengan menentukan hal-hal atau pendekatan spesifik yang **TIDAK Boleh** dilakukan berdasarkan bug atau pola buruk yang pernah dilakukan AI pada sesi-sesi koding sebelumnya.

AI sering memiliki kecenderungan default (*default behavior*) seperti menginstall library baru padahal sudah ada utility bawaan, atau menggunakan inline styles.

---

## 🛠️ Contoh Negative Prompting

```text
Buatkan fungsi utilitas untuk menghitung selisih tanggal di `src/utils/date.ts`.

CATATAN LARANGAN (APA YANG TIDAK BOLEH DILAKUKAN):
- JANGAN install library tambahan seperti moment.js atau date-fns! Gunakan Native JavaScript `Date` atau `Intl.DateTimeFormat`.
- JANGAN gunakan `console.log` di dalam fungsi ini.
- JANGAN gunakan tipe `any`.
- JANGAN ubah file konfigurasi `tsconfig.json`.
```
