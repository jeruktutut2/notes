# 01 - Ask AI to Write Tests (Unit & E2E Tests)

## 🎯 Definisi & Konsep
**Ask AI to Write Tests** adalah instruksi wajib kepada AI untuk membuat berkas pengujian otomatis bersamaan dengan saat AI memproduksi fitur baru.

AI sangat handal dalam menghasilkan boilerplate pengujian (seperti Jest, Vitest, Cypress, atau Playwright) dalam hitungan detik.

---

## 🛠️ Jenis Pengujian Utama dalam Vibe Coding

1. **Unit Tests (Vitest / Jest)**: Menguji logika murni dari fungsi-fungsi utilitas atau reducer.
2. **Integration Tests**: Menguji interaksi antara API controller dan database.
3. **End-to-End (E2E) Tests (Playwright)**: Menguji seluruh alur pengguna di layar tampilan sesungguhnya.

---

## 💬 Contoh Prompt Pembuatan Unit Test

```text
Saya baru saja menyetujui implementasi modul `src/utils/calculator.ts`.
Tolong buatkan unit test komprehensif menggunakan Vitest di file `src/utils/calculator.test.ts`.

Cakup skenario:
1. Input valid normal.
2. Input batas (edge cases) seperti 0 atau angka negatif.
3. Throw error jika input bernilai null atau string non-numeric.

Setelah kodenya dibuat, jalankan perintah `npm test` di terminal untuk memastikan semua test PASS.
```
