# 02 - If Errors Persist, Ask AI to Create a List of Possible Causes

## 🎯 Definisi & Konsep
**List Possible Causes** adalah teknik meminta AI untuk memproduksi hipotesis analisis akar masalah (*Root Cause Analysis*) yang berisi beberapa skenario penyebab potensial ketika sebuah kesalahan terus berulang meski sudah dicoba diperbaiki.

Ini menggeser pola pikir dari sekadar "menebak-nebak perbaikan" menjadi "hipotesis yang teruji".

---

## 💬 Contoh Prompt Analisis Penyebab

```text
Perbaikan sebelumnya masih belum menyelesaikan masalah CORS error ini di environment staging.

JANGAN langsung berikan kode baru. 
Tolong buatkan daftar 4 kemungkinan penyebab utama (Root Causes) mengapa error ini bisa terjadi (misal: urutan middleware Express, konfigurasi reverse proxy NGINX, header wildcard, atau opsi preflight request OPTIONS).

Urutkan dari yang paling mungkin terjadi hingga yang paling jarang.
```
