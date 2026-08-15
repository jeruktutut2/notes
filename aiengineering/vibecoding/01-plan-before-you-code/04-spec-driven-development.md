# 04 - Implement Spec-Driven Development (SDD)

## 🎯 Definisi & Konsep
**Spec-Driven Development (SDD)** adalah pendekatan pengembangan di mana seluruh logika aplikasi, kebutuhan data, alur user, dan kontrak API didefinisikan secara eksplisit dalam dokumen spesifikasi (misalnya `spec.md` atau `requirements.md`) *sebelum* pengkodean dimulai.

Spesifikasi ini menjadi "Single Source of Truth" yang dirujuk oleh pengembang dan AI Coding Assistant sepanjang siklus proyek.

---

## 🛠️ Manfaat SDD dalam Vibe Coding
- **Mencegah Scope Creep**: AI tidak akan menambahkan fitur acak di luar dokumen spesifikasi.
- **Memudahkan Refactoring**: Saat melakukan refactoring, AI merujuk pada `spec.md` untuk memastikan fungsi tidak ada yang rusak atau hilang.
- **Reusabilitas Konteks**: Jika Anda berpindah AI agent / membuka sesi chat baru, Anda cukup melampirkan file `spec.md`.

---

## 📄 Contoh Template File `spec.md`

```markdown
# Product Specification: User Notification System

## 1. Overview
Sistem untuk mengirimkan notifikasi in-app dan email kepada pengguna ketika terjadi aktivitas akun.

## 2. Technical Stack
- Node.js + Express
- PostgreSQL (Prisma ORM)
- Resend API (Email)

## 3. Data Model
User {
  id: String (UUID)
  email: String (Unique)
  notificationPreferences: JSON
}

Notification {
  id: String (UUID)
  userId: String (FK)
  title: String
  message: String
  isRead: Boolean (Default: false)
  createdAt: DateTime
}

## 4. API Endpoints Contract
- `GET /api/notifications` -> Mengembalikan list notifikasi user yang sedang login.
- `PATCH /api/notifications/:id/read` -> Tandai notifikasi sebagai dibaca.

## 5. Non-Functional Requirements
- Response time API di bawah 200ms.
- Semua kueri wajib menggunakan transaksi aman database.
```

---

## 💬 Contoh Prompt Penggunaan SDD
```text
Bacalah file spec.md yang sudah kita setujui.
Tolong buatkan file Prisma Migration dan Schema berdasarkan Bagian 3 (Data Model) dari spec.md tersebut.
```
