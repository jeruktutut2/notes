# 03 - For Unrelated Tasks, Proactively Clean and Start New Sessions

## 🎯 Definisi & Konsep
**Proactive Session Cleaning** adalah tindakan menutup atau mereset sesi chat aktif ketika beralih dari satu modul/tugas ke tugas lain yang tidak saling berhubungan (misal: selesai mengerjakan fitur *Database Migration* lalu ingin berpindah mengerjakan *Styling CSS Navbar*).

---

## 🛠️ Manfaat Pembersihan Sesi Proaktif
- **Menghemat Biaya Token & Kuota**: Tidak mengirimkan riwayat percakapan lama yang tidak relevan di setiap request baru.
- **Meningkatkan Kecepatan Respon**: Response time LLM menjadi jauh lebih cepat.
- **Hasil Lebih Fokus**: AI tidak akan mencoba menyambungkan masalah CSS dengan masalah database migration dari topik sebelumnya.

---

## 💬 Contoh Alur Sesi
1. *Sesi 1 (Backend API Auth)* -> Selesai -> `git commit -m "feat: complete auth api"` -> **Tutup Sesi / Clear Chat**.
2. *Sesi 2 (Frontend UI Dashboard)* -> **Buka Sesi Baru** -> Berikan prompt khusus UI dashboard.
