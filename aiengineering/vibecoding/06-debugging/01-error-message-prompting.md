# 01 - Prompt Error Messages and Let AI Do the Rest

## 🎯 Definisi & Konsep
**Prompt Error Messages** adalah menempelkan pesan kesalahan (*error message* & *stack trace*) secara utuh tanpa dipotong, beserta baris kode yang dicurigai, dan menginstruksikan AI untuk menjelaskan apa yang terjadi sebelum memberikan solusinya.

Jangan hanya meminta AI memberikan kode perbaikan! Selalu minta penjelasan sederhana tentang **mengapa error tersebut bisa terjadi**.

---

## 💬 Contoh Prompt Debugging Berbasis Error Log

```text
Aplikasi saya mengalami crash saat mencoba memanggil endpoint `/api/checkout`. 
Berikut stack trace error lengkap dari terminal:

TypeError: Cannot read properties of undefined (reading 'price')
    at calculateTotal (src/services/cartService.ts:42:21)
    at processCheckout (src/controllers/checkoutController.ts:18:12)

Berikut isi file `src/services/cartService.ts` seputar baris 42.

Tolong jelaskan:
1. Mengapa error `price of undefined` ini terjadi?
2. Bagaimana cara terbaik memperbaiki kode tersebut agar tahan terhadap nilai null/undefined (defensive programming)?
```
