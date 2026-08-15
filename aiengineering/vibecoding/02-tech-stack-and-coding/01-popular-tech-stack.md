# 01 - Pick a Popular Tech Stack Rather Than New/Niche Ones

## 🎯 Definisi & Konsep
**Pick a Popular Tech Stack** adalah prinsip memilih bahasa pemrograman, framework, dan library yang sudah mapan dan memiliki populasi penggunaan besar di industri (seperti Next.js, Express, React, Python/FastAPI, TailwindCSS, PostgreSQL).

---

## 🛠️ Mengapa Stack Populer Sangat Penting untuk Vibe Coding?

1. **Volume Data Pelatihan LLM**: Model AI (Claude, GPT-4, Gemini) dilatih dari miliaran baris kode di GitHub dan internet. Semakin populer library tersebut, semakin sedikit bug / hallucinatory syntax yang diproduksi AI.
2. **Ketersediaan Solusi Error**: Jika terjadi bug pada library populer, solusi dan solusi alternatifnya sudah umum dikenali oleh AI.
3. **Kompatibilitas Tools**: Tools pelengkap seperti linter, MCP server, dan debugger AI bekerja optimal pada ekosistem populer.

---

## 📊 Perbandingan Stack

| Kategori | Stack Populer (Sangat Direkomendasikan) | Stack Niche/Baru (Hindari untuk Vibe Coding Cepat) |
|---|---|---|
| **Frontend** | React / Next.js / Vue.js | Framework JS eksperimental baru rilis 2 bulan lalu |
| **Styling** | Vanilla CSS / TailwindCSS | Custom CSS pre-processor eksotik tanpa dokumentasi umum |
| **Backend** | Node.js (Express/Hono) / Python (FastAPI) | Bahasa/Framework backend eksoterik yang jarang dipakai |
| **Database** | PostgreSQL / SQLite (Prisma/Drizzle ORM) | Custom DB kustom tanpa ORM standar |

---

## 💬 Contoh Prompt Instruksi Tech Stack
```text
Kita akan membangun proyek web dashboard ini menggunakan React 18 (TypeScript), Vite, TailwindCSS, dan Zustand untuk state management.
Gunakan hanya library baku dan populer dari ekosistem React ini. Jangan install npm package yang jarang terdengar atau tidak dipelihara lagi.
```
