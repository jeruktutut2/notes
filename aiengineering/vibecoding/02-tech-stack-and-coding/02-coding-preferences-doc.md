# 02 - Document Style and Coding Preferences for AI

## 🎯 Definisi & Konsep
**Document Coding Preferences** adalah membuat file konfigurasi instruksi permanen (seperti `AGENTS.md`, `CLAUDE.md`, atau `.cursorrules`) di akar repositori untuk menetapkan konvensi pengkodean, standar penamaan, struktur arsitektur, dan preferensi gaya yang wajib diikuti AI.

Tanpa file panduan ini, AI akan menulis kode berdasarkan standar acak yang seringkali bertabrakan dengan gaya tim Anda.

---

## 🛠️ Contoh Isi File `AGENTS.md` / `CLAUDE.md`

```markdown
# Coding Standards & Guidelines

## Tech Stack
- Frontend: React 18, TypeScript, TailwindCSS
- State Management: React Context / Zustand
- Form Handling: React Hook Form + Zod

## Code Style Rules
- Gunakan Functional Components dengan `const ComponentName: React.FC = () => {}`.
- Gunakan TypeScript strict type. Dilarang keras menggunakan tipe `any`.
- Gunakan async/await untuk penanganan asynchronous, sertakan try-catch blok.
- Semua nama file komponen wajib PascalCase (contoh: `UserProfileCard.tsx`).
- Semua utility function diletakkan di folder `src/utils/` dan wajib diberi JSDoc comment.
- Jangan pernah menyertakan komentar berlebihan yang hanya menjelaskan sintaks dasar JS.
```

---

## 💬 Contoh Prompt Menggunakan File Preferences
```text
Sebelum membuat fitur autentikasi ini, baca dan taati seluruh aturan yang ada di AGENTS.md.
Pastikan semua tipe data menggunakan TypeScript interface yang ketat tanpa menggunakan `any`.
```
