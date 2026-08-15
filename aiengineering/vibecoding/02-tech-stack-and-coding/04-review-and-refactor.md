# 04 - Regularly Ask AI to Review and Refactor Codebase

## 🎯 Definisi & Konsep
**Regularly Review & Refactor** adalah kebiasaan menyisipkan sesi khusus di mana Anda menginstruksikan AI untuk meninjau ulang (*code review*) dan membersihkan (*refactor*) seluruh atau sebagian modul sebelum menambahkan fitur baru.

AI cenderung mengambil "jalur paling mudah" saat memecahkan masalah (seperti menumpuk kode, membuat duplicate helpers, atau mengabaikan pembersihan memori). Sesi refactoring rutin mencegah penumpukan utang teknis (*technical debt*).

---

## 🛠️ Kapan Harus Melakukan Refactoring?
- **Setelah menyelesaikan 1 Fase / Milestone**.
- **Ketika satu file mulai melebihi 250 baris**.
- **Sebelum memulai pengerjaan fitur besar berikutnya**.

---

## 💬 Contoh Prompt Sesi Refactoring

### Prompt Code Review & Code Smell Check:
```text
Tolong lakukan Code Review menyeluruh pada folder `src/services/`. 
Cari:
1. Kode mati (dead code / unused imports / unused variables).
2. Duplikasi logika yang bisa diekstrak ke shared utility.
3. Potensi masalah performa atau unhandled promise rejections.
Berikan daftar rekomendasi perbaikannya terlebih dahulu tanpa mengubah kode.
```

### Prompt Eksekusi Refactor:
```text
Berdasarkan daftar rekomendasi nomor 1 dan 2 dari review tadi, tolong lakukan refactoring sekarang. 
Pastikan semua pengujian (tests) tetap pass setelah refactoring selesai.
```
