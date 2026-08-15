# 03 - Keep Code Modular & Aim for Smaller Files

## 🎯 Definisi & Konsep
**Keep Code Modular** adalah instruksi eksplisit kepada AI agar tidak membuat file monolithic raksasa (misal file 800 baris yang berisi komponen UI, API call, state, dan styling sekaligus), melainkan memecahnya menjadi file-file kecil yang berfokus pada 1 tanggung jawab tunggal (*Single Responsibility Principle*).

---

## 🛠️ Mengapa File Kecil Sangat Penting dalam Vibe Coding?
1. **Batas Context Window & Token Cost**: File berukuran > 500 baris menghabiskan token saat AI membacanya dan meningkatkan risiko kesalahan saat mengedit (*edit collision*).
2. **Keterbacaan**: File kecil (di bawah 150-200 baris) jauh lebih mudah dipahami oleh manusia maupun AI.
3. **Pemberian Instruksi Presisi**: Anda dapat memberi instruksi khusus pada file kecil tertentu tanpa mempengaruhi logika di file lainnya.

---

## 📐 Batasan Ideal Struktur Modul
- **Komponen UI**: Max 100 - 150 baris per file.
- **Custom Hooks / Helper**: Max 80 - 100 baris per file.
- **Route Handlers / API Controllers**: Max 100 baris per file.

---

## 💬 Contoh Prompt untuk Modularisasi
```text
File `Dashboard.tsx` saat ini sudah terlalu panjang (450 baris). 
Tolong lakukan modularisasi:
1. Pisahkan bagian Header menjadi `src/components/dashboard/DashboardHeader.tsx`.
2. Pisahkan bagian Chart menjadi `src/components/dashboard/AnalyticsChart.tsx`.
3. Pisahkan kueri data ke custom hook `src/hooks/useDashboardData.ts`.
4. Pastikan file `Dashboard.tsx` utama hanya menjadi container yang bersih.
```
