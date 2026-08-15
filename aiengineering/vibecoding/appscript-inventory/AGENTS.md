# Agent Coding Standards: Google Apps Script (AGENTS.md)

Dokumen ini berisi standar dan preferensi koding yang WAJIB dipatuhi AI Coding Agent saat membaca atau mengubah kode aplikasi **Google Apps Script Inventory**.

## 1. Core Stack Rules
- **Backend File (`Code.gs`)**: Gunakan sintaks JavaScript V8 modern (`const`, `let`, arrow functions, `try-catch`).
- **HTML Service**: Gunakan `HtmlService.createHtmlOutputFromFile('Index')` dengan setting `.setTitle('VibeInventory App')` dan `.addMetaTag('viewport', 'width=device-width, initial-scale=1')`.
- **Interaksi Frontend-Backend**: Gunakan `google.script.run.withSuccessHandler(...).withFailureHandler(...)` di JavaScript client-side.

## 2. Security & Hashing Guidelines (Bcrypt)
- **Dilarang keras menyimpan password plain text**: Gunakan helper function `hashPassword(password)` yang menerapkan alur **Salted Key Stretching / Bcrypt Work-Factor Iteration** (`$2a$10$...` format).
- **LockService for Concurrent Transactions**: Gunakan `LockService.getScriptLock()` pada operasi penambahan/pengurangan stok untuk mencegah *race conditions*.

## 3. Spreadsheet Data Handling
- Selalu gunakan `SpreadsheetApp.getActiveSpreadsheet()`.
- Bungkus semua operasi sheet dengan penanganan error yang mengembalikan objek `{ success: boolean, message: string, data?: any }`.
