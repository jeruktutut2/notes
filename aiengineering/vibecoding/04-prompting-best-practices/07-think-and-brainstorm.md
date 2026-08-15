# 07 - Explicitly Tell AI to "Think" or "Brainstorm" Before Complex Problems

## 🎯 Definisi & Konsep
**Tell AI to "Think" or "Brainstorm"** adalah teknik memaksa AI untuk melakukan analisis ruang pencarian masalah (*Chain-of-Thought reasoning*) dan membuat draf opsi pendekatan sebelum mulai menulis baris kode pertama.

Ini mencegah AI terburu-buru memberikan solusi pertama yang melintas (yang seringkali suboptimal).

---

## 💬 Contoh Prompt Think / Brainstorm

```text
Kami mengalami masalah di mana pengiriman notifikasi email sering terhenti jika ada lebih dari 500 pengguna bersamaan.

Tolong JANGAN tulis kode dulu. 
1. Pikirkan dan analisis (Think & Brainstorm) 3 pendekatan arsitektur berbeda untuk menangani antrean email (background queue) ini.
2. Bandingkan kelebihan dan kekurangan masing-masing opsi (misal: Redis + BullMQ vs AWS SQS vs Database-backed Queue).
3. Rekomendasikan mana solusi yang paling efisien untuk tech stack kita.
```
