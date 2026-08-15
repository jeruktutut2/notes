# 01 - Leverage Long Context Window When Available and Necessary

## 🎯 Definisi & Konsep
**Leverage Long Context Window** adalah memanfaat kemampuan LLM modern yang mendukung konteks besar (misalnya 200k - 1 juta token) untuk membaca repositori utuh, dokumentasi API lengkap, atau log aplikasi yang panjang sekaligus.

Namun, konteks panjang harus digunakan dengan bijak ("needle in a haystack problem"—semakin banyak info acak ditaruh, semakin ada risiko AI mengabaikan detail kecil).

---

## 🛠️ Kapan Menggunakan Long Context Window?
- **Penyelidikan Codebase Warisan (Legacy Codebase Audit)**.
- **Membaca Dokumentasi SDK / API Baru secara Lengkap**.
- **Menganalisis Log Stack Trace Panjang**.

---

## 💬 Contoh Prompt Pemanfaatan Context Panjang
```text
Saya menyertakan seluruh dokumentasi APIPayment Gateway versi terbaru (50 halaman markdown).
Tolong baca spesifikasi ini dan buatkan adapter class `PaymentGatewayAdapter.ts` yang mengimplementasikan interface `IPaymentProcessor` kita.
```
