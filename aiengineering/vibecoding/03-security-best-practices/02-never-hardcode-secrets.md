# 02 - Never Hardcode Credentials; Use Env Variables Instead

## 🎯 Definisi & Konsep
**Never Hardcode Credentials** adalah aturan mutlak dalam pengkodean yang melarang penulisan rahasia seperti API Keys, Password Database, Private Keys, atau Auth Tokens secara langsung di dalam source code repository.

Sebagai gantinya, gunakan **Environment Variables** (`.env`) dan pastikan file `.env` tersebut terdaftar di dalam `.gitignore`.

---

## 🛑 Contoh Kesalahan vs Perbaikan

❌ **BURUK (Hardcoded Secret)**:
```typescript
// db.ts
const dbUrl = "postgres://admin:PasswordRahasia123@localhost:5432/mydb";
```

✅ **BENAR (Environment Variables)**:
```typescript
// db.ts
const dbUrl = process.env.DATABASE_URL;
const stripeKey = process.env.STRIPE_SECRET_KEY;

if (!dbUrl || !stripeKey) {
  throw new Error("Missing critical environment variables!");
}
```

---

## 💬 Contoh Prompt Koreksi AI
```text
Saya melihat kamu menaruh string API Key langsung di `services/openaiService.ts`. 
Segera hentikan ini! 
1. Pindahkan key tersebut ke file `.env` dengan variabel `OPENAI_API_KEY`.
2. Buatkan file `.env.example` sebagai template tanpa menaruh nilai rahasia aslinya.
3. Pastikan `.env` terdaftar di `.gitignore`.
```
