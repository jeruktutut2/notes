# ADMIN DASHBOARD

## note
    🎯 Elemen di dalam bg-white seperti text, border, icon, dll sebaiknya:
1. Teks:
Gunakan abu-abu gelap atau hitam:

text-gray-900 → teks utama

text-gray-700 → teks sekunder

text-gray-500 → teks penjelas atau deskripsi

2. Border:
Untuk pemisah antar elemen:

border-gray-200 atau border-gray-300

Jangan pakai border-black (terlalu keras)

3. Shadow:
Gunakan bayangan lembut untuk membedakan antar blok:

shadow atau shadow-sm

shadow-md untuk elemen yang aktif/muncul seperti modal atau dropdown

4. Icon / Button:
Pakai text-gray-600 atau warna branding (biru, hijau, dsb)

Gunakan hover:text-gray-800 agar terasa interaktif

✅ 1. Contoh Text Utama & Sekunder
📌 Text Utama (text-gray-900)
Digunakan untuk informasi penting, headline, atau isi utama.

html
Copy
Edit
<h1 class="text-xl font-semibold text-gray-900">Dashboard Overview</h1>
<p class="text-gray-900">Total Revenue: $24,000</p>
📎 Text Sekunder (text-gray-500 / gray-700)
Digunakan untuk label, penjelasan, atau informasi tambahan.

html
Copy
Edit
<p class="text-sm text-gray-500">Updated 2 hours ago</p>
<p class="text-sm text-gray-700">Compared to last month</p>
✅ 2. Contoh Pemisah Antar Elemen
Garis horizontal tipis:
html
Copy
Edit
<hr class="border-t border-gray-200 my-4" />
Atau dengan padding/margin:
html
Copy
Edit
<div class="mb-4">
  <label class="block text-sm text-gray-700">Email</label>
  <input type="email" class="border border-gray-300 rounded px-3 py-2 w-full" />
</div>
✅ 3. Membuat Blok Terpisah
Membedakan antar blok berarti membuat area berbeda (misal: card, section) terasa terpisah secara visual dengan:

Bayangan (shadow)

Border atau rounded

Jarak antar elemen (margin, gap)

Background berbeda jika perlu

Contoh:
html
Copy
Edit
<div class="bg-white p-4 rounded-lg shadow">
  <h2 class="text-lg font-semibold text-gray-900">User Statistics</h2>
  <p class="text-sm text-gray-500">Last 30 days</p>
</div>

<div class="bg-white p-4 rounded-lg shadow mt-4">
  <h2 class="text-lg font-semibold text-gray-900">Sales Report</h2>
  <p class="text-sm text-gray-500">Compared to previous period</p>
</div>
✅ 4. Contoh Icon/Button Interaktif
📌 Icon (menggunakan Heroicons di Nuxt):
html
Copy
Edit
<Bars3Icon class="h-6 w-6 text-gray-600 hover:text-gray-800 cursor-pointer" />
text-gray-600 → warna default

hover:text-gray-800 → warna saat hover

cursor-pointer → jadi seperti tombol

📌 Button dengan efek hover & transisi:
html
Copy
Edit
<button class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition">
  Save Changes
</button>
hover:bg-blue-700 → efek saat di-hover

transition → animasi halus saat warna berubah


max-w-md