# Modul 03: Security Best Practices

> **"Never Hardcode your Secrets"** — Jangan sekali-kali membiarkan AI menaruh password, API key, atau token secara langsung di dalam kode. Gunakan environment variables.

---

## 📌 Definisi Umum
**Security Best Practices** dalam Vibe Coding adalah kumpulan disiplin untuk memastikan aplikasi yang dibuat bersama AI bebas dari celah keamanan kritis (seperti kebocoran credential, SQL Injection, XSS, dan salah konfigurasi CORS).

AI tidak secara otomatis memprioritaskan keamanan kecuali Anda menginstruksikannya secara eksplisit.

---

## 📄 Daftar Sub-Topik & Panduan Praktis

1. [📂 `01-ai-security-audit.md`](./01-ai-security-audit.md)
   - Meminta AI melakukan audit keamanan aplikasi secara spesifik.
2. [📂 `02-never-hardcode-secrets.md`](./02-never-hardcode-secrets.md)
   - Larangan keras hardcode rahasia/credentials dan penggunaan `.env`.

---

## 🛡️ Checklist Keamanan Cepat
- [ ] Tidak ada API Key / Secret Token terikat di file JS/TS.
- [ ] File `.env` sudah masuk ke `.gitignore`.
- [ ] Semua input pengguna di-sanitize (menggunakan Zod / OWASP practices).
- [ ] AI diminta melakukan audit keamanan sebelum release.
