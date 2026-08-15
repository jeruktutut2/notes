# 01 - Plan What You Need to Develop (MVP & Different Phases)

## 🎯 Definisi & Konsep
**Plan MVP & Phases** adalah proses membatasi ruang lingkup (scope) fitur yang akan dibangun pada tahap awal (Minimum Viable Product) dan membaginya menjadi beberapa fase eksekusi logis.

Dalam Vibe Coding, meminta AI membuat seluruh aplikasi kompleks dalam 1 prompt adalah penyebab utama kegagalan (*hallucination*, *missing components*, & kode berantakan).

---

## 🛠️ Aturan Praktis
1. **Fokus pada Core Value**: Tentukan 1-2 fitur utama yang harus ada agar aplikasi berjalan.
2. **Pisahkan Fitur Sekunder**: Fitur seperti autentikasi kompleks, tema dark mode, atau analisis analytics dimasukkan ke Fase 2 atau 3.
3. **Dokumentasikan Rencana**: Minta AI untuk menulis dokumen rencana (misal `plan.md` atau `architecture.md`) di dalam repositori.

---

## 💬 Contoh Prompt AI

### Prompt Perencanaan MVP:
```text
Saya ingin membangun aplikasi "Task Tracker untuk Freelancer". 
Tolong bantu saya merencanakan fitur Minimum Viable Product (MVP) dan bagi pengembangannya ke dalam 3 fase.
Jangan tulis kode dulu. Buatkan outline dokumen rencana dalam bentuk markdown.
```

### Output Harapan AI:
```markdown
# Rencana Pengembangan Task Tracker

## Fase 1: MVP (Core Functions)
- Tambah, edit, hapus tugas (CRUD sederhana)
- Penanda status: To Do, In Progress, Done
- Penyimpanan lokal (LocalStorage / SQLite)

## Fase 2: Manfaat Tambahan
- Kategori proyek & Klien
- Timer pelacak waktu pengerjaan

## Fase 3: Integrasi & Polishing
- Autentikasi user
- Laporan ekspor PDF/CSV
```
