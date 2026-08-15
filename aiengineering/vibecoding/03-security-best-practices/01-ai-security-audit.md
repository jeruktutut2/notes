# 01 - Explicitly Ask AI to Perform a Security Audit

## 🎯 Definisi & Konsep
**Explicitly Ask AI for Security Audit** adalah sesi khusus di mana Anda menugaskan AI untuk bertindak sebagai Pakar Keamanan Siber (*Cybersecurity Auditor*) untuk memindai seluruh codebase dari kerentanan umum (OWASP Top 10).

Karena AI fokus pada fungsionalitas saat pertama kali mengode, pemeriksaan keamanan terpisah sangat krusial dilakukan sebelum kode di-deploy.

---

## 🛠️ Item yang Wajib Dipindai dalam Audit
1. **Injection Flaws**: SQL Injection, Command Injection.
2. **Broken Authentication & Authorization**: Celah pada sesi token, pengecekan role user yang terlewat.
3. **Cross-Site Scripting (XSS)**: Sanitasi rendering HTML/user input.
4. **Exposure Data Sensitif**: Menampilkan password hash atau API response berlebihan.

---

## 💬 Contoh Prompt Audit Keamanan

```text
Bertindaklah sebagai Senior Application Security Engineer (AppSec). 
Lakukan audit keamanan pada file controller `src/controllers/authController.ts` dan `src/controllers/userController.ts`.

Periksa hal-hal berikut:
1. Apakah ada celah SQL Injection atau NoSQL Injection?
2. Apakah penanganan JWT Token dan password hashing sudah sesuai dengan standar industri (misal bcrypt dengan salt rounds yang cukup)?
3. Apakah ada data sensitif (seperti hashed password) yang tidak sengaja terkirim di JSON response?

Berikan laporan temuan lengkap dengan tingkat keparahan (High/Medium/Low) dan rekomendasikan perbaikan kodenya.
```
