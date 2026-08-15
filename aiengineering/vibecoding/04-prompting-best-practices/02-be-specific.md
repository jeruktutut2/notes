# 02 - Be Specific About What You Want vs High-Level Vague Instructions

## 🎯 Definisi & Konsep
**Be Specific** adalah kebiasaan menyertakan detail teknis yang jelas (nama file, tipe data, return value, library yang digunakan, dan constraint) daripada memberikan instruksi tingkat tinggi yang samar (*vague*).

---

## 🛠️ Perbandingan Contoh

❌ **Samar (Vague)**:
> "Buatkan halaman login yang bagus dan aman."

✅ **Spesifik (Vibe Coding Standard)**:
> "Buatkan halaman login pada file `src/pages/Login.tsx`. 
> Gunakan TailwindCSS dengan latar belakang `bg-slate-900` dan card `bg-slate-800`. 
> Tambahkan input field Email dan Password, serta tombol 'Sign In'. 
> Panggil fungsi `loginUser(email, password)` dari `@/services/auth`. 
> Jika terjadi error, tampilkan alert merah di bawah tombol submit."

---

## 💡 Elemen Kunci Instruksi Spesifik
1. **Lokasi File Target**: `src/components/...`
2. **Konteks Library**: "Gunakan Axios / Fetch / TanStack Query..."
3. **State & Error Handling**: "Tampilkan loading spinner saat status `isSubmitting`..."
