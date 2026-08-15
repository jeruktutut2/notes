# 📘 Modul 9 — Guardrails & AI Safety

Modul ini mempelajari implementasi **Guardrails (Pagar Pengaman)** ganda untuk melindungi aplikasi AI dari ancaman manipulasi input dan kebocoran informasi rahasia.

---

## 🛡️ Lapisan Keamanan Guardrails

```
[User Request] 
      │
      ▼
┌──────────────────────┐
│  INPUT GUARDRAILS    │ ── (Blokir Prompt Injection / Kata Kasar / Scope Limit)
└──────────┬───────────┘
           │ (Lolos)
           ▼
┌──────────────────────┐
│     LLM ENGINE       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  OUTPUT GUARDRAILS   │ ── (Redaksi PII / Email / NIK KTP / No HP)
└──────────┬───────────┘
           │
           ▼
 [Safe Response to User]
```

---

## 🚀 Cara Menjalankan (Oleh Pengguna)

```bash
# Pastikan Ollama sudah berjalan
ollama serve

# Jalankan simulasi uji keamanan Guardrails
python 09_guardrails/main.py
```
