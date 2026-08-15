# 03 - Illustrate AI with Examples (Mockups, Code Samples, Images)

## 🎯 Definisi & Konsep
**Illustrate AI with Examples** adalah teknik memberikan contoh konkret (seperti sketsa wireframe, gambar UI, cuplikan kode rujukan, atau sampel JSON response) kepada AI sebelum meminta AI menghasilkan kode.

Satu contoh gambar atau sampel JSON bernilai 1.000 kata instruksi instruksional.

---

## 🛠️ Jenis Input Contoh yang Efektif
1. **Mockup / Gambar UI**: Screenshot dari desain Figma, sketsa di kertas, atau referensi website lain.
2. **Sampel JSON / Payload API**: Contoh struktur data yang diharapkan.
3. **Code Sample Rujukan**: Contoh pattern penulisan fungsi atau arsitektur yang Anda sukai dari proyek lain.

---

## 💬 Contoh Prompt & Penggunaan

### Contoh 1: Menggunakan Screenshot Mockup
```text
Lihat gambar mockup dashboard yang saya unggah [dashboard_mockup.png].
Tolong buatkan komponen Layout React + TailwindCSS yang memiliki sidebar di sebelah kiri dan statistik card di bagian atas seperti gambar tersebut.
```

### Contoh 2: Menggunakan Sampel JSON Data
```text
Saya ingin membuat fungsi formatter data. Berikut contoh format JSON input dari API:
{
  "user_id": "USR-102",
  "meta": { "first_name": "Budi", "last_name": "Santoso" },
  "orders": [{ "id": 1, "amount": 150000 }]
}

Buatkan fungsi TypeScript `parseUserProfile(data)` yang mengubah JSON tersebut menjadi object DTO berikut:
{
  "id": "USR-102",
  "fullName": "Budi Santoso",
  "totalOrderValue": 150000
}
```
