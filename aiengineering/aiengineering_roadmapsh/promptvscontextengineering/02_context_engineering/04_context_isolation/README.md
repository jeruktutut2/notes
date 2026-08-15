# 04. Context Isolation

Modul ini mempelajari teknik *Context Isolation* (Isolasi Konteks) untuk menjaga kerahasiaan data antar-pengguna (*Multi-Tenant Privacy*) dan mencegah percampuran state antar-agen.

---

## 📌 Apa Saja Yang Harus Dipelajari?

### 1. Multi-Tenant Privacy Isolation
- **Definisi**: Memastikan bahwa data sensitif milik Tenant A (misal: Perusahaan X) tidak akan pernah terselip atau bocor ke dalam context window yang diproses untuk Tenant B (Perusahaan Y).
- **Teknik Isolasi**:
  - **Namespace Memory Isolation**: Mengisolasi key memori di Redis/Vector DB berdasarkan `tenant_id`.
  - **Context Boundaries (XML Tag Isolation)**: Mengurung dokumen dalam tag terisolasi `<tenant_data tenant_id="...">` dan mengonfirmasi batas isolasi sebelum eksekusi LLM.

### 2. PII Sanitization & Redaction
- **Definisi**: Mengamankan informasi pribadi (*Personally Identifiable Information* seperti No HP, NIK, Email, Kartu Kredit) dengan menggantinya menggunakan token acak (`[PII_PHONE_1]`) sebelum dikirim ke LLM vendor. Pasca-generasi, token dikembalikan (*unmasked*) di server lokal.

### 3. Sub-Agent Context Isolation
- **Definisi**: Saat memecah tugas kompleks ke beberapa Sub-Agent, berikan **HANYA** konteks relevan yang dibutuhkan sub-agent tersebut ketimbang membagikan seluruh prompt history raksasa.

---

## 💻 Skrip Interaktif
Jalankan file `main.py` di folder ini untuk melihat simulasi PII Sanitization dan Tenant Isolation Boundary.
