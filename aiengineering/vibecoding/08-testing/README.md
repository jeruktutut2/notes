# Modul 08: Testing

> **"Force AI To Test by Default"** — Perilaku standar sebagian besar AI tools menghasilkan kode yang hanya mengutamakan implementasi fungsional dengan cakupan pengujian (test coverage) minimal. Setiap kali AI membangun fitur, paksa AI untuk langsung menulis pengujian dasar.

---

## 📌 Definisi Umum
**Testing** dalam Vibe Coding adalah elemen kunci yang menjamin aplikasi tetap stabil meskipun kode terus dibuat dan diubah secara otomatis oleh AI. Tanpa pengujian otomatis (Unit, Integration, dan End-to-End Tests), Anda tidak akan pernah yakin apakah fitur baru yang dibuat AI merusak fitur lama (*regression*).

---

## 📄 Daftar Sub-Topik & Panduan Praktis

1. [📂 `01-ai-test-generation.md`](./01-ai-test-generation.md)
   - Meminta AI membuat pengujian otomatis (Unit Test & E2E Test) untuk kestabilan produk.
2. [📂 `02-test-driven-development.md`](./02-test-driven-development.md)
   - Mempertimbangkan pendekatan Test-Driven Development (TDD) bersama AI.
3. [📂 `03-breaking-tests-for-bugs.md`](./03-breaking-tests-for-bugs.md)
   - Ketika menemukan bug, minta AI menulis pengujian yang gagal terlebih dahulu (*breaking test*), baru kemudian memperbaikinya.
4. [📂 `04-refactor-with-tests.md`](./04-refactor-with-tests.md)
   - Melakukan refactoring secara berkala dengan aman ketika pengujian sudah tersedia.
