# 04 - Install and Ask AI to Use MCP (e.g. Playwright for Browser), When Possible

## 🎯 Definisi & Konsep
**Install and Use MCP (Model Context Protocol)** adalah mengintegrasikan protokol MCP seperti Playwright Browser Automation Server atau Database Inspector MCP Server.

Dengan MCP, AI Coding Assistant tidak hanya membaca teks kode, tetapi dapat membuka browser sesungguhnya, mengklik elemen, mengambil screenshot, memeriksa log konsol browser, dan melakukan verifikasi UI secara mandiri tanpa harus menyuruh pengembang melakukannya secara manual.

---

## 💬 Contoh Penggunaan MCP Playwright
```text
Gunakan MCP Playwright Browser Tool untuk:
1. Membuka `http://localhost:3000/login`.
2. Isi field username dengan `admin` dan password `secret123`.
3. Klik tombol 'Submit'.
4. Ambil screenshot halaman setelah redirect dan periksa apakah ada error di console log browser.
```
